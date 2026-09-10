---
description: Agente de declarações e anexos. Mapear os anexos do edital, gerar as declarações e montar o checklist de habilitação da submissão.
---

# /projeto-anexos

Aciona o agente de declarações e anexos para blindar a habilitação: tudo que o edital exige anexar, mapeado, gerado ou cobrado com prazo.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. Verifique se existe `edital.md`. Se não, rode `/edital-analisar` antes: o mapa de anexos nasce das exigências do edital.
3. Anuncie:
   ```
   🔍 Próximo passo: mapear os anexos do edital e gerar as declarações (agente de anexos). Tempo estimado: 2 a 4 minutos.
   ```
4. Acione o agente `captador-anexos`. Ele lista os anexos exigidos com o item do edital, classifica nos três grupos (o sistema gera, a OSC já tem, só o captador fornece), gera as declarações com os dados do perfil e monta o checklist mestre.
5. Mostre o checklist para aprovação (aprovar e salvar / ajustar) e responda às perguntas do agente sobre os itens que só você pode fornecer.
6. Confirme o salvamento: declarações em `projetos/{edital-slug}/documentos/` e o checklist em `projetos/{edital-slug}/checklist-anexos.md`. Informe os caminhos.
7. Próximo passo: `/projeto-avaliar` (se a proposta e o orçamento já existem) ou a estação que o `estado.md` apontar.

## Regras

- Cada anexo listado cita o item do edital que o exige.
- Declaração gerada fica "aguardando assinatura" até o captador confirmar.
- Nenhum dado inventado: o que falta no perfil vira pergunta.
- Português correto, sem travessão.
