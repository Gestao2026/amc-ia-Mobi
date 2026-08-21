# Estado atual do ambiente

> Levantamento de 21/08/2026, 19h. Atualizar a cada rodada de estruturação.
> O histórico completo de cada ação está no [índice](README.md).

---

## 1. Os cinco lugares onde há documento

| Onde | Arquivos | Volume | Papel |
|---|---|---|---|
| **Pasta `_82` no Google Drive**, via unidade `M:` | 4.795 | 10,43 GB | Fonte da verdade dos documentos de cliente. **Não é sua**, é da mentora |
| **Pasta `_82` cópia local**, na Área de Trabalho | 2.712 | 5,40 GB | Cópia manual, já higienizada. **Agora redundante**, o backup a substitui |
| **Projeto AMC IA**, `C:\amc-ia-Mobi` | 1.785 | 1,56 GB | Estúdio dos 4 agentes. **899 dos arquivos são cópia do `_82`** |
| **Pasta MOBI**, na Área de Trabalho | 4.597 | 8,92 GB | Acervo pessoal e profissional, em 13 categorias |
| **Backups**, `C:\Users\rosep\Backups` | 7.156 | 11,99 GB | Rede de proteção. Ninguém trabalha aqui |

Dentro dos backups: `pasta-82\atual` com 4.792 arquivos e 10,43 GB,
`amc-ia-mobi` com 1.109 e 1,56 GB, `credenciais` com 15.

Mais o **backup do projeto na nuvem**, em `G:\Meu Drive\AMC-IA-Backup`.

**Disco livre: 265,4 GB.**

## 2. As automações

| O que | Situação |
|---|---|
| Tarefa "AMC IA - Backup diario", 12h30 | **Ativa.** Rodou em 21/08 às 12h30:01, resultado 0 |
| Backup do Projeto AMC IA para o disco | Rodando |
| Backup das credenciais para o disco, **nunca para a nuvem** | Rodando |
| Backup do projeto para o Google Drive | Rodando |
| **Backup da pasta `_82` do Drive** | **Rodando.** Primeira carga feita em 21/08 às 18h, 10,43 GB em 27 minutos |
| Unidade virtual `M:` | Montada. Sobe pela inicialização do usuário |

**Atenção na unidade `M:`:** em 21/08 ela caiu entre duas verificações e precisou ser remontada à mão. **A confirmação de que sobe sozinha só vem no próximo reinício.** Se `M:` não aparecer no Explorer depois de reiniciar, é preciso trocar a abordagem.

## 3. A Área de Trabalho

Seis pastas: `CONTROLE EDITAIS`, `Credenciais AMC IA`, `Implentações Claude`, `MOBI`, `RESULTADO FINAL SNJ`, `_82 - Rosepaula Aparecida Andrade Rodrigues`. Mais **27 arquivos soltos**, nunca organizados.

## 4. O repositório

**Tudo versionado.** O commit `9b0a57a`, de 21/08, trouxe 64 arquivos e 4.056 linhas: as 12 estruturações, o modelo, o índice, este estado, os scripts de backup e da unidade `M:`.

---

# O que está pendente

## Grupo A. Não depende de ninguém

**Concluído em 21/08.** Backup da `_82`, commit no Git, registro das credenciais, exclusão dos instaladores e da `_DUPLICADOS`, e o ajuste de tratamento nos registros.

## Grupo B. Depende da mentora

| # | O que | Por quê |
|---|---|---|
| B1 | **Fechar o link público** da pasta `_82` e compartilhar com `gestao.mobilizando@gmail.com` | Qualquer pessoa com o link vê CNH, CPF e RG de dirigentes de clientes. **É a pendência mais grave da lista** |
| B2 | **As 2.551 cópias soltas** em `06 - Clientes` no Drive, 5,04 GB | Três clientes divergem e exigem conferência |
| B3 | **Avisar** sobre o `.gdoc` renomeado e as duas planilhas atualizadas na pasta dela | Cortesia e transparência |

**Situação em 21/08 às 19h: as permissões continuam inalteradas.**

## Grupo C. Decisões suas, sem prazo

| # | O que | Por quê importa |
|---|---|---|
| C1 | **A regra de fronteira entre o `_82` e o Projeto AMC IA** | 899 dos arquivos de `minhas-oscs` são cópia do que está no `_82`. **É a decisão estrutural mais importante que falta** |
| C2 | **Aposentar a cópia local do `_82`**, 5,40 GB | Agora é possível: o backup diário já protege a pasta |
| C3 | **Os compactados de `MOBI\90-BACKUPS-BRUTOS`**, cerca de 2,2 GB | Precisa abrir e comparar antes |
| C4 | **A árvore completa** do computador e do Drive | Pedido da captadora, adiado |
| C5 | **Os 27 arquivos soltos e as outras pastas da Área de Trabalho** | `CONTROLE EDITAIS`, `RESULTADO FINAL SNJ` e `Implentações Claude` nunca foram olhadas |
| C6 | **Confirmar a unidade `M:` no próximo reinício** | Ver item 2 |

---

# Ordem recomendada

1. **Cobrar B1 da mentora.** Não é urgência de organização, é exposição de dado pessoal de terceiro.
2. **Decidir C1**, que destrava a limpeza dos 899 arquivos duplicados e define de vez quem guarda o quê.
3. **C2**, aposentar a cópia local, que libera 5,40 GB e acaba com a chance de as duas versões divergirem de novo.
4. O resto conforme a agenda permitir.
