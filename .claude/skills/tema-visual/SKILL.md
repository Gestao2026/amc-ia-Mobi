---
name: tema-visual
description: Aplicar um tema visual (cores, fontes e formas) a uma peça da AMC IA ou da Mobilizando, como apresentação, documento, Dossiê do Edital, relatório, carteira, página ou card. Traz o tema Mobilizando, tirado do Manual de Marca e das decisões da pasta 09, e permite criar temas novos com o OK da captadora. Usar quando ela pedir "aplica a identidade da Mobilizando", "deixa na cara da marca", "que cores e fontes eu uso", ou ao montar peça visual que sai em nome da Mobilizando.
---

# Tema visual

Versão nossa da skill `theme-factory` da Anthropic (licença Apache 2.0, ver `LICENSE.txt`). A original traz 10 temas genéricos em inglês e continua disponível pela conta dela como `anthropic-skills:theme-factory`. Esta aqui fala português, conhece a marca e segue as regras do projeto.

## Temas disponíveis

| Tema | Arquivo | Para quê |
|---|---|---|
| **Mobilizando** | `temas/mobilizando.md` | Tudo o que sai em nome da Mobilizando Impacto Social |

Amostra visual do tema: `temas/mobilizando-amostra.html`.

## Quando NÃO usar

- **Proposta, formulário e anexo que vão para o financiador.** Seguem o formulário oficial e o modelo do edital, sem identidade da Mobilizando. "Está no edital" vale também para a forma.
- **Peça que sai em nome da OSC cliente** (material da própria organização). Aí vale a identidade da OSC, não a da Mobilizando. Sem tema da OSC cadastrado, perguntar a ela.
- **Reel.** Segue o método próprio, no documento de ganchos da pasta 09.

## Passo a passo

### 1. Ler a fonte da verdade

Antes de aplicar, conferir se nada mudou: reler o `00_INDICE_Estrutura_do_Projeto.md` (seção 6, decisões) e o `02_CONTEUDO_Guia_Visual_Feed_2026.md`, na pasta `mobilizando mkt - pasta 09/`. É a leitura obrigatória da frente de Marketing (CLAUDE.md). Se houver decisão mais nova que o arquivo do tema, vale a decisão, e o tema se atualiza com uma linha no Histórico abaixo.

### 2. Mostrar o tema e confirmar

Peça em nome da Mobilizando usa o tema Mobilizando, sem perguntar: é a identidade dela, uma só, em tela e em papel (decisão de 28/09/2026). Perguntar só quando a peça não for da Mobilizando ou quando nenhum tema servir:

```
1. Tema Mobilizando
2. Criar um tema novo
```

Se ela quiser ver o tema antes, mostrar a amostra (`temas/mobilizando-amostra.html`).

### 3. Aplicar

Ler o arquivo do tema escolhido e aplicar em toda a peça:

- cores nos papéis descritos no tema, com o azul `#19336B` e nunca o `#070552`;
- Poppins Bold no título, Poppins SemiBold no texto e Inter no apoio;
- no máximo duas formas da marca por peça;
- símbolo da Mobilizando na versão de cor certa para o fundo.

Como aplicar em cada formato:

| Formato | Como |
|---|---|
| Página HTML ou artefato | tokens CSS do tema em `:root`, fontes pelo Google Fonts |
| Word (`.docx`) | skill de Word; estilos de título e corpo com as fontes e cores do tema; fontes embutidas ou PDF junto |
| PowerPoint (`.pptx`) | skill de PowerPoint; tema do slide mestre com as cores e fontes |
| Canva | kit de marca oficial "Mobilizando Impacto Social" (id `kAHVYC-Fz-w`), que já traz a marca |
| Imagem gerada por script | cores e fontes do tema; os geradores do feed ficam no scratchpad, conforme o Guia Visual |

### 4. Conferir antes de entregar

- **Contraste:** nenhum texto dourado sobre branco ou creme; texto sobre fundo escuro sempre branco.
- **Português:** acento, vírgula e ponto final em todo texto da peça, inclusive título e card (CLAUDE.md). Sem travessão.
- **Nada fora do tema:** a lista "Fora do tema" do arquivo do tema.

### 5. Mostrar e pedir aprovação

```
1. Aprovar e salvar
2. Quero ajustar algo
```

Peça de marketing aprovada termina na pasta 09, com o registro combinado lá (arquivo vivo, Histórico e decisão na seção 6).

## Criar um tema novo

Quando nenhum tema serve (por exemplo, um tema para uma OSC cliente ou para uma área, como meio ambiente):

1. Partir do material de quem é a marca: manual, logo, site ou peça oficial. Nunca inventar a identidade de uma organização real.
2. Montar o arquivo no mesmo formato de `temas/mobilizando.md`: paleta com papel de cada cor, contraste, tipografia, formas, logo e o que fica fora.
3. Mostrar a ela e só gravar em `temas/{slug}.md` com o OK.
4. Tema de OSC cliente que traga dado sensível ou nome de dirigente não entra neste repositório, que é público: fica em `minhas-oscs/{slug}/`.

## Histórico

- 28/09/2026 (Claude Code): tema refeito na identidade do feed, sem exceção, por decisão dela (um azul só, #19336B; Poppins no texto).
- 28/09/2026 (Claude Code): skill criada a pedido dela, adaptada da `theme-factory` da Anthropic, com o tema Mobilizando.
