# Converte as quatro páginas do dia em PDF e as coloca na pasta RADARES DO DIA da Área de Trabalho.
# Chamado pela rotina local "Radares do dia na Área de Trabalho" (9h30), depois que ela baixa
# as páginas publicadas. Decisão da captadora em 15/09/2026.
#
# Cada PDF é gerado primeiro num arquivo provisório e só então substitui o do dia anterior.
# Se a conversão de uma página falhar, o PDF de ontem daquela página fica onde está.

param(
    [Parameter(Mandatory = $true)][string]$Resumo,
    [Parameter(Mandatory = $true)][string]$Mercado,
    [Parameter(Mandatory = $true)][string]$Geral,
    [Parameter(Mandatory = $true)][string]$Ppl
)

$ErrorActionPreference = 'Stop'

$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if (-not (Test-Path $edge)) { $edge = 'C:\Program Files\Microsoft\Edge\Application\msedge.exe' }
if (-not (Test-Path $edge)) { Write-Output 'FALHA: Microsoft Edge não encontrado.'; exit 1 }

$destino = Join-Path ([Environment]::GetFolderPath('Desktop')) 'RADARES DO DIA'
if (-not (Test-Path $destino)) { New-Item -ItemType Directory -Path $destino | Out-Null }

# Perfil próprio do Edge, para não esbarrar numa janela do Edge que esteja aberta.
$perfil = Join-Path $env:TEMP 'radares-do-dia-edge'

$paginas = [ordered]@{
    'Resumo da manhã'               = $Resumo
    'Radar de Mercado e Patrocínio' = $Mercado
    'Radar Geral'                   = $Geral
    'Radar PPL'                     = $Ppl
}

$falhas = 0
foreach ($nome in $paginas.Keys) {
    $origem = $paginas[$nome]
    $final = Join-Path $destino "$nome.pdf"
    $provisorio = Join-Path $destino "$nome.novo.pdf"

    if (-not (Test-Path $origem)) {
        Write-Output "FALHA: $nome, página baixada não encontrada em $origem"
        $falhas++
        continue
    }

    if (Test-Path $provisorio) { Remove-Item $provisorio -Force }
    $url = ([System.Uri](Resolve-Path $origem).Path).AbsoluteUri

    $argumentos = @(
        '--headless=new', '--disable-gpu', '--no-first-run', '--no-pdf-header-footer',
        "--user-data-dir=`"$perfil`"", '--virtual-time-budget=15000',
        "--print-to-pdf=`"$provisorio`"", "`"$url`""
    )
    $processo = Start-Process -FilePath $edge -ArgumentList $argumentos -Wait -PassThru -WindowStyle Hidden

    if ((Test-Path $provisorio) -and ((Get-Item $provisorio).Length -gt 1000)) {
        Move-Item -Path $provisorio -Destination $final -Force
        $kb = [math]::Round((Get-Item $final).Length / 1KB)
        Write-Output "OK: $nome.pdf ($kb KB)"
    } else {
        if (Test-Path $provisorio) { Remove-Item $provisorio -Force }
        Write-Output "FALHA: $nome, o Edge não gerou o PDF (código $($processo.ExitCode)). O PDF anterior foi mantido."
        $falhas++
    }
}

Write-Output "Pasta: $destino"
if ($falhas -gt 0) { exit 1 }
