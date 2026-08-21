# 11 - Consolidação das credenciais dos clientes

| Campo | Valor |
|---|---|
| Data | 2026-08-20 e 21/08/2026 |
| Onde | `Área de Trabalho\Credenciais AMC IA`, `Área de Trabalho\SENHAS CLIENTES` e `C:\amc-ia-Mobi\_credenciais-nao-sincronizar` |
| Tipo | Consolidação e decisão de segurança |
| Situação | Concluída |
| Autorizada por | Rosepaula, com as três opções de destino na mesa |
| Reversível | Parcialmente. O que foi retirado está na Lixeira do Windows |

> **Nota:** este registro foi escrito em 21/08/2026 às 18h, depois do fato, para
> fechar a lacuna de rastreabilidade. A execução foi feita em outra sessão. Os
> números aqui vêm da conferência do estado final e do `LEIA-ME.md` da pasta.

---

## 1. Por que foi feito

As senhas e acessos dos clientes estavam em **três lugares ao mesmo tempo**, sem
que nenhum fosse o oficial:

- `Área de Trabalho\SENHAS CLIENTES`
- `Área de Trabalho\Credenciais AMC IA`
- `C:\amc-ia-Mobi\_credenciais-nao-sincronizar`

A terceira guardava o certificado digital e-CNPJ da MUPA em `.pfx`, **com a senha
escrita no nome do arquivo**. E uma cópia desse certificado chegou a parar no
Google Drive, em 20/08/2026.

O risco é direto: quem tiver o `.pfx` e a senha assina em nome da organização.

## 2. O que foi executado

1. As três fontes foram consolidadas numa pasta única: **`Área de Trabalho\Credenciais AMC IA`**, hoje com 14 arquivos e 0,8 MB, organizada por cliente.
2. Foi criada a planilha mestre **`_ACESSOS AMC IA.xlsx`**, com quatro abas: os 49 acessos, 10 conflitos e pendências, os alertas de segurança e as 12 organizações da carteira ainda sem login anotado.
3. **92 credenciais** foram comparadas contra a planilha, e os arquivos conferidos **por hash MD5**. Os dois `.pfx` da pasta do projeto eram byte a byte idênticos ao que ficou em `mupa/`.
4. As três cópias redundantes foram para a Lixeira, depois da conferência.
5. Um `LEIA-ME.md` foi deixado na pasta, explicando onde está cada coisa e a regra de manutenção.

## 3. A decisão de segurança

A pasta entrou no backup diário das 12h30, **mas só para o disco local**. Ela
**nunca sobe para o Google Drive**.

| | Vai para o disco | Vai para a nuvem |
|---|---|---|
| Projeto AMC IA | sim | sim |
| Pasta `_82` | sim | não se aplica, a origem já é nuvem |
| **Credenciais** | **sim** | **não, de propósito** |

O `scripts/backup-diario.bat` traz um aviso explícito no bloco 3, alertando que
mover aquele robocopy para o bloco da nuvem exporia as senhas de todos os
clientes e o certificado e-CNPJ da MUPA.

**A consequência precisa ficar clara:** esse backup protege contra apagar sem
querer, **não contra o disco C: morrer**. A cópia mora no mesmo disco do
original. Se a proteção contra falha de disco virar prioridade, a saída não é
subir a pasta como está, é um cofre de senhas ou um arquivo criptografado.

## 4. Verificação feita em 21/08 às 18h

| O que | Situação |
|---|---|
| `C:\amc-ia-Mobi\_credenciais-nao-sincronizar` | **Não existe mais** |
| `Área de Trabalho\SENHAS CLIENTES` | **Não existe mais** |
| `Área de Trabalho\Credenciais AMC IA` | 14 arquivos, organizada por cliente |
| `C:\Users\rosep\Backups\credenciais` | 15 arquivos, backup rodando |
| Certificado `.pfx` ou `.p12` no Google Drive | **Nenhum.** A cópia exposta foi removida |

## 5. Como reverter

O que foi retirado está na **Lixeira do Windows**, enquanto ela não for esvaziada.
Não há script de reversão, porque a operação foi consolidação e não movimentação
em massa.

## 6. O que ficou pendente

- **10 conflitos** registrados na aba "Conflitos e pendencias" da planilha: a mesma conta com senha ou login diferente em arquivos distintos.
- **12 organizações** da carteira sem nenhum login anotado.
- **Senhas em texto aberto.** A planilha e os `.docx` não são cofre. A aba "Alertas de seguranca" lista senhas repetidas entre clientes e senha fraca.
- **A senha do certificado da MUPA** continua num `.docx` na mesma pasta do `.pfx`. Separar os dois seria mais seguro.

## 7. Regras que passam a valer

- **Senha e certificado nunca sobem para a nuvem.** Nem em backup, nem em pasta sincronizada.
- **Senha nunca no nome do arquivo.** Foi assim que o `.pfx` da MUPA circulou.
- A planilha `_ACESSOS AMC IA.xlsx` é a fonte da verdade. Os `.docx` das subpastas são só comprovante da origem.
- Existe **uma** pasta de credenciais na máquina. Ao encontrar uma segunda, consolidar na hora.
- Antes de apagar qualquer cópia de credencial, conferir por hash que o conteúdo já existe no lugar oficial.
