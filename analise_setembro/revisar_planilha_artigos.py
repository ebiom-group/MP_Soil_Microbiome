"""Revisão campo a campo da aba 'Metadata - Bacteria' contra os artigos/suplementos (pasta artigos/) e o NCBI/ENA.

Entrada : ../results/dados_complementares/Database_Plastic-Soil.xlsx (versão baixada em 15/10/2026)
          dados_ncbi/runs_biosample.tsv
Saídas  : revisao_artigos_correcoes.tsv      — uma linha por célula (valor atual → correto, tipo, fonte)
          planilha_bacteria_revisada.tsv     — aba inteira com as correções aplicadas + coluna ACAO
          REVISAO_ARTIGOS.md                 — relatório (gerado no fim)

Tipos: ERRO (contradiz artigo/NCBI) · PREENCHER (vazio, valor está no artigo) · SUGESTÃO (decisão do grupo)
       · PADRONIZAÇÃO (vocabulário/formato) · REMOVER (linha não é 16S)
"""
import re
import numpy as np
import pandas as pd

X = '../results/dados_complementares/Database_Plastic-Soil.xlsx'
orig = pd.read_excel(X, 'Metadata - Bacteria')
c = orig.copy().astype(object).set_index('SAMPLE', drop=False)
o = orig.set_index('SAMPLE')
ncbi = pd.read_csv('dados_ncbi/runs_biosample.tsv', sep='\t').set_index('run_accession').reindex(c.index)
c['ACAO'] = pd.Series(np.nan, index=c.index, dtype=object)
LOG = []

FONTES = {
    'PRJNA564156': 'Bandopadhyay et al. 2020, PeerJ 8:e9015 (+ Supplemental R1)',
    'PRJNA631499': 'Bandopadhyay et al. 2020, Front. Microbiol. 11:587074 (+ Data Sheet 1)',
    'PRJNA630025': 'Rüthi et al. 2020, Front. Environ. Sci. 8:562263 (Tabela 1; Data Sheets 1–5)',
    'PRJNA702448': 'Tanunchai et al. 2021, Environ. Sci. Eur. 33:105; Guliyev et al. 2022, Polymers 14:2801; suplementar d1em00426c',
    'PRJNA1054347': 'Zhang et al. 2024, Sci. Total Environ. 933:172874 (+ mmc1: Texto S1, Tabela S2)',
    'PRJNA1021161': 'Qiu et al. 2024, ISME J. 18:wrad017 (+ Supporting Information, Texto S1)',
    'PRJNA1155845': 'Yang et al. 2025, J. Hazard. Mater. 489:137676 (+ mmc2: Tabela S1)',
    'PRJEB59875': 'Menicagli et al. 2023, Sci. Total Environ. 880:163293',
    'PRJNA932786': 'Adhikari et al. (ACS Agric. Sci. Technol., as2c00333) — só o Supporting Information (Tabela S1)',
    'PRJNA853344': 'Purahong et al. 2021, Environ. Sci. Technol. (es1c02695) — só o Supporting Information',
}


def same(a, b):
    if pd.isna(a) and pd.isna(b): return True
    if pd.isna(a) or pd.isna(b): return False
    fa, fb = (str(x).replace(',', '.').strip() for x in (a, b))
    try: return abs(float(fa) - float(fb)) < 1e-9
    except ValueError: return fa == fb


def setv(idx, col, val, tipo, fonte):
    for i in ([idx] if isinstance(idx, str) else list(idx)):
        v = val(i) if callable(val) else val
        if same(c.at[i, col], v): continue
        LOG.append(dict(SAMPLE=i, BIOPROJECT=c.at[i, 'BIOPROJECT'], SAMPLE_NAME=c.at[i, 'SAMPLE_NAME'], COLUNA=col,
                        VALOR_ATUAL=o.at[i, col], VALOR_CORRETO=v, TIPO=tipo, FONTE=fonte))
        c.at[i, col] = v


P = lambda proj: c.index[c.BIOPROJECT == proj]
n = c.SAMPLE_NAME.astype(str)
PROPS = ['POLYMER_AROMATIC_RINGS', 'BIODEGRADABLE', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)', 'CHEMICAL_COMPOSITION',
         'HARDNESS', 'DEGRADABILITY_RATE', 'PLASTIC_GROUPPING', 'POLYMER_COLOR', 'POLYMER_SIZE', 'POLYMER_SIZE_METRIC', 'POLYMER_FORMAT']

# =====================================================================================================================
# PRJNA564156 — solo bulk, Knoxville-TN × Mount Vernon-WA, 2015–2016
# =====================================================================================================================
p = P('PRJNA564156'); F = FONTES['PRJNA564156']
site = ncbi.loc[p, 'geo_loc_name'].str.contains('Knoxville').map({True: 'TN', False: 'WA'})
# bloco de valores por sítio da própria planilha (fonte original não está nos arquivos: Sintim et al. 2019)
bloco = {'TN': {'CLIMATE': 'Humid subtropical', 'ANNUAL_RAINFALL(mm)': '1260', 'AVG_ANNUAL_TEMPERATURE': '14,4', 'pH': '6,03 ± 0,36',
                'SOC(g/kg)': 23.32, 'TN(g/kg)': 1.54, 'C/N': '15,14', 'DOC(mg/kg)': 102.51, 'DIN(mg/kg)': '24,01',
                'NH4(mg/kg)': 4.15, 'NO3(mg/kg)': 19.86, 'AP(mg/kg)': 5.31, 'AK(mg/kg)': 78.44},
         'WA': {'CLIMATE': 'Mediterranean', 'ANNUAL_RAINFALL(mm)': '830', 'AVG_ANNUAL_TEMPERATURE': '9,9', 'pH': '6,24 ± 0,11',
                'SOC(g/kg)': np.nan, 'TN(g/kg)': np.nan, 'C/N': np.nan, 'DOC(mg/kg)': np.nan, 'DIN(mg/kg)': np.nan,
                'NH4(mg/kg)': np.nan, 'NO3(mg/kg)': np.nan, 'AP(mg/kg)': np.nan, 'AK(mg/kg)': np.nan}}
for col in bloco['TN']:
    setv(p, col, lambda i, col=col: bloco[site[i]][col], 'ERRO',
         'NCBI geo_loc_name: o bloco de valores de sítio estava na linha de outro local (clima/química de TN aplicados a WA e vice-versa); '
         'pH do sítio: Front. Microbiol. 11:587074 (TN 6,03 ± 0,36; WA 6,24 ± 0,11)')
setv(p, 'SAMPLING_SEASON', lambda i: 'Spring' if str(ncbi.at[i, 'collection_date']).endswith('-05') else 'Fall', 'PREENCHER',
     F + ': "collected … in the Spring (May) and Fall (September) of 2015 and 2016"')
setv(p, 'CULTIVAR', 'Cucurbita pepo', 'PADRONIZAÇÃO', F + ': "pie pumpkin (Cucurbita pepo)"; mesmo nome usado em PRJNA631499')
wg = p[ncbi.loc[p, 'title'].eq('Weedguard')]
setv(wg, 'POLYMER_TYPE', 'Cellulose paper', 'SUGESTÃO', F + ', Tabela 1: WeedGuardPlus = cellulose paper mulch (controle positivo, não é plástico)')
setv(wg, 'POLYMER_SIZE', 479, 'SUGESTÃO', F + ', Tabela 1: espessura 479 µm')
setv(wg, 'POLYMER_SIZE_METRIC', 'µm', 'SUGESTÃO', F + ', Tabela 1')
setv(wg, 'POLYMER_FORMAT', 'Film', 'SUGESTÃO', F + ', Tabela 1')
setv(wg, 'BIODEGRADABLE', 'Biodegradable', 'SUGESTÃO', F + ': "biodegradable cellulose paper mulch"')
nm = p[ncbi.loc[p, 'title'].eq('No Mulch')]
setv(nm, 'POLYMER_FORMAT', np.nan, 'ERRO', F + ': tratamento sem mulch não tem formato de polímero')
setv(nm, 'POLYMER_TYPE', 'NONE', 'PADRONIZAÇÃO', 'controles sem plástico = NONE (como nos demais projetos)')

# =====================================================================================================================
# PRJNA631499 — plastisfera de campo (2016-09) e culturas de enriquecimento (2016-07)
# =====================================================================================================================
p = P('PRJNA631499'); F = FONTES['PRJNA631499']
enr = p[ncbi.loc[p, 'isolation_source'].eq('enrichment culture')]
fld = p.difference(enr)
setv(enr, 'SOIL_FRACTION', 'Enrichment_culture', 'ERRO', 'NCBI isolation_source = "enrichment culture"; ' + F + ': culturas em meio M9 com filmes não intemperizados')
setv(enr, 'SOIL_TEMPERATURE(C)', 30, 'PREENCHER', F + ': "incubated … at 30 °C with shaking at 120 rpm" (temperatura de incubação)')
setv(enr, 'POLYMER_SIZE', '4 x 4', 'PREENCHER', F + ': filmes cortados em pedaços de 4 × 4 cm² (a espessura de cada filme continua na Tabela S1)')
setv(enr, 'POLYMER_SIZE_METRIC', 'cm', 'PREENCHER', F)
tn = fld[ncbi.loc[fld, 'geo_loc_name'].str.contains('Knoxville')]; wa = fld.difference(tn)
setv(tn, 'SOIL_TEMPERATURE(C)', 16.8, 'ERRO', F + ', Data Sheet 1 Tabela S2: temperatura média anual do solo em TN = 16,8 ± 0,18 °C (valor 46250 é erro de digitação/formatação)')
setv(tn, 'pH', '5,8 ± 0,08', 'SUGESTÃO', F + ', Tabela S2: pH no outono de 2016 (data destas amostras) = 5,8 ± 0,08; o 6,03 é a média do estudo')
setv(wa, 'pH', '5,54 ± 0,03', 'SUGESTÃO', F + ', Tabela S2: pH no outono de 2016 = 5,54 ± 0,03')

# =====================================================================================================================
# PRJNA630025 — mesocosmos, Barba Peider (Alpes) e Villum (Ártico)
# =====================================================================================================================
p = P('PRJNA630025'); F = FONTES['PRJNA630025']
fung = p[n[p].str.endswith('_fung')]
c.loc[fung, 'ACAO'] = 'REMOVER: run de ITS (fungos); pertence à aba Metadata - Fungi'
for i in fung: LOG.append(dict(SAMPLE=i, BIOPROJECT='PRJNA630025', SAMPLE_NAME=n[i], COLUNA='(linha inteira)', VALOR_ATUAL='presente',
                               VALOR_CORRETO='remover da aba Bacteria', TIPO='REMOVER', FONTE='ENA experiment_title: "DNA-Seq of fungal community"'))
bac = p.difference(fung)
ch = bac[c.loc[bac, 'COUNTRY'].eq('Switzerland')]; gl = bac.difference(ch)
T1 = F + ', Tabela 1'
for idx, vals in [(ch, {'SOC(g/kg)': 1.4, 'TN(g/kg)': '<0.2', 'C/N': np.nan, 'pH': 6.5, 'ANNUAL_RAINFALL(mm)': 1500}),
                  (gl, {'SOC(g/kg)': 24.7, 'TN(g/kg)': 2.5, 'C/N': 9.9, 'pH': 6.9, 'ANNUAL_RAINFALL(mm)': 188})]:
    nome = 'Barba Peider' if idx is ch else 'Villum'
    for col, v in vals.items():
        txt = {'SOC(g/kg)': 'C (%) × 10', 'TN(g/kg)': 'N (%) × 10', 'C/N': 'C/N = C%/N%', 'pH': 'pH [H2O]',
               'ANNUAL_RAINFALL(mm)': 'Annual precipitation'}[col]
        setv(idx, col, v, 'ERRO', f'{T1} ({nome}): {txt}' + (' — N < 0,02 % (abaixo do limite), C/N não calculável' if (col in ('TN(g/kg)', 'C/N') and idx is ch) else ''))
bp = ch  # Barba Peider: prefixo P = plastisfera, S = solo (Data Sheet 2, Fig. S2: "plastisphere (P) and bulk soil (S)")
setv(bp, 'SOIL_FRACTION', lambda i: 'Plastosphere' if n[i].startswith('P') else 'Bulk', 'ERRO',
     F + ', Data Sheet 2 (Fig. S2): "plastisphere (P) and bulk soil (S)" — prefixo do nome da biblioteca')

# =====================================================================================================================
# PRJNA702448 — microcosmo PBSA × (NH4)2SO4, solo de Bad Lauchstädt
# =====================================================================================================================
p = P('PRJNA702448'); F = FONTES['PRJNA702448']
setv(p, '16S_REGION', 'V4', 'ERRO', 'Tanunchai et al. 2021: "16S rRNA gene V4 region … primer pair 515F/806R"')
setv(p, 'SOIL_FRACTION', lambda i: 'Plastosphere' if n[i].startswith('P_') else 'Bulk', 'PREENCHER',
     'NCBI isolation_source (PBSA_plastic × soil); Tanunchai et al. 2021: PBSA × solo correspondente')
ctrl = p[n[p].str.startswith(('Control', 'Initial'))]
setv(ctrl, 'POLYMER_TYPE', 'NONE', 'PADRONIZAÇÃO', 'controle sem PBSA')
for col in ['BIODEGRADABLE', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)', 'CHEMICAL_COMPOSITION', 'HARDNESS', 'DEGRADABILITY_RATE', 'PLASTIC_GROUPPING']:
    setv(ctrl, col, np.nan, 'ERRO', 'controle sem plástico não deve ter propriedades de polímero')
grp = lambda i: ('initial' if n[i].startswith('Initial') else 'SN' if n[i].startswith('ControlSN') else 'S' if n[i].startswith('ControlS')
                 else 'PSN' if 'PSN' in n[i] else 'PS')
ph = {'initial': 7.5, 'S': 7.5, 'SN': 6.7, 'PS': 7.5, 'PSN': 6.3}
tnv = {'initial': np.nan, 'S': 1.9, 'SN': 4.6, 'PS': 1.9, 'PSN': 5.1}
setv(p, 'pH', lambda i: ph[grp(i)], 'PREENCHER', 'Tanunchai et al. 2021 (Resultados, Fig. S2a): pH inicial 7,5; controle e PS ≈ 7,5; control SN 6,7; PSN 6,3 '
     '(para amostras de plastisfera, pH do solo do tratamento)')
setv(p, 'TN(g/kg)', lambda i: tnv[grp(i)], 'PREENCHER', 'Guliyev et al. 2022 (Polymers, Fig. 3/texto): TN control S 0,19 %, PS 0,19 %, control SN 0,46 %, PSN 0,51 %')
setv(p, 'WATER_CONTENT(%)', 17.5, 'ERRO', 'Tanunchai et al. 2021: "soil water contents of all treatments at 17.5%" (= 50 % da capacidade de retenção)')
setv(p, 'SOIL_TEMPERATURE(C)', 22, 'ERRO', 'Tanunchai et al. 2021: "air temperature at 22 °C during the 90-day experiment"')
setv(p, 'ANNUAL_RAINFALL(mm)', '489–525', 'ERRO', 'suplementar d1em00426c (mesmo campo GCEF, Bad Lauchstädt): "average annual precipitations at 489 – 525 mm"')
setv(p, 'AVG_ANNUAL_TEMPERATURE', '8,9–9,7', 'ERRO', 'suplementar d1em00426c: "mean temperature at 8.9 – 9.7 °C"')

# =====================================================================================================================
# PRJNA1054347 — mulch PE × PBAT em milho, Changwu
# =====================================================================================================================
p = P('PRJNA1054347'); F = FONTES['PRJNA1054347']
setv(p[n[p].eq('M4')], 'SAMPLING_DEPTH', '0-20', 'ERRO', F + ': "five undisturbed soil cores from each plot (0–20 cm)"')
rz = p[c.loc[p, 'SOIL_FRACTION'].eq('Rhizosphere')]
setv(rz, 'SOIL_TEMPERATURE(C)', np.nan, 'ERRO', F + ', Tabela S2: temperatura do solo só foi medida no bulk (24,4/26,6/24,3); a planilha copiou o valor do bulk para a rizosfera')
setv(p, 'TILLAGE', 'Yes', 'PREENCHER', F + ': "The field was plowed before sowing"')
pl = p[c.loc[p, 'POLYMER_TYPE'].isin(['PE', 'PBAT'])]
setv(pl, 'POLYMER_SIZE', 10, 'PREENCHER', F + ': filmes "100 cm wide and 0.01 mm thick" (espessura)')
setv(pl, 'POLYMER_SIZE_METRIC', 'µm', 'PREENCHER', F)
setv(pl, 'POLYMER_FORMAT', 'Film', 'PREENCHER', F + ': film mulching')

# =====================================================================================================================
# PRJNA1021161 — microcosmo PE/PLA, Yangling
# =====================================================================================================================
p = P('PRJNA1021161'); F = FONTES['PRJNA1021161']
setv(p, 'SOIL_TYPE', np.nan, 'ERRO', F + ': solo de Yangling (34°20′N, 108°04′E); o artigo não informa a classificação — "Cumulic Haplustolls" é o solo de Changwu (PRJNA1054347)')
setv(p, 'ANNUAL_RAINFALL(mm)', np.nan, 'ERRO', F + ': não informado; 584 mm é a chuva de Changwu (PRJNA1054347), outro local')
setv(p, 'AVG_ANNUAL_TEMPERATURE', np.nan, 'ERRO', F + ': não informado; 9,1 °C é a temperatura de Changwu (PRJNA1054347)')

# =====================================================================================================================
# PRJNA1155845 — microcosmo PLA/PET × glifosato, solo e intestino de E. crypticus
# =====================================================================================================================
p = P('PRJNA1155845'); F = FONTES['PRJNA1155845']
its = p[p.str.startswith('SRR30519')]
c.loc[its, 'ACAO'] = 'REMOVER: run de ITS (fungos); os 16S são SRR30517334–381'
for i in its: LOG.append(dict(SAMPLE=i, BIOPROJECT='PRJNA1155845', SAMPLE_NAME=n[i], COLUNA='(linha inteira)', VALOR_ATUAL='presente',
                              VALOR_CORRETO='remover da aba Bacteria', TIPO='REMOVER', FONTE='sequências ITS (~217 pb, 47 % não classificadas no SILVA)'))
b16 = p.difference(its)
core = n[b16].str.replace('^S_', '', regex=True).str.replace(r'\d+$', '', regex=True)
trat = core.map({'Con': 'Control', 'Gly': 'Glyphosate', 'PLA': 'PLA', 'PET': 'PET', 'GA': 'PLA-Gly', 'GE': 'PET-Gly'})
S1 = pd.DataFrame({'NH4': [0.31, 0.32, 0.42, 0.36, 0.40, 0.42], 'SOM': [0.41, 0.39, 1.77, 1.47, 1.67, 1.39],
                   'AP': [4.12, 4.21, 3.52, 11.21, 3.74, 10.61], 'NO3': [7.62, 5.56, 0.29, 5.56, 0.15, 6.08]},
                  index=['Control', 'Glyphosate', 'PLA', 'PET', 'PLA-Gly', 'PET-Gly'])
setv(b16, 'SOC(g/kg)', lambda i: round(S1.at[trat[i], 'SOM'] * 10 / 1.724, 2), 'ERRO',
     F + ': SOM (%) do tratamento × 10 / 1,724 — valores estavam trocados entre tratamentos')
setv(b16, 'DIN(mg/kg)', lambda i: round(S1.at[trat[i], 'NH4'] + S1.at[trat[i], 'NO3'], 2), 'ERRO',
     F + ': DIN = NH4⁺-N + NO3⁻-N do tratamento — valores estavam trocados entre tratamentos')
gut = b16[ncbi.loc[b16, 'sample_title'].eq('gut')]
setv(gut, 'SOIL_FRACTION', 'Gut', 'ERRO', 'NCBI sample_title = "gut"; ' + F + ': intestino de Enchytraeus crypticus')
setv(gut, 'ENV_TYPE', 'Invertebrate gut', 'ERRO', F + ': intestino de Enchytraeus crypticus (os valores de solo são do solo do tratamento)')
setv(p, 'TILLAGE', np.nan, 'SUGESTÃO', F + ': microcosmo em laboratório (béquer), preparo do solo não se aplica')

# =====================================================================================================================
# PRJEB59875 — duna costeira, Toscana
# =====================================================================================================================
p = P('PRJEB59875'); F = FONTES['PRJEB59875']
setv(p, 'SOIL_FRACTION', 'Rhizosphere', 'ERRO', F + ': "Rhizosphere sand samples were collected by gently shaking the roots" (todas as amostras)')
code = n[p].str.split().str[1]
setv(p, 'CULTIVAR', lambda i: 'Sporobolus pumilus' if code[i].startswith('Sp') else 'Thinopyrum junceum', 'ERRO',
     'Nome no ENA (E = Thinopyrum junceum, Sp = Sporobolus pumilus); ' + F + ': S. pumilus com HDPE foi excluído (só 2 sobreviveram)')
plast = p[c.loc[p, 'POLYMER_TYPE'].notna()]
setv(plast, 'POLYMER_SIZE', '25 x 25', 'PADRONIZAÇÃO', F + ': "Plastic fragments (25 cm × 25 cm)"')
setv(plast, 'POLYMER_SIZE_METRIC', 'cm', 'PADRONIZAÇÃO', F)

# =====================================================================================================================
# PRJNA932786 — mesocosmo com Lumbricus terrestris, Puyallup-WA
# =====================================================================================================================
p = P('PRJNA932786'); F = FONTES['PRJNA932786']
setv(p, 'SOC(g/kg)', 17.11, 'ERRO', F + ': "Soil organic matter 29.5 g/kg" é matéria orgânica; SOC ≈ 29,5 / 1,724 = 17,1 g/kg')
setv(p, 'YEAR_PERIOD', '2021', 'PREENCHER', 'NCBI collection_date = 2021-05; Supporting Information (vídeos de 04/2021)')

# =====================================================================================================================
# Polímeros — tipo de PE e densidade (todas as linhas)
# =====================================================================================================================
pe = c.index[c.POLYMER_TYPE.eq('PE')]
tipo_pe = {'PRJNA564156': ('LLDPE', 'Bandopadhyay et al. 2020 (Tabela 1): "Linear low-density polyethylene"'),
           'PRJNA631499': ('LLDPE', 'Bandopadhyay et al. 2020 (Tabela S1): "Linear low-density polyethylene"'),
           'PRJNA630025': ('LDPE', 'Rüthi et al. 2020: "waste bag made of low-density PE"'),
           'PRJNA932786': ('LDPE', 'Adhikari et al., Supporting Information (Fig. S5/S6): LDPE')}
for i in pe:
    pj = c.at[i, 'BIOPROJECT']
    if pj in tipo_pe:
        setv(i, 'DENSITY_(g/cm³)', '0,91-0,94', 'ERRO', tipo_pe[pj][1] + ' — 0,94–0,97 é a densidade do HDPE; LDPE/LLDPE = 0,91–0,94')
        setv(i, 'POLYMER_TYPE', tipo_pe[pj][0], 'SUGESTÃO', tipo_pe[pj][1] + ' (manter "PE" se o grupo preferir agrupar todos os PE)')
    else:
        setv(i, 'DENSITY_(g/cm³)', '0,91-0,97', 'SUGESTÃO', FONTES[pj] + ': tipo de PE não informado; usar a faixa geral do PE (0,91–0,97)')
tps = c.index[c.POLYMER_TYPE.eq('TPS/polyester')]
setv(tps, 'BIODEGRADABLE', 'Biodegradable', 'PREENCHER', 'Bandopadhyay et al. 2020 (Tabela 1): Naturecycle = biodegradable mulch (blend of starch and polyesters)')
setv(tps, 'PLASTIC_GROUPPING', 'Biodegradable_polyester', 'PREENCHER', 'mesma classe dos outros blends de amido/poliéster')

# =====================================================================================================================
# Padronização de vocabulário (todas as linhas)
# =====================================================================================================================
VOC = {'SOIL_FRACTION': {'Plastisphere': 'Plastosphere'}, 'CLIMATE': {'Humid Subtropical': 'Humid subtropical'},
       'SOIL_TYPE': {'Sandy_loam': 'Sandy loam'}, 'POLYMER_SIZE_METRIC': {'uM': 'µm'}, 'TILLAGE': {'YES': 'Yes'},
       'BIODEGRADABLE': {'BIODEGRADABLE': 'Biodegradable'}, 'CHEMICAL_COMPOSITION': {'–[CH₂–CH₂]n–': '–CH₂–CH₂–'}}
for col, m in VOC.items():
    for i in c.index[c[col].isin(m.keys())]:
        setv(i, col, m[c.at[i, col]], 'PADRONIZAÇÃO', f'vocabulário: usar "{m[c.at[i, col]]}" em toda a planilha')

# =====================================================================================================================
L = pd.DataFrame(LOG)
rem = set(c.index[c.ACAO.fillna('').str.startswith('REMOVER')])
L = L[(L.TIPO == 'REMOVER') | ~L.SAMPLE.isin(rem)].sort_values(['BIOPROJECT', 'TIPO', 'COLUNA', 'SAMPLE_NAME'])
L.to_csv('revisao_artigos_correcoes.tsv', sep='\t', index=False)
c.reset_index(drop=True).to_csv('planilha_bacteria_revisada.tsv', sep='\t', index=False)
print('células:', (L.TIPO != 'REMOVER').sum(), '| linhas a remover:', (L.TIPO == 'REMOVER').sum())
print(L.groupby(['BIOPROJECT', 'TIPO']).size().unstack(fill_value=0))
print(L[L.TIPO != 'REMOVER'].groupby(['BIOPROJECT', 'COLUNA']).size().to_string())
