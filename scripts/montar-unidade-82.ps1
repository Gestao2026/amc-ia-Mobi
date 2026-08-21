# ---------------------------------------------------------------------------
# Cria a unidade virtual M: apontando para a pasta _82 no Google Drive.
#
# Para que serve: o caminho real da pasta tem 104 caracteres de prefixo, o que
# estoura o limite de 260 do Windows em 2.588 arquivos. Pela unidade M: o
# prefixo cai para 2 caracteres e todos os arquivos abrem no Explorer e no Office.
#
# A unidade NAO guarda nada. E apenas um apelido para a mesma pasta.
# Roda no login pela tarefa "AMC IA - Unidade M pasta 82".
# Documentado em docs/estruturacoes/
# ---------------------------------------------------------------------------

$LETRA = 'M:'
$ALVO  = 'G:\.shortcut-targets-by-id\1YxXksuP6SHlVKA4bT5gaC0WG4Wy4OXej\_82 - Rosepaula Aparecida Andrade Rodrigues'
$LOG   = 'C:\Users\rosep\Backups\_historico-backup.log'

function Anota($msg) {
    $linha = "{0:yyyy-MM-dd HH:mm:ss}  unidade {1}  {2}" -f (Get-Date), $LETRA, $msg
    try { Add-Content -LiteralPath $LOG -Value $linha -Encoding UTF8 } catch {}
}

# O Google Drive demora para montar o G: depois do login. Espera ate 5 minutos.
$pronto = $false
for ($i = 0; $i -lt 60; $i++) {
    if (Test-Path -LiteralPath $ALVO) { $pronto = $true; break }
    Start-Sleep -Seconds 5
}

if (-not $pronto) {
    Anota "nao criada: o Google Drive nao montou a pasta em 5 minutos"
    exit 1
}

if (Test-Path -LiteralPath "$LETRA\") {
    Anota "ja existia, nada a fazer"
    exit 0
}

& subst $LETRA $ALVO | Out-Null

if (Test-Path -LiteralPath "$LETRA\") { Anota "criada com sucesso" }
else { Anota "FALHOU ao criar" ; exit 1 }
