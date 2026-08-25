# Estrutura padrão da pasta `_82` (padrão da mentoria)

> Resgatada em 24/08/2026 a partir de três fontes cruzadas: os documentos
> `04 - Controle de Submissões.docx` e `06 - Clientes.docx` da mentoria, o
> levantamento feito em 20/08/2026 e a leitura da pasta viva no Drive.
> **Nome de pasta aqui não muda.** A estrutura é da mentoria, e a captadora é
> apenas Editora da pasta original. Ver `docs/estruturacoes/2026-08-20-02-pasta-82-diagnostico.md`.

---

## 1. A raiz. Onze pastas

```
_82 - Rosepaula Aparecida Andrade Rodrigues\
├── 01 - Núcleo
├── 02 - Plano Captador Visionário
├── 03 - Plano de Ação
├── 04 - Controle de Submissão_          (o underscore final é do padrão)
├── 05 - Financeiro
├── 06 - Clientes
├── 07 - Equipe
├── 08 - Checkpoint
├── 09 - Acervo Digital
├── 10 - Assessoria
└── 11 - Backup Sistema AMC IA
```

---

## 2. `04 - Controle de Submissão_`. A mineração de editais

```
04 - Controle de Submissão_\
└── 01 - Mineração de Editais
    ├── 01 - Planejamento de Submissões        (a planilha de controle)
    ├── 02 - Editais Abertos
    │   ├── 01 - Continuos
    │   ├── 02 - Lei de Incentivo
    │   │   ├── 01 - Cultura
    │   │   ├── 02 - Esporte
    │   │   ├── 03 - Fundos
    │   │   └── 04 - Reciclagem
    │   ├── 03 - Empresa Privada
    │   ├── 04 - Internacionais
    │   ├── 05 - Transferegov
    │   ├── 06 - Editais Públicos
    │   ├── 07 - Fundos Públicos
    │   └── 08 - Fundos Privados
    ├── 03 - Editais Analisar
    ├── 04 - Editais Analisados
    ├── 05 - Histórico Editais _ Enviados
    └── 06 - Histórico de Editais _ Não Submetidos
```

### As duas categorias que se desdobram por esfera

`02 - Lei de Incentivo` (nas quatro áreas) e `07 - Fundos Públicos` repetem, por
baixo, a esfera e depois a natureza jurídica:

```
{área ou Fundos Públicos}\
├── 01 - Federal
├── 02 - Estadual
└── 03 - Municipal
        ├── 01 - Ambos
        ├── 02 - Sem Fins
        ├── 03 - Com Fins
        ├── 04 - MEI
        ├── 05 - Pessoa Física
        └── 06 - Sem informação
                └── NN - {Nome do financiador}
```

As demais categorias de `02 - Editais Abertos` não se desdobram: recebem direto a
pasta `NN - {Nome do financiador}`.

---

## 3. `06 - Clientes`. As três categorias

```
06 - Clientes\
├── 01 - OSC-Organizações da Sociedade Civil
├── 02 - Empresa Privada
└── 03 - Outros Modelos
        ├── X7, X8, X9, X10 - CaptaDrive - Cliente X    (esqueleto vazio, o modelo)
        └── X - CaptaDrive - Clientes Standby           (prospects, não é modelo)
```

Cada cliente é uma pasta `NN - CaptaDrive - {Nome do cliente}`, numerada em
sequência, dentro da categoria correspondente.

---

## 4. O CaptaDrive do cliente. Duas variantes

A variante depende da natureza do proponente, não da vontade de quem organiza.

### Variante A. OSC (associação, fundação, instituto)

```
NN - CaptaDrive - {Cliente}\
├── 01 - Gestão Documental
│   ├── 01 - Declarações
│   ├── 02 - Informações Institucionais
│   ├── 03 - Atas e Constituição
│   ├── 04 - Certidões Negativas
│   ├── 05 - Alvarás e Licenças
│   ├── 06 - Dados Bancários
│   └── 07 - Serviços
├── 02 - Editais
│   └── NN - {Nome do edital}
└── 1 - Controle de Submissão.xlsx
```

### Variante B. Produtora, empresa e pessoa física

```
NN - CaptaDrive - {Cliente}\
├── 01 - Gestão Documental
│   ├── 01 - Documentos
│   └── 02 - Portfolio
├── 02 - Editais
│   └── NN - {Nome do edital}
└── 1 - Controle de Submissão.xlsx
```

Produtora e pessoa física não têm ata de constituição nem certidão negativa de
OSC. Têm documento pessoal e portfólio, e é isso que a variante B reflete.

### `07 - Serviços`. As habilitações

Subpasta livre, uma por órgão ou registro que mantém a organização apta. Não tem
lista fixa: cada cliente tem as suas. Exemplos reais em uso:

| Cliente | O que tem |
|---|---|
| Ponto Cultural | `01 - CMDCA`, `02 - CMAS`, `04 - Diversos`, `05 - Acessos`, `06 - Leis de Incentivo` |
| e-Missão | `01 - CMAS`, `02 - CMDCA`, `03 - OSCIP`, `03 - FazDeNovo CMDCA` |
| Rede Amor e Compaixão | `01 - Parceria e-Missão`, `02 - CEBAS`, `03 - Ministério da Cultura`, `04 - Ministério do Esporte`, `05 - Relatórios Certificações` |

---

## 5. A pasta de edital. Sete subpastas, sempre as mesmas

```
NN - {Nome do edital}\
├── 01 - Edital
├── 02 - Anexos
├── 03 - Manuais
├── 04 - Projeto
├── 05 - Orçamento
├── 06 - Resultados
└── 07 - Documentos Específicos
```

É o nível onde mais aparece divergência, quase sempre por hífen sem espaço
(`07- Documentos Específicos`) ou por nome encurtado (`07 - Documentos`).

---

## 6. Regras de nomeação do padrão

1. **Numeração com dois dígitos e hífen com espaço dos dois lados:** `01 - Nome`.
2. **Nome de pasta não muda.** Nem para corrigir acento, enquanto a cópia for
   espelho da pasta da mentora. Corrigir de um lado só cria divergência.
3. **Nome de arquivo também não muda**, pelo mesmo motivo.
4. **Caminho longo se resolve com unidade virtual (`subst`), nunca renomeando.**
   O padrão consome 179 caracteres só em nome de pasta na cadeia mais profunda.
5. **Um cliente, uma pasta, uma categoria.** Cliente não fica solto na raiz de
   `06 - Clientes` e dentro da categoria ao mesmo tempo.
6. **Pasta de edital é por edital**, com o nome do edital, nunca por ano ou órgão.

---

## 7. Onde a cópia da Área de Trabalho diverge hoje

Medido em 24/08/2026 na pasta `C:\Users\rosep\Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues`.

### 7.1. O que já está certo

- As **11 pastas da raiz** existem, todas.
- `01 - Mineração de Editais` tem as **6 subpastas completas**, incluindo
  `03 - Editais Analisar`, `04 - Editais Analisados` e `08 - Fundos Privados`,
  que **não existem na pasta viva do Drive**.
- **37 das 52 pastas de edital** seguem exatamente as sete subpastas.
- Os 18 clientes estão soltos na raiz de `06 - Clientes`, sem a duplicação por
  categoria que existe no Drive.

### 7.2. Pastas fora do padrão dentro do CaptaDrive

| Cliente | O que está fora |
|---|---|
| e-Missão | `03 - Registros e Comunicacao` |
| Ponto Cultural | `EDITAIS` e `PONTO CULTURAL` |
| Núcleo Arte e Música Esperança | `_RESGATE DRIVE 17-08-2026` |
| Faz de Conta | `01 - Documentos` no nível do CaptaDrive, fora da Gestão Documental |

### 7.3. As 15 pastas de edital que divergem

| Cliente | Pasta de edital | Divergência |
|---|---|---|
| e-Missão | `01 - Edital MROSC` | `07- Documentos Específicos`, hífen sem espaço |
| e-Missão | `03 - Edital Fundo Brasil` | as sete subpastas com hífen sem espaço |
| e-Missão | `00 - Projeto Base Capacitar PPP` | estrutura própria, não é edital |
| e-Missão | `Fundo Brasil - Projeto Egressos` | `PROJETO NOVO` |
| Mededicas | `02 - Criação PNAB 042026` | `07 - Documentos` em vez de `07 - Documentos Específicos` |
| Mededicas | `04 - VideoDança 042026` | idem |
| Núcleo Arte | `01 - Base - Projetos` | `NATÁLIA MACHADO` |
| Quintal Eh | `01 - Edital Fapemig` | `01. Edital` com ponto, e `03 - Projetos` |

### 7.4. Erros de digitação na Gestão Documental

Variantes em uso hoje: `01- Documentos` e `02- Portfolio` (STK, sem espaço),
`02 - Portifolio` (Bandeja), `02 - Portfólio` (Faz de Conta), contra
`02 - Portfolio` das demais. Nas OSC, os nomes das sete subpastas estão corretos.

### 7.5. A divergência que não é de estrutura

A cópia da Área de Trabalho tem **176 arquivos** em `04 - Controle de Submissão_`
contra **171** na pasta viva do Drive, e **22 pastas** em `06 - Clientes` contra
**27**. A numeração dos clientes também difere: aqui o Núcleo Arte é o `08`, no
Drive é o `10`. Ou seja, **as duas pastas não são espelho uma da outra desde 07/08**.
Estruturar a cópia local sem decidir isso antes é organizar a pasta errada.
