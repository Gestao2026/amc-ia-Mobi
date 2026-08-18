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
🔍 Próximo passo: analisar o edital e extrair critérios, prazos e exigências (8 pontos). Tempo estimado: 2 a 4 minutos.
```

## Passo 3. Extração

Consulte `.claude/skills/editais-fundamentos/SKILL.md`. Extraia e organize:

1. **Identificação.** Órgão, número do edital, objeto, modalidade (termo de fomento, colaboração, chamamento, lei de incentivo).
2. **Quem pode participar.** Natureza jurídica aceita, tempo de existência, território, área temática.
3. **Documentos exigidos** para habilitação.
4. **Valores.** Teto total, teto por item ou categoria, percentuais máximos (pessoal, administrativo), contrapartida exigida.
5. **Despesas permitidas e vedadas.**
6. **Critérios de pontuação** e seus pesos. O que mais pontua e o que derruba.
7. **Prazos.** Data e hora de submissão, vigência do projeto, cronograma do edital.
8. **Forma de submissão.** Plataforma (Transferegov, sistema próprio), formato dos anexos, formulário oficial.

## Passo 4. Salvamento

Crie ou atualize a pasta `minhas-oscs/{ativa}/projetos/{edital-slug}/` e salve `edital.md` com a extração. Crie também um `estado.md` marcando a etapa "edital analisado". Informe o caminho.

## Passo 5. Próximo passo

Sugira `/projeto-elegibilidade` (CaptaDoc) para checar se a OSC pode participar antes de qualquer elaboração.

## Regras

- Não invente exigência que não esteja no edital. Se algo estiver ambíguo, marque "verificar no edital".
- Português correto, sem travessão.
