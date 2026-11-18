---
description: Cadastrar uma nova OSC (organização) e defini-la como ativa. Porta de entrada do sistema.
---

# /osc-nova

Cadastra uma organização da sociedade civil no sistema e a define como ativa. É a porta de entrada: sem OSC cadastrada não há contexto para minerar editais ou elaborar projetos.

## Passo 0. Contexto

Leia `minhas-oscs/.ativa`. Se já houver OSCs cadastradas, mencione que esta será mais uma na carteira.

Antes de cadastrar do zero, verifique a conexão com o CaptaHub (`CAPTAHUB_API_TOKEN` no `.env`). Se estiver conectado, a OSC pode já existir na carteira: ofereça `/osc-importar` para trazer os dados prontos do CaptaHub, e só siga com o cadastro manual se o captador preferir ou se a OSC não estiver lá.

## Passo 1. Entrevista (UMA pergunta por vez)

Conduza o cadastro com base no modelo `minhas-oscs/MODELO-perfil-osc.md`. Pergunte na ordem, uma por vez, numerando quando houver opção:

1. Nome da organização.
2. CNPJ.
3. Natureza jurídica (1. Associação, 2. Fundação, 3. OSCIP, 4. Organização religiosa, 5. Cooperativa social, 6. Outra).
4. Data de fundação (para calcular o tempo de existência).
5. Município e UF da sede, e territórios onde atua.
6. Área(s) temática(s) de atuação.
7. Missão e principais programas.
8. Experiência com editais e projetos já aprovados (valor, financiador, ano).
9. Situação documental: passe o checklist do modelo e pergunte o que a OSC já tem em dia.

Use qualquer dado que o usuário já tenha dado antes, sem repetir a pergunta.

## Passo 2. Confirmação

Resuma os dados coletados e o slug que será gerado (kebab-case do nome, ex: `instituto-semente`). Peça OK.

## Passo 3. Geração e salvamento

Após o OK:
1. Crie a pasta `minhas-oscs/{slug}/` e a subpasta `projetos/`.
2. Salve `minhas-oscs/{slug}/perfil-osc.md` preenchido segundo o modelo.
3. Grave o slug em `minhas-oscs/.ativa`.
4. Informe o caminho absoluto do `perfil-osc.md`.

## Passo 3.1. Subir para o CaptaHub (classe B, oferece e espera o OK)

A finalidade deste comando é cadastrar a OSC **localmente** e torná-la ativa. Criar o cliente na carteira é um segundo efeito, e escrita em sistema externo não se desfaz daqui. Por isso a criação **não sai sozinha** (ver a classificação de chamadas no CLAUDE.md).

Se o CaptaHub estiver conectado:

1. **Cheque que ela ainda não existe na carteira** (`python3 scripts/captahub-api.py clientes`, compare por nome). **Esta leitura é classe A e roda sem perguntar**, porque é ela que impede duplicar o que a captadora mandou criar.
2. **Ofereça em uma linha, dizendo o que a checagem encontrou**, e espere o OK. Se não existir lá: "A OSC ainda não está na carteira do CaptaHub. Quer que eu crie agora?" Se já existir: diga isso, não crie nada, e ofereça apenas gravar o id no perfil.
3. **Com o OK**, crie o cliente: `python3 scripts/captahub-api.py cliente-criar --nome "{nome}" --uf {uf} --municipio "{municipio}" --areas-tematicas "{areas}" ...` com os campos coletados (`status_documental` como JSON completo, se houver).
4. Grave o `id` retornado no `perfil-osc.md` na linha `ID CaptaHub: {id}`.
5. Confirme em uma linha: "Sincronizado com o CaptaHub: OSC criada na carteira." Se a API falhar, avise que a sincronização ficou pendente e siga.

**Sem o OK, não grave nada e siga normalmente.** O perfil local fica sinalizado como "fora do CaptaHub" até ela decidir subir, e `/captahub-sincronizar` resolve isso depois, a qualquer momento.

## Passo 4. Próximo passo

Sugira `/edital-minerar` para encontrar editais alinhados, ou `/edital-analisar` se o captador já tem um edital em mãos.

## Regras

- Anuncie o próximo passo antes da geração se demorar.
- Português correto, sem travessão.
- Não mostre código. Informe apenas o caminho do arquivo salvo.
