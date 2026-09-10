---
description: Declarações e anexos. Mapear os anexos do edital, gerar as declarações e montar o checklist de habilitação da submissão.
---

# /projeto-anexos

Aciona o agente de declarações e anexos para blindar a habilitação: tudo que o edital exige anexar, mapeado, gerado ou cobrado com prazo.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. Verifique a pasta do projeto:
   - Sem `edital.md`, rode `/edital-analisar` antes: o mapa de anexos nasce dos blocos 6 e 7 da leitura do edital.
   - Sem `elegibilidade.md`, rode `/projeto-elegibilidade` antes.
   - Com veredito INAPTO NO MOMENTO, não prossiga: explique o impedimento.
3. Anuncie:
   ```
   🔍 Próximo passo: mapear os anexos do edital e gerar as declarações (4 passos). Tempo estimado: 2 a 4 minutos.
   ```
4. Acione o agente `captador-anexos`. Ele lista os anexos exigidos com o item do edital, separa os três momentos (inscrição, habilitação, prestação de contas), classifica nos três grupos (o sistema gera, a OSC já tem, só a captadora fornece), gera as declarações com os dados do perfil e monta o checklist mestre.
5. Responda às perguntas do agente sobre os itens que só você pode fornecer, uma por vez.
6. Mostre o checklist para aprovação:
   ```
   1. Aprovar e salvar
   2. Quero ajustar algo
   ```
7. Confirme o salvamento e informe os caminhos: declarações em `projetos/{edital-slug}/documentos/` e o checklist em `projetos/{edital-slug}/checklist-anexos.md`.
8. Próximo passo: `/projeto-avaliar` (se a proposta e o orçamento já existem) ou a estação que o `estado.md` apontar.

## Regras

- Cada anexo listado cita o item do edital que o exige. Facultativo separado do obrigatório.
- Toda tabela de documento sai com as colunas Enviado e Data em branco.
- Declaração gerada fica "aguardando assinatura" até a captadora confirmar.
- Nenhum dado inventado: o que falta no perfil vira pergunta. Quem assina é o representante legal, não o contato.
- Este comando não grava nada no CaptaHub.
- Português correto, sem travessão.
