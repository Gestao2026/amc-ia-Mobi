---
description: Puxar os editais do CaptaHub e listar os mais alinhados ao perfil da OSC ativa (escopo, valor, prazo, área).
---

# /edital-minerar

Os editais vêm do CaptaHub (a fonte da verdade). Este comando entra no CaptaHub, atualiza o cache local e lista os editais com maior aderência ao perfil da OSC ativa.

## Passo 0. Contexto

Leia `minhas-oscs/.ativa` e o `perfil-osc.md`. Se não houver OSC ativa, oriente `/osc-nova` primeiro.

## Passo 1. Anúncio

```
🔍 Próximo passo: puxar os editais do CaptaHub e listar os alinhados à OSC. Tempo estimado: cerca de 30 segundos.
```

## Passo 2. Atualizar do CaptaHub

Rode `scripts/captahub-editais.py` para puxar os editais ao vivo e atualizar o cache. Se o CaptaHub não estiver conectado (sem credenciais no `.env`), avise que está usando o último cache local e ofereça `/captahub-conectar`. O sistema não trava: segue com o cache.

## Passo 3. Execução

Acione o agente `minerador-editais`. Ele roda `scripts/minerar-editais.py` com os filtros do perfil (escopo, área, faixa de valor, prazo mínimo), descarta vencidos e aplica o ranking de aderência (ALTA, MÉDIA, BAIXA).

Filtros opcionais que o captador pode pedir: só um escopo (municipal/estadual/nacional), faixa de valor específica, prazo mínimo de dias para submeter, palavra-chave de área.

## Passo 3.1. Fallback de varredura web (quando o CaptaHub não traz candidato)

Se a mineração do CaptaHub não retornar nenhum edital alinhado ao perfil (zero candidatos, ou nenhum com aderência ALTA ou MÉDIA), NÃO pare por aí. Acione o agente `minerador-web` como complemento: ele varre a web (portais de editais, Transferegov, leis de incentivo, fundações e institutos) procurando editais abertos que sirvam à OSC, confirma o prazo na fonte e devolve candidatos no mesmo formato.

Anuncie antes: "🔍 Próximo passo: o CaptaHub não trouxe edital alinhado, fazendo uma varredura na web (cerca de 1 a 2 minutos)." Passe ao agente o perfil da OSC e os editais que o CaptaHub já trouxe (para não repetir).

O CaptaHub continua sendo a fonte principal. A varredura web é cobertura extra: o que aparecer vem marcado como "ainda não está no CaptaHub", e os bons devem ser cadastrados lá para entrar na carteira.

## Passo 4. Entrega

Apresente a lista priorizada (top 10 a 15) em tabela: edital, órgão, escopo, valor, prazo, aderência, motivo em uma linha. Se houver resultados da varredura web, traga-os em um bloco à parte, marcado como "fonte: web, ainda não está no CaptaHub".

Para os de ALTA aderência, ofereça abrir o projeto: criar a pasta `projetos/{edital-slug}/` e gravar um `edital.md` inicial com os dados (da base do CaptaHub ou da fonte web). Para os achados na web, sugira também cadastrá-los no CaptaHub.

## Passo 5. Próximo passo

Sugira `/edital-analisar` para aprofundar o edital escolhido e, na sequência, `/projeto-elegibilidade`.

## Regras

- Nunca recomende edital com prazo vencido.
- A aderência é indicativa; o veredito de elegibilidade é do CaptaDoc.
- Português correto, sem travessão.
