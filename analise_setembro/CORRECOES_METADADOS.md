# Correções dos metadados — aba "Metadata - Bacteria"

Comparação entre a planilha `Database_Plastic-Soil.xlsx` e os metadados depositados pelos autores no **NCBI BioSample / ENA** (baixados em 29/09/2026, cópia em `dados_ncbi/`) e nos artigos originais.

* `correcoes_planilha.tsv`: uma linha por célula a alterar (SAMPLE, coluna, valor atual → correto, fonte). Dá para filtrar no Google Sheets.
* `planilha_bacteria_corrigida.tsv`: a aba inteira já corrigida, com as colunas novas sugeridas no final.
* `gerar_correcoes.py`: regenera tudo.

## 1. Tipo de dado

* **Todas as 553 amostras do `conjunto_alex` são 16S rRNA (bactérias).** São 314 em V4 (515F/806R) e 239 em V3‑V4. Na tabela final, 100 % dos ASVs estão classificados como *Bacteria*: arqueias, cloroplasto e mitocôndria foram removidos no pipeline. Não há fungos no conjunto.
* A **aba "Metadata - Bacteria" tem 84 runs de fungos (ITS)** que não deveriam estar lá:
  * **PRJNA630025**: 36 runs `*_fung` (ITS).
  * **PRJNA1155845**: 48 runs `SRR30519516–SRR30519563` (ITS). Os de 16S são `SRR30517334–SRR30517381`.
* ⚠️ **As abas e as configs do projeto‑09 estão trocadas.** As sequências de `SRR30517*` são 16S V4 típicas (251 pb, começam com TACG, 100 % classificadas no SILVA). As de `SRR30519*` são ITS (cerca de 217 pb, 47 % "Unassigned" no SILVA). Mas:
  * `auto-bash/configs/projeto-09-bacteria.conf` usa **SRR30519** (ITS) como bactéria → **`results/projeto-09-bacteria` é, na verdade, ITS processado com SILVA** e precisa ser refeito.
  * `projeto-09-fungo.conf` usa **SRR30517** (16S) como fungo.
  * A aba **"Metadata - Fungi"** lista SRR30517 (16S) para PRJNA1155845. O certo seria SRR30519.
  * O `conjunto_alex` usa o conjunto certo (SRR30517).
* A aba "Metadata - Fungi" também lista, para **PRJNA1054347** (36) e **PRJNA702448** (31), os **mesmos runs da aba Bacteria**. Esses BioProjects só têm esses runs no NCBI, e eles são 16S, então os dados de ITS desses estudos precisam ser procurados em outro BioProject.

## 2. Resumo por projeto

| Projeto | Gravidade | Problema | Amostras afetadas | Fonte |
|---|---|---|---|---|
| PRJNA564156 | 🔴 alta | Polímero trocado em relação ao tratamento registrado no NCBI. A mesma parcela aparece com polímeros diferentes entre coletas (32 de 42 parcelas). Clima Knoxville/Mount Vernon invertido em 50 amostras. "Weedguard" (mulch de **papel**) não é plástico. | 131 | NCBI BioSample (título, parcela, local) |
| PRJNA1155845 | 🔴 alta | **24 amostras são intestino de *Enchytraeus crypticus*, não solo** (as sem prefixo `S_`). Tratamento glifosato sem coluna própria. 48 runs de ITS na aba de bactérias. | 24 | NCBI + artigo (J. Hazard. Mater. 2025) |
| PRJNA631499 | 🔴 alta | **46 amostras de 2016‑07 são culturas de enriquecimento em laboratório** (3 e 6 semanas), não plastisfera de campo. Clima invertido. | 56 | NCBI isolation_source |
| PRJEB59875 | 🔴 alta | Polímero e planta desalinhados em relação ao nome da amostra. Todas são **rizosfera** (não plastisfera). | 17 | Nome no ENA + artigo (Menicagli et al. 2023) |
| PRJNA702448 | 🟠 média | `S_PS*`/`S_PSN*` são solo **com PBSA** (estavam como controle). `SOIL_FRACTION` vazio. Adubação N aparece em todas as amostras. Controles têm propriedades de PBSA. | 31 | NCBI env_local_scale |
| PRJNA630025 | 🟠 média | 36 runs de ITS na aba de bactérias. A correspondência entre nome (P/S/VPI) e polímero/fração **não pode ser verificada no NCBI** (só 2 BioSamples, um por local). A análise não encontrou diferença plastisfera × bulk, o que é suspeito. | 24 | ENA library_name; artigo Rüthi et al. 2020 |
| PRJNA1054347 | 🟡 baixa | BM5 e BM6: nome = bulk, mas o NCBI diz rizosfera. M4 com profundidade 0 (demais 0‑20). | 12 | NCBI env_medium |
| PRJNA1021161 | 🟢 ok | Anotação correta. Dose, fotoenvelhecimento e tempo estão só no nome; foram sugeridas colunas. | 0 | NCBI isolation_source |
| PRJNA932786 | 🟢 ok | Correto (só réplicas "b" = solo). O artigo e a aba de projetos dizem **LDPE**; a planilha diz PE. Sugestão: usar LDPE. | 4 | NCBI env_medium |

Linhas da aba que **não estão no `conjunto_alex`**: PRJNA853344 (2 runs, SRR19868794/95) e PRJNA631499 `BDM07160016PL`, `BDM07160014PL`. Verificar se falharam no QC.

## 3. Colunas novas sugeridas

| Coluna | Para quê | Projetos |
|---|---|---|
| `TRATAMENTO_ORIGINAL` | nome do tratamento como o autor depositou (ex.: BioAgri, Weedguard, "0.5% photoaged PE") | todos |
| `TIPO_AMOSTRA` | solo / plastisfera / rizosfera / intestino / cultura de enriquecimento | todos |
| `GLIFOSATO` | Sim/Não | PRJNA1155845 |
| `ADUBACAO_N` | Sim/Não | PRJNA702448 |
| `DOSE_MP(%)`, `FOTOENVELHECIMENTO`, `TEMPO_INCUBACAO` | desenho fatorial | PRJNA1021161, PRJNA631499 |
| `LOCAL`, `DATA_COLETA` | local e data da coleta | PRJNA564156, PRJNA631499, PRJNA630025 |
| `ACAO` | remover / verificar | onde aplicável |

**Vocabulário a padronizar na planilha inteira:** `BIODEGRADABLE` escrito também como `BIODEGRADABLE` (maiúsculas); densidade do PE digitada como `0,94-0,167`; `starch/Polyester blend` e `Polyester blend` sem nenhuma propriedade; decimais misturando vírgula e ponto (`1,24` e `1.24`); controles ora `NONE`, ora vazio; a coluna se chama `PLASTIC_GROUPPING` (PP duplicado).

Valores novos em colunas existentes: `SOIL_FRACTION` = `Gut` e `Enrichment_culture`; `POLYMER_TYPE` = `Cellulose paper` (Weedguard) e `NONE` para todos os controles (hoje há `NONE` e vazio misturados).

## 4. Tabelas por projeto (valores corretos)

Em negrito: células que mudam. O valor atual da planilha aparece entre colchetes.

### PRJNA564156  (168 linhas na aba)

| SAMPLE | SAMPLE_NAME | TRATAMENTO_ORIGINAL | POLYMER_TYPE | BIODEGRADABLE | PLASTIC_GROUPPING | CLIMATE | LOCAL | DATA_COLETA |
|---|---|---|---|---|---|---|---|---|
| SRR10076545 | BDM05150001BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076544 | BDM05150002BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076465 | BDM05150003BF | PLA/PHA | **PLA/PHA** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076454 | BDM05150004BF | Naturecycle | **starch/Polyester blend** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076443 | BDM05150005BF | No Mulch | **NONE** [PLA/PHA] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_polyester] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076432 | BDM05150006BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076421 | BDM05150007BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076410 | BDM05150008BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076399 | BDM05150009BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076388 | BDM05150010BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076543 | BDM05150011BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076532 | BDM05150012BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076521 | BDM05150013BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076510 | BDM05150014BF | Polyethylene | **PE** [_(vazio)_] | **NO_BIODEGRADABLE** [_(vazio)_] | **Thermoplastic** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076499 | BDM05150015BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076488 | BDM05150016BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076477 | BDM05150017BF | Polyethylene | **PE** [PBAT] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_copolyester] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076468 | BDM05150018BF | BioAgri | **starch/PBAT** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_copolyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076467 | BDM05150019BF | PLA/PHA | **PLA/PHA** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076466 | BDM05150020BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076464 | BDM05150021BF | Organix | **PLA/PBAT** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-05 |
| SRR10076463 | BDM05150029BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076462 | BDM05150030BF | BioAgri | **starch/PBAT** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_copolyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076461 | BDM05150031BF | PLA/PHA | **PLA/PHA** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076460 | BDM05150032BF | Naturecycle | **starch/Polyester blend** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076459 | BDM05150033BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076458 | BDM05150034BF | Organix | **PLA/PBAT** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076457 | BDM05150035BF | Polyethylene | **PE** [_(vazio)_] | **NO_BIODEGRADABLE** [_(vazio)_] | **Thermoplastic** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076456 | BDM05150036BF | PLA/PHA | **PLA/PHA** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076455 | BDM05150037BF | No Mulch | **NONE** [PBAT] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076453 | BDM05150038BF | Weedguard | **Cellulose paper** [PBAT] | Biodegradable | **Non-plastic (paper)** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076452 | BDM05150039BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076451 | BDM05150040BF | Organix | **PLA/PBAT** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076450 | BDM05150041BF | Naturecycle | **starch/Polyester blend** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076449 | BDM05150042BF | Polyethylene | **PE** [PBAT] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076448 | BDM05150043BF | Naturecycle | **starch/Polyester blend** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076447 | BDM05150044BF | Weedguard | **Cellulose paper** [PLA/PHA] | Biodegradable | **Non-plastic (paper)** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076446 | BDM05150045BF | Polyethylene | **PE** [PLA/PHA] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076445 | BDM05150046BF | BioAgri | **starch/PBAT** [PLA/PHA] | Biodegradable | **Biodegradable_copolyester** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076444 | BDM05150047BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076442 | BDM05150048BF | No Mulch | **NONE** [PLA/PHA] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076441 | BDM05150049BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2015-05 |
| SRR10076537 | BDM05160001BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076536 | BDM05160002BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076535 | BDM05160003BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076534 | BDM05160004BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076533 | BDM05160005BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076531 | BDM05160006BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076530 | BDM05160007BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076529 | BDM05160008BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076528 | BDM05160009BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076527 | BDM05160010BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076526 | BDM05160011BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076525 | BDM05160012BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076524 | BDM05160013BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076523 | BDM05160014BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076522 | BDM05160015BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076520 | BDM05160016BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076519 | BDM05160017BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076518 | BDM05160018BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076517 | BDM05160019BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076516 | BDM05160020BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076515 | BDM05160021BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2016-05 |
| SRR10076394 | BDM05160029BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076393 | BDM05160030BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076392 | BDM05160031BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076391 | BDM05160032BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076390 | BDM05160033BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076389 | BDM05160034BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076387 | BDM05160035BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076386 | BDM05160036BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076385 | BDM05160037BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076384 | BDM05160038BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076383 | BDM05160039BF | BioAgri | starch/PBAT | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076382 | BDM05160040BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076381 | BDM05160041BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076380 | BDM05160042BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076379 | BDM05160043BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076378 | BDM05160044BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076542 | BDM05160045BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076541 | BDM05160046BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076540 | BDM05160047BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076539 | BDM05160048BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076538 | BDM05160049BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2016-05 |
| SRR10076440 | BDM09150001BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076439 | BDM09150002BF | BioAgri | starch/PBAT | Biodegradable | Biodegradable_copolyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076438 | BDM09150003BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076437 | BDM09150004BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076436 | BDM09150005BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076435 | BDM09150006BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076434 | BDM09150007BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076433 | BDM09150008BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Humid subtropical** [Mediterranean] | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076431 | BDM09150009BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076430 | BDM09150010BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076429 | BDM09150011BF | BioAgri | starch/PBAT | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076428 | BDM09150012BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076427 | BDM09150013BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076426 | BDM09150014BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076425 | BDM09150015BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076424 | BDM09150016BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076423 | BDM09150017BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076422 | BDM09150018BF | BioAgri | starch/PBAT | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076420 | BDM09150019BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076419 | BDM09150020BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076418 | BDM09150021BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2015-09 |
| SRR10076417 | BDM09150029BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076416 | BDM09150030BF | BioAgri | starch/PBAT | Biodegradable | Biodegradable_copolyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076415 | BDM09150031BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076414 | BDM09150032BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076413 | BDM09150033BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076412 | BDM09150034BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076411 | BDM09150035BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076409 | BDM09150036BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076408 | BDM09150037BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076407 | BDM09150038BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076406 | BDM09150039BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076405 | BDM09150040BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076404 | BDM09150041BF | Naturecycle | starch/Polyester blend | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076403 | BDM09150042BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076402 | BDM09150043BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076401 | BDM09150044BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076400 | BDM09150045BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076398 | BDM09150046BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076397 | BDM09150047BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076396 | BDM09150048BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076395 | BDM09150049BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2015-09 |
| SRR10076514 | BDM09160001BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076513 | BDM09160002BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076512 | BDM09160003BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076511 | BDM09160004BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076509 | BDM09160005BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076508 | BDM09160006BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076507 | BDM09160007BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076506 | BDM09160008BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076505 | BDM09160009BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076504 | BDM09160010BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076503 | BDM09160011BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076502 | BDM09160012BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076501 | BDM09160013BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076500 | BDM09160014BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076498 | BDM09160015BF | Naturecycle | **starch/Polyester blend** [Polyester blend] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076497 | BDM09160016BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076496 | BDM09160017BF | Polyethylene | PE | NO_BIODEGRADABLE | Thermoplastic | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076495 | BDM09160018BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076494 | BDM09160019BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076493 | BDM09160020BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076492 | BDM09160021BF | Organix | PLA/PBAT | Biodegradable | Biodegradable_polyester | Humid subtropical | USA: Knoxville in Tennessee | 2016-09 |
| SRR10076491 | BDM09160029BF | Weedguard | **Cellulose paper** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Non-plastic (paper)** [_(vazio)_] | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076490 | BDM09160030BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076489 | BDM09160031BF | PLA/PHA | PLA/PHA | Biodegradable | Biodegradable_polyester | **Mediterranean** [Humid subtropical] | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076487 | BDM09160032BF | Naturecycle | **starch/Polyester blend** [PLA] | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076486 | BDM09160033BF | No Mulch | **NONE** [PLA] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076485 | BDM09160034BF | Organix | **PLA/PBAT** [PLA] | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076484 | BDM09160035BF | Polyethylene | **PE** [PLA] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076483 | BDM09160036BF | PLA/PHA | **PLA/PHA** [PLA] | Biodegradable | Biodegradable_polyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076482 | BDM09160037BF | No Mulch | **NONE** [PLA] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076481 | BDM09160038BF | Weedguard | **Cellulose paper** [PLA] | Biodegradable | **Non-plastic (paper)** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076480 | BDM09160039BF | BioAgri | **starch/PBAT** [PLA] | Biodegradable | **Biodegradable_copolyester** [Biodegradable_polyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076479 | BDM09160040BF | Organix | **PLA/PBAT** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076478 | BDM09160041BF | Naturecycle | **starch/Polyester blend** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076476 | BDM09160042BF | Polyethylene | **PE** [PBAT] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076475 | BDM09160043BF | Naturecycle | **starch/Polyester blend** [PBAT] | Biodegradable | **Biodegradable_polyester** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076474 | BDM09160044BF | Weedguard | **Cellulose paper** [PBAT] | Biodegradable | **Non-plastic (paper)** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076473 | BDM09160045BF | Polyethylene | **PE** [PBAT] | **NO_BIODEGRADABLE** [Biodegradable] | **Thermoplastic** [Biodegradable_copolyester] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076472 | BDM09160046BF | BioAgri | **starch/PBAT** [PBAT] | Biodegradable | Biodegradable_copolyester | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076471 | BDM09160047BF | PLA/PHA | **PLA/PHA** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076470 | BDM09160048BF | No Mulch | NONE | _(vazio)_ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |
| SRR10076469 | BDM09160049BF | Organix | **PLA/PBAT** [_(vazio)_] | **Biodegradable** [_(vazio)_] | **Biodegradable_polyester** [_(vazio)_] | Mediterranean | USA: Mount Vernon in Washington State | 2016-09 |

### PRJNA631499  (88 linhas na aba)

| SAMPLE | SAMPLE_NAME | TRATAMENTO_ORIGINAL | POLYMER_TYPE | SOIL_FRACTION | EXPERIMENT_TYPE | TEMPO_INCUBACAO | CLIMATE | LOCAL |
|---|---|---|---|---|---|---|---|---|
| SRR11748993 | BDM07160001PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11748992 | BDM07160002PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749132 | BDM07160003PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749131 | BDM07160004PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749130 | BDM07160005PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749129 | BDM07160006PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749128 | BDM07160007PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749127 | BDM07160008PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749126 | BDM07160009PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749125 | BDM07160010PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749124 | BDM07160011PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749123 | BDM07160012PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749121 | BDM07160013PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749120 | BDM07160014PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749119 | BDM07160015PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749118 | BDM07160016PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749117 | BDM07160017PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749116 | BDM07160018PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749115 | BDM07160019PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749114 | BDM07160020PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749113 | BDM07160021PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749112 | BDM07160022PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749110 | BDM07160023PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749109 | BDM07160024PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 3 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749108 | BDM07160025PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749107 | BDM07160026PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749106 | BDM07160027PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749105 | BDM07160028PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749104 | BDM07160029PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749103 | BDM07160030PL | BioAgri | starch/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749102 | BDM07160031PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749101 | BDM07160032PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749099 | BDM07160033PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749098 | BDM07160034PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749097 | BDM07160035PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749096 | BDM07160036PL | PLA/PHA | PLA/PHA | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749095 | BDM07160037PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749094 | BDM07160038PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749093 | BDM07160039PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749092 | BDM07160040PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749091 | BDM07160041PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749090 | BDM07160042PL | Organix | PLA/PBAT | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749088 | BDM07160043PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749087 | BDM07160044PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749086 | BDM07160045PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749085 | BDM07160046PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749084 | BDM07160047PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749083 | BDM07160048PL | Naturecycle | starch/Polyester blend | **Enrichment_culture** [Plastosphere] | Ex_situ | 6 week | **Humid subtropical** [_(vazio)_] | USA: Knoxville in Tennessee |
| SRR11749077 | BDM09160002PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749024 | BDM09160003PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749013 | BDM09160004PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749002 | BDM09160005PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11748991 | BDM09160006PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749122 | BDM09160007PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749100 | BDM09160009PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749089 | BDM09160010PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749076 | BDM09160011PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749065 | BDM09160012PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749054 | BDM09160013PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749032 | BDM09160015PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749029 | BDM09160016PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749028 | BDM09160017PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749027 | BDM09160018PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749026 | BDM09160019PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749025 | BDM09160020PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749023 | BDM09160021PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749022 | BDM09160022PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749020 | BDM09160024PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Humid subtropical | USA: Knoxville in Tennessee |
| SRR11749018 | BDM09160026PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749017 | BDM09160027PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749016 | BDM09160028PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749015 | BDM09160029PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749014 | BDM09160030PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749012 | BDM09160031PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749010 | BDM09160033PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749009 | BDM09160034PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749008 | BDM09160035PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749007 | BDM09160036PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749006 | BDM09160037PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749004 | BDM09160039PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749003 | BDM09160040PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749001 | BDM09160041PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11749000 | BDM09160042PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11748999 | BDM09160043PL | BioAgri | starch/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11748998 | BDM09160044PL | Polyethylene | PE | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11748997 | BDM09160045PL | PLA/PHA | PLA/PHA | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11748996 | BDM09160046PL | Organix | PLA/PBAT | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |
| SRR11748994 | BDM09160048PL | Naturecycle | starch/Polyester blend | Plastosphere | In_situ | _(vazio)_ | Mediterranean | USA: Mount Vernon in Washington State |

### PRJNA1155845  (96 linhas na aba)

| SAMPLE | SAMPLE_NAME | TIPO_AMOSTRA | TRATAMENTO_ORIGINAL | POLYMER_TYPE | GLIFOSATO | SOIL_FRACTION | ENV_TYPE | ACAO |
|---|---|---|---|---|---|---|---|---|
| SRR30519546 | Con1 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517364 | Con1 | Intestino de Enchytraeus crypticus | Controle | NONE | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519545 | Con2 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517363 | Con2 | Intestino de Enchytraeus crypticus | Controle | NONE | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519544 | Con3 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517362 | Con3 | Intestino de Enchytraeus crypticus | Controle | NONE | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519543 | Con4 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517361 | Con4 | Intestino de Enchytraeus crypticus | Controle | NONE | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519542 | GA1 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517360 | GA1 | Intestino de Enchytraeus crypticus | PLA + glifosato | PLA | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517359 | GA2 | Intestino de Enchytraeus crypticus | PLA + glifosato | PLA | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519541 | GA2 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519539 | GA3 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517357 | GA3 | Intestino de Enchytraeus crypticus | PLA + glifosato | PLA | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519538 | GA4 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517356 | GA4 | Intestino de Enchytraeus crypticus | PLA + glifosato | PLA | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519537 | GE1 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517355 | GE1 | Intestino de Enchytraeus crypticus | PET + glifosato | PET | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519536 | GE2 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517354 | GE2 | Intestino de Enchytraeus crypticus | PET + glifosato | PET | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517353 | GE3 | Intestino de Enchytraeus crypticus | PET + glifosato | PET | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519535 | GE3 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517352 | GE4 | Intestino de Enchytraeus crypticus | PET + glifosato | PET | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519534 | GE4 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519533 | Gly1 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517351 | Gly1 | Intestino de Enchytraeus crypticus | Glifosato | NONE | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517350 | Gly2 | Intestino de Enchytraeus crypticus | Glifosato | NONE | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519532 | Gly2 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517349 | Gly3 | Intestino de Enchytraeus crypticus | Glifosato | NONE | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519531 | Gly3 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517348 | Gly4 | Intestino de Enchytraeus crypticus | Glifosato | NONE | Sim | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519530 | Gly4 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519528 | PET1 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517346 | PET1 | Intestino de Enchytraeus crypticus | PET | PET | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517345 | PET2 | Intestino de Enchytraeus crypticus | PET | PET | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519527 | PET2 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517344 | PET3 | Intestino de Enchytraeus crypticus | PET | PET | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519526 | PET3 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519525 | PET4 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517343 | PET4 | Intestino de Enchytraeus crypticus | PET | PET | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517342 | PLA1 | Intestino de Enchytraeus crypticus | PLA | PLA | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519524 | PLA1 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517341 | PLA2 | Intestino de Enchytraeus crypticus | PLA | PLA | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519523 | PLA2 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519522 | PLA3 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517340 | PLA3 | Intestino de Enchytraeus crypticus | PLA | PLA | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30519521 | PLA4 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517339 | PLA4 | Intestino de Enchytraeus crypticus | PLA | PLA | Não | **Gut** [Bulk] | **Invertebrate gut** [Agricultural] | _(vazio)_ |
| SRR30517381 | S_Con1 | Solo | Controle | NONE | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519563 | S_Con1 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517380 | S_Con2 | Solo | Controle | NONE | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519562 | S_Con2 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517369 | S_Con3 | Solo | Controle | NONE | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519551 | S_Con3 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519540 | S_Con4 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517358 | S_Con4 | Solo | Controle | NONE | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30517347 | S_GA1 | Solo | PLA + glifosato | PLA | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519529 | S_GA1 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519520 | S_GA2 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517338 | S_GA2 | Solo | PLA + glifosato | PLA | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519519 | S_GA3 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517337 | S_GA3 | Solo | PLA + glifosato | PLA | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30517336 | S_GA4 | Solo | PLA + glifosato | PLA | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519518 | S_GA4 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517335 | S_GE1 | Solo | PET + glifosato | PET | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519517 | S_GE1 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517334 | S_GE2 | Solo | PET + glifosato | PET | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519516 | S_GE2 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519561 | S_GE3 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517379 | S_GE3 | Solo | PET + glifosato | PET | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30517378 | S_GE4 | Solo | PET + glifosato | PET | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519560 | S_GE4 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517377 | S_Gly1 | Solo | Glifosato | NONE | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519559 | S_Gly1 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517376 | S_Gly2 | Solo | Glifosato | NONE | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519558 | S_Gly2 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517375 | S_Gly3 | Solo | Glifosato | NONE | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519557 | S_Gly3 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517374 | S_Gly4 | Solo | Glifosato | NONE | Sim | Bulk | Agricultural | _(vazio)_ |
| SRR30519556 | S_Gly4 | ITS (fungo) | _(vazio)_ | _(vazio)_ | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517373 | S_PET1 | Solo | PET | PET | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519555 | S_PET1 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517372 | S_PET2 | Solo | PET | PET | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519554 | S_PET2 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517371 | S_PET3 | Solo | PET | PET | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519553 | S_PET3 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519552 | S_PET4 | ITS (fungo) | _(vazio)_ | PET | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517370 | S_PET4 | Solo | PET | PET | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30517368 | S_PLA1 | Solo | PLA | PLA | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519550 | S_PLA1 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30519549 | S_PLA2 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517367 | S_PLA2 | Solo | PLA | PLA | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519548 | S_PLA3 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |
| SRR30517366 | S_PLA3 | Solo | PLA | PLA | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30517365 | S_PLA4 | Solo | PLA | PLA | Não | Bulk | Agricultural | _(vazio)_ |
| SRR30519547 | S_PLA4 | ITS (fungo) | _(vazio)_ | PLA | _(vazio)_ | Bulk | Agricultural | REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi |

### PRJEB59875  (25 linhas na aba)

| SAMPLE | SAMPLE_NAME | TRATAMENTO_ORIGINAL | POLYMER_TYPE | CULTIVAR | SOIL_FRACTION | BIODEGRADABLE | PLASTIC_GROUPPING |
|---|---|---|---|---|---|---|---|
| ERR10890547 | 1 EC | Controle | NONE | Thinopyrum junceum | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890564 | 10 SpC | Controle | NONE | Sporobolus pumilus | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890565 | 11 SpC | Controle | **NONE** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_copolyester] |
| ERR10890566 | 12 SpC | Controle | **NONE** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | **_(vazio)_** [Biodegradable] | **_(vazio)_** [Biodegradable_copolyester] |
| ERR10890552 | 19 EMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890548 | 2 EC | Controle | NONE | Thinopyrum junceum | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890553 | 20 EMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890554 | 21 EMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890555 | 22 EMB | Sacola Mater-Bi | **starch/PBAT** [HDPE] | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | **Biodegradable** [NO_BIODEGRADABLE] | **Biodegradable_copolyester** [Thermoplastic] |
| ERR10890556 | 23 EMB | Sacola Mater-Bi | **starch/PBAT** [HDPE] | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | **Biodegradable** [NO_BIODEGRADABLE] | **Biodegradable_copolyester** [Thermoplastic] |
| ERR10890567 | 24 SpMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890568 | 25 SpMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890569 | 26 SpMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890570 | 27 SpMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890571 | 28 SpMB | Sacola Mater-Bi | **starch/PBAT** [PBAT] | Sporobolus pumilus | **Rhizosphere** [Plastosphere] | Biodegradable | Biodegradable_copolyester |
| ERR10890549 | 3 EC | Controle | NONE | Thinopyrum junceum | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890557 | 35 EPE | Sacola de polietileno | HDPE | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | NO_BIODEGRADABLE | Thermoplastic |
| ERR10890558 | 36 EPE | Sacola de polietileno | HDPE | Thinopyrum junceum | **Rhizosphere** [Plastosphere] | NO_BIODEGRADABLE | Thermoplastic |
| ERR10890559 | 37 EPE | Sacola de polietileno | **HDPE** [_(vazio)_] | **Thinopyrum junceum** [Sporobolus pumilus] | Rhizosphere | **NO_BIODEGRADABLE** [_(vazio)_] | **Thermoplastic** [_(vazio)_] |
| ERR10890560 | 38 EPE | Sacola de polietileno | **HDPE** [_(vazio)_] | **Thinopyrum junceum** [Sporobolus pumilus] | Rhizosphere | **NO_BIODEGRADABLE** [_(vazio)_] | **Thermoplastic** [_(vazio)_] |
| ERR10890561 | 39 EPE | Sacola de polietileno | **HDPE** [_(vazio)_] | **Thinopyrum junceum** [Sporobolus pumilus] | Rhizosphere | **NO_BIODEGRADABLE** [_(vazio)_] | **Thermoplastic** [_(vazio)_] |
| ERR10890550 | 4 EC | Controle | NONE | Thinopyrum junceum | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890551 | 6 EC | Controle | NONE | Thinopyrum junceum | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890562 | 7 SpC | Controle | NONE | Sporobolus pumilus | Rhizosphere | _(vazio)_ | _(vazio)_ |
| ERR10890563 | 8 SpC | Controle | NONE | Sporobolus pumilus | Rhizosphere | _(vazio)_ | _(vazio)_ |

### PRJNA702448  (31 linhas na aba)

| SAMPLE | SAMPLE_NAME | TRATAMENTO_ORIGINAL | POLYMER_TYPE | SOIL_FRACTION | FERTILIZATION | ADUBACAO_N | BIODEGRADABLE |
|---|---|---|---|---|---|---|---|
| SRR15247080 | ControlS1 | Control soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247078 | ControlS2 | Control soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247077 | ControlS3 | Control soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247076 | ControlS4 | Control soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247079 | ControlS5 | Control soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247064 | ControlSN1 | N fertilization | NONE | **Bulk** [_(vazio)_] | Chemical | Sim | **_(vazio)_** [Biodegradable] |
| SRR15247062 | ControlSN2 | N fertilization | NONE | **Bulk** [_(vazio)_] | Chemical | Sim | **_(vazio)_** [Biodegradable] |
| SRR15247061 | ControlSN3 | N fertilization | NONE | **Bulk** [_(vazio)_] | Chemical | Sim | **_(vazio)_** [Biodegradable] |
| SRR15247060 | ControlSN4 | N fertilization | NONE | **Bulk** [_(vazio)_] | Chemical | Sim | **_(vazio)_** [Biodegradable] |
| SRR15247059 | ControlSN5 | N fertilization | NONE | **Bulk** [_(vazio)_] | Chemical | Sim | **_(vazio)_** [Biodegradable] |
| SRR15247081 | Initial_soil | Initial soil | NONE | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | **_(vazio)_** [Biodegradable] |
| SRR15247083 | P_PS1 | PBSA | PBSA | **Plastosphere** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247082 | P_PS2 | PBSA | PBSA | **Plastosphere** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247070 | P_PS3 | PBSA | PBSA | **Plastosphere** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247063 | P_PS4 | PBSA | PBSA | **Plastosphere** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247058 | P_PS5 | PBSA | PBSA | **Plastosphere** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247057 | P_PSN1 | PBSA and N fertilization | PBSA | **Plastosphere** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247056 | P_PSN2 | PBSA and N fertilization | PBSA | **Plastosphere** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247055 | P_PSN3 | PBSA and N fertilization | PBSA | **Plastosphere** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247054 | P_PSN4 | PBSA and N fertilization | PBSA | **Plastosphere** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247053 | P_PSN5 | PBSA and N fertilization | PBSA | **Plastosphere** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247075 | S_PS1 | PBSA | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247074 | S_PS2 | PBSA | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247073 | S_PS3 | PBSA | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247072 | S_PS4 | PBSA | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247069 | S_PS5 | PBSA | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | **_(vazio)_** [Chemical] | Não | Biodegradable |
| SRR15247068 | S_PSN1 | PBSA and N fertilization | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247071 | S_PSN2 | PBSA and N fertilization | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247067 | S_PSN3 | PBSA and N fertilization | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247066 | S_PSN4 | PBSA and N fertilization | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | Chemical | Sim | Biodegradable |
| SRR15247065 | S_PSN5 | PBSA and N fertilization | **PBSA** [_(vazio)_] | **Bulk** [_(vazio)_] | Chemical | Sim | Biodegradable |

### PRJNA630025  (72 linhas na aba)

| SAMPLE | SAMPLE_NAME | LOCAL | POLYMER_TYPE | SOIL_FRACTION | ACAO |
|---|---|---|---|---|---|
| SRR11852045 | P13_bac | Barba Peider | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852015 | P13_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852044 | P14_bac | Barba Peider | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852014 | P14_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852033 | P15_bac | Barba Peider | PE | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852013 | P15_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852022 | P16_bac | Barba Peider | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852012 | P16_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852011 | P17_bac | Barba Peider | PE | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852010 | P17_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852000 | P18_bac | Barba Peider | PE | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852009 | P18_fung | _(vazio)_ | PBAT | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11851989 | P19_bac | Barba Peider | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852008 | P19_fung | _(vazio)_ | PLA | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11851978 | P20_bac | Barba Peider | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852007 | P20_fung | _(vazio)_ | PLA | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11851975 | P21_bac | Barba Peider | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852006 | P21_fung | _(vazio)_ | PLA | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11851974 | S13_bac | Barba Peider | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852005 | S13_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852043 | S14_bac | Barba Peider | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852004 | S14_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852042 | S15_bac | Barba Peider | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852003 | S15_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852041 | S16_bac | Barba Peider | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852002 | S16_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852040 | S17_bac | Barba Peider | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11852001 | S17_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852039 | S18_bac | Barba Peider | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851999 | S18_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852038 | S19_bac | Barba Peider | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851998 | S19_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852037 | S20_bac | Barba Peider | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851997 | S20_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852036 | S21_bac | Barba Peider | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851996 | S21_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852035 | VPI10_bac | Villum | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851995 | VPI10_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852034 | VPI11_bac | Villum | PE | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851994 | VPI11_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852032 | VPI12_bac | Villum | PE | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851993 | VPI12_fung | _(vazio)_ | PBAT | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852031 | VPI13_bac | Villum | PE | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851992 | VPI13_fung | _(vazio)_ | PBAT | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852030 | VPI14_bac | Villum | PE | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851991 | VPI14_fung | _(vazio)_ | PBAT | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852029 | VPI15_bac | Villum | PE | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851990 | VPI15_fung | _(vazio)_ | PLA | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852028 | VPI16_bac | Villum | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851988 | VPI16_fung | _(vazio)_ | PLA | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852027 | VPI17_bac | Villum | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851987 | VPI17_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852026 | VPI18_bac | Villum | PBAT | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851986 | VPI18_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852025 | VPI28_bac | Villum | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851985 | VPI28_fung | _(vazio)_ | PLA | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852024 | VPI29_bac | Villum | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851984 | VPI29_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852023 | VPI30_bac | Villum | PBAT | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851983 | VPI30_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852021 | VPI31_bac | Villum | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851982 | VPI31_fung | _(vazio)_ | PE | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852020 | VPI32_bac | Villum | PLA | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851981 | VPI32_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852019 | VPI33_bac | Villum | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851980 | VPI33_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852018 | VPI34_bac | Villum | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851979 | VPI34_fung | _(vazio)_ | PE | Bulk | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852017 | VPI35_bac | Villum | PLA | Bulk | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851977 | VPI35_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |
| SRR11852016 | VPI36_bac | Villum | PE | Plastosphere | VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra) |
| SRR11851976 | VPI36_fung | _(vazio)_ | PBAT | Plastosphere | REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi |

### PRJNA1054347  (36 linhas na aba)

| SAMPLE | SAMPLE_NAME | POLYMER_TYPE | SOIL_FRACTION | SAMPLING_DEPTH | ACAO |
|---|---|---|---|---|---|
| SRR27301219 | BM1 | PBAT | Bulk | 0-20 | _(vazio)_ |
| SRR27301218 | BM2 | PBAT | Bulk | 0-20 | _(vazio)_ |
| SRR27301217 | BM3 | PBAT | Bulk | 0-20 | _(vazio)_ |
| SRR27301216 | BM4 | PBAT | Bulk | 0-20 | _(vazio)_ |
| SRR27301215 | BM5 | PBAT | Bulk | 0-20 | VERIFICAR: nome indica solo bulk, mas o NCBI diz env_medium="rhizosphere soil" |
| SRR27301214 | BM6 | PBAT | Bulk | 0-20 | VERIFICAR: nome indica solo bulk, mas o NCBI diz env_medium="rhizosphere soil" |
| SRR27301223 | F1 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301222 | F2 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301211 | F3 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301200 | F4 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301193 | F5 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301192 | F6 | NONE | Bulk | 0-20 | _(vazio)_ |
| SRR27301191 | M1 | PE | Bulk | 0-20 | _(vazio)_ |
| SRR27301190 | M2 | PE | Bulk | 0-20 | _(vazio)_ |
| SRR27301189 | M3 | PE | Bulk | 0-20 | _(vazio)_ |
| SRR27301188 | M4 | PE | Bulk | 0 | VERIFICAR: SAMPLING_DEPTH = 0, as demais amostras têm 0-20 |
| SRR27301221 | M5 | PE | Bulk | 0-20 | _(vazio)_ |
| SRR27301220 | M6 | PE | Bulk | 0-20 | _(vazio)_ |
| SRR27301199 | RBM1 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301198 | RBM2 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301197 | RBM3 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301196 | RBM4 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301195 | RBM5 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301194 | RBM6 | PBAT | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301213 | RF1 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301212 | RF2 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301210 | RF3 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301209 | RF4 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301208 | RF5 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301207 | RF6 | NONE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301206 | RM1 | PE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301205 | RM2 | PE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301204 | RM3 | PE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301203 | RM4 | PE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301202 | RM5 | PE | Rhizosphere | 0-20 | _(vazio)_ |
| SRR27301201 | RM6 | PE | Rhizosphere | 0-20 | _(vazio)_ |

### PRJNA1021161  (111 linhas na aba)

| SAMPLE | SAMPLE_NAME | POLYMER_TYPE | DOSE_MP(%) | FOTOENVELHECIMENTO | TEMPO_INCUBACAO |
|---|---|---|---|---|---|
| SRR26191042 | 0.5PE-100days-replicate1 | PE | 0.5 | virgem | 100 dias |
| SRR26191041 | 0.5PE-100days-replicate2 | PE | 0.5 | virgem | 100 dias |
| SRR26191040 | 0.5PE-100days-replicate3 | PE | 0.5 | virgem | 100 dias |
| SRR26191078 | 0.5PE-25days-replicate1 | PE | 0.5 | virgem | 25 dias |
| SRR26191067 | 0.5PE-25days-replicate2 | PE | 0.5 | virgem | 25 dias |
| SRR26191032 | 0.5PE-25days-replicate3 | PE | 0.5 | virgem | 25 dias |
| SRR26191077 | 0.5PE-50days-replicate1 | PE | 0.5 | virgem | 50 dias |
| SRR26191076 | 0.5PE-50days-replicate2 | PE | 0.5 | virgem | 50 dias |
| SRR26191075 | 0.5PE-50days-replicate3 | PE | 0.5 | virgem | 50 dias |
| SRR26191024 | 0.5PE-75days-replicate1 | PE | 0.5 | virgem | 75 dias |
| SRR26191023 | 0.5PE-75days-replicate2 | PE | 0.5 | virgem | 75 dias |
| SRR26191022 | 0.5PE-75days-replicate3 | PE | 0.5 | virgem | 75 dias |
| SRR26191008 | 0.5PE10d-100days-replicate1 | PE | 0.5 | 10 dias | 100 dias |
| SRR26191007 | 0.5PE10d-100days-replicate2 | PE | 0.5 | 10 dias | 100 dias |
| SRR26191006 | 0.5PE10d-100days-replicate3 | PE | 0.5 | 10 dias | 100 dias |
| SRR26191097 | 0.5PE10d-25days-replicate1 | PE | 0.5 | 10 dias | 25 dias |
| SRR26191096 | 0.5PE10d-25days-replicate2 | PE | 0.5 | 10 dias | 25 dias |
| SRR26191095 | 0.5PE10d-25days-replicate3 | PE | 0.5 | 10 dias | 25 dias |
| SRR26191068 | 0.5PE10d-50days-replicate1 | PE | 0.5 | 10 dias | 50 dias |
| SRR26191066 | 0.5PE10d-50days-replicate2 | PE | 0.5 | 10 dias | 50 dias |
| SRR26191065 | 0.5PE10d-50days-replicate3 | PE | 0.5 | 10 dias | 50 dias |
| SRR26191014 | 0.5PE10d-75days-replicate1 | PE | 0.5 | 10 dias | 75 dias |
| SRR26191061 | 0.5PE10d-75days-replicate2 | PE | 0.5 | 10 dias | 75 dias |
| SRR26191060 | 0.5PE10d-75days-replicate3 | PE | 0.5 | 10 dias | 75 dias |
| SRR26191011 | 0.5PE5d-100days-replicate1 | PE | 0.5 | 5 dias | 100 dias |
| SRR26191010 | 0.5PE5d-100days-replicate2 | PE | 0.5 | 5 dias | 100 dias |
| SRR26191009 | 0.5PE5d-100days-replicate3 | PE | 0.5 | 5 dias | 100 dias |
| SRR26191012 | 0.5PE5d-25days-replicate1 | PE | 0.5 | 5 dias | 25 dias |
| SRR26191110 | 0.5PE5d-25days-replicate2 | PE | 0.5 | 5 dias | 25 dias |
| SRR26191099 | 0.5PE5d-25days-replicate3 | PE | 0.5 | 5 dias | 25 dias |
| SRR26191071 | 0.5PE5d-50days-replicate1 | PE | 0.5 | 5 dias | 50 dias |
| SRR26191070 | 0.5PE5d-50days-replicate2 | PE | 0.5 | 5 dias | 50 dias |
| SRR26191069 | 0.5PE5d-50days-replicate3 | PE | 0.5 | 5 dias | 50 dias |
| SRR26191017 | 0.5PE5d-75days-replicate1 | PE | 0.5 | 5 dias | 75 dias |
| SRR26191016 | 0.5PE5d-75days-replicate2 | PE | 0.5 | 5 dias | 75 dias |
| SRR26191015 | 0.5PE5d-75days-replicate3 | PE | 0.5 | 5 dias | 75 dias |
| SRR26191107 | 0.5PLA-100days-replicate1 | PLA | 0.5 | virgem | 100 dias |
| SRR26191106 | 0.5PLA-100days-replicate2 | PLA | 0.5 | virgem | 100 dias |
| SRR26191105 | 0.5PLA-100days-replicate3 | PLA | 0.5 | virgem | 100 dias |
| SRR26191087 | 0.5PLA-25days-replicate1 | PLA | 0.5 | virgem | 25 dias |
| SRR26191086 | 0.5PLA-25days-replicate2 | PLA | 0.5 | virgem | 25 dias |
| SRR26191085 | 0.5PLA-25days-replicate3 | PLA | 0.5 | virgem | 25 dias |
| SRR26191034 | 0.5PLA-50days-replicate1 | PLA | 0.5 | virgem | 50 dias |
| SRR26191033 | 0.5PLA-50days-replicate2 | PLA | 0.5 | virgem | 50 dias |
| SRR26191031 | 0.5PLA-50days-replicate3 | PLA | 0.5 | virgem | 50 dias |
| SRR26191052 | 0.5PLA-75days-replicate1 | PLA | 0.5 | virgem | 75 dias |
| SRR26191051 | 0.5PLA-75days-replicate2 | PLA | 0.5 | virgem | 75 dias |
| SRR26191050 | 0.5PLA-75days-replicate3 | PLA | 0.5 | virgem | 75 dias |
| SRR26191039 | 1.5PE-100days-replicate1 | PE | 1.5 | virgem | 100 dias |
| SRR26191038 | 1.5PE-100days-replicate2 | PE | 1.5 | virgem | 100 dias |
| SRR26191013 | 1.5PE-100days-replicate3 | PE | 1.5 | virgem | 100 dias |
| SRR26191021 | 1.5PE-25days-replicate1 | PE | 1.5 | virgem | 25 dias |
| SRR26191058 | 1.5PE-25days-replicate2 | PE | 1.5 | virgem | 25 dias |
| SRR26191047 | 1.5PE-25days-replicate3 | PE | 1.5 | virgem | 25 dias |
| SRR26191074 | 1.5PE-50days-replicate1 | PE | 1.5 | virgem | 50 dias |
| SRR26191073 | 1.5PE-50days-replicate2 | PE | 1.5 | virgem | 50 dias |
| SRR26191072 | 1.5PE-50days-replicate3 | PE | 1.5 | virgem | 50 dias |
| SRR26191020 | 1.5PE-75days-replicate1 | PE | 1.5 | virgem | 75 dias |
| SRR26191019 | 1.5PE-75days-replicate2 | PE | 1.5 | virgem | 75 dias |
| SRR26191018 | 1.5PE-75days-replicate3 | PE | 1.5 | virgem | 75 dias |
| SRR26191002 | 1.5PE10d-100days-replicate1 | PE | 1.5 | 10 dias | 100 dias |
| SRR26191109 | 1.5PE10d-100days-replicate2 | PE | 1.5 | 10 dias | 100 dias |
| SRR26191108 | 1.5PE10d-100days-replicate3 | PE | 1.5 | 10 dias | 100 dias |
| SRR26191091 | 1.5PE10d-25days-replicate1 | PE | 1.5 | 10 dias | 25 dias |
| SRR26191090 | 1.5PE10d-25days-replicate2 | PE | 1.5 | 10 dias | 25 dias |
| SRR26191088 | 1.5PE10d-25days-replicate3 | PE | 1.5 | 10 dias | 25 dias |
| SRR26191037 | 1.5PE10d-50days-replicate1 | PE | 1.5 | 10 dias | 50 dias |
| SRR26191036 | 1.5PE10d-50days-replicate2 | PE | 1.5 | 10 dias | 50 dias |
| SRR26191035 | 1.5PE10d-50days-replicate3 | PE | 1.5 | 10 dias | 50 dias |
| SRR26191055 | 1.5PE10d-75days-replicate1 | PE | 1.5 | 10 dias | 75 dias |
| SRR26191054 | 1.5PE10d-75days-replicate2 | PE | 1.5 | 10 dias | 75 dias |
| SRR26191053 | 1.5PE10d-75days-replicate3 | PE | 1.5 | 10 dias | 75 dias |
| SRR26191005 | 1.5PE5d-100days-replicate1 | PE | 1.5 | 5 dias | 100 dias |
| SRR26191004 | 1.5PE5d-100days-replicate2 | PE | 1.5 | 5 dias | 100 dias |
| SRR26191003 | 1.5PE5d-100days-replicate3 | PE | 1.5 | 5 dias | 100 dias |
| SRR26191094 | 1.5PE5d-25days-replicate1 | PE | 1.5 | 5 dias | 25 dias |
| SRR26191093 | 1.5PE5d-25days-replicate2 | PE | 1.5 | 5 dias | 25 dias |
| SRR26191092 | 1.5PE5d-25days-replicate3 | PE | 1.5 | 5 dias | 25 dias |
| SRR26191064 | 1.5PE5d-50days-replicate1 | PE | 1.5 | 5 dias | 50 dias |
| SRR26191063 | 1.5PE5d-50days-replicate2 | PE | 1.5 | 5 dias | 50 dias |
| SRR26191062 | 1.5PE5d-50days-replicate3 | PE | 1.5 | 5 dias | 50 dias |
| SRR26191059 | 1.5PE5d-75days-replicate1 | PE | 1.5 | 5 dias | 75 dias |
| SRR26191057 | 1.5PE5d-75days-replicate2 | PE | 1.5 | 5 dias | 75 dias |
| SRR26191056 | 1.5PE5d-75days-replicate3 | PE | 1.5 | 5 dias | 75 dias |
| SRR26191104 | 1.5PLA-100days-replicate1 | PLA | 1.5 | virgem | 100 dias |
| SRR26191103 | 1.5PLA-100days-replicate2 | PLA | 1.5 | virgem | 100 dias |
| SRR26191102 | 1.5PLA-100days-replicate3 | PLA | 1.5 | virgem | 100 dias |
| SRR26191084 | 1.5PLA-25days-replicate1 | PLA | 1.5 | virgem | 25 dias |
| SRR26191083 | 1.5PLA-25days-replicate2 | PLA | 1.5 | virgem | 25 dias |
| SRR26191082 | 1.5PLA-25days-replicate3 | PLA | 1.5 | virgem | 25 dias |
| SRR26191030 | 1.5PLA-50days-replicate1 | PLA | 1.5 | virgem | 50 dias |
| SRR26191029 | 1.5PLA-50days-replicate2 | PLA | 1.5 | virgem | 50 dias |
| SRR26191028 | 1.5PLA-50days-replicate3 | PLA | 1.5 | virgem | 50 dias |
| SRR26191049 | 1.5PLA-75days-replicate1 | PLA | 1.5 | virgem | 75 dias |
| SRR26191048 | 1.5PLA-75days-replicate2 | PLA | 1.5 | virgem | 75 dias |
| SRR26191046 | 1.5PLA-75days-replicate3 | PLA | 1.5 | virgem | 75 dias |
| SRR26191045 | CK-100days-replicate1 | NONE | 0 | _(vazio)_ | 100 dias |
| SRR26191044 | CK-100days-replicate2 | NONE | 0 | _(vazio)_ | 100 dias |
| SRR26191043 | CK-100days-replicate3 | NONE | 0 | _(vazio)_ | 100 dias |
| SRR26191112 | CK-25days-replicate1 | NONE | 0 | _(vazio)_ | 25 dias |
| SRR26191111 | CK-25days-replicate2 | NONE | 0 | _(vazio)_ | 25 dias |
| SRR26191089 | CK-25days-replicate3 | NONE | 0 | _(vazio)_ | 25 dias |
| SRR26191081 | CK-50days-replicate1 | NONE | 0 | _(vazio)_ | 50 dias |
| SRR26191080 | CK-50days-replicate2 | NONE | 0 | _(vazio)_ | 50 dias |
| SRR26191079 | CK-50days-replicate3 | NONE | 0 | _(vazio)_ | 50 dias |
| SRR26191027 | CK-75days-replicate1 | NONE | 0 | _(vazio)_ | 75 dias |
| SRR26191026 | CK-75days-replicate2 | NONE | 0 | _(vazio)_ | 75 dias |
| SRR26191025 | CK-75days-replicate3 | NONE | 0 | _(vazio)_ | 75 dias |
| SRR26191101 | Untreated-replicate1 | NONE | 0 | _(vazio)_ | 0 (solo inicial) |
| SRR26191100 | Untreated-replicate2 | NONE | 0 | _(vazio)_ | 0 (solo inicial) |
| SRR26191098 | Untreated-replicate3 | NONE | 0 | _(vazio)_ | 0 (solo inicial) |

### PRJNA932786  (12 linhas na aba)

| SAMPLE | SAMPLE_NAME | TRATAMENTO_ORIGINAL | POLYMER_TYPE | TIPO_AMOSTRA |
|---|---|---|---|---|
| SRR23373543 | 10b | No microplastics | NONE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373576 | 11b | No microplastics | NONE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373575 | 12b | No microplastics | NONE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373578 | 1b | PBAT microplastics | PBAT | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373577 | 2b | PBAT microplastics | PBAT | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373566 | 3b | PBAT microplastics | PBAT | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373555 | 4b | PBAT microplastics | PBAT | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373548 | 5b | PE microplastics | PE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373547 | 6b | PE microplastics | PE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373546 | 7b | PE microplastics | PE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373545 | 8b | PE microplastics | PE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |
| SRR23373544 | 9b | No microplastics | NONE | Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos) |

## 5. Fontes

* NCBI BioSample / ENA: atributos por amostra em `dados_ncbi/runs_biosample.tsv`.
* PRJNA564156 / PRJNA631499: mesmo experimento de mulch biodegradável em Knoxville-TN e Mount Vernon-WA; título do BioSample = produto aplicado na parcela.
* PRJNA1155845: *The combination of microplastics and glyphosate affects the microbiome of soil inhabitant Enchytraeus crypticus*. J. Hazard. Mater. 2025, doi:10.1016/j.jhazmat.2025.137676.
* PRJEB59875: Menicagli et al. 2023, *Plastic litter changes the rhizosphere bacterial community of coastal dune plants* (PMID 37030390).
* PRJNA630025: Rüthi et al. 2020, Front. Environ. Sci., doi:10.3389/fenvs.2020.562263.
