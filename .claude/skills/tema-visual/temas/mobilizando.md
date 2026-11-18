# Tema Mobilizando

A identidade visual própria da Mobilizando Impacto Social, a mesma do feed aprovada em 23/09/2026, aplicada a qualquer peça: apresentação, documento, relatório, dossiê, página e card.

**Decisão dela em 28/09/2026:** o tema segue a identidade do feed **em tudo, sem exceção**. Um azul só, o `#19336B`, também em papel e PDF. Poppins no título e no texto, Inter só no apoio.

**Fonte da verdade:** o `02_CONTEUDO_Guia_Visual_Feed_2026.md` e as decisões da seção 6 do `00_INDICE_Estrutura_do_Projeto.md`, na pasta `mobilizando mkt - pasta 09/`. O Manual de Marca é a origem da paleta e das fontes, mas onde o Guia decidiu diferente, vale o Guia. Se este tema divergir da pasta 09, vale a pasta 09, e este arquivo se corrige.

## Paleta

| Cor | Hex | Papel |
|---|---|---|
| Azul | `#19336B` | Cor de texto sobre fundo claro; fundo da família "a lei diz" |
| Verde | `#1d624d` | Fundo da família "edital na mão"; títulos e faixas |
| Magenta | `#7f126f` | Fundo da família "editais abertos"; número grande, selo, alerta |
| Dourado | `#d1b484` | Fundo da família "com a Rosepaula"; arco, grifo, filete. **Nunca texto sobre fundo claro** |
| Creme | `#FAF6EE` | Quadro de destaque e papel |
| Branco | `#FFFFFF` | Fundo de documento e texto sobre fundo escuro |

O azul `#070552` do Manual **não se usa**: é quase preto e lê pior (decisão de 23/09/2026, estendida a tudo em 28/09/2026).

**Contraste (conferir sempre).**
- Texto sobre branco ou creme: azul `#19336B`, verde ou magenta. Nunca dourado.
- Texto sobre azul, verde ou magenta: branco.
- Texto sobre dourado ou creme: azul `#19336B`.
- Dourado só como fundo, forma, filete, grifo ou número grande sobre fundo escuro.

## As quatro famílias de conteúdo

A cor diz o que a peça é antes de a pessoa ler. Vale no feed e serve de guia fora dele.

| Família | Etiqueta | Cor |
|---|---|---|
| A regra | A LEI DIZ | azul |
| O caminho | EDITAL NA MÃO | verde |
| A oportunidade | EDITAIS ABERTOS | magenta |
| As pessoas | COM A ROSEPAULA | dourado |

Peça institucional que não cabe em nenhuma usa a etiqueta A MOBILIZANDO, de uso raro (25/09/2026).

## Tipografia

| Uso | Fonte |
|---|---|
| Título | **Poppins Bold** |
| Texto e listas | **Poppins SemiBold** |
| Etiqueta da família | Poppins Bold |
| Fonte da lei, legenda, rodapé | **Inter** |

As duas são do Google Fonts, gratuitas. Em página HTML, carregar pelo Google Fonts. Em Word e PowerPoint, embutir as fontes no arquivo ou entregar também em PDF, porque quem abre pode não ter as fontes. Nunca trocar por Arial Black nem por Montserrat.

Em peça para celular (1080x1350): título de 58 a 72 px, até 4 linhas; texto de 40 a 52 px; nada abaixo de 30 px. Em documento, manter a mesma hierarquia em tamanho de leitura.

## Formas da marca

Aprovadas por ela em 23/09/2026. No máximo **duas formas por peça**, fora a etiqueta e o rodapé.

- **Arco:** curva grossa e aberta, dourada, com uma curva fina branca por dentro, saindo do canto superior direito.
- **Bloco de canto único:** retângulo reto com um só canto arredondado, para palavra-chave e destaque.
- **Malha de linhas finas:** pauta discreta no rodapé, lembrando a folha de formulário e de edital.
- **Fundo de cor sólida:** a cor da família com grão fino, sem mancha e sem papel texturizado.
- **Símbolo em marca d'água:** o símbolo grande, a 14% de opacidade, nunca por cima de texto nem de foto.

Os oito elementos gráficos (grifo, selo de carimbo, citação da lei, checklist, etiqueta de prazo, linha do tempo, número grande e marca d'água) estão na seção 6.1 do Guia Visual do Feed, com a regra de uso de cada um.

## Símbolo e logo

- O símbolo da Mobilizando entra em toda peça, na versão de cor que combina com o fundo (decisão de 21/09/2026).
- Fundo escuro, foto, azul, verde ou magenta: símbolo branco com dourado.
- Fundo branco ou claro: símbolo marinho, magenta ou verde, com dourado, na cor de destaque da peça.
- Fundo dourado: símbolo marinho, porque as partes douradas somem.
- Arquivos no Canva (conta `rosepaulaandrade`, pasta "Logo completa" > PNG > Símbolo > Sem fundo) e na pasta `ARQUIVOS LOGO MOBILIZANDO_V2` da pasta 09. Os PNG "Sem fundo" têm lascas azuis nas bordas: limpar antes de usar em fundo verde.
- **Usos proibidos pelo Manual:** trocar a cor da logo, girar, usar em preto.

## Foto

Só a família das pessoas leva foto. A foto nunca entra recortada em moldura rasgada; entra inteira, nos formatos A, B e C da seção 5.1 do Guia Visual do Feed, com etiqueta e faixa de cor da família. Nada de pessoa de terceiros nem de imagem de IA.

## Fora do tema

O azul `#070552`, texto dourado sobre fundo claro, Arial Black, Montserrat, gradiente roxo, layout todo centralizado, folhas, papel rasgado e textura de papel, megafone, foguete, chuva de dinheiro, emoji na arte, brilho de promessa fácil e imagem gerada por IA.

## Tokens para página HTML

```css
:root {
  --mobi-azul: #19336B;
  --mobi-verde: #1d624d;
  --mobi-magenta: #7f126f;
  --mobi-dourado: #d1b484;
  --mobi-creme: #FAF6EE;
  --mobi-branco: #FFFFFF;
  --mobi-texto: #19336B;
  --mobi-fonte-titulo: 'Poppins', sans-serif;  /* 700 no título, 600 no texto */
  --mobi-fonte-apoio: 'Inter', sans-serif;
}
```

## Melhor uso

Apresentação institucional, portfólio, carteira Projetos em Captação, Dossiê do Edital entregue ao cliente, relatório de resultados, proposta comercial da assessoria, página da assessoria, cards e carrosséis.
