# 10 - Achado: a pasta _82 está aberta por link público

| Campo | Valor |
|---|---|
| Data | 2026-08-21 |
| Onde | Pasta `_82 - Rosepaula Aparecida Andrade Rodrigues` no Google Drive |
| Tipo | Achado de segurança e privacidade. **Nenhuma alteração foi feita** |
| Situação | Achado registrado. A correção depende da dona da pasta |
| Identificador da pasta | `1YxXksuP6SHlVKA4bT5gaC0WG4Wy4OXej` |
| Proprietário | `lealprojetos2823@gmail.com` |

---

## 1. Como o achado apareceu

A captadora pediu que a pasta voltasse a aparecer em "Compartilhados comigo" no
Google Drive. Ao consultar a conta para entender por que ela não aparecia, as
permissões da pasta vieram à tona.

## 2. O que foi encontrado

As permissões da pasta são exatamente duas:

| Quem | Permissão |
|---|---|
| **Qualquer pessoa com o link** | **Pode ver** |
| `lealprojetos2823@gmail.com` | Proprietário |

**O e-mail da captadora não consta.** Ela acessa a pasta na condição de "qualquer
pessoa com o link". Foi confirmado por consulta direta que a pasta **não aparece**
na lista de compartilhados dela.

Isso explica dois fatos que vinham incomodando desde 20/08:

- Por que a pasta não aparece em "Compartilhados comigo": ela nunca foi compartilhada com o e-mail dela.
- Por que o caminho no Windows tem 104 caracteres de prefixo, passando por `G:\.shortcut-targets-by-id\`: é assim que o Google Drive materializa uma pasta acessada por link, sem atalho no Meu Drive.

## 3. Por que isso é grave

**Qualquer pessoa que tenha o link abre a pasta inteira e vê tudo.** Sem senha,
sem estar logada, sem convite. Um link repassado num grupo, colado num e-mail ou
indexado em algum lugar dá acesso a todo o acervo.

O que está exposto, entre 4.795 arquivos de 23 organizações:

- `CNH-Germano - representante legal.pdf` e `Comprovante residencia.pdf`, do dirigente do Levanta e Brilha
- CPF, RG, atas, estatutos, dados bancários e certidões das organizações
- Documentos pessoais de membros de coletivos, como em Mededicas

São dados pessoais de terceiros, entregues à assessoria em relação de confiança.
A responsabilidade por eles não deixa de ser da captadora só porque a pasta é da
mentora.

## 4. O que foi verificado, e está correto

Havia a dúvida de se as alterações de 20/08 teriam ficado presas no computador,
já que a permissão visível é de leitura. Foram conferidas direto na nuvem:

| O que | Situação na nuvem |
|---|---|
| Renomeação do `.gdoc` da estruturação 04 | **Sincronizada.** O documento se chama `Lista de presença AGE 26_02_2026 - Centro Missionário` |
| Retirada dos 1.226 `desktop.ini` da estruturação 09 | **Sincronizada.** A pasta `3- DOCUMENTOS INSTITUCIONAIS ANTERIORES` tem agora só os 2 documentos |

Ou seja, a escrita funciona apesar da permissão listada ser de leitura. O Google
Drive costuma mostrar ao não proprietário apenas parte da lista de permissões.

## 5. Dois detalhes de propriedade que apareceram

- O Google Docs da lista de presença pertence a **`germano@levantaebrilha.com.br`**, o representante do próprio cliente, e não à mentora.
- **Vários arquivos dentro da pasta da mentora pertencem à captadora** (`gestao.mobilizando@gmail.com`). A propriedade dentro da pasta é mista.

Isso importa: se o compartilhamento for revogado um dia, os arquivos de que ela é
dona continuam dela, mas os demais não.

## 6. O que precisa ser feito

**Com a dona da pasta, com prioridade:**

1. Trocar "qualquer pessoa com o link pode ver" por compartilhamento nominal, com o e-mail de cada pessoa que precisa de acesso.
2. Incluir `gestao.mobilizando@gmail.com` como Editor.

Isso resolve os dois problemas de uma vez: fecha a exposição e faz a pasta
aparecer em "Compartilhados comigo", que é o que a captadora queria.

**Enquanto isso não acontece:**

3. Criar um atalho da pasta no "Meu Drive" da captadora, pelo navegador. Não copia nada, não muda a propriedade, não consome cota, e permite marcar "Disponível off-line" pelo Explorer.

## 7. O que NÃO foi feito, e por quê

- **Nenhuma permissão foi alterada.** A pasta é da mentora e mexer no compartilhamento dela é decisão dela.
- **O atalho não foi criado por aqui.** As ferramentas disponíveis só permitem **mover** a pasta, o que a tiraria do Drive da mentora. Criar atalho exige o navegador.

## 8. Regras que passam a valer

- **Pasta com documento pessoal de terceiro nunca fica em "qualquer pessoa com o link".** Compartilhamento é sempre nominal, por e-mail.
- Ao começar a trabalhar numa pasta compartilhada, **conferir as permissões dela antes**, e não depois de meses de uso.
- O link de uma pasta assim é credencial. Não se cola em conversa, grupo ou e-mail sem pensar.
- Documento pessoal de dirigente de cliente (CNH, CPF, RG, comprovante de residência) merece pasta com acesso restrito, mesmo dentro de um ambiente já compartilhado.
