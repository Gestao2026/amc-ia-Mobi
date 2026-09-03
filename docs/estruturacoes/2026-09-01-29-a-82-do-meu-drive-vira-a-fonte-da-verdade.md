# 29 - A _82 do Meu Drive vira a fonte da verdade

| Campo | Valor |
|---|---|
| Data | 2026-09-01 |
| Pasta afetada | `G:\Meu Drive\_82 - Rosepaula Aparecida Andrade Rodrigues` (nova fonte da verdade), as duas cópias da Área de Trabalho (deixaram de existir), `scripts/backup-diario.bat` |
| Tipo | Mudança de fonte da verdade, com ajuste de backup |
| Situação | Concluída. **2 pendências**, no item 9 |
| Autorizada por | A captadora, que fez a migração das pastas à mão e comunicou a mudança, confirmando a nova fonte da verdade e autorizando incluí-la no backup |
| Reversível | A migração das pastas foi manual e não tem desfazer automático. A alteração do script é reversível pelo histórico do Git |

---

## 1. Por que foi feito

Até 01/09/2026 a estrutura documental vivia em três cópias, com uma inversão incômoda de titularidade: a fonte da verdade era a `_82` no Google Drive da mentora, onde a captadora é apenas **Editora, não dona**. As cópias de trabalho ficavam na Área de Trabalho, no disco `C:`, e divergiam entre si.

A comparação byte a byte de 01/09 (registro 28) mediu o tamanho do problema: das duas cópias da Área de Trabalho, **37 conteúdos existiam só na antiga e 95 só na nova**. Nenhuma das duas podia ser descartada sem perda, e nenhuma das duas era a referência.

A captadora resolveu a raiz: passou a trabalhar numa cópia **no Drive dela**, onde é dona.

## 2. O que foi decidido, e por quem

- **A fonte da verdade passa a ser `G:\Meu Drive\_82 - Rosepaula Aparecida Andrade Rodrigues`.** Decisão da captadora, comunicada em 01/09/2026.
- **A `_82` sai da Área de Trabalho.** As duas cópias que viviam lá deixaram de existir. A Área de Trabalho deixa de guardar estrutura documental.
- **A nova fonte da verdade entra no script de backup**, no sentido nuvem para disco, igual ao que já era feito com a pasta da mentora. O script não roda sozinho: desde a regra NADA RODA SOZINHO, de 01/09/2026, ele só executa quando a captadora manda.
- **O bloco da pasta da mentora continua no script**, porque ela permanece acessível e a captadora segue sem ser dona dela. Proteger contra revogação de acesso continua valendo.
- **Nada foi apagado dos backups.** A cópia congelada da antiga `_82` da Área de Trabalho fica onde está, como registro histórico.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Cópias vivas da `_82` | 3 (mentora no Drive, duas na Área de Trabalho) |
| `_82` antiga na Área de Trabalho | 2.856 arquivos, 5,7 GB |
| `_82 - do Drive 2026-09-01` na Área de Trabalho | 2.634 arquivos, 5,3 GB |
| Conteúdo exclusivo de uma das duas | 37 na antiga, 95 na nova |
| Cobertura de backup da pasta de trabalho | **nenhuma**, desde o desligamento de 28/08 (registro 21) |

## 4. O que foi executado

1. **A captadora migrou as pastas à mão** para `G:\Meu Drive`, fora deste sistema. Nenhum script participou.
2. **Conferência por amostragem dos exclusivos**, feita aqui, somente leitura: o `.rar` de 69 MB do histórico de editais, os anexos preenchidos do ARREDA, o clipping da Bárbara Almeida e o CNPJ da STK foram localizados na nova pasta. Também apareceu uma pasta `RECUPERADO - Mededicas - PNAB Ciclo 2`, sinal de migração conferida e não de descarte.
3. **Novo bloco 2b no `scripts/backup-diario.bat`**, copiando `G:\Meu Drive\_82 ...` para `C:\Users\rosep\Backups\meu-drive-82\atual`, com as mesmas exclusões do bloco da mentora (`desktop.ini`, `.gdoc`, `.gsheet`, `.gslides`) e com guarda `if exist`, para pular sem erro se o Drive não estiver montado.
4. **Comentários atualizados** nos blocos 4 e 5 do script, que ainda descreviam a `_82` da Área de Trabalho como pasta viva.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Cópias vivas da `_82` | 3 | 2 (a da captadora e a da mentora) |
| Fonte da verdade | Drive da mentora | **Meu Drive da captadora** |
| Titularidade da fonte da verdade | Editora | **Dona** |
| Arquivos na fonte da verdade | não se aplica | 2.228 (fora `desktop.ini`), 5,3 GB, 969 pastas |
| Blocos de backup no script | 5 | 6 |
| Cobertura de backup da pasta de trabalho | nenhuma | prevista no script, para o disco local |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `docs/estruturacoes/2026-09-01-28-comparacao-byte-a-byte-das-duas-pastas-82.md` | A comparação que motivou a mudança |
| `docs/estruturacoes/_detalhado/2026-09-01-28-*.md` | Os quatro relatórios de apoio, arquivo por arquivo |
| `scripts/backup-diario.bat` | O bloco 2b e os comentários atualizados |
| `C:\Users\rosep\Backups\_historico-backup.log` | Cada execução do backup, com data e resultado |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| `_82` da mentora no Drive | `Backups\pasta-82\atual` | Sim. 3.330 arquivos, 5,8 GB |
| `_82` antiga da Área de Trabalho | `Backups\desktop-82\atual` | Congelado em 28/08, 2.776 arquivos. Não acompanhou os últimos dias |

## 8. Como reverter

A migração das pastas foi manual e **não tem desfazer automático**. O caminho de volta, se um dia for preciso, é copiar de `C:\Users\rosep\Backups\desktop-82\atual` para onde a captadora quiser, lembrando que essa cópia parou em 28/08 e não tem o que foi produzido entre 28/08 e 01/09.

A alteração do script se desfaz removendo o bloco 2b e restaurando os comentários, tudo disponível no histórico do Git.

## 9. O que ficou pendente

1. **A contagem não fecha, e vale conferir.** A nova fonte da verdade tem 2.228 arquivos, contra 2.856 da cópia antiga e 2.634 da cópia nova, medidas em 01/09. Parte da diferença é esperada, porque a captadora está eliminando as pastas irmãs duplicadas (26 casos, relatório do registro 28). Mas a diferença não foi comprovada arquivo a arquivo. **Recomendação:** rodar a comparação por hash entre `Backups\desktop-82\atual` e a nova pasta, para separar o que foi limpeza do que ficou para trás. Depende da captadora avisar que terminou de organizar.
2. **O bloco existe, mas ainda não rodou.** Desde a regra NADA RODA SOZINHO, de 01/09/2026, a tarefa agendada está desabilitada e o script só executa quando a captadora pede. Enquanto ela não mandar rodar, a nova fonte da verdade continua **sem nenhuma cópia no disco**. A primeira execução baixa os 5,3 GB de uma vez, porque a pasta fica em streaming; as seguintes copiam só o que mudou.

## 10. Regras que passam a valer

- **A fonte da verdade da estrutura documental é `G:\Meu Drive\_82 - Rosepaula Aparecida Andrade Rodrigues`.** Substitui a regra anterior, que apontava para o Drive da mentora.
- **A Área de Trabalho não guarda mais estrutura documental.** Nada de `_82` ali.
- **A pasta da mentora continua protegida e continua no backup**, mas deixa de ser a referência. A captadora segue sendo apenas Editora dela.
- **Pasta que vive na nuvem precisa de cópia no disco.** Google Drive é sincronização, não backup: exclusão e corrupção sincronizam junto. A regra antiga dizia que origem no disco tem segunda camada na nuvem. Agora vale também o inverso.
- **A regra de não apagar continua inteira.** Nenhuma pasta chamada `_82 - Rosepaula Aparecida Andrade Rodrigues` se apaga, em nenhuma cópia, em nenhum nível. Pasta vazia continua sendo estrutura, não sobra.
