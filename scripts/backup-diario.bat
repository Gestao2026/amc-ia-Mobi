@echo off
rem ---------------------------------------------------------------------------
rem Backup diario da AMC IA. Nunca apaga nada no destino.
rem Destino padrao de TODO backup: C:\Users\rosep\Backups
rem Documentado em docs/backup.md e em docs/estruturacoes/
rem ---------------------------------------------------------------------------

set BASE=C:\Users\rosep\Backups
set LOG=%BASE%\_historico-backup.log

if not exist "%BASE%" mkdir "%BASE%"
if not exist "%BASE%\amc-ia-mobi" mkdir "%BASE%\amc-ia-mobi"
if not exist "%BASE%\pasta-82" mkdir "%BASE%\pasta-82"
if not exist "%BASE%\credenciais" mkdir "%BASE%\credenciais"

echo ---------------------------------------- >> "%LOG%"
echo Backup iniciado em %date% %time% >> "%LOG%"

rem --- 1. Projeto AMC IA (disco local -> pasta de backups) --------------------
robocopy "C:\amc-ia-Mobi\minhas-oscs"  "%BASE%\amc-ia-mobi\minhas-oscs"  /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\captador"     "%BASE%\amc-ia-mobi\captador"     /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\base-editais" "%BASE%\amc-ia-mobi\base-editais" /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\parcerias"    "%BASE%\amc-ia-mobi\parcerias"    /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\docs"         "%BASE%\amc-ia-mobi\docs"         /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"

rem --- 2. Pasta _82 (Drive do mentor -> disco local) --------------------------
rem     Sentido inverso do backup acima. A origem e a nuvem, o destino e o disco.
rem     Protege contra o dono revogar o acesso ou apagar algo. A captadora e
rem     apenas Editora dessa pasta, nao dona.
rem     A leitura e feita pelo caminho real do Drive, nao pela unidade M:, para
rem     o backup nao depender da unidade virtual estar montada.
rem     Religado em 21/08/2026 as 18h, com o aval da captadora. A primeira carga
rem     baixou os 10,43 GB de uma vez; as seguintes copiam so o que mudou.
set P82=G:\.shortcut-targets-by-id\1YxXksuP6SHlVKA4bT5gaC0WG4Wy4OXej\_82 - Rosepaula Aparecida Andrade Rodrigues
if exist "%P82%" (
  rem  /XF desktop.ini : o Google Drive recria esses arquivos sozinho na maquina.
  rem  Eles NAO existem na nuvem, sao so enfeite de icone de pasta do Windows.
  rem  Nao adianta apagar, voltam. Entao ficam de fora do backup.
  rem  /XF *.gdoc *.gsheet *.gslides : ponteiros para arquivos do Google. Nao
  rem  copiam (erro 1 no robocopy) e nao tem conteudo proprio.
  robocopy "%P82%" "%BASE%\pasta-82\atual" /E /R:1 /W:1 /NP /NFL /NDL /XF desktop.ini *.gdoc *.gsheet *.gslides /LOG+:"%LOG%"
) else (
  echo Pasta _82 do Drive indisponivel, backup dela foi pulado >> "%LOG%"
)

rem --- 3. Credenciais dos clientes (Area de Trabalho -> disco local, SO LOCAL) -
rem     Pasta de senhas, certificado digital e acessos dos clientes. Decisao da
rem     captadora em 21/08/2026: entra no backup, mas NAO sobe para o Google
rem     Drive. Por isso esta linha fica aqui e nao no bloco 4, e por isso o
rem     destino e %BASE%, que mora no disco. Segredo nao vai para nuvem.
rem     ATENCAO: se um dia mover este robocopy para o bloco 4, as senhas de
rem     todos os clientes e o certificado e-CNPJ da MUPA passam a ficar na conta
rem     Google. Nao faca isso sem decisao explicita.
set CRED=C:\Users\rosep\Desktop\Credenciais AMC IA
if exist "%CRED%" (
  robocopy "%CRED%" "%BASE%\credenciais" /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
) else (
  echo Pasta Credenciais AMC IA nao encontrada na Area de Trabalho, backup dela foi pulado >> "%LOG%"
)

rem --- 4. Segunda camada fora da maquina (protege contra falha do disco) ------
rem     Se o disco C: morrer, a copia acima morre junto. Esta linha mantem uma
rem     copia do projeto na nuvem. Para desligar, comente as tres linhas abaixo.
rem     As credenciais do bloco 3 NAO entram aqui, de proposito.
robocopy "C:\amc-ia-Mobi\minhas-oscs"  "G:\Meu Drive\AMC-IA-Backup\minhas-oscs"  /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\captador"     "G:\Meu Drive\AMC-IA-Backup\captador"     /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"
robocopy "C:\amc-ia-Mobi\base-editais" "G:\Meu Drive\AMC-IA-Backup\base-editais" /E /R:1 /W:1 /NP /NFL /NDL /LOG+:"%LOG%"

echo Backup concluido em %date% %time% >> "%LOG%"
exit /b 0
