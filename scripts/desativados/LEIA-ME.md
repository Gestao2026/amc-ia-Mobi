# Scripts desativados

Nada aqui roda. Um script vai parar nesta pasta quando ele ainda faz sentido
guardar, mas não deve mais ser executado do jeito que está.

A extensão é trocada de propósito (`.ps1` vira `.ps1.desativado`) para que o
arquivo não possa ser chamado por engano. Além disso, cada um leva uma trava
dentro, logo no começo, que interrompe a execução caso alguém renomeie de volta
sem ler o motivo.

| Arquivo | Desativado em | Por quê |
|---|---|---|
| `sincronizar-82.ps1.desativado` | 26/08/2026 | Sincronizava a `_82` do Drive e a da Área de Trabalho nos dois sentidos. As duas divergiram: o Drive está correto desde 25/08 e a Área de Trabalho ficou na versão anterior. Como o script é aditivo e nunca apaga, rodar duplicaria a `06 - Clientes`, misturando a estrutura corrigida com os nomes antigos |
| `sincronizar-clientes-airtable.py.desativado` | 31/08/2026 | Puxava a carteira do CaptaHub e atualizava a base Airtable `appKWLTFSCcWucXfQ`. O **projeto MAPA foi encerrado** e o Airtable saiu de cena. Rodar agora escreve numa base que ninguém mantém |
| `sincronizar-clientes.bat.desativado` | 31/08/2026 | O atalho do Agendador do Windows para o script acima. Nunca chegou a ser agendado. Desativado junto, para não sobrar chamada viva |
| `ler-planilha-submissao.py.desativado` | 31/08/2026 | Lia a planilha mestra de submissões e comparava com o Airtable, gravando Status e Data de submissão com `--aplicar`. Sem o Airtable, o outro lado da comparação deixou de existir. **A leitura da planilha em si continua valendo** e vale reaproveitar o código se a comparação passar a ser com o CaptaHub |

## Se precisar religar algum

1. Ler o cabeçalho do próprio arquivo. O motivo da desativação está escrito lá,
   com o estado das pastas na data.
2. Confirmar que a condição que motivou o desligamento mudou.
3. Renomear de volta e apagar o bloco de trava.
4. Rodar primeiro em simulação, sem `-Executar`, e ler o relatório linha por
   linha antes de qualquer coisa.
