<?php
/**
 * Configuracao da ponte (mcp-instagram) na HostGator. EXEMPLO.
 *
 * COMO USAR
 * 1. Copie este arquivo como `mcp-instagram-config.php`.
 * 2. Preencha os valores reais.
 * 3. Envie para UM NIVEL ACIMA do public_html do subdominio, ou seja,
 *    IRMAO da pasta que contem o token.php, nunca dentro dela.
 * 4. Permissao 600 (so o dono le).
 *
 * NUNCA versione o arquivo preenchido. Nunca o coloque dentro do
 * public_html: fora dele, mesmo que o PHP pare de ser interpretado, o
 * arquivo nao pode ser baixado pela web.
 *
 * A chave AES (INSTAGRAM_TOKEN_ENCRYPTION_KEY) NAO entra aqui, nem em
 * lugar nenhum desta hospedagem: ela existe apenas no Render. O que
 * chega aqui ja esta cifrado, e a ponte nunca precisa decifrar nada.
 */

return [
    // Mesmo valor de MCP_INSTAGRAM_PONTE_SECRET no Render.
    // Gere com: openssl rand -base64 32
    'PONTE_SECRET' => '',

    // Banco em localhost: nenhuma liberacao de IP e necessaria.
    //
    // Pode ser O MESMO banco que o mcp-linkedin ja usa. Nao e preciso
    // criar banco nem usuario novo: o que separa os dois componentes e
    // a TABELA e o ALVO, logo abaixo. Se preferir isolamento total,
    // crie um banco proprio e ajuste os tres campos.
    'DB_HOST' => 'localhost',
    'DB_NAME' => 'rosepa59_mcp_linkedin',
    'DB_USER' => 'rosepa59_mcp_linkedin',
    'DB_PASS' => '',

    // Estes dois sao o que impede o Instagram de ler ou gravar o token
    // do LinkedIn, e vice-versa. Nao reaproveite os valores do outro
    // componente.
    'DB_TABLE' => 'mcp_instagram_tokens',
    'ALVO' => 'mcp-instagram:instagram-access-token',
];
