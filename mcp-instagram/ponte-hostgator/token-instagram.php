<?php
/**
 * Ponte de armazenamento do token do Instagram (mcp-instagram).
 *
 * Render --HTTPS autenticado--> este arquivo --> MySQL em localhost
 *
 * O MySQL permanece acessível somente localmente na HostGator.
 *
 * PROPRIEDADE DE SEGURANCA:
 * Este arquivo nunca recebe nem conhece a chave AES.
 * O valor armazenado em "secret" chega cifrado pelo Render.
 *
 * Nada aqui grava senha, segredo, token ou ciphertext em log.
 *
 * Gemeo do token.php (mcp-linkedin), que vive no mesmo docroot. As
 * unicas diferencas sao o caminho do config, o alvo e a tabela padrao.
 * Divergir dele em qualquer outro ponto e erro: o token.php ja esta em
 * producao e revisado.
 */

declare(strict_types=1);

ini_set('display_errors', '0');
ini_set('log_errors', '0');
error_reporting(0);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');
header('Referrer-Policy: no-referrer');

/**
 * Resposta JSON curta e encerramento.
 */
function responder(int $codigo, array $corpo): void
{
    http_response_code($codigo);
    echo json_encode($corpo, JSON_UNESCAPED_SLASHES);
    exit;
}

// ---------------------------------------------------------------
// 1. HTTPS obrigatorio
// ---------------------------------------------------------------

$ehHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || (($_SERVER['SERVER_PORT'] ?? '') === '443')
    || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');

if (!$ehHttps) {
    responder(400, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 2. Configuracao
// ---------------------------------------------------------------

$caminhoConfig = __DIR__ . '/../mcp-instagram-config.php';

if (!is_readable($caminhoConfig)) {
    responder(500, ['status' => 'erro']);
}

$config = require $caminhoConfig;

foreach ([
    'PONTE_SECRET',
    'DB_HOST',
    'DB_NAME',
    'DB_USER',
    'DB_PASS'
] as $obrigatoria) {
    if (
        !isset($config[$obrigatoria]) ||
        !is_string($config[$obrigatoria]) ||
        $config[$obrigatoria] === ''
    ) {
        responder(500, ['status' => 'erro']);
    }
}

// ---------------------------------------------------------------
// 3. Autenticacao por segredo compartilhado
// ---------------------------------------------------------------

$segredoRecebido = $_SERVER['HTTP_X_MCP_PONTE_SECRET'] ?? '';

if ($segredoRecebido === '') {
    $cabecalhoAuth =
        $_SERVER['HTTP_AUTHORIZATION']
        ?? ($_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '');

    if (stripos($cabecalhoAuth, 'Bearer ') === 0) {
        $segredoRecebido = substr($cabecalhoAuth, 7);
    }
}

if (!hash_equals(
    (string) $config['PONTE_SECRET'],
    (string) $segredoRecebido
)) {
    responder(401, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 4. Metodo HTTP
// ---------------------------------------------------------------

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    responder(405, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 5. Entrada JSON
// ---------------------------------------------------------------

$bruto = file_get_contents('php://input');

if ($bruto === false || strlen($bruto) > 65536) {
    responder(400, ['status' => 'erro']);
}

$entrada = json_decode($bruto, true);

if (!is_array($entrada)) {
    responder(400, ['status' => 'erro']);
}

$acao = $entrada['acao'] ?? '';

if (!is_string($acao) || !in_array($acao, [
    'ler',
    'gravar',
    'excluir'
], true)) {
    responder(400, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 6. Alvo FIXO
// ---------------------------------------------------------------
//
// O cliente NAO envia o alvo.
//
// Isso elimina uma fonte desnecessaria de erro e impede que o cliente
// escolha outra chave de armazenamento.
//
// Este e o unico alvo permitido por esta ponte, e e o que separa o
// Instagram do LinkedIn: os dois compartilham banco e segredo, mas
// nunca a etiqueta nem a tabela.

$alvo = 'mcp-instagram:instagram-access-token';

// ---------------------------------------------------------------
// 7. Banco MySQL local
// ---------------------------------------------------------------

$tabela = $config['DB_TABLE'] ?? 'mcp_instagram_tokens';

if (
    !is_string($tabela) ||
    preg_match('/^[A-Za-z0-9_]+$/', $tabela) !== 1
) {
    responder(500, ['status' => 'erro']);
}

try {
    $pdo = new PDO(
        sprintf(
            'mysql:host=%s;dbname=%s;charset=utf8mb4',
            $config['DB_HOST'],
            $config['DB_NAME']
        ),
        $config['DB_USER'],
        $config['DB_PASS'],
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_EMULATE_PREPARES => false,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]
    );
} catch (Throwable $e) {
    responder(500, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 8. Operacoes
// ---------------------------------------------------------------

try {

    // -----------------------------------------------------------
    // LER
    // -----------------------------------------------------------

    if ($acao === 'ler') {

        $stmt = $pdo->prepare(
            "SELECT secret
             FROM `$tabela`
             WHERE target_name = ?
             LIMIT 1"
        );

        $stmt->execute([$alvo]);

        $linha = $stmt->fetch();

        if (
            !$linha ||
            !isset($linha['secret']) ||
            !is_string($linha['secret']) ||
            $linha['secret'] === ''
        ) {
            responder(200, ['status' => 'vazio']);
        }

        responder(200, [
            'status' => 'ok',
            'secret' => $linha['secret']
        ]);
    }

    // -----------------------------------------------------------
    // GRAVAR
    // -----------------------------------------------------------

    if ($acao === 'gravar') {

        $segredo = $entrada['secret'] ?? '';

        if (!is_string($segredo) || $segredo === '') {
            responder(400, ['status' => 'erro']);
        }

        $stmt = $pdo->prepare(
            "INSERT INTO `$tabela`
                (target_name, secret)
             VALUES
                (?, ?)
             ON DUPLICATE KEY UPDATE
                secret = VALUES(secret)"
        );

        $stmt->execute([
            $alvo,
            $segredo
        ]);

        responder(200, ['status' => 'ok']);
    }

    // -----------------------------------------------------------
    // EXCLUIR
    // -----------------------------------------------------------

    if ($acao === 'excluir') {

        $stmt = $pdo->prepare(
            "DELETE FROM `$tabela`
             WHERE target_name = ?"
        );

        $stmt->execute([$alvo]);

        responder(200, ['status' => 'ok']);
    }

} catch (Throwable $e) {

    responder(500, ['status' => 'erro']);
}

// ---------------------------------------------------------------
// 9. Fallback
// ---------------------------------------------------------------

responder(400, ['status' => 'erro']);
