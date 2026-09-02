# Automações da base MAPA CLIENTES, cópia de segurança

> Base `appKWLTFSCcWucXfQ` (MAPA CLIENTES | EDITAIS E PROJETOS).
> Configuração completa lida em 02/09/2026, antes de qualquer alteração.

O projeto MAPA foi desligado em 31/08/2026, mas **as automações da base
continuaram publicadas e mandando e-mail** para `gestao.mobilizando@gmail.com`.
Foi o que a captadora percebeu em 02/09/2026, recebendo duas atualizações por dia.

## As cinco automações encontradas

| Nome | Quando dispara | O que faz | Estado em 02/09 |
|---|---|---|---|
| Alerta diário de prazo e marcos | todo dia às 8h | manda e-mail com marcos, prazos e pipeline | publicada, mandando |
| Alerta de data do resultado | todo dia às 8h | manda e-mail com resultados previstos | publicada, mandando |
| Relatório de fim de semana | sábado às 9h | manda e-mail com o panorama da semana | publicada, mandando |
| Consulta semanal de resultado | segunda às 9h | manda e-mail dos projetos sem data de retorno | publicada, mandando |
| Enviar para Não Submetidos | todo dia às 7h | cria ficha, não manda e-mail | **continuava ligada**, ver abaixo |

As duas que chegam todo dia são a primeira e a segunda, ambas às 8h.

## Para recriar qualquer uma delas

O arquivo `configuracao-completa.json` guarda gatilho, filtros, campos e o texto
do e-mail de cada uma, exatamente como estavam. Basta devolver o conteúdo pela
API de automações do Airtable ou remontar na tela.

## O que foi feito em 02/09/2026

As quatro automações que mandavam e-mail foram **desligadas na tela e apagadas**.
Não existem mais na base. A configuração de cada uma está em
`configuracao-completa.json`, com gatilho, filtros, tabelas, campos e assunto,
suficiente para remontar qualquer uma se o MAPA voltar.

A quinta, **Enviar para Não Submetidos**, foi apenas **desligada**, não apagada.
Ela continua na base, agora com o interruptor em OFF.

## A descoberta desagradável

A pausa feita em 31/08/2026 por condição impossível **nunca chegou a valer**. Ao
abrir a tela, o Airtable mostrava o aviso de que havia alterações não publicadas,
esperando alguém clicar em Update. Ou seja: entre 31/08 e 02/09 a automação
continuou rodando todo dia às 7h com as condições antigas.

**A lição vale para qualquer automação do Airtable:** alteração feita pela API
entra como rascunho e só passa a valer depois de publicada na tela. O único
desligamento que funciona de verdade é o interruptor, e ele só existe na tela.

O caminho, quando precisar: abrir `https://airtable.com/{baseId}/automations`,
escolher a automação na lista da esquerda e clicar no seletor ON que fica no alto,
ao lado do nome. Os selos ON da lista são apenas rótulos, não clicam.
