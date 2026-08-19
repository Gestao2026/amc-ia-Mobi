<?php
/**
 * Configuracao da ponte (mcp-linkedin) na HostGator. EXEMPLO.
 *
 * COMO USAR
 * 1. Copie este arquivo como `mcp-linkedin-config.php`.
 * 2. Preencha os valores reais.
 * 3. Envie para UM NIVEL ACIMA do public_html do subdominio, ou seja,
 *    IRMAO da pasta que contem o token.php, nunca dentro dela.
 * 4. Permissao 600 (so o dono le).
 *
 * NUNCA versione o arquivo preenchido. Nunca o coloque dentro do
 * public_html: fora dele, mesmo que o PHP pare de ser interpretado, o
 * arquivo nao pode ser baixado pela web.
 *
 * A chave AES (LINKEDIN_TOKEN_ENCRYPTION_KEY) NAO entra aqui, nem em
 * lugar nenhum desta hospedagem: ela existe apenas no Render. O que
 * chega aqui ja esta cifrado, e a ponte nunca precisa decifrar nada.
 */

return [
    // Mesmo valor de MCP_LINKEDIN_PONTE_SECRET no Render.
    // Gere com: openssl rand -base64 32
    'PONTE_SECRET' => '',

    // Banco em localhost: nenhuma liberacao de IP e necessaria.
    'DB_HOST' => 'localhost',
    'DB_NAME' => 'rosepa59_mcp_linkedin',
    'DB_USER' => 'rosepa59_mcp_linkedin',
    'DB_PASS' => '',

    // Opcionais: os padroes abaixo ja sao os usados pelo token.php.
    'DB_TABLE' => 'mcp_linkedin_tokens',
    'ALVO' => 'mcp-linkedin:linkedin-access-token',
];
