# 13 - Análise da pasta Documentos e comparação com a MOBI

| Campo | Valor |
|---|---|
| Data | 2026-08-21 |
| Pasta afetada | `C:\Users\rosep\OneDrive - {organizacao}\Documentos` e `C:\Users\rosep\Desktop\MOBI` |
| Tipo | Diagnóstico |
| Situação | **Apenas diagnóstico. Nada foi movido, renomeado ou apagado.** |
| Autorizada por | A captadora, em 21/08/2026: "apenas analise e me retorne sobre como está a estrutura. Não mexa em nada, não apague nada, quero só um relatório." |
| Reversível | Não se aplica, nenhuma alteração foi feita |

---

## 1. Por que foi feito

A captadora quer organizar a pasta `Documentos` e pediu o diagnóstico antes de
qualquer execução.

O diagnóstico encontrou um problema maior do que a desorganização: **existem duas
árvores paralelas e nenhuma contém a outra.** A estruturação 01, de 20/08,
organizou a pasta MOBI. O que não estava visível na ocasião é que a MOBI foi
montada a partir de uma exportação do OneDrive, e o OneDrive continuou vivo.

Números que sustentam:

- A árvore MOBI teve **1 arquivo** alterado depois de 19/07/2026.
- A pasta Documentos teve **88 arquivos** alterados no mesmo período, o mais
  recente em 20/08/2026.

Isso responde a pergunta que ficou em aberto na análise de 21/08 registrada em
`_detalhado/`: não houve migração para a nuvem, houve dessincronização.

## 2. O que foi decidido, e por quem

Nada foi decidido ainda. O plano está em `_detalhado/2026-08-21-13-plano-de-organizacao.md`
e depende de três respostas da captadora, registradas ali como Fase 0.

Descartado nesta etapa, e por quê:

- **Escolher uma árvore e apagar a outra.** Inviável: 303 arquivos existem só na
  Documentos e 1.667 só na MOBI. O plano passou a ser de fusão.
- **Reorganizar dentro do OneDrive.** Mover arquivo lá dispara ressincronização
  de 13 GB, porque para o OneDrive mover é apagar e recriar.

## 3. Estado antes

| Medida | Documentos | MOBI |
|---|---|---|
| Arquivos | 4.126 | 6.243 |
| Volume | 13,37 GB | 11,64 GB |
| Pastas | 2.505 | não medido nesta análise |
| Pastas vazias | 1.221 (49% do total) | não medido |
| Pastas com um único item | 279 | não medido |
| Profundidade máxima | 12 níveis | 6 níveis |
| Caminho mais longo | 253 caracteres | 248 caracteres |
| Arquivos com caminho acima de 240 caracteres | 560 | 0 |
| Última atividade real | 20/08/2026 | 19/07/2026 |

Sobreposição entre as duas:

| Conjunto | Arquivos | Volume |
|---|---|---|
| Em comum (mesmo nome e tamanho) | 3.439 | 2,69 GB |
| Só na Documentos | 303 | 10,50 GB |
| Só na MOBI | 1.667 | 8,22 GB |

## 4. O que foi executado

Nenhuma alteração. Só leitura de metadados, em quatro passadas:

1. Estrutura, profundidade, tipos, duplicatas internas, padrões de nome, pastas
   vazias, idade e material sensível por nome de arquivo.
2. Segundo nível das pastas de maior volume e sobreposição com a MOBI.
3. Atividade posterior a 19/07/2026 e arquivos exclusivos de cada lado.
4. Separação entre arquivo exclusivo de verdade e arquivo apenas renomeado, já
   que a estruturação 01 renomeou 660 arquivos.

A leitura foi de metadados de propósito: a pasta fica no OneDrive, e abrir
conteúdo forçaria o download de arquivo que estivesse só na nuvem.

## 5. Estado depois

Igual ao estado antes. Diagnóstico não altera nada.

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `_detalhado/2026-08-21-13-relatorio-completo.md` | Diagnóstico completo, com listas e caminhos reais |
| `_detalhado/2026-08-21-13-plano-de-organizacao.md` | Plano de fusão em 6 fases, com mapa de destino |
| `_detalhado/LEIA-ME.md` | Por que a pasta detalhada não sobe para o GitHub |

## 7. Backup feito antes

Não se aplica, nada foi alterado. Mas o diagnóstico revelou uma exposição:

| Origem | Situação |
|---|---|
| `Desktop\MOBI` | **Sem backup nenhum.** Guarda 8,22 GB que não existem em outro lugar, incluindo 304 arquivos de gestão documental (certidões, atas, alvarás, CMAS) |

Corrigir isso é a Fase 1 do plano e precisa vir antes de qualquer movimento.

## 8. Como reverter

Não se aplica.

## 9. O que ficou pendente

- **As três decisões da Fase 0:** destino dos 8,59 GB de vídeo de curso; saída do
  material pessoal do OneDrive institucional; o que a pasta Documentos vira depois.
- **Fase 1, rede de segurança**, incluindo pôr a MOBI no backup diário.
- **Herança de segurança:** um arquivo de senha guardado dentro da mesma pasta do
  certificado digital, em dois anos diferentes, e duas planilhas de senha em uso
  que ficaram fora da consolidação da estruturação 11. Detalhe em `_detalhado/`.

## 10. Regras que passam a valer

**Sobre registro e histórico**

- Todo relatório ou plano gerado por análise entra em `docs/estruturacoes/`, nunca
  solto na Área de Trabalho.
- O registro da estruturação (números, decisões, regras) fica no arquivo numerado
  e **vai para o GitHub**.
- O relatório detalhado (caminhos, nomes de arquivo, dados pessoais) fica em
  `_detalhado/`, que está no `.gitignore` e **não sobe para o GitHub**.
- Os dois carregam o mesmo número, para se encontrarem.

**Sobre árvore duplicada**

- **Uma árvore só é a oficial.** Foi a duplicação, não a bagunça, que gerou o
  problema desta estruturação.
- **Backup é cópia, não é segunda casa de trabalho.** Trabalhar em dois lugares
  foi o que fez as árvores divergirem.
- **Virada de ano não copia a pasta do ano anterior.** Foi assim que arquivos
  idênticos foram parar em 2025 e 2026 ao mesmo tempo.
