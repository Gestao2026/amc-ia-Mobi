---
name: revisar-portugues
description: Revisão de português de um texto ou arquivo da AMC IA (proposta, parecer, orçamento, dossiê, legenda, roteiro de reel, página). Confere acentuação, travessão e pontuação conforme as regras do CLAUDE.md, aponta cada problema com a linha e propõe a correção. Só altera o arquivo com o OK da captadora. Usar quando ela pedir "revisa o português", "confere a acentuação", "tem travessão?" ou antes de entregar um texto a ela, se ela pedir.
---

# Revisar português

Revisão sob pedido. Nada aqui roda sozinho: a skill só age quando a captadora chama, ou quando ela pede a revisão de uma entrega (regra NADA RODA SOZINHO do CLAUDE.md).

## O que se confere

As três regras do CLAUDE.md, nesta ordem:

1. **Acentuação** (Acordo Ortográfico de 1990), inclusive a lista de palavras que jamais podem aparecer sem acento.
2. **Travessão.** Nenhum travessão (—) em texto de proposta, parecer, orçamento, legenda ou página. Trocar por vírgula, ponto, dois pontos ou parênteses. A meia-risca solta entre espaços ( – ) conta como travessão.
3. **Pontuação** (decisão de 21/09/2026). Vírgula onde a escrita pede e ponto final no fim de toda frase, inclusive gancho de reel, texto na tela, legenda, título de card e item de lista que forma frase. Frase sem ponto só em rótulo curto: botão, etiqueta, nome de coluna.

**Fica de fora, sempre:** nome de arquivo, variável, slug, chave JSON, caminho, comando com barra e identificador interno. Esses continuam em ASCII sem acento.

## Passo a passo

### 1. Saber o que revisar

- Se ela deu o caminho, usar esse arquivo.
- Se colou o texto na conversa, revisar o texto colado.
- Se não disse, perguntar em uma linha qual arquivo ou texto.

Arquivos aceitos pelo conferidor: `.md`, `.html`, `.htm`, `.txt` e `.docx`. Para PDF, pedir o arquivo de origem (Word ou `.md`), porque corrigir PDF não resolve a fonte.

### 2. Rodar o conferidor

Anunciar antes, se o arquivo for longo:

```
🔍 Próximo passo: revisar o português de {arquivo} (3 passos). Tempo estimado: 30 a 90 segundos.
```

```bash
python .claude/skills/revisar-portugues/scripts/revisar.py "<arquivo>"
```

Ele aceita vários arquivos de uma vez. Aponta acento e travessão com o número da linha (ou do parágrafo, no Word). Não altera nada.

O conferidor é heurístico:
- **CORRIGIR**: a forma sem acento não existe; é erro.
- **CONFERIR**: a forma sem acento também existe ("esta proposta" está certo; "esta pronto" não). Decidir pelo contexto, lendo a frase.
- Ele não conhece todas as palavras. Uma palavra fora da lista passa sem aviso, e é por isso que o passo 3 existe.

Texto colado na conversa não passa pelo conferidor: vai direto para o passo 3.

### 3. Reler frase por frase

A releitura é a verificação que vale (CLAUDE.md, verificação obrigatória). Ler o texto inteiro, frase por frase, procurando:

- acento que o conferidor não pegou;
- vírgula faltando ou sobrando;
- frase ou item de lista sem ponto final;
- travessão que tenha escapado (por exemplo, dentro de tabela ou de título).

Não corrigir estilo, conteúdo nem escolha de palavra. Revisão de português não é reescrita. Se algo do conteúdo chamar a atenção, apontar à parte, em uma linha, sem mexer.

### 4. Mostrar o resultado

Um quadro curto, só com o que precisa mudar:

| Onde | Está assim | Fica assim | Regra |
|---|---|---|---|
| linha 12 | "nao ha prazo" | "não há prazo." | acento e ponto final |
| linha 30 | "meta — 200 pessoas" | "meta: 200 pessoas" | travessão |

Depois, o total por regra (acento, travessão, pontuação) e as dúvidas de CONFERIR que dependem dela, se houver.

Se não houver nada: dizer em uma linha que o texto está limpo nas três regras.

### 5. Corrigir só com o OK

```
1. Aprovar e corrigir tudo
2. Corrigir só parte (diga quais)
3. Só o relatório, não mexer
```

Com o OK, fazer **edições cirúrgicas**: trocar só o trecho apontado, nada além. No `.docx`, editar pelo Word preservando a formatação (usar a skill de Word); nunca recriar o documento. Depois de corrigir, rodar o conferidor de novo e confirmar:

```
✅ Concluído: {N} correções em {arquivo}. Caminho: {caminho absoluto}
```

## Limites

- Arquivo na pasta `_82` ou em `06 - Clientes`: só relatório. Corrigir ali depende de ela dizer que pode, conforme as regras dessas pastas.
- Arquivo de outra pessoa (cliente, financiador, edital): só relatório, nunca corrigir.
- Documento assinado ou já protocolado: só relatório.
