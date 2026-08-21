# Estado atual do ambiente

> Levantamento de 21/08/2026, 18h. Atualizar a cada rodada de estruturação.
> O histórico completo de cada ação está no [índice](README.md).

---

## 1. Os cinco lugares onde há documento

| Onde | Arquivos | Volume | Papel |
|---|---|---|---|
| **Pasta `_82` no Google Drive**, via unidade `M:` | 4.795 | 10,43 GB | Fonte da verdade dos documentos de cliente. **Não é sua**, é da mentora |
| **Pasta `_82` cópia local**, na Área de Trabalho | 2.712 | 5,40 GB | Cópia manual, já higienizada. Candidata a ser aposentada |
| **Projeto AMC IA**, `C:\amc-ia-Mobi` | 1.705 | 1,56 GB | Estúdio dos 4 agentes. **899 dos arquivos são cópia do `_82`** |
| **Pasta MOBI**, na Área de Trabalho | 6.243 | 11,64 GB | Acervo pessoal e profissional, reorganizado em 13 categorias |
| **Backups**, `C:\Users\rosep\Backups` | 2.363 | 1,56 GB | Rede de proteção. Ninguém trabalha aqui |

Mais o **backup do projeto na nuvem**, em `G:\Meu Drive\AMC-IA-Backup`, com 1.177 arquivos e 1,74 GB.

## 2. As automações

| O que | Situação |
|---|---|
| Tarefa "AMC IA - Backup diario", 12h30 | **Ativa e funcionando.** Rodou hoje às 12h30:01, resultado 0. Próxima em 22/08 |
| Backup do Projeto AMC IA para o disco | Rodando |
| Backup das credenciais para o disco | Rodando. 15 arquivos copiados |
| Backup do projeto para o Google Drive | Rodando |
| **Backup da pasta `_82` do Drive** | **SUSPENSO** desde 21/08, a pedido da captadora |
| Unidade virtual `M:` | Montada. Sobe pela inicialização do usuário |

**Atenção na unidade `M:`:** ela foi criada e recriada por processos desta ferramenta. Ainda **não foi testada num login real da captadora**. A confirmação só vem no próximo reinício: se `M:` aparecer sozinha no Explorer, está resolvido. Se não aparecer, é preciso trocar a abordagem.

## 3. A Área de Trabalho

Seis pastas: `CONTROLE EDITAIS`, `Credenciais AMC IA`, `Implentações Claude`, `MOBI`, `RESULTADO FINAL SNJ`, `_82 - Rosepaula Aparecida Andrade Rodrigues`.

Mais **27 arquivos soltos**, nunca organizados.

## 4. O repositório

Dez itens fora do controle de versão, entre eles a pasta `docs/estruturacoes/` inteira, o `scripts/backup-diario.bat`, o `scripts/montar-unidade-82.ps1` e o `docs/backup.md`. **Nada dos últimos dois dias foi versionado.**

---

# O que está pendente

## Grupo A. Não depende de ninguém

| # | O que | Ganho | Tempo |
|---|---|---|---|
| A1 | **Backup da pasta `_82` do Drive**, 10,43 GB. Era o combinado para as 18h | Fecha a única lacuna de proteção que resta | 15 a 25 min |
| A2 | **Commit no Git** de tudo dos últimos dois dias | Histórico versionado | 2 min |
| A3 | **Registrar a estruturação 11**, das credenciais, feita hoje sem registro | Rastreabilidade completa | 5 min |
| A4 | **Excluir instaladores** de `MOBI\90-BACKUPS-BRUTOS` | 1,63 GB | 2 min |
| A5 | **Excluir `MOBI\_DUPLICADOS`** | 1,05 GB | 2 min |
| A6 | Corrigir "dono" para "dona" nos registros 01 a 09 | Consistência | 2 min |

## Grupo B. Depende da mentora

| # | O que | Por quê |
|---|---|---|
| B1 | **Fechar o link público** da pasta `_82` e compartilhar com `gestao.mobilizando@gmail.com` | Hoje qualquer pessoa com o link vê CNH, CPF e RG de dirigentes de clientes. **É a pendência mais grave da lista** |
| B2 | **As 2.551 cópias soltas** em `06 - Clientes` no Drive, 5,04 GB | São a arrumação de 18/08 que ficou pela metade. Três clientes divergem e exigem conferência |

**Situação em 21/08 às 18h: as permissões continuam inalteradas.** A mentora ainda não respondeu.

## Grupo C. Decisões suas, sem prazo

| # | O que | Por quê importa |
|---|---|---|
| C1 | **A regra de fronteira entre o `_82` e o Projeto AMC IA** | 899 dos 1.045 arquivos de `minhas-oscs` são cópia do que está no `_82`. Enquanto não houver regra, ninguém sabe qual versão manda. **É a decisão estrutural mais importante que falta** |
| C2 | **Aposentar a cópia local do `_82`**, 5,40 GB | Só faz sentido depois que A1 rodar |
| C3 | **Os compactados de `MOBI\90-BACKUPS-BRUTOS`**, 2,35 GB | Precisa abrir e comparar antes |
| C4 | **A árvore completa** do computador e do Drive, explicada em detalhe | Pedido da captadora, adiado |
| C5 | **Os 27 arquivos soltos e as outras pastas da Área de Trabalho** | `CONTROLE EDITAIS`, `RESULTADO FINAL SNJ` e `Implentações Claude` nunca foram olhadas |

---

# Ordem recomendada

1. **A1**, o backup da `_82`. É 18h, é o combinado, e é a única lacuna de proteção que sobrou.
2. **A2 a A6** na sequência, que são rápidos e fecham a rastreabilidade.
3. **Cobrar B1 da mentora.** Não é urgência de organização, é exposição de dado pessoal de terceiro.
4. **Decidir C1**, que destrava a limpeza dos 899 arquivos duplicados.
5. O resto conforme a agenda permitir.
