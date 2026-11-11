"""Gera REVISAO_ARTIGOS.md a partir de revisao_artigos_correcoes.tsv (rodar depois de revisar_planilha_artigos.py)."""
import pandas as pd

L = pd.read_csv('revisao_artigos_correcoes.tsv', sep='\t')
cur = pd.read_excel('../results/dados_complementares/Database_Plastic-Soil.xlsx', 'Metadata - Bacteria')
from revisar_planilha_artigos import FONTES  # noqa: E402  (reexecuta o script; saídas idênticas)

COLS = [c for c in cur.columns if c not in ('BIOPROJECT', 'SAMPLE', 'SAMPLE_NAME', 'status', 'who', 'where')]
GEN = {'POLYMER_AROMATIC_RINGS', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)', 'CHEMICAL_COMPOSITION', 'HARDNESS',
       'DEGRADABILITY_RATE', 'PLASTIC_GROUPPING'}
# colunas conferidas e corretas (valor bate com artigo/suplemento/NCBI)
OK = {
 'PRJNA564156': '16S_REGION POLYMER_TYPE POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT BIODEGRADABLE SOIL_FRACTION SAMPLING_DEPTH SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE TILLAGE COUNTRY YEAR_PERIOD pH',
 'PRJNA631499': '16S_REGION POLYMER_TYPE POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT BIODEGRADABLE SOIL_FRACTION SAMPLING_DEPTH CULTIVAR SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE TILLAGE COUNTRY YEAR_PERIOD SAMPLING_SEASON SOIL_TEMPERATURE(C)',
 'PRJNA630025': '16S_REGION POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT SAMPLING_DEPTH EXPERIMENT_TYPE COUNTRY YEAR_PERIOD SOIL_TEMPERATURE(C) BIODEGRADABLE',
 'PRJNA702448': 'POLYMER_TYPE POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT BIODEGRADABLE CULTIVAR SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE FARM_SYSTEM FERTILIZATION COUNTRY CLIMATE SOC(g/kg) C/N DENSITY_(g/cm³)',
 'PRJNA1054347': '16S_REGION POLYMER_TYPE BIODEGRADABLE SOIL_FRACTION SAMPLING_DEPTH CULTIVAR SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE FARM_SYSTEM FERTILIZATION COUNTRY CLIMATE ANNUAL_RAINFALL(mm) AVG_ANNUAL_TEMPERATURE YEAR_PERIOD SAMPLING_SEASON SOIL_TEMPERATURE(C) WATER_CONTENT(%) SOC(g/kg) TN(g/kg) C/N pH DOC(mg/kg) DIN(mg/kg) NH4(mg/kg) NO3(mg/kg) AP(mg/kg) AK(mg/kg)',
 'PRJNA1021161': '16S_REGION POLYMER_TYPE POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT BIODEGRADABLE SOIL_FRACTION SAMPLING_DEPTH EXPERIMENT_TYPE ENV_TYPE COUNTRY SOC(g/kg) TN(g/kg) C/N pH AP(mg/kg) AK(mg/kg)',
 'PRJNA1155845': '16S_REGION POLYMER_TYPE POLYMER_SIZE POLYMER_SIZE_METRIC POLYMER_FORMAT BIODEGRADABLE SAMPLING_DEPTH EXPERIMENT_TYPE COUNTRY YEAR_PERIOD SOIL_TEMPERATURE(C) WATER_CONTENT(%) NH4(mg/kg) NO3(mg/kg) AP(mg/kg)',
 'PRJEB59875': '16S_REGION POLYMER_TYPE POLYMER_FORMAT BIODEGRADABLE SAMPLING_DEPTH SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE COUNTRY YEAR_PERIOD SAMPLING_SEASON pH',
 'PRJNA932786': 'POLYMER_TYPE POLYMER_FORMAT BIODEGRADABLE SOIL_FRACTION SOIL_TYPE EXPERIMENT_TYPE COUNTRY WATER_CONTENT(%) pH',
 'PRJNA853344': '16S_REGION POLYMER_TYPE BIODEGRADABLE CULTIVAR SOIL_TYPE EXPERIMENT_TYPE ENV_TYPE FARM_SYSTEM FERTILIZATION COUNTRY CLIMATE ANNUAL_RAINFALL(mm) AVG_ANNUAL_TEMPERATURE',
}
OK = {k: set(v.split()) for k, v in OK.items()}
PRIO = ['ERRO', 'PREENCHER', 'SUGESTÃO', 'PADRONIZAÇÃO']
SYM = {'ERRO': '✗', 'PREENCHER': '+', 'SUGESTÃO': '~', 'PADRONIZAÇÃO': 's'}

projs = ['PRJNA564156', 'PRJNA631499', 'PRJNA630025', 'PRJNA702448', 'PRJNA1054347', 'PRJNA1021161', 'PRJNA1155845',
         'PRJEB59875', 'PRJNA932786', 'PRJNA853344']
M = pd.DataFrame('', index=COLS, columns=projs)
cel = L[L.TIPO != 'REMOVER']
for pj in projs:
    d = cur[cur.BIOPROJECT == pj]
    for col in COLS:
        t = cel[(cel.BIOPROJECT == pj) & (cel.COLUNA == col)].TIPO.unique()
        tipo = next((x for x in PRIO if x in t), None)
        if tipo: M.at[col, pj] = SYM[tipo]
        elif col in OK[pj]: M.at[col, pj] = '✓'
        elif d[col].isna().all(): M.at[col, pj] = '—'
        elif col in GEN: M.at[col, pj] = 'R'
        else: M.at[col, pj] = '?'

w = []
A = w.append
A('# Revisão da aba "Metadata - Bacteria" contra os artigos e o NCBI\n')
A('Escrito em 15/10/2026. A base é a planilha **baixada hoje** (`Database_Plastic-Soil.xlsx`), comparada campo a campo com os artigos e suplementos '
  'em `artigos/` e com os metadados do NCBI/ENA (`dados_ncbi/`).\n')
A('**Arquivos gerados**')
A('* `revisao_artigos_correcoes.tsv`: uma linha por célula, com valor atual → correto, tipo e fonte (artigo, tabela ou trecho citado). É o arquivo para filtrar e corrigir a planilha online.')
A('* `planilha_bacteria_revisada.tsv`: a aba inteira com todas as correções aplicadas, mais a coluna `ACAO` (linhas a remover).')
A('* `revisar_planilha_artigos.py`: o script com cada regra e sua fonte, para reproduzir ou ajustar.\n')
A('> **Versão final para subir na planilha online:** `planilha_bacteria_padronizada.xlsx` (unidades, números e NA padronizados) e `correcoes_finais.tsv` (todas as diferenças). Ver `PADRONIZACAO.md`.\n')

n_rem = (L.TIPO == 'REMOVER').sum()
A('## 1. Resumo\n')
A(f'* **{len(cel)} células** em {cel.SAMPLE.nunique()} amostras, e **{n_rem} linhas a remover** (runs de ITS).')
tab = cel.groupby(['BIOPROJECT', 'TIPO']).size().unstack(fill_value=0).reindex(projs).fillna(0).astype(int)
tab['REMOVER (linhas)'] = L[L.TIPO == 'REMOVER'].groupby('BIOPROJECT').size().reindex(projs).fillna(0).astype(int)
A('\n| Projeto | ' + ' | '.join(tab.columns) + ' |'); A('|---|' + '---|' * len(tab.columns))
for pj, r in tab.iterrows(): A(f'| {pj} | ' + ' | '.join(str(v) for v in r) + ' |')
A('\n**Tipos:** **ERRO** = contradiz o artigo ou o NCBI · **PREENCHER** = estava vazio e o valor está no artigo · '
  '**SUGESTÃO** = decisão do grupo (valor mais preciso, mas muda a categoria) · **PADRONIZAÇÃO** = mesmo significado, grafia diferente · '
  '**REMOVER** = a linha não é 16S.\n')

A('## 2. Erros mais importantes (mudam a análise)\n')
A('| Projeto | O que estava errado | Correção | Fonte |')
A('|---|---|---|---|')
for row in [
 ('PRJNA564156', 'Clima, chuva, temperatura e **toda a química do solo** (SOC, TN, C/N, DOC, DIN, NH4, NO3, AP, AK) deslocados: 25 amostras de TN com valores de WA e 25 de WA com valores de TN. pH trocado em 3 amostras.', 'Valores atribuídos pelo sítio real (NCBI `geo_loc_name`). A química do solo (fonte: Sintim et al. 2019) é de TN; WA fica vazio.', 'NCBI + Front. Microbiol. (pH)'),
 ('PRJNA631499', '48 **culturas de enriquecimento** de laboratório marcadas como plastisfera. Temperatura do solo em TN = **46250**.', '`SOIL_FRACTION` = Enrichment_culture (30 °C, 3–6 semanas). Temperatura em TN = 16,8 °C.', 'Front. Microbiol. métodos; Data Sheet 1, Tabela S2'),
 ('PRJNA630025', 'SOC, TN, C/N, pH e chuva **não batem** com a Tabela 1 do artigo (ex.: SOC 119 g/kg × 1,4 g/kg; pH 4,4 × 6,5). Fração errada em 6 amostras de Barba Peider. 36 runs de ITS.', 'Valores da Tabela 1. Fração pelo prefixo P/S. Remover os `*_fung`.', 'Rüthi et al. 2020, Tabela 1 e Fig. S2'),
 ('PRJNA702448', '**Região 16S = V4** (515F/806R), não V3‑V4. Umidade 60 % (real 17,5 %), temperatura 20 °C (real 22 °C), chuva 404 mm (real 489–525 mm), temperatura média 9,8 °C (real 8,9–9,7 °C). Controles com propriedades de PBSA. pH e TN vazios.', 'Corrigido; pH e TN preenchidos por tratamento.', 'Tanunchai et al. 2021; Guliyev et al. 2022; d1em00426c'),
 ('PRJNA1155845', '**SOC e DIN trocados entre tratamentos** em 28 de 48 amostras. **24 amostras são intestino** de *E. crypticus*. 48 runs de ITS.', 'SOC = SOM × 10/1,724 e DIN = NH4 + NO3 do tratamento (Tabela S1). `SOIL_FRACTION` = Gut. Remover SRR30519*.', 'Yang et al. 2025, Tabela S1; NCBI'),
 ('PRJEB59875', '14 amostras como plastisfera; 37–39 EPE como *Sporobolus*.', 'Todas são **rizosfera**. 35–39 EPE = *Thinopyrum junceum*.', 'Menicagli et al. 2023, métodos'),
 ('PRJNA1021161', 'Tipo de solo e clima (Cumulic Haplustolls, 584 mm, 9,1 °C) copiados de **outro estudo** (Changwu, PRJNA1054347). Este é de Yangling.', 'Esvaziados: o artigo não informa.', 'Qiu et al. 2024, métodos'),
 ('PRJNA932786', 'SOC = 29,5 g/kg, mas esse valor é **matéria orgânica**.', 'SOC ≈ 17,1 g/kg (29,5 / 1,724).', 'Adhikari et al., SI Tabela S1'),
 ('PRJNA1054347', 'Temperatura do solo da rizosfera copiada do bulk. M4 com profundidade 0.', 'Rizosfera vazia (não medida). M4 = 0–20.', 'Zhang et al. 2024, Tabela S2'),
 ('Polímeros (todos)', 'PE de baixa densidade (LDPE/LLDPE) com densidade de HDPE (0,94–0,97) ou digitada como "0,94-0,167". `TPS/polyester` sem nenhuma propriedade.', 'LDPE/LLDPE = 0,91–0,94. Naturecycle = Biodegradable.', 'PeerJ Tabela 1; Rüthi; Adhikari'),
]:
    A('| ' + ' | '.join(row) + ' |')

A('\n## 3. Matriz de verificação (todas as colunas × projetos)\n')
A('**Legenda:** ✓ conferido e correto · ✗ corrigido (erro) · + preenchido com valor do artigo · ~ sugestão · s padronização de grafia · '
  '**?** não verificável (o valor não está nos arquivos fornecidos) · **R** propriedade genérica do polímero (referência de literatura, não do artigo) · — vazio / não se aplica\n')
A('| Coluna | ' + ' | '.join(p.replace('PRJNA', 'NA').replace('PRJEB', 'EB') for p in projs) + ' |')
A('|---|' + ':-:|' * len(projs))
for col, r in M.iterrows():
    A(f'| `{col}` | ' + ' | '.join(r) + ' |')

A('\n## 4. O que não pôde ser verificado e por quê\n')
A('| Projeto | Campos "?" | Motivo / o que falta |')
A('|---|---|---|')
for pj in projs:
    q = [c for c in COLS if M.at[c, pj] == '?']
    if not q: continue
    motivo = {
     'PRJNA564156': 'Química do solo, chuva e temperatura vêm de **Sintim et al. 2019**, que não está na pasta. Cor do PE (16 de 24 como "Black") não aparece no artigo. A fertilização também está em Sintim/Ghimire.',
     'PRJNA631499': 'Mesma fonte (Sintim et al. 2019). Chuva e temperatura (1260/830 mm; 14,4/9,9 °C) não aparecem: a Tabela S3 do PeerJ dá os valores medidos (TN 1313/866 mm e 15,8 °C; WA 885/945 mm e 11,6/11,5 °C).',
     'PRJNA630025': 'Polímero por amostra: o NCBI e os suplementos não ligam amostra → polímero. Fração em Villum (`VPI*`): sem prefixo P/S. Temperatura média: o artigo só dá a do **solo** (−1,8 / −5,4 °C). Tipo de solo e umidade não constam.',
     'PRJNA702448': 'Profundidade (0–5) e ano (2019/2020) não aparecem nos três artigos.',
     'PRJNA1021161': 'Clima e tipo de solo de Yangling não são informados. Umidade foi mantida em "60 % da capacidade de campo" (não é % gravimétrica).',
     'PRJNA1155845': 'Tipo de solo, clima (~1450 mm, ~17 °C) e estação não constam no artigo (local: Ningbo, Zhejiang).',
     'PRJEB59875': 'Chuva (~910 mm) e temperatura (~14,6 °C) não constam (provavelmente em Menicagli et al. 2023a, que não está na pasta).',
     'PRJNA932786': '**O artigo principal não está na pasta** (só o Supporting Information). Faltam profundidade, tamanho da partícula (250 µm), região 16S e clima.',
     'PRJNA853344': '**O artigo principal não está na pasta** (só o SI). Fora do `conjunto_alex` (2 runs).',
     'PRJNA1054347': 'Cor do filme ("Black") não é mencionada.',
    }.get(pj, '')
    A(f'| {pj} | {", ".join("`" + x + "`" for x in q)} | {motivo} |')

A('\n## 5. Decisões para o grupo (tipo SUGESTÃO)\n')
A('1. **Tipo de PE**: os artigos especificam LLDPE (PRJNA564156/631499), LDPE (PRJNA630025/932786) e HDPE (PRJEB59875). Sugiro usar o tipo exato em `POLYMER_TYPE`. Se o grupo preferir agrupar, mantenha "PE", mas corrija a densidade de qualquer forma.')
A('2. **Weedguard (PRJNA564156)**: é papel de celulose (controle positivo do estudo). Sugestão: `POLYMER_TYPE` = "Cellulose paper" em vez de vazio, para não misturar com o "sem mulch".')
A('3. **pH em PRJNA631499**: a Tabela S2 dá o pH exatamente na coleta destas amostras (outono de 2016). Sugiro usá-lo no lugar da média do estudo.')
A('4. **PRJNA1155845**: `TILLAGE` = "No" num microcosmo de laboratório. Sugiro deixar vazio (não se aplica).')
A('5. **Formato numérico**: a planilha mistura vírgula e ponto decimal ("15,14" e "15.14"), além de textos em colunas numéricas ("~910", "6,03 ± 0,36", "489–525"). Para análise, o ideal é colunas numéricas só com número (com ponto) e uma coluna separada para desvio ou faixa.\n')

A('## 6. Artigos que faltam na pasta\n')
A('* **PRJNA932786**: artigo principal de Adhikari et al. (ACS Agric. Sci. Technol., DOI do suplementar as2c00333).')
A('* **PRJNA853344**: artigo principal de Purahong et al. 2021 (ES&T, es1c02695).')
A('* **Sintim et al. 2019** (Sci. Total Environ.): fonte da química do solo e do clima de PRJNA564156/631499.')
A('* **Menicagli et al. 2023a**: clima do local de PRJEB59875.\n')

A('## 7. Fontes usadas por projeto\n')
for pj in projs: A(f'* **{pj}**: {FONTES[pj]}')
open('REVISAO_ARTIGOS.md', 'w').write('\n'.join(w) + '\n')
print(M.to_string())
