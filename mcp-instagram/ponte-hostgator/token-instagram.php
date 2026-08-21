<?php
/**
 * Ponte de armazenamento do token do Instagram (mcp-instagram).
 *
 * Render --HTTPS autenticado--> este arquivo --> MySQL em localhost
 *
 * Existe para o MySQL da HostGator continuar escutando somente em
 * localhost. A alternativa (conexao direta do Render ao MySQL) exigiria
 * liberar em Remote MySQL uma faixa CIDR que o Render COMPARTILHA com
 * todos os outros clientes da regiao, expondo o banco a qualquer
 * servico hospedado la.
 *
 * PROPRIEDADE DE SEGURANCA CENTRAL: este arquivo NUNCA recebe, conhece
 * ou guarda a chave AES. O valor em `secret` ja chega cifrado
 * (AES-256-GCM) pelo Render, e so ele tem a chave. Um comprometimento
 * total desta hospedagem (banco, PHP e config.php) entrega apenas
 * texto cifrado, inutil sem a chave.
 *
 * Nada aqui grava senha, segredo, token ou ciphertext em log.
 *
 * Instalacao: ver README.md desta pasta.
 */

declare(strict_types=1);

// Nunca exibir erro ao cliente: uma mensagem de erro do PDO pode
// conter credencial de banco ou trecho de consulta.
ini_set('display_errors', '0');
ini_set('log_errors', '0');
error_reporting(0);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');
header('Referrer-Policy: no-referrer');

/** Resposta JSON curta e encerramento. Nunca inclui detalhe interno. */
function responder(int $codigo, array $corpo): void
{
    http_response_code($codigo);
    echo json_encode($corpo, JSON_UNESCAPED_SLASHES);
    exit;
}

// ---------------------------------------------------------------
// 1. HTTPS obrigatorio
// ---------------------------------------------------------------
// O envelope AES ja protege o token, mas o segredo da ponte viaja em
// cabecalho: em HTTP simples ele iria em claro pela internet.
$ehHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || (($_SERVER['SERVER_PORT'] ?? '') === '443')
    // A HostGator termina o TLS antes do PHP em algumas configuracoes,
    // repassando o esquema original neste cabecalho.
    || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');

if (!$ehHttps) {
    responder(400, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 2. Configuracao (fora do public_html)
// ---------------------------------------------------------------
$caminhoConfig = __DIR__ . '/../mcp-instagram-config.php';
if (!is_readable($caminhoConfig)) {
    responder(500, ['status' => 'erro']);
}
$config = require $caminhoConfig;

foreach (['PONTE_SECRET', 'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASS'] as $obrigatoria) {
    if (empty($config[$obrigatoria])) {
        responder(500, ['status' => 'erro']);
    }
}

// ---------------------------------------------------------------
// 3. Autenticacao por segredo compartilhado
// ---------------------------------------------------------------
// Em hospedagem compartilhada o cabecalho `Authorization` costuma ser
// removido pelo CGI/FastCGI antes de chegar ao PHP, por isso o
// cabecalho proprio vem primeiro. O .htaccess desta pasta tenta
// preservar o `Authorization`, mas nao dependemos disso.
$segredoRecebido = $_SERVER['HTTP_X_MCP_PONTE_SECRET'] ?? '';

if ($segredoRecebido === '') {
    $cabecalhoAuth = $_SERVER['HTTP_AUTHORIZATION'] ?? ($_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '');
    if (stripos($cabecalhoAuth, 'Bearer ') === 0) {
        $segredoRecebido = substr($cabecalhoAuth, 7);
    }
}

// hash_equals: comparacao em tempo constante, contra ataque de
// temporizacao. Nunca usar === para comparar segredo.
if (!hash_equals((string) $config['PONTE_SECRET'], (string) $segredoRecebido)) {
    // 401 sem dizer o motivo: nao informar se o segredo estava
    // ausente, curto ou so incorreto.
    responder(401, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 4. Entrada
// ---------------------------------------------------------------
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    responder(405, ['status' => 'erro']);
}

$bruto = file_get_contents('php://input');
if ($bruto === false || strlen($bruto) > 65536) {
    responder(400, ['status' => 'erro']);
}

$entrada = json_decode($bruto, true);
if (!is_array($entrada)) {
    responder(400, ['status' => 'erro']);
}

$acao = $entrada['acao'] ?? '';
$alvo = $entrada['alvo'] ?? '';

// O alvo aceito e fixo: o cliente nao escolhe qual credencial ler ou
// gravar, entao nao ha como usar esta ponte como armazenamento
// generico nem para varrer outras chaves.
$alvoEsperado = $config['ALVO'] ?? 'mcp-instagram:instagram-access-token';
if (!is_string($alvo) || !hash_equals($alvoEsperado, $alvo)) {
    responder(400, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 5. Banco (localhost) via PDO com prepared statements
// ---------------------------------------------------------------
$tabela = $config['DB_TABLE'] ?? 'mcp_instagram_tokens';
// A tabela vem da configuracao do servidor, nunca da requisicao, mas
// ainda assim so aceitamos um identificador simples: nome de tabela
// nao pode ser parametrizado por prepared statement.
if (preg_match('/^[A-Za-z0-9_]+$/', $tabela) !== 1) {
    responder(500, ['status' => 'erro']);
}

try {
    $pdo = new PDO(
        sprintf('mysql:host=%s;dbname=%s;charset=utf8mb4', $config['DB_HOST'], $config['DB_NAME']),
        $config['DB_USER'],
        $config['DB_PASS'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_EMULATE_PREPARES => false,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );
} catch (Throwable $e) {
    // A mensagem do PDO pode conter usuario e host do banco: nunca
    // ecoar nem registrar.
    responder(500, ['status' => 'erro']);
}

try {
    if ($acao === 'ler') {
        $stmt = $pdo->prepare("SELECT secret FROM `$tabela` WHERE target_name = ? LIMIT 1");
        $stmt->execute([$alvo]);
        $linha = $stmt->fetch();

        if (!$linha || !isset($linha['secret']) || $linha['secret'] === '') {
            responder(200, ['status' => 'vazio']);
        }
        responder(200, ['status' => 'ok', 'secret' => $linha['secret']]);
    }

    if ($acao === 'gravar') {
        $segredo = $entrada['secret'] ?? '';
        if (!is_string($segredo) || $segredo === '') {
            responder(400, ['status' => 'erro']);
        }

        $stmt = $pdo->prepare(
            "INSERT INTO `$tabela` (target_name, secret) VALUES (?, ?)
             ON DUPLICATE KEY UPDATE secret = VALUES(secret)"
        );
        $stmt->execute([$alvo, $segredo]);
        responder(200, ['status' => 'ok']);
    }

    if ($acao === 'excluir') {
        $stmt = $pdo->prepare("DELETE FROM `$tabela` WHERE target_name = ?");
        $stmt->execute([$alvo]);
        // Apagar o que nao existe nao e erro.
        responder(200, ['status' => 'ok']);
    }
} catch (Throwable $e) {
    responder(500, ['status' => 'erro']);
}

responder(400, ['status' => 'erro']);
