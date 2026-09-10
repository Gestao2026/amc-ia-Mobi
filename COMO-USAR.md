# Como Usar a AMC IA

Guia rápido para o captador. O sistema te conduz do edital ao projeto pronto para submeter, na ordem certa, sem deixar você pular etapas que reprovam projeto.

## A jornada em 9 passos

```
1. Cadastrar a OSC        /osc-nova
2. Pegar editais          /edital-minerar          (puxa do CaptaHub)
3. Analisar o edital      /edital-analisar
4. Checar elegibilidade   /projeto-elegibilidade   (CaptaDoc)
5. Escrever a proposta    /projeto-escrever        (CaptaBuilder)
6. Montar o orçamento     /projeto-orcamento       (CaptaBudget, com cotações na web)
7. Preparar os anexos     /projeto-anexos          (declarações e checklist)
8. Avaliar e revisar      /projeto-avaliar         (CaptaScore) + /projeto-revisar
9. Exportar e submeter    /projeto-exportar        (Word, PDF e planilha prontos)
```

**Atalho:** o comando `/projeto-completo` roda a linha inteira de uma vez, com o chefe do CaptaSuite validando cada estação e pedindo a sua aprovação nos pontos-chave. É o caminho recomendado quando você já escolheu o edital.

A AMC IA é o estúdio que produz o projeto. A gestão da carteira (pipeline, clientes, prazos) fica no CaptaHub, e é de lá que vêm os editais. Conecte uma vez com `/captahub-conectar`.

## Primeiro uso

1. Abra a pasta do projeto no Claude Code.
2. Diga "oi" ou já comece com `/osc-nova`. O sistema cadastra a sua primeira organização, uma pergunta por vez.
3. Com a OSC cadastrada, rode `/edital-minerar` para ver os editais mais alinhados, ou `/edital-analisar` se você já tem um edital em mãos (cole o texto, o PDF ou o link).

## A regra de ouro do sistema

A AMC IA nunca deixa você escrever a proposta antes de checar a elegibilidade. Esse é o Gate de Elegibilidade. Ele existe para acabar com a pior dor do captador: gastar semanas num projeto e descobrir, tarde demais, que a OSC nem podia participar.

## O CaptaSuite. Quem faz o quê

O time tem um chefe e cinco estações.

**O chefe**

- **Captador (`captador-chefe`).** Consultor sênior com mais de 25 anos de mercado. Domina o MROSC, as leis de incentivo e as regras de prestação de contas. Ele escolhe qual edital vale a pena disputar (e diz qual não disputar), valida cada estação em três níveis (Aprovado, Aprovado com ressalvas, Refazer) e é o único que libera a submissão. Se ele não liberar, o projeto não sai.

**A linha de montagem**

- **CaptaDoc.** Diz se a OSC pode participar (APTO, APTO COM PENDÊNCIAS, INAPTO) e lista os documentos.
- **CaptaBuilder.** Escreve a proposta completa, bloco a bloco, ancorada no edital.
- **CaptaBudget.** Monta o orçamento por rubrica, com memória de cálculo, sem tomar glosa. Faz cotação na web: 3 fontes por item, e o valor que entra é a mediana.
- **Anexos (`captador-anexos`).** Mapeia todos os anexos do edital, gera as declarações e monta o checklist de habilitação. É o que evita perder por documento faltando.
- **CaptaScore.** Dá nota por critério e estima a chance de aprovação antes de você enviar. É o que ninguém mais faz.

**Apoio**

- **Revisor (`revisor-proposta`).** A última leitura antes de submeter. Confere completude, coerência, conformidade com o edital, português e se a proposta bate com o perfil real da sua OSC. Salva o `revisao.md`.
- **Contratos (`captador-contrato`).** Minuta o contrato de assessoria com a OSC e analisa o termo de fomento ou colaboração do financiador quando o projeto é aprovado.
- **Mineradores.** `minerador-editais` puxa do CaptaHub; `minerador-web` varre a web quando o CaptaHub não traz nada alinhado.

## Atendendo várias OSCs

Se você é assessor e atende mais de uma organização, cada uma tem a sua pasta. Use `/osc-trocar` para alternar entre elas e `/osc-perfil` para ver ou atualizar os dados de uma OSC.

## Virar um captador contratado (Fase 2. Posicionar)

Dominar a técnica é metade. A outra metade é ser encontrado e contratado. A Fase 2 cuida do seu negócio como assessor, e o público aqui são os gestores de OSC que vão te contratar.

```
1. Cadastrar você e a marca   /captador-perfil
2. Estruturar a oferta        /assessoria-estruturar   (escopo, pacotes, preço)
3. Se posicionar              /captador-conteudo       (carrossel, post, reel)
4. Página da assessoria       /captador-pagina         (captura de leads de OSC)
5. Anúncios para atrair OSCs  /captador-anuncio
6. Vender o contrato          /assessoria-pitch        (roteiro da reunião)
7. Fechar o contrato          /contrato                (minuta da assessoria)
```

Comece sempre pelo `/captador-perfil`. Sem ele, o conteúdo e a página saem genéricos. Se você ainda tem poucos projetos aprovados, o sistema apoia a sua autoridade na jornada de origem e no método, não só no currículo.

## O que o sistema salva na pasta do projeto

Cada projeto vive em `minhas-oscs/{sua-osc}/projetos/{edital}/` e acumula:

| Arquivo | Quem gera |
|---|---|
| `edital.md` | `/edital-analisar` |
| `elegibilidade.md` | CaptaDoc |
| `proposta.md` | CaptaBuilder |
| `orcamento.md` e `cotacoes.md` | CaptaBudget |
| `checklist-anexos.md` e `documentos/` | Anexos |
| `score.md` | CaptaScore |
| `revisao.md` | Revisor |
| `parecer-chefe.md` | Captador (chefe) |
| `estado.md` | todos, a cada etapa |
| `entrega-final/` | `/projeto-exportar` |

## Explorar o exemplo

Já deixei uma organização fictícia cadastrada (Instituto Semente) com um projeto completo de exemplo (proposta, orçamento e a entrega final exportada), só para você ver o sistema funcionando. Rode `/osc-trocar`, escolha o Instituto Semente e abra a pasta `projetos/edital-cultura-viva-2026/entrega-final/` para ver os arquivos prontos. Pode apagar a pasta `minhas-oscs/exemplo-instituto-semente/` quando quiser.

## Ver os agentes trabalhando (Sala dos Agentes)

Abra `sala-dos-agentes.html` (na raiz do projeto) no navegador e deixe em uma janela ao lado enquanto trabalha. É um escritório em pixel art onde cada agente da captação circula até a sua estação e mostra num balão o que está fazendo a cada passo do sistema. O comando `/sala-agentes` te dá o caminho e explica o elenco. Se todos estiverem parados, é só porque nada aconteceu nos últimos segundos.

## Atualizar a base de editais

A pasta `base-editais/` tem os editais abertos do momento da exportação. Para atualizar, use `/configurar` ou conecte o CaptaHub com `/captahub-conectar`.

## Se alguma coisa não funcionar

**O PDF não é gerado na exportação.** O sistema procura o Google Chrome (ou o Edge) para gerar o PDF sozinho. Se não achar nenhum dos dois, ele gera os arquivos `-impressao.html`: abra no navegador e use Imprimir, depois Salvar como PDF. O resultado é o mesmo.

**Os comandos com `python3` dão erro no Windows.** Alguns computadores só têm o comando `python`. Abra o `.claude/settings.json` e troque `python3` por `python` nas linhas de hook e de permissão.

**O sistema reclama de acentuação.** O verificador separa em dois blocos. **CORRIGIR** é erro de verdade, arrume. **CONFERIR** são palavras como "esta", em que a forma sem acento também existe ("esta proposta" está certo, "esta pronto" está errado): só mude se for o caso.
