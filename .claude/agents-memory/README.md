# Memória dos Agentes

Os agentes da AMC IA são stateless por padrão, mas guardam memória persistente em dois escopos:

- **Global por agente:** `.claude/agents-memory/{nome-agente}.md`. Preferências do captador e padrões validados que valem para qualquer OSC (ex: estilo de redação preferido, financiadores recorrentes, modelos de orçamento aprovados).
- **Por OSC e agente:** `minhas-oscs/{ativa}/agentes/{nome-agente}.md`. Contexto específico daquela organização (ex: histórico de editais já tentados, documentos pendentes recorrentes, áreas que mais aprovam).

Ambas as pastas ficam fora do git. Só este `README.md` é versionado.

## Schema

```markdown
# Memória do agente {nome}

## Preferências observadas
- padrões do captador

## Padrões validados
- decisões que funcionaram (propostas aprovadas, orçamentos sem glosa)

## Notas por sessão
- `2026-06-26`: descrição curta do que foi decidido
```

## Higiene

- Nunca gravar tokens, senhas, CPF/CNPJ de terceiros ou dados sensíveis de beneficiários.
- Cada nota de sessão com data no formato AAAA-MM-DD.
- Máximo de ~500 linhas por arquivo.
- Se o captador pedir "ignore a memória", o agente não carrega nem atualiza.

## Fluxo

No Passo 0, todo agente lê as duas memórias (se existirem). Ao encerrar, anexa aprendizados genéricos na memória global e aprendizados da organização na memória por OSC.
