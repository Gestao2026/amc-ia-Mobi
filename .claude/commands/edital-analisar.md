---
description: Ler um edital (PDF, link ou texto colado) e extrair critérios, prazos, exigências, o que pontua e o que derruba.
---

# /edital-analisar

Lê um edital por completo e o transforma em um resumo estruturado que alimenta os 4 agentes. Sem entender o edital, nada do resto funciona.

## Passo 0. Contexto

Leia `minhas-oscs/.ativa` e o `perfil-osc.md`.

## Passo 1. Obter o edital

Pergunte como o captador vai fornecer o edital:
1. Colar o texto.
2. Caminho de um PDF na máquina (leia o arquivo).
3. Link do edital (use a leitura de página; se indisponível, peça o texto ou o PDF).

## Passo 2. Anúncio

```
🔍 Próximo passo: fazer a primeira leitura do edital e dos anexos (11 blocos). Tempo estimado: 4 a 8 minutos.
```

## Passo 3. A primeira leitura

**Leia `minhas-oscs/MODELO-edital.md` antes de começar.** Ele define os 11 blocos e todos os campos do `edital.md`. A extração segue aquele modelo, na ordem, e não uma lista livre.

Consulte também `.claude/skills/editais-fundamentos/SKILL.md`.

Leia o edital inteiro **e cada anexo**, não só o edital. A maior parte do que decide está nos anexos: o termo de execução costuma fixar o valor real, os formulários revelam qual campo alimenta qual critério, as planilhas revelam a estrutura de rubricas, e os anexos de critérios trazem a escala que o corpo do edital não detalha.

Regras de preenchimento, todas do modelo:

- Todo campo cita o item do edital ou do anexo.
- Campo sem previsão no edital fica escrito **não encontrado**, com onde foi procurado. Nunca deduzir pelo que é comum no setor.
- Campo que não se aplica fica escrito **não se aplica**.
- Documento facultativo que pontua vem rotulado como facultativo, separado do obrigatório.
- Os três momentos da ficha documental (inscrição, habilitação, prestação de contas) nunca se misturam.
- Divergência entre edital e anexo vai numerada no bloco 11, com a leitura mais exigente adotada.

## Passo 4. Salvamento e entrega

Crie ou atualize a pasta `minhas-oscs/{ativa}/projetos/{edital-slug}/` e salve `edital.md` com os 11 blocos. Crie também um `estado.md` marcando a etapa "edital analisado". Informe o caminho.

**A análise de edital não tem teto de tamanho.** Ela é documento técnico, e a profundidade acompanha a complexidade do edital.

Abra pelo **semáforo e pela ficha**, que é o resumo executivo e serve para decidir em dez segundos se vale a pena entrar. **Isso não substitui nem limita a análise:** o restante dos blocos vem na sequência, na mesma resposta.

A prioridade é **completude, precisão e utilidade estratégica**. Em tudo o que entregar, deixe rotulado o que é **exigência do edital**, o que é **risco**, o que é **critério de avaliação** e o que é **recomendação sua**, e diga como cada coisa impacta a elaboração de um projeto competitivo.

Só gere Word e PDF se o captador pedir, com `/edital-dossie`.

## Passo 5. Próximo passo

Sugira `/projeto-elegibilidade` (CaptaDoc) para checar se a OSC pode participar antes de qualquer elaboração.

## Regras

- Não invente exigência que não esteja no edital. Se algo estiver ambíguo, marque "verificar no edital".
- Português correto, sem travessão.
