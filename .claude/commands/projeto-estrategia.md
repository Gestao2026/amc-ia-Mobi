---
description: CaptaEstrategista. Decidir se vale a pena entrar no edital e qual é a estratégia para aumentar a chance de aprovação.
---

# /projeto-estrategia

Aciona o CaptaEstrategista, a quinta estação da linha de montagem. Ele entra **depois** do sinal verde da elegibilidade e **antes** de qualquer linha de proposta ser escrita.

A elegibilidade responde "podemos participar". Esta etapa responde **"vale a pena entrar, e como ganhamos"**.

## Passo 0. Contexto e dependência

Leia `minhas-oscs/.ativa`, o `perfil-osc.md` e, na pasta do projeto, o `edital.md` e o `elegibilidade.md`.

**Dependência dura:**

- Sem `edital.md`, oriente `/edital-analisar` primeiro.
- Sem `elegibilidade.md`, oriente `/projeto-elegibilidade` primeiro.
- Com veredito **INAPTO NO MOMENTO**, não rode. Não existe estratégia para quem não pode entrar. Explique e ofereça `/edital-minerar`.

## Passo 1. A entrevista

No máximo cinco perguntas, **uma por vez**, e só as que o disco não responde. Se o perfil ou o dossiê já respondem, não pergunte.

1. Qual é o projeto ou a ideia que a organização quer inscrever? (se não houver, a etapa roda no **modo B**)
2. Quanto tempo e quantas pessoas você tem para este edital até o prazo?
3. Existe algo que o cliente não pode ou não quer fazer?
4. Você tem resultado ou parecer de edição anterior deste edital ou deste financiador?
5. Existe evidência forte do cliente que ainda não está no perfil?

## Passo 2. Anúncio

```
🔍 Próximo passo: avaliar se vale a pena entrar neste edital e montar a estratégia (CaptaEstrategista, 8 análises). Tempo estimado: 3 a 6 minutos.
```

Se for buscar na web, anuncie em uma linha o que vai procurar.

## Passo 3. Execução

Acione o agente `captador-estrategista`. Ele produz as oito análises e a recomendação em quatro estados, com toda afirmação rotulada em uma das quatro marcas: `[EDITAL]`, `[DADO]`, `[INFERÊNCIA]` ou `[RECOMENDAÇÃO]`.

**Trava de privacidade na busca externa:** nenhuma pesquisa pode conter nome da organização, CNPJ, nome de dirigente ou endereço. A busca é sobre o edital e o financiador, nunca sobre quem se inscreve.

## Passo 4. Entrega

Mostre na tela, **sem teto de tamanho**, nesta ordem: o semáforo e a decisão em uma frase; as três razões; as oito análises; o que falta saber; o próximo passo.

Salve em `projetos/{edital-slug}/estrategia.md` e informe o caminho. Atualize o `estado.md` seguindo `minhas-oscs/MODELO-estado.md`, marcando a linha da estratégia e gravando o semáforo na ficha. **Não reescreva um `estado.md` antigo para encaixá-lo no modelo**: acrescente o que falta e deixe o resto como está.

## Passo 5. Próximo passo, conforme o semáforo

| Semáforo | O que fazer |
|---|---|
| 🟢 Prioridade alta | Sugira `/projeto-escrever` |
| 🟡 Oportunidade condicionada | Liste os ajustes nomeados, com prazo, e diga que a escrita pode começar em paralelo |
| 🟠 Baixa prioridade | Mostre a conta de esforço contra retorno e pergunte se ela quer seguir assim mesmo |
| 🔴 Não recomendar | Explique o motivo, ofereça `/edital-minerar`, e **pergunte se ela quer seguir assim mesmo** |

**O 🔴 não trava a elaboração.** O único Gate duro do sistema continua sendo o da elegibilidade. Se a captadora disser que segue, registre a confirmação dela no `estrategia.md`, com a data, e o trabalho continua normalmente.

## Regras

- Não prometa aprovação, em nenhuma formulação.
- Não invente concorrência, número de inscritos nem histórico de programa. Sem fonte oficial, escreva que não encontrou e onde procurou.
- Não misture recomendação com exigência do edital.
- Português correto, sem travessão. Não mostre código.
