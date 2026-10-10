---
description: Gerar conteúdo do Instagram da Mobilizando (reel, carrossel, card ou story), a partir da pasta 09, no método de reels da Mentoria AMC e na identidade própria da marca. Pilar 5 (Audiência).
---

# /captador-conteudo

Gera conteúdo que posiciona a captadora como referência em captação e atrai gestores de OSC, no perfil @rosepaula_rodrigues.

> **A pasta 09 é a fonte da verdade** (`mobilizando mkt - pasta 09/`). Este comando **não guarda regra própria** de gancho, legenda, cor ou horário: ele lê a pasta a cada uso e segue o que estiver lá. Se uma decisão nova entrar no `00_INDICE`, ela passa a valer na próxima peça, sem mexer aqui. Em divergência entre este arquivo e a pasta 09, vale a pasta 09.

## Passo 0. Leitura obrigatória, antes de propor qualquer coisa

Sem esperar pedido (regra do CLAUDE.md, convivência com o chat do claude.ai):

1. `00_INDICE_Estrutura_do_Projeto.md` inteiro, **começando pelos dois blocos da seção 0, "Onde paramos"**, e a seção 6 de decisões.
2. Os documentos do formato pedido:

| Formato | Documentos |
|---|---|
| Reel | `02_CONTEUDO_REF_Metodo_Reels_do_Captador_Mentoria_AMC.md` (método), `02_CONTEUDO_Desafio_30_Dias_2026.md` (ganchos aprovados por data), `02_CONTEUDO_Ganchos_Reels_2026.md` (a última leva é o molde; trilhas e ids ficam ali), `02_CONTEUDO_REF_Inventario_Acervo_2026.md` (imagem) |
| Card, carrossel ou story | `02_CONTEUDO_Guia_Visual_Feed_2026.md` (cores, famílias, fontes, formas, elementos), `02_CONTEUDO_Feed_Carrosseis_e_Cards_2026.md` e `02_CONTEUDO_Cronograma_Feed_Outubro_2026.html` (o que está previsto), `02_CONTEUDO_Series_Feed_Textos_*` (séries fixas) |
| Qualquer um | `02_CONTEUDO_Linha_Editorial_2026.md` (tom e seção 5A), `02_CONTEUDO_REF_Publico_do_Instagram_2026.md` (quem segue), `02_CONTEUDO_Quando_a_Rosepaula_Aparece_2026.md` |

3. **O que já está agendado**, pela conexão do Metricool (só leitura), para não repetir tema nem horário e para honrar o gancho que a peça anterior prometeu na legenda.
4. As memórias de marketing do `MEMORY.md` (imagem, foto de terceiros, Canva, trilha, cores e fontes).

Diga em uma linha quais arquivos foram usados. **Não refazer o que já existe:** se o gancho, o texto ou a pauta já estão na pasta, partir deles.

## Passo 1. Entrevista curta

Uma pergunta por vez, com opções numeradas, e só o que a pasta 09 não responder:

1. Formato (1. reel, 2. carrossel, 3. card, 4. story).
2. Para reel: qual data do cronograma, ou quantos reels (uma leva inteira ou um só).
3. Para feed: qual peça do cronograma, ou tema novo (e aí, qual família).

Se o pedido contrariar uma decisão registrada no índice, aponte a decisão e espere o OK antes de seguir.

## Passo 2. Geração

Anuncie o próximo passo e acione o agente `posicionador-captador`, que escreve no molde da pasta 09:

- **Reel:** o formato de saída do método (bloco 10): categoria, gancho da tela, entrega parcial item a item, caixa de saída, cena, trilha, duração, legenda completa na ordem das 6 partes, fonte e teste da lacuna. A legenda termina chamando o reel seguinte, que precisa existir no horário.
- **Feed:** textos lâmina a lâmina, família e etiqueta, elementos gráficos (no máximo dois), texto alternativo e legenda.

**Integridade, sem exceção:** todo número, lei, artigo, prazo e valor é conferido na fonte primária antes de ir para a peça, com a data da conferência. O que não foi conferido sai marcado `[CONFERIR]` e **não vai ao ar**. "A maioria" só com fonte. Nunca prometer aprovação.

## Passo 3. Arte e vídeo

- **Identidade:** aplicar pela skill `tema-visual` e pelo `02_CONTEUDO_Guia_Visual_Feed_2026.md`. No reel, seguir o que o índice registrar sobre a identidade dos reels; enquanto não houver decisão, apresentar amostra antes de produzir a leva.
- **Imagem:** Canva Pro dela primeiro; banco gratuito só com licença comercial conferida item a item (o Pexels serve; no Mixkit, conferir cada vídeo). Sem rosto de terceiros, sem imagem de IA. Tela de portal público pode ser gravada.
- **Vídeo:** 1080x1920, dentro da duração do método, sem áudio no arquivo (a trilha entra pelo Metricool, escolhida por ela).
- Salvar com o padrão de nome da pasta 09 (`02_CONTEUDO_AAAA-MM-DD_TIPO_Tema_Rede.ext`), em `02_CONTEUDO_VIDEOS_EDITADOS/` ou `02_CONTEUDO_POSTAGENS_PRONTAS/`.

## Passo 4. Revisão, aprovação e agendamento

1. Revisão de português pela skill `revisar-portugues` (acento, pontuação e travessão), no texto da tela e na legenda.
2. Prévia única da leva para ela:
   ```
   1. Aprovar
   2. Quero ajustar algo
   ```
3. **Agendar no Metricool só com o OK dela, a cada leva.** Publicar é escrita externa. Depois de agendar, conferir e anotar os ids.

## Passo 5. Registro (obrigatório, na mesma conversa)

- Roteiros e legendas no documento vivo da pasta 09 (a próxima seção do `02_CONTEUDO_Ganchos_Reels_2026.md`, no caso de reel), com uma linha no Histórico.
- Decisão nova na seção 6 do `00_INDICE`, e o bloco do Claude Code da seção 0 reescrito (passagem de turno).
- Rascunho não aprovado fica marcado como rascunho.

## Regras de escrita

- Português com acentuação e pontuação completas, também no texto da tela. Sem travessão, sem ponto de exclamação, sem hashtag, sem meta-texto.
- Tema de apelo universal, com 90% de apelo geral e 10% de produto; todo reel de apelo geral termina num serviço da arquitetura da assessoria.
- A trajetória dela é prova de autoridade, não promessa de serviço.
