# Portal do Cliente. Mensagem 3, pendente de crédito

> **Enviada em 14/09/2026 e concluída**, com custo de 2,1 créditos e o plano aprovado pela captadora no editor. Foi acrescentada ao fim a linha "Não altere regras de linha, permissões nem gatilhos fora do que foi pedido". A conferência está no item 4 dos próximos passos de `docs/portal-clientes-arquitetura.md`. O texto abaixo fica como registro.
>
> Escrita em 13/09/2026, quando a primeira tentativa foi recusada com "workspace is out of credits".
> A captadora pediu **só esta correção**. Custo esperado: cerca de 1 crédito.
> Os créditos diários do plano gratuito renovam à meia-noite UTC, que é 21h de Brasília.

## Por que ela existe

Na conferência de 13/09, o painel da administradora busca apenas editais em andamento. Sem lista de finalizados, a captadora não tem caminho para abrir o edital finalizado, e é na página dele que se marca o resultado (aprovado ou reprovado). O cliente enxerga os finalizados dele; a administradora não.

Enquanto não houver edital finalizado no portal, o defeito não tem efeito prático.

---

## Texto a enviar (copiar daqui)

Uma correção pequena e só ela. Não mude nada além disto.

PROBLEMA
No painel da administradora, a lista busca apenas editais em andamento (buscarEditais(["em_andamento"])). Por isso a administradora não tem caminho para abrir um edital finalizado, e é justamente na página do edital finalizado que ela marca o resultado como aprovado ou reprovado.

CORREÇÃO
1. No painel da administradora, busque também os editais finalizados.
2. Em cada organização, mantenha a lista de editais em andamento como está e acrescente, logo abaixo, uma lista "Finalizados", com o nome do edital como link para a página dele, a data de submissão (ou "submissão não registrada") e o resultado: "Aguardando resultado", "Aprovado em dd/mm/aaaa" ou "Reprovado em dd/mm/aaaa". Os finalizados que ainda aguardam resultado aparecem primeiro.
3. A contagem "N editais em andamento" e a "Próxima entrega" continuam considerando só os editais em andamento. Edital finalizado não entra no cálculo de atraso nem na ordenação das organizações.
4. Editais apagados continuam fora do painel, só na página de Apagados.

Texto em português do Brasil, com acentuação correta e sem travessão.
