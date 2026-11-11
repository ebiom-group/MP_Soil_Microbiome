# Microbioma bacteriano de solos expostos a plásticos — conclusões (`conjunto_alex`)

**Dados:** 553 amostras de 16S rRNA, 9 BioProjects, 6 países, 47.472 ASVs. Os dados complementares vêm de `Database_Plastic-Soil.xlsx`.
**Análise completa:** [`analise_microbioma_plasticos.ipynb`](analise_microbioma_plasticos.ipynb). As figuras estão em [`figuras/`](figuras/) e as tabelas em [`tabelas/`](tabelas/).

## ▶ Rodada de 15/10/2026 — planilha corrigi263597da e padronizada (notebook atual)

**Notebook:** [`analise_microbioma_plasticos.ipynb`](analise_microbioma_plasticos.ipynb) (gerado por `build_notebook.py`). Figuras em `figuras/principal/`, tabelas em `tabelas/principal/`.
**Dados:** aba *Metadata - Bacteria* da planilha atualizada pelo grupo (557 linhas; 553 no `conjunto_alex`).
**Análises:** alfa (riqueza, Shannon, Faith PD; média de 10 rarefações a 12.000 leituras), beta (Bray–Curtis, PERMANOVA, PERMDISP) e PCoA,
por variável, com gráficos de barra, dispersão e média. **Validação:** confusão com o projeto, testes dentro do projeto, envfit, Random Forest com projeto novo.

### Resultado por variável

| Variável | Confusão com projeto | R² global | R² dentro do projeto | Veredito |
|---|---|---|---|---|
| `SOIL_FRACTION` | V = 0,74 | 0,251 | **0,084** (p = 0,001) | **efeito validado** — plastisfera/intestino/enriquecimento diferem do solo em 4 de 5 projetos |
| `POLYMER_TYPE` | V = 0,61 | 0,271 | **0,034** (p = 0,001) | **efeito validado**, pequeno |
| `POLYMER_SIZE` | V = 0,81 | 0,384 | 0,027 (p = 0,001) | validado, mas a categoria quase identifica o estudo |
| `BIODEGRADABLE` | V = 0,39 | 0,054 | 0,005 (p = 0,001) | efeito pequeno, mas consistente |
| `DENSITY_(g/cm³)` | η² = 0,28 | 0,039 | 0,002 (p = 0,009) | pequeno; é propriedade do polímero (equivale a `POLYMER_TYPE`) |
| `pH`, `SOC`, `TN`, `C/N`, `DOC`, `NH4`, `NO3`, `AP`, `AK` | η² = 0,21–1,00 | 0,04–0,29 | 0,001–0,025 | **confundidas com sítio/tratamento**: são médias de artigo (1–5 projetos com variação interna) |

### Principais conclusões
1. **O projeto domina tudo.** As variáveis explicam 4–38 % da composição **globalmente**, mas só 0,1–8 % **dentro do projeto**. O R² global é,
   na maior parte, diferença entre estudos (solo, região do 16S, laboratório).
2. **A fração do solo é o efeito mais forte e mais robusto.** Dentro do projeto, R² = 8,4 %; Random Forest acerta a fração com 95 % de acurácia
   balanceada misturando projetos, mas **48 % num projeto novo** (acaso = 33 %): o padrão existe, mas a assinatura exata muda entre estudos.
3. **O tipo de polímero tem efeito real, porém pequeno** (R² 3,4 % dentro do projeto). Ele é significativo dentro de **5 dos 9 projetos**:
   PRJNA1054347 (R² 0,16), PRJNA1155845 (0,20), PRJNA631499 (0,11), PRJNA702448 (0,20) e PRJEB59875 (0,11, p = 0,06). Não há efeito em
   PRJNA1021161, PRJNA564156, PRJNA630025 e PRJNA932786.
4. **Plástico × sem plástico quase não é previsível** a partir dos gêneros (Random Forest: 63 % misturando projetos, 61 % num projeto novo; acaso = 50 %).
   **Biodegradável × não biodegradável não generaliza** (38 % num projeto novo; acaso = 33 %).
5. **Diversidade alfa:** a queda aparece nos microcosmos (PLA e PET em PRJNA1155845, PBSA em PRJNA702448); os filmes de mulch no campo e o PE/PLA de PRJNA1021161 não mudam a diversidade
   (gráficos de médias por projeto, painel c). O modelo misto confirma efeito de `POLYMER_TYPE` e `BIODEGRADABLE` dentro do projeto (p < 0,05).
6. **Variáveis de solo não podem ser testadas como causa** com estes dados: todas são médias por sítio ou tratamento. O envfit mostra que pH, SOC e
   C/N se alinham com os eixos da PCoA (r² 0,30–0,47), mas isso reflete os locais. Para testá-las, seria preciso medir o solo por amostra.
7. **Rarefação estável:** coeficiente de variação mediano entre 10 rarefações < 1 % (riqueza, Shannon, Faith).

### Pontos para revisar na planilha
* 2 amostras de `TPS/polyester` (SRR10076379, SRR10076381) estão com `BIODEGRADABLE = NA`; as outras 42 estão como Biodegradable.

---

## Rodadas anteriores (29–30/09/2026)
O conteúdo abaixo é das rodadas anteriores (metadados corrigidos por script). O notebook dessa versão está em
`versoes_anteriores/analise_microbioma_plasticos_v1.ipynb`; as comparações para artigo continuam em `analise_v2_comparacoes.ipynb`.

> ✅ **Versão atualizada com os metadados corrigidos** (ver [`CORRECOES_METADADOS.md`](CORRECOES_METADADOS.md)).
> Este relatório cobre **483 amostras de solo, rizosfera e plastisfera de campo**. As 24 amostras de intestino de *E. crypticus* e as 46 culturas de enriquecimento
> estão analisadas em [`analise_v2_comparacoes.ipynb`](analise_v2_comparacoes.ipynb). Os temas com potencial de artigo estão em [`TOP10_COMPARACOES_ARTIGO.md`](TOP10_COMPARACOES_ARTIGO.md).

---

## 1. Principais conclusões

1. **O estudo de origem domina a variação da comunidade; o plástico tem efeito pequeno.**
   Na PERMANOVA global (Bray–Curtis, nível de gênero), a região do 16S explica 11,6 % da variação e o BioProject mais 50,5 %. Depois deles, a fração explica 1,1 % e a classe do tratamento (controle, papel, biodegradável ou não biodegradável) **0,5 %** (p = 0,004). Com permutações restritas a dentro de cada projeto, o efeito do tratamento continua significativo (R² = 0,5 %, p = 0,002).
   → Comparações entre estudos precisam controlar o projeto.

2. **O plástico no solo não altera a diversidade alfa de forma consistente, mas os biodegradáveis reduzem a uniformidade.**
   A meta-análise compara plástico e controle dentro da mesma fração, em 8 estratos:
   - Riqueza: g = −0,16 [−0,74; 0,43], p = 0,60
   - Shannon: g = 0,06, p = 0,86
   - Faith PD: g = −0,18, p = 0,47

   A heterogeneidade é alta (I² de 67–81 %), com efeitos em direções opostas. O plástico **reduz** a diversidade nos microcosmos (PRJNA1155845 g ≈ −1,4; PRJNA702448 g ≈ −1,4) e a **aumenta** no campo (milho g = +2,4; duna g = +0,9). No modelo misto, os **biodegradáveis reduzem o Shannon (−0,33 DP, p = 0,0001), a equitabilidade (p = 0,0004) e a riqueza (p = 0,045)**. Os não biodegradáveis não têm efeito significativo (Shannon p = 0,07).

3. **A plastisfera é um habitat distinto, e isso se repete entre estudos.**
   Nos EUA (2016-09), a plastisfera tem riqueza de **587 ASVs contra 1.673 no solo** (−65 %) e Shannon de 4,7 contra 6,7 (p ≈ 10⁻¹²), e 384 de 512 gêneros diferem. Em 4 desenhos independentes (TN, WA e PBSA com e sem N), o R² plastisfera × solo vai de 0,33 a 0,57. Há um **núcleo de 17 gêneros enriquecidos** e **52 depletados** em ≥ 3 desenhos.
   - **Enriquecidos:** *Stenotrophomonas*, *Rhodococcus*, *Pseudomonas*, *Dyadobacter*, *Neorhizobium*, *Brevundimonas*, *Bosea*, *Caulobacter*, *Roseomonas*, Alcaligenaceae…
   - **Depletados:** oligotróficos (*Ca.* Udaeobacter, RB41, Vicinamibacteraceae, Rokubacteriales) e **nitrificantes**. A guilda nitrificante tem mediana de 1,2 % no solo e 0,02 % na plastisfera.
   - **Patescibacteria (Saccharimonadia):** 12–20 % na plastisfera dos EUA, contra cerca de 3 % no solo.
   - Exceção: em PRJNA630025 (Alpes/Ártico), não há diferença entre as frações, e a anotação da fração desse projeto não pôde ser verificada.

4. **Poucos gêneros respondem ao plástico de forma consistente no solo bulk.** Na comparação plástico × controle, 11 de 538 gêneros têm q < 0,05, todos com |ΔCLR| < 0,7.
   - ↓ com plástico: Ellin6055, AKYG587, FFCH7168, *Skermanella*, *Solirubrobacter*, Subgroup_25, *Nakamurella*, *Terrimonas*.
   - ↑ com plástico: *Janthinobacterium*, Obscuribacteraceae e o clado "27F-1492R" (Myxococcota).
   - Os degradadores clássicos (*Pseudomonas*, *Rhodococcus*…) sobem **só na plastisfera** (ΔCLR de 3 a 5). O efeito do plástico é **local**.

5. **O efeito do polímero depende do desenho experimental.** Resultados por projeto:

   | Projeto | Tratamento | R² polímero (BC) | p | Observação |
   |---|---|---|---|---|
   | PRJNA1155845 (microcosmo, solo) | PLA, PET e glifosato | **0,83** | 0,001 | PLA domina: *Lysobacter* chega a 39 % e a riqueza cai 68 %. Glifosato R² 0,02 (p = 0,17); interação polímero × glifosato no Shannon. |
   | PRJNA1054347 (mulch de milho) | PE, PBAT | **0,16** | 0,001 | Efeito maior no solo bulk (R² 0,30) que na rizosfera (0,18); interação p = 0,015. |
   | PRJNA631499 (plastisfera de campo) | 5 filmes | **0,16** | 0,001 | O sítio pesa mais (0,35). |
   | PRJNA702448 (Alemanha) | PBSA | 0,08 | 0,003 | Interação N × PBSA (R² 0,17): com N, o efeito do PBSA dobra. |
   | PRJEB59875 (duna, rizosfera) | Mater-Bi, HDPE | 0,10 / 0,16 (UniFrac) | 0,06 / 0,007 | Resultado limítrofe; a planta pesa tanto quanto o plástico. |
   | PRJNA564156 (bulk, 2 anos) | 5 filmes + papel + sem mulch | 0,03 | **0,005** | **Antes da correção era nulo.** Significativo só em Mount Vernon-WA nas coletas de setembro. O papel altera mais que os plásticos. |
   | PRJNA630025 (Alpes/Ártico) | PE, PBAT, PLA | 0,04 | 0,08 | Sítio R² 0,64. Anotação a confirmar. |
   | PRJNA1021161 (microcosmo) | PE/PLA, dose, fotoenvelhecimento, tempo | 0,02 | 0,32 | Só o PE fotoenvelhecido por 5 dias difere (R² 0,03–0,05; Shannon −0,38, p = 0,005). |
   | PRJNA932786 (mesocosmo) | PE, PBAT | 0,18 | 0,43 | n = 12, sem poder estatístico. |

6. **Biodegradável × não biodegradável.** A comparação direta dentro de 8 estratos dá g de Shannon = 0,00 (p = 1,0, I² = 79 %). Só o microcosmo PLA × PET (PRJNA1155845) mostra diferença grande. Contra o controle, só os biodegradáveis reduzem a diversidade no modelo misto. A mensagem é que **o efeito depende de formato, dose, planta e manejo, mais do que da biodegradabilidade**.

7. **As variáveis de solo e clima não podem ser separadas do estudo.** Usando os centróides dos cerca de 10 locais, o PC3 se correlaciona com C/N (ρ = −0,85), SOC (ρ = −0,74), pH (ρ = 0,64) e K (ρ = 0,89), todos com p < 0,05. O resultado é **apenas exploratório**.

---

## 1b. Análises adicionais (seção 9 do notebook): t‑SNE, modelos lineares, heatmaps, ISA e db‑RDA

| Análise | Resultado principal |
|---|---|
| **t‑SNE** (Bray–Curtis) | As amostras se agrupam **por projeto**. Isso se mantém nas perplexidades 10, 30 e 50. A única separação clara além do projeto é **plastisfera × solo** (EUA). Controle, biodegradável e não biodegradável ficam misturados dentro de cada projeto. Ver `figuras/09_tsne_*.png`. |
| **Modelo linear misto (alfa)** | Com a interação classe × fração, **os dois tipos de plástico reduzem a diversidade no solo bulk**. Biodegradável: Shannon −0,42 DP (p < 0,001), riqueza −0,20 (p = 0,007), Faith −0,21 (p = 0,012). Não biodegradável: Shannon −0,23 DP (p = 0,02), riqueza −0,16 (p = 0,049). **Na rizosfera, o efeito some**: a interação é positiva (Shannon +0,57, p = 0,012). Isso confirma que a rizosfera "tampona" o plástico. A ANOVA com projeto fixo dá o mesmo resultado (CLASSE no Shannon: p = 0,0003). |
| **Modelo linear por gênero** (CLR ~ classe + estrato) | Biodegradável × controle: 10 de 530 gêneros com q < 0,05. Perdem abundância *Adhaeribacter*, *Terrimonas*, *Paenibacillus*, S085, JG30‑KF‑CM66 e RB41; ganham *Nitrolancea*, *Cutibacterium* e *Escherichia‑Shigella*. Estes dois últimos são **prováveis contaminantes de kit/manipulação** e não devem ser interpretados. Não biodegradável × controle: 0 gêneros. |
| **Heatmaps** | `09_heatmap_R2_permanova.png`: R² por projeto × fator. O plástico só domina em PRJNA1155845; nos demais, sítio, N e fração pesam mais. `09_heatmap_generos_chave.png`: os gêneros do núcleo da plastisfera separam claramente a plastisfera dos demais compartimentos. |
| **ISA (IndVal.g)** | **Compartimento:** 354 indicadores, 99 da plastisfera e 255 do solo. Na plastisfera: *Pseudomonas* (IndVal 0,91), *Massilia*, *Rhodococcus*, Microbacteriaceae, **TM7a e LWQ8 (Patescibacteria)**, *Brevundimonas* e *Caulobacter*. No solo: SC‑I‑84, KD4‑96, *Gaiella*, TK10, Rokubacteriales e RB41. **Classe de plástico no solo:** nenhum indicador significativo. **Polímero na plastisfera:** 96 dos 105 indicadores são do **PE**, e são taxa típicos de solo (*Bryobacter*, *Ca.* Udaeobacter, Ellin6067, *Bacillus*). Ou seja, **a plastisfera do PE se parece com o solo**, enquanto a dos biodegradáveis é mais seletiva. Isso é coerente com a riqueza 44 % maior no PE. |
| **db‑RDA parcial global** (Bray–Curtis, gênero; `Condition(projeto)`) | O projeto remove 60 % da inércia. Do que sobra, fração + classe explicam 1,7 % (p = 0,005): fração 1,0 % e classe 0,55 %, ambas com p = 0,005. |
| **db‑RDA ambiental** | pH, SOC, C/N, chuva e temperatura explicam 45 % (p = 0,005). Mas os **VIF vão de 39 a 390**: as variáveis são colineares e constantes dentro do projeto. Esse R² é, na prática, o efeito do local. **Não interpretar como causal.** |
| **db‑RDA por projeto** (ASV) | Os resultados batem com a PERMANOVA. PRJNA1155845: R² 0,84 (CAP1 = 79 %, PLA isolado). PRJNA702448: 0,52 (N 0,19, fração 0,13, PBSA 0,08). PRJNA1054347: 0,27. PRJNA631499: polímero 0,16 (PE separado dos biodegradáveis no CAP1). PRJNA564156: polímero 0,03 (p = 0,002, com sítio e coleta removidos). PRJNA1021161: 0,07, só o tempo é significativo. |

Tabelas: `tabelas/09_*.csv`. Figuras: `figuras/09_*.png`.

---

## 2. Composição geral

Filos dominantes (média das 483 amostras): Proteobacteria 25,9 %, Acidobacteriota 13,5 %, Actinobacteriota 12,1 %, Chloroflexi 9,9 %, Firmicutes 8,4 %, Bacteroidota 6,9 %, Planctomycetota 6,3 %, Patescibacteria 3,8 % e Verrucomicrobiota 3,7 %. Esse é um perfil típico de solo agrícola.
A plastisfera tem mais Proteobacteria e Actinobacteriota copiotróficas e menos Acidobacteriota, Verrucomicrobiota e Methylomirabilota. No desenho dos EUA (2016-09), do bulk para a plastisfera: Proteobacteria passa de 17 % para 34 %, Actinobacteriota de 15 % para 28 % e **Patescibacteria de 3 % para 15 %**. No sentido oposto, Acidobacteriota cai de 18 % para 0,4 %, Chloroflexi de 19 % para 3 % e Planctomycetota de 11 % para 0,7 %. Ver [`figuras/03_*`](figuras/).

---

## 3. Metadados

Todas as correções (feitas pela comparação com NCBI/ENA e com os artigos) estão em [`CORRECOES_METADADOS.md`](CORRECOES_METADADOS.md) e em `correcoes_planilha.tsv`. Esta análise usa `meta_corrigida.tsv`.
Pendentes de confirmação: a fração em PRJNA630025, BM5/BM6 em PRJNA1054347 e o que significa "Weedguard" (tratado como mulch de papel).

---

## 4. Limitações

- **Efeito de lote:** região (V4 × V3-V4), primers, plataforma, solo e desenho mudam juntos com o projeto. O único jeito honesto de testar o efeito do plástico é **dentro** de cada estudo, e foi isso que foi feito.
- **Controles:** 7 dos 9 projetos têm controle sem plástico (PRJNA630025 e PRJNA631499 não têm). As comparações plástico × controle são feitas dentro da mesma fração (8 estratos).
- **Rarefação** em 12.000 leituras (mínimo do conjunto). A abundância diferencial usa contagens brutas com CLR.
- **Níveis taxonômicos:** "(NC)" indica gênero não classificado, rotulado pelo nível mais baixo disponível. Rótulos como "27F-1492R", "AKYG587" e "I-8" são nomes de clados não cultivados do SILVA.
- **A PERMANOVA sequencial** depende da ordem dos termos. Os termos do desenho foram colocados antes do polímero, o que torna o teste do polímero conservador.

---

## 5. Próximos passos sugeridos

1. Confirmar as pendências da seção 3 (principalmente a fração em PRJNA630025) e aplicar as correções na planilha online.
2. Incluir PRJNA1079663 e PRJNA853344, que estão "DONE" na planilha mas fora do conjunto.
3. Fazer uma análise **funcional** (PICRUSt2 ou FAPROTAX), com foco no ciclo do N (nitrificantes depletados na plastisfera) e em genes de degradação (esterases, cutinases, PETase).
4. Para robustez da abundância diferencial, aplicar ANCOM-BC2 ou MaAsLin2 com projeto como efeito aleatório e comparar com a meta-análise CLR usada aqui.
5. Fazer redes de coocorrência plastisfera × bulk (desenho dos EUA, n = 72).

---

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `analise_microbioma_plasticos.ipynb` | Notebook executado, com todas as figuras e tabelas |
| `build_notebook.py` | Gera o notebook (edite aqui e execute de novo) |
| `analise_v2_comparacoes.ipynb` / `build_notebook_v2.py` / `util_analise.py` | Comparações candidatas a artigo (todas as 553 amostras) |
| `TOP10_COMPARACOES_ARTIGO.md` | Ranking dos 10 temas com potencial de artigo |
| `gerar_correcoes.py` → `preparar_metadados.py` → `meta_corrigida.tsv` | Correção dos metadados |
| `.venv/` | Ambiente Python (pandas, scikit-bio, statsmodels, seaborn…) |
| `tabelas/01–08_*.csv` | Resumos por projeto, alfa, meta-análise, PERMANOVAs, abundância diferencial, plastisfera, degradadores e ambiente |
| `figuras/01–07_*.png` | Desenho amostral, QC, composição, alfa, PCoA, forest plots, projetos específicos |

Para executar de novo:

```bash
cd analise_setembro
.venv/bin/python gerar_correcoes.py && .venv/bin/python preparar_metadados.py
.venv/bin/python build_notebook.py && .venv/bin/jupyter nbconvert --to notebook --execute --inplace analise_microbioma_plasticos.ipynb
.venv/bin/python build_notebook_v2.py && .venv/bin/jupyter nbconvert --to notebook --execute --inplace analise_v2_comparacoes.ipynb
```
