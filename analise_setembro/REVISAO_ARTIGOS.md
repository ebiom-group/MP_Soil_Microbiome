# Revisão da aba "Metadata - Bacteria" contra os artigos e o NCBI

Escrito em 15/10/2026. A base é a planilha **baixada hoje** (`Database_Plastic-Soil.xlsx`), comparada campo a campo com os artigos e suplementos em `artigos/` e com os metadados do NCBI/ENA (`dados_ncbi/`).

**Arquivos gerados**
* `revisao_artigos_correcoes.tsv`: uma linha por célula, com valor atual → correto, tipo e fonte (artigo, tabela ou trecho citado). É o arquivo para filtrar e corrigir a planilha online.
* `planilha_bacteria_revisada.tsv`: a aba inteira com todas as correções aplicadas, mais a coluna `ACAO` (linhas a remover).
* `revisar_planilha_artigos.py`: o script com cada regra e sua fonte, para reproduzir ou ajustar.

> **Versão final para subir na planilha online:** `planilha_bacteria_padronizada.xlsx` (unidades, números e NA padronizados) e `correcoes_finais.tsv` (todas as diferenças). Ver `PADRONIZACAO.md`.

## 1. Resumo

* **2978 células** em 549 amostras, e **84 linhas a remover** (runs de ITS).

| Projeto | ERRO | PADRONIZAÇÃO | PREENCHER | SUGESTÃO | REMOVER (linhas) |
|---|---|---|---|---|---|
| PRJNA564156 | 639 | 360 | 216 | 134 | 0 |
| PRJNA631499 | 76 | 40 | 184 | 48 | 0 |
| PRJNA630025 | 195 | 0 | 0 | 9 | 36 |
| PRJNA702448 | 232 | 11 | 92 | 0 | 0 |
| PRJNA1054347 | 19 | 12 | 108 | 12 | 0 |
| PRJNA1021161 | 113 | 96 | 0 | 72 | 0 |
| PRJNA1155845 | 104 | 48 | 0 | 48 | 48 |
| PRJEB59875 | 17 | 35 | 0 | 0 | 0 |
| PRJNA932786 | 16 | 24 | 12 | 4 | 0 |
| PRJNA853344 | 0 | 2 | 0 | 0 | 0 |

**Tipos:** **ERRO** = contradiz o artigo ou o NCBI · **PREENCHER** = estava vazio e o valor está no artigo · **SUGESTÃO** = decisão do grupo (valor mais preciso, mas muda a categoria) · **PADRONIZAÇÃO** = mesmo significado, grafia diferente · **REMOVER** = a linha não é 16S.

## 2. Erros mais importantes (mudam a análise)

| Projeto | O que estava errado | Correção | Fonte |
|---|---|---|---|
| PRJNA564156 | Clima, chuva, temperatura e **toda a química do solo** (SOC, TN, C/N, DOC, DIN, NH4, NO3, AP, AK) deslocados: 25 amostras de TN com valores de WA e 25 de WA com valores de TN. pH trocado em 3 amostras. | Valores atribuídos pelo sítio real (NCBI `geo_loc_name`). A química do solo (fonte: Sintim et al. 2019) é de TN; WA fica vazio. | NCBI + Front. Microbiol. (pH) |
| PRJNA631499 | 48 **culturas de enriquecimento** de laboratório marcadas como plastisfera. Temperatura do solo em TN = **46250**. | `SOIL_FRACTION` = Enrichment_culture (30 °C, 3–6 semanas). Temperatura em TN = 16,8 °C. | Front. Microbiol. métodos; Data Sheet 1, Tabela S2 |
| PRJNA630025 | SOC, TN, C/N, pH e chuva **não batem** com a Tabela 1 do artigo (ex.: SOC 119 g/kg × 1,4 g/kg; pH 4,4 × 6,5). Fração errada em 6 amostras de Barba Peider. 36 runs de ITS. | Valores da Tabela 1. Fração pelo prefixo P/S. Remover os `*_fung`. | Rüthi et al. 2020, Tabela 1 e Fig. S2 |
| PRJNA702448 | **Região 16S = V4** (515F/806R), não V3‑V4. Umidade 60 % (real 17,5 %), temperatura 20 °C (real 22 °C), chuva 404 mm (real 489–525 mm), temperatura média 9,8 °C (real 8,9–9,7 °C). Controles com propriedades de PBSA. pH e TN vazios. | Corrigido; pH e TN preenchidos por tratamento. | Tanunchai et al. 2021; Guliyev et al. 2022; d1em00426c |
| PRJNA1155845 | **SOC e DIN trocados entre tratamentos** em 28 de 48 amostras. **24 amostras são intestino** de *E. crypticus*. 48 runs de ITS. | SOC = SOM × 10/1,724 e DIN = NH4 + NO3 do tratamento (Tabela S1). `SOIL_FRACTION` = Gut. Remover SRR30519*. | Yang et al. 2025, Tabela S1; NCBI |
| PRJEB59875 | 14 amostras como plastisfera; 37–39 EPE como *Sporobolus*. | Todas são **rizosfera**. 35–39 EPE = *Thinopyrum junceum*. | Menicagli et al. 2023, métodos |
| PRJNA1021161 | Tipo de solo e clima (Cumulic Haplustolls, 584 mm, 9,1 °C) copiados de **outro estudo** (Changwu, PRJNA1054347). Este é de Yangling. | Esvaziados: o artigo não informa. | Qiu et al. 2024, métodos |
| PRJNA932786 | SOC = 29,5 g/kg, mas esse valor é **matéria orgânica**. | SOC ≈ 17,1 g/kg (29,5 / 1,724). | Adhikari et al., SI Tabela S1 |
| PRJNA1054347 | Temperatura do solo da rizosfera copiada do bulk. M4 com profundidade 0. | Rizosfera vazia (não medida). M4 = 0–20. | Zhang et al. 2024, Tabela S2 |
| Polímeros (todos) | PE de baixa densidade (LDPE/LLDPE) com densidade de HDPE (0,94–0,97) ou digitada como "0,94-0,167". `TPS/polyester` sem nenhuma propriedade. | LDPE/LLDPE = 0,91–0,94. Naturecycle = Biodegradable. | PeerJ Tabela 1; Rüthi; Adhikari |

## 3. Matriz de verificação (todas as colunas × projetos)

**Legenda:** ✓ conferido e correto · ✗ corrigido (erro) · + preenchido com valor do artigo · ~ sugestão · s padronização de grafia · **?** não verificável (o valor não está nos arquivos fornecidos) · **R** propriedade genérica do polímero (referência de literatura, não do artigo) · — vazio / não se aplica

| Coluna | NA564156 | NA631499 | NA630025 | NA702448 | NA1054347 | NA1021161 | NA1155845 | EB59875 | NA932786 | NA853344 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `16S_REGION` | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ? | ✓ |
| `POLYMER_TYPE` | ~ | ~ | ~ | s | ✓ | ✓ | ✓ | ✓ | ~ | ✓ |
| `POLYMER_SIZE` | ~ | + | ✓ | ✓ | + | ✓ | ✓ | s | ? | ? |
| `POLYMER_SIZE_METRIC` | ~ | + | ✓ | ✓ | + | s | ✓ | s | s | ? |
| `POLYMER_FORMAT` | ✗ | ✓ | ✓ | ✓ | + | ✓ | ✓ | ✓ | ✓ | ? |
| `POLYMER_COLOR` | ? | ? | — | — | ? | — | — | — | — | ? |
| `POLYMER_AROMATIC_RINGS` | R | R | R | — | R | — | R | R | R | — |
| `BIODEGRADABLE` | + | + | ✓ | ✗ | s | ✓ | ✓ | ✓ | ✓ | ✓ |
| `DENSITY_(g/cm³)` | ✗ | ✗ | ✗ | ✗ | ~ | ~ | R | R | ✗ | R |
| `MOLECULAR_WEIGHT_(g/mol)` | R | R | R | ✗ | R | R | R | R | R | R |
| `CHEMICAL_COMPOSITION` | R | R | R | ✗ | R | R | R | s | R | R |
| `HARDNESS` | R | R | R | ✗ | R | R | R | R | R | R |
| `DEGRADABILITY_RATE` | R | R | R | ✗ | R | R | R | R | R | R |
| `PLASTIC_GROUPPING` | + | + | R | ✗ | R | R | R | R | R | R |
| `SOIL_FRACTION` | ✓ | ✗ | ✗ | + | ✓ | ✓ | ✗ | ✗ | ✓ | s |
| `SAMPLING_DEPTH` | ✓ | ✓ | ✓ | ? | ✗ | ✓ | ✓ | ✓ | ? | — |
| `CULTIVAR` | s | ✓ | — | ✓ | ✓ | — | — | ✗ | — | ✓ |
| `SOIL_TYPE` | ✓ | ✓ | ? | ✓ | ✓ | ✗ | ? | ✓ | s | ✓ |
| `EXPERIMENT_TYPE` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `ENV_TYPE` | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✗ | ✓ | ? | ✓ |
| `FARM_SYSTEM` | ? | ? | — | ✓ | ✓ | — | — | — | ? | ✓ |
| `FERTILIZATION` | ? | ? | — | ✓ | ✓ | — | — | — | — | ✓ |
| `TILLAGE` | s | s | — | — | + | — | ~ | — | — | — |
| `COUNTRY` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `CLIMATE` | ✗ | ? | ? | ✓ | ✓ | — | s | ? | ? | ✓ |
| `ANNUAL_RAINFALL(mm)` | ✗ | ? | ✗ | ✗ | ✓ | ✗ | ? | ? | ? | ✓ |
| `AVG_ANNUAL_TEMPERATURE` | ✗ | ? | ? | ✗ | ✓ | ✗ | ? | ? | ? | ✓ |
| `YEAR_PERIOD` | ✓ | ✓ | ✓ | ? | ✓ | — | ✓ | ✓ | + | ? |
| `SAMPLING_SEASON` | + | ✓ | — | — | ✓ | — | ? | ✓ | — | — |
| `SOIL_TEMPERATURE(C)` | — | ✗ | ✓ | ✗ | ✗ | — | ✓ | — | — | — |
| `WATER_CONTENT(%)` | — | — | ? | ✗ | ✓ | — | ✓ | — | ✓ | ? |
| `SOC(g/kg)` | ✗ | ? | ✗ | ✓ | ✓ | ✓ | ✗ | — | ✗ | — |
| `TN(g/kg)` | ✗ | ? | ✗ | + | ✓ | ✓ | — | — | — | — |
| `C/N` | ✗ | ? | ✗ | ✓ | ✓ | ✓ | — | — | — | — |
| `pH` | ✗ | ~ | ✗ | + | ✓ | ✓ | — | ✓ | ✓ | — |
| `DOC(mg/kg)` | ✗ | ? | — | — | ✓ | — | — | — | — | — |
| `DIN(mg/kg)` | ✗ | ? | — | — | ✓ | — | ✗ | — | — | — |
| `NH4(mg/kg)` | ✗ | ? | — | — | ✓ | — | ✓ | — | — | — |
| `NO3(mg/kg)` | ✗ | ? | — | — | ✓ | — | ✓ | — | — | — |
| `AP(mg/kg)` | ✗ | ? | — | — | ✓ | ✓ | ✓ | — | — | — |
| `AK(mg/kg)` | ✗ | ? | — | — | ✓ | ✓ | — | — | — | — |

## 4. O que não pôde ser verificado e por quê

| Projeto | Campos "?" | Motivo / o que falta |
|---|---|---|
| PRJNA564156 | `POLYMER_COLOR`, `FARM_SYSTEM`, `FERTILIZATION` | Química do solo, chuva e temperatura vêm de **Sintim et al. 2019**, que não está na pasta. Cor do PE (16 de 24 como "Black") não aparece no artigo. A fertilização também está em Sintim/Ghimire. |
| PRJNA631499 | `POLYMER_COLOR`, `FARM_SYSTEM`, `FERTILIZATION`, `CLIMATE`, `ANNUAL_RAINFALL(mm)`, `AVG_ANNUAL_TEMPERATURE`, `SOC(g/kg)`, `TN(g/kg)`, `C/N`, `DOC(mg/kg)`, `DIN(mg/kg)`, `NH4(mg/kg)`, `NO3(mg/kg)`, `AP(mg/kg)`, `AK(mg/kg)` | Mesma fonte (Sintim et al. 2019). Chuva e temperatura (1260/830 mm; 14,4/9,9 °C) não aparecem: a Tabela S3 do PeerJ dá os valores medidos (TN 1313/866 mm e 15,8 °C; WA 885/945 mm e 11,6/11,5 °C). |
| PRJNA630025 | `SOIL_TYPE`, `CLIMATE`, `AVG_ANNUAL_TEMPERATURE`, `WATER_CONTENT(%)` | Polímero por amostra: o NCBI e os suplementos não ligam amostra → polímero. Fração em Villum (`VPI*`): sem prefixo P/S. Temperatura média: o artigo só dá a do **solo** (−1,8 / −5,4 °C). Tipo de solo e umidade não constam. |
| PRJNA702448 | `SAMPLING_DEPTH`, `YEAR_PERIOD` | Profundidade (0–5) e ano (2019/2020) não aparecem nos três artigos. |
| PRJNA1054347 | `POLYMER_COLOR` | Cor do filme ("Black") não é mencionada. |
| PRJNA1155845 | `SOIL_TYPE`, `ANNUAL_RAINFALL(mm)`, `AVG_ANNUAL_TEMPERATURE`, `SAMPLING_SEASON` | Tipo de solo, clima (~1450 mm, ~17 °C) e estação não constam no artigo (local: Ningbo, Zhejiang). |
| PRJEB59875 | `CLIMATE`, `ANNUAL_RAINFALL(mm)`, `AVG_ANNUAL_TEMPERATURE` | Chuva (~910 mm) e temperatura (~14,6 °C) não constam (provavelmente em Menicagli et al. 2023a, que não está na pasta). |
| PRJNA932786 | `16S_REGION`, `POLYMER_SIZE`, `SAMPLING_DEPTH`, `ENV_TYPE`, `FARM_SYSTEM`, `CLIMATE`, `ANNUAL_RAINFALL(mm)`, `AVG_ANNUAL_TEMPERATURE` | **O artigo principal não está na pasta** (só o Supporting Information). Faltam profundidade, tamanho da partícula (250 µm), região 16S e clima. |
| PRJNA853344 | `POLYMER_SIZE`, `POLYMER_SIZE_METRIC`, `POLYMER_FORMAT`, `POLYMER_COLOR`, `YEAR_PERIOD`, `WATER_CONTENT(%)` | **O artigo principal não está na pasta** (só o SI). Fora do `conjunto_alex` (2 runs). |

## 5. Decisões para o grupo (tipo SUGESTÃO)

1. **Tipo de PE**: os artigos especificam LLDPE (PRJNA564156/631499), LDPE (PRJNA630025/932786) e HDPE (PRJEB59875). Sugiro usar o tipo exato em `POLYMER_TYPE`. Se o grupo preferir agrupar, mantenha "PE", mas corrija a densidade de qualquer forma.
2. **Weedguard (PRJNA564156)**: é papel de celulose (controle positivo do estudo). Sugestão: `POLYMER_TYPE` = "Cellulose paper" em vez de vazio, para não misturar com o "sem mulch".
3. **pH em PRJNA631499**: a Tabela S2 dá o pH exatamente na coleta destas amostras (outono de 2016). Sugiro usá-lo no lugar da média do estudo.
4. **PRJNA1155845**: `TILLAGE` = "No" num microcosmo de laboratório. Sugiro deixar vazio (não se aplica).
5. **Formato numérico**: a planilha mistura vírgula e ponto decimal ("15,14" e "15.14"), além de textos em colunas numéricas ("~910", "6,03 ± 0,36", "489–525"). Para análise, o ideal é colunas numéricas só com número (com ponto) e uma coluna separada para desvio ou faixa.

## 6. Artigos que faltam na pasta

* **PRJNA932786**: artigo principal de Adhikari et al. (ACS Agric. Sci. Technol., DOI do suplementar as2c00333).
* **PRJNA853344**: artigo principal de Purahong et al. 2021 (ES&T, es1c02695).
* **Sintim et al. 2019** (Sci. Total Environ.): fonte da química do solo e do clima de PRJNA564156/631499.
* **Menicagli et al. 2023a**: clima do local de PRJEB59875.

## 7. Fontes usadas por projeto

* **PRJNA564156**: Bandopadhyay et al. 2020, PeerJ 8:e9015 (+ Supplemental R1)
* **PRJNA631499**: Bandopadhyay et al. 2020, Front. Microbiol. 11:587074 (+ Data Sheet 1)
* **PRJNA630025**: Rüthi et al. 2020, Front. Environ. Sci. 8:562263 (Tabela 1; Data Sheets 1–5)
* **PRJNA702448**: Tanunchai et al. 2021, Environ. Sci. Eur. 33:105; Guliyev et al. 2022, Polymers 14:2801; suplementar d1em00426c
* **PRJNA1054347**: Zhang et al. 2024, Sci. Total Environ. 933:172874 (+ mmc1: Texto S1, Tabela S2)
* **PRJNA1021161**: Qiu et al. 2024, ISME J. 18:wrad017 (+ Supporting Information, Texto S1)
* **PRJNA1155845**: Yang et al. 2025, J. Hazard. Mater. 489:137676 (+ mmc2: Tabela S1)
* **PRJEB59875**: Menicagli et al. 2023, Sci. Total Environ. 880:163293
* **PRJNA932786**: Adhikari et al. (ACS Agric. Sci. Technol., as2c00333) — só o Supporting Information (Tabela S1)
* **PRJNA853344**: Purahong et al. 2021, Environ. Sci. Technol. (es1c02695) — só o Supporting Information
