# Padronização de unidades e formatos — aba "Metadata - Bacteria"

Aplicada sobre a planilha revisada (`planilha_bacteria_revisada.tsv`). As saídas são `planilha_bacteria_padronizada.xlsx`, pronta para colar na planilha online (aba **Metadata - Bacteria** + aba com as linhas de ITS a remover), e `correcoes_finais.tsv`, com **todas** as diferenças em relação à planilha online atual (revisão por artigo + padronização).

## Regras gerais

* **Vazio = `NA`** em todas as colunas.
* **Números:** ponto decimal (`15.14`, não `15,14`), sem `~` e sem separador de milhar.
* **Média ± desvio:** fica só a média (ex.: `6,03 ± 0,36` → `6.03`). Os desvios estão no relatório da revisão.
* **Faixa:** `min-max` (ex.: `489–525` → `489-525`). **Dimensões:** `a x b`.
* **Controles sem plástico:** `POLYMER_TYPE = NONE` e propriedades do polímero `NA`.

## Unidade de cada coluna

| Coluna | Unidade / formato |
|---|---|
| `POLYMER_SIZE` | µm (cm × 10 000; mm × 1 000). Filmes: espessura; pedaços: "a x b"; partículas: diâmetro |
| `POLYMER_SIZE_METRIC` | sempre "µm" (NA se não há tamanho) |
| `POLYMER_THICKNESS(µm)` | espessura do filme em µm (NA para partículas, controles e quando o artigo não informa) |
| `POLYMER_PIECE_SIZE(µm)` | tamanho do pedaço ("a x b") ou diâmetro da partícula, em µm (NA para mulch inteiro no campo ou não informado) |
| `POLYMER_AROMATIC_RINGS` | 1 = tem anel aromático (tereftalato: PET, PBAT e blends), 0 = não tem, NA = controle ou composição desconhecida |
| `DENSITY_(g/cm³)` | g/cm³ |
| `MOLECULAR_WEIGHT_(g/mol)` | g/mol, número inteiro, faixa "min-max" |
| `SAMPLING_DEPTH` | cm, "min-max" |
| `ANNUAL_RAINFALL(mm)` | mm/ano |
| `AVG_ANNUAL_TEMPERATURE` | °C (temperatura média anual do ar) |
| `SOIL_TEMPERATURE(C)` | °C (campo: média do solo; laboratório: temperatura de incubação) |
| `WATER_CONTENT(%)` | % (gravimétrico ou % da capacidade de retenção, como no artigo) |
| `SOC(g/kg)` | g/kg (carbono orgânico; quando o artigo dá matéria orgânica, SOC = MO / 1,724) |
| `TN(g/kg)` | g/kg |
| `C/N` | adimensional |
| `pH` | adimensional (média; o desvio foi removido) |
| `DOC(mg/kg)` | mg/kg |
| `DIN(mg/kg)` | mg/kg (NH4⁺-N + NO3⁻-N) |
| `NH4(mg/kg)` | mg/kg |
| `NO3(mg/kg)` | mg/kg |
| `AP(mg/kg)` | mg/kg |
| `AK(mg/kg)` | mg/kg |
| `YEAR_PERIOD` | ano ou "ano-ano" |

## Vocabulário unificado

| Coluna | Antes | Depois |
|---|---|---|
| `BIODEGRADABLE` | NO_BIODEGRADABLE | Non_biodegradable |
| `CULTIVAR` | Maize | Zea mays |
| `CULTIVAR` | barley | Hordeum vulgare |
| `CLIMATE` | Temperate Continental | Temperate continental |
| `ENV_TYPE` | Coastal Dune | Coastal dune |
| `DEGRADABILITY_RATE` | Extremely Low | Extremely low |
| `DEGRADABILITY_RATE` | Moderate to Fast | Moderate to fast |
| `CHEMICAL_COMPOSITION` | Polyester Blend | Polyester blend |
| `POLYMER_SIZE` | 4 x 4 cm; 2–5 × 2–5 mm; 25 x 25 cm; 1 mm | 40000 x 40000; 2000-5000 x 2000-5000; 250000 x 250000; 1000 (µm) |
| `MOLECULAR_WEIGHT_(g/mol)` | 10⁴ – 10⁶; 6 x 10⁴ – 2 x 10⁵; 10,000 - 50,000 | 10000-1000000; 60000-200000; 10000-50000 |
| `YEAR_PERIOD` | 2019/2020; 2019–2022 | 2019-2020; 2019-2022 |

## Observação sobre POLYMER_SIZE

A coluna mistura grandezas diferentes: **espessura** dos filmes de mulch (10–479 µm), **dimensão dos pedaços** de filme (40000 x 40000 µm) e **diâmetro** de partículas (30–250 µm). Agora a unidade é a mesma, mas, para comparar entre estudos, as colunas `POLYMER_THICKNESS(µm)` e `POLYMER_PIECE_SIZE(µm)`, logo após `POLYMER_SIZE`, separam as duas medidas. Exemplo: em PRJNA702448 o filme tem 50 µm de espessura e foi cortado em pedaços de 2000-5000 µm; em PRJNA630025 a espessura não é informada.

## Resumo das diferenças em relação à planilha online

| Tipo | Células |
|---|---|
| ERRO | 1411 |
| FORMATO | 2622 |
| PADRONIZAÇÃO | 613 |
| PREENCHER | 564 |
| REMOVER | 84 |
| SUGESTÃO | 217 |
