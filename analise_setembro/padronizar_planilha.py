"""Padroniza unidades, formatos numéricos e vocabulário da aba 'Metadata - Bacteria' já revisada.

Entrada : planilha_bacteria_revisada.tsv (saída de revisar_planilha_artigos.py)
Saídas  : planilha_bacteria_padronizada.tsv / .xlsx — aba pronta para substituir a online
          correcoes_finais.tsv — TODAS as diferenças entre a planilha online atual e a padronizada (revisão + padronização)
          PADRONIZACAO.md — regras e unidades de cada coluna

Regras
  * vazio → NA
  * número: ponto decimal, sem separador de milhar, sem "~"; "média ± dp" → média; faixa → "min-max"
  * POLYMER_SIZE sempre em µm (cm × 10 000, mm × 1 000); dimensões → "a x b"; POLYMER_SIZE_METRIC = µm
  * MOLECULAR_WEIGHT em g/mol, número inteiro ("10⁴ – 10⁶" → "10000-1000000")
  * SAMPLING_DEPTH em cm, "min-max"
  * vocabulário único por coluna (ver VOC)
"""
import re
import numpy as np
import pandas as pd

r = pd.read_csv('planilha_bacteria_revisada.tsv', sep='\t', dtype=str, keep_default_na=False, na_values=[''])
online = pd.read_excel('../results/dados_complementares/Database_Plastic-Soil.xlsx', 'Metadata - Bacteria', dtype=str)
rev_log = pd.read_csv('revisao_artigos_correcoes.tsv', sep='\t', dtype=str)
NA = 'NA'

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')


def fmt(x):
    x = float(x)
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else ('%.6g' % x)


def num(v):
    """'~14,6' → '14.6'; '6,03 ± 0,36' → '6.03'; '8,9–9,7' → '8.9-9.7'; '<0.2' → '<0.2'."""
    if pd.isna(v) or str(v).strip() in ('', 'nan', 'NA'): return NA
    s = str(v).strip().replace('~', '').replace('−', '-')
    s = s.split('±')[0].strip()
    s = re.sub(r'(\d),(\d)', r'\1.\2', s)
    s = re.sub(r'\s*[–—]\s*|\s+-\s+', '-', s)
    m = re.fullmatch(r'(<|>)?\s*(-?\d+(?:\.\d+)?)', s)
    if m: return (m.group(1) or '') + fmt(m.group(2))
    m = re.fullmatch(r'(-?\d+(?:\.\d+)?)-(-?\d+(?:\.\d+)?)', s)
    if m: return f'{fmt(m.group(1))}-{fmt(m.group(2))}'
    raise ValueError(f'valor numérico não reconhecido: {v!r}')


def mw(v):
    """'6 x 10⁴ – 2 x 10⁵' → '60000-200000'; '10,000 - 50,000' → '10000-50000'."""
    if pd.isna(v): return NA
    s = re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+', lambda m: '^' + m.group(0).translate(SUP), str(v)).replace(',', '')
    parts = re.split(r'\s*[–—-]\s*', s)
    out = []
    for p_ in parts:
        p_ = p_.strip()
        m = re.fullmatch(r'(?:(\d+(?:\.\d+)?)\s*x\s*)?10\^(\d+)', p_)
        out.append(fmt(float(m.group(1) or 1) * 10 ** int(m.group(2))) if m else fmt(p_))
    return '-'.join(out)


FATOR = {'µm': 1, 'um': 1, 'mm': 1000, 'cm': 10000}


def tamanho(v, unid):
    if pd.isna(v): return NA
    f = FATOR[str(unid).strip().lower().replace('µ', 'u').replace('uM'.lower(), 'um')] if pd.notna(unid) else 1
    s = re.sub(r'(\d),(\d)', r'\1.\2', str(v)).replace('×', 'x')
    def conv(t):
        t = t.strip()
        m = re.fullmatch(r'(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)', t)
        return f'{fmt(float(m.group(1)) * f)}-{fmt(float(m.group(2)) * f)}' if m else fmt(float(t) * f)
    return ' x '.join(conv(t) for t in s.split('x'))


NUM = ['DENSITY_(g/cm³)', 'SAMPLING_DEPTH', 'ANNUAL_RAINFALL(mm)', 'AVG_ANNUAL_TEMPERATURE', 'SOIL_TEMPERATURE(C)',
       'WATER_CONTENT(%)', 'SOC(g/kg)', 'TN(g/kg)', 'C/N', 'pH', 'DOC(mg/kg)', 'DIN(mg/kg)', 'NH4(mg/kg)', 'NO3(mg/kg)',
       'AP(mg/kg)', 'AK(mg/kg)', 'POLYMER_AROMATIC_RINGS']
VOC = {
    'BIODEGRADABLE': {'NO_BIODEGRADABLE': 'Non_biodegradable'},
    'CULTIVAR': {'Maize': 'Zea mays', 'barley': 'Hordeum vulgare'},
    'CLIMATE': {'Temperate Continental': 'Temperate continental'},
    'ENV_TYPE': {'Coastal Dune': 'Coastal dune'},
    'DEGRADABILITY_RATE': {'Extremely Low': 'Extremely low', 'Moderate to Fast': 'Moderate to fast'},
    'CHEMICAL_COMPOSITION': {'Polyester Blend': 'Polyester blend'},
}
SEM_ANEL = {'PE', 'LDPE', 'LLDPE', 'HDPE', 'PLA', 'PBSA', 'PLA/PHA', 'Cellulose paper'}   # sem anel aromático
COM_ANEL = {'PET', 'PBAT', 'TPS/PBAT', 'PLA/PBAT'}                                     # tereftalato

p = r.copy()
remover = p.ACAO.fillna('').str.startswith('REMOVER')
# controles sem polímero → NONE (convenção da planilha) — exceto linhas a remover
ctrl = p.POLYMER_TYPE.isna() & ~remover
p.loc[ctrl, 'POLYMER_TYPE'] = 'NONE'
# tamanho em µm
p['POLYMER_SIZE'] = [tamanho(v, u) for v, u in zip(p.POLYMER_SIZE, p.POLYMER_SIZE_METRIC)]
p['POLYMER_SIZE_METRIC'] = np.where(p.POLYMER_SIZE.eq(NA), NA, 'µm')
p['MOLECULAR_WEIGHT_(g/mol)'] = p['MOLECULAR_WEIGHT_(g/mol)'].map(mw)
for col in NUM:
    p[col] = p[col].map(num)
# anel aromático: 1/0 pela química do polímero; NA para controles e composição desconhecida
p['POLYMER_AROMATIC_RINGS'] = np.select([p.POLYMER_TYPE.isin(COM_ANEL), p.POLYMER_TYPE.isin(SEM_ANEL)], ['1', '0'], NA)
p['YEAR_PERIOD'] = p.YEAR_PERIOD.map(lambda v: NA if pd.isna(v) else re.sub(r'\s*[–/—]\s*', '-', str(v)))
for col, m in VOC.items():
    p[col] = p[col].replace(m)
p = p.fillna(NA).replace({'': NA, 'nan': NA})

# ---------------------------------------------------------------- espessura × tamanho do pedaço/partícula (µm)
# POLYMER_SIZE mistura grandezas; estas duas colunas separam o que cada artigo informa.
ESP_MULCH = {'TPS/PBAT': '26', 'TPS/polyester': '48', 'PLA/PBAT': '20', 'PLA/PHA': '33', 'LLDPE': '47'}  # PeerJ Tab. 1 / Front. Tab. S1

def espessura(r):
    pj, pol = r.BIOPROJECT, r.POLYMER_TYPE
    if pol in ('NONE', NA): return NA
    if pj in ('PRJNA564156', 'PRJNA631499'): return ESP_MULCH.get(pol, NA)
    return {'PRJNA702448': '50', 'PRJNA1054347': '10'}.get(pj, NA)      # Tanunchai 2021 (50 µm); Zhang 2024 (0,01 mm)


def pedaco(r):
    if r.POLYMER_TYPE in ('NONE', NA): return NA
    pj = r.BIOPROJECT
    if pj == 'PRJNA631499': return '40000 x 40000' if r.SOIL_FRACTION == 'Enrichment_culture' else NA   # 4 × 4 cm²; campo ~8 cm² sem dimensão
    if pj in ('PRJNA630025', 'PRJNA702448', 'PRJEB59875', 'PRJNA1021161', 'PRJNA1155845', 'PRJNA932786'):
        return r.POLYMER_SIZE     # pedaço (4×4 cm; 2–5 mm; 25×25 cm) ou diâmetro da partícula (75; 30; 250 µm)
    return NA                      # filmes de mulch em campo (PRJNA564156, PRJNA1054347) e PRJNA853344 (não informado)


# papel de celulose (Weedguard, PRJNA564156) não é plástico: tipo e todos os atributos de polímero = NA
papel = p.POLYMER_TYPE.eq('Cellulose paper')
p.loc[papel, ['POLYMER_TYPE', 'POLYMER_AROMATIC_RINGS', 'BIODEGRADABLE', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)',
              'CHEMICAL_COMPOSITION', 'HARDNESS', 'DEGRADABILITY_RATE', 'PLASTIC_GROUPPING']] = NA
nonec = p.POLYMER_TYPE.eq('NONE') | papel         # controles e papel: nenhum atributo de polímero
p.loc[nonec, ['POLYMER_SIZE', 'POLYMER_SIZE_METRIC', 'POLYMER_FORMAT', 'POLYMER_COLOR']] = NA
esp = p.apply(espessura, axis=1); ped = p.apply(pedaco, axis=1)
pos = list(p.columns).index('POLYMER_SIZE') + 1
p.insert(pos, 'POLYMER_PIECE_SIZE(µm)', ped)
p.insert(pos, 'POLYMER_THICKNESS(µm)', esp)

# checagem: nenhum valor numérico fora do padrão
for col in NUM + ['MOLECULAR_WEIGHT_(g/mol)']:
    bad = p[col][~p[col].str.fullmatch(r'NA|<?-?\d+(\.\d+)?(--?\d+(\.\d+)?)?')]
    assert bad.empty, (col, bad.unique()[:5])
assert p.POLYMER_SIZE[~p.POLYMER_SIZE.str.fullmatch(r'NA|\d+(\.\d+)?(-\d+)?( x \d+(-\d+)?)?')].empty

p.to_csv('planilha_bacteria_padronizada.tsv', sep='\t', index=False)
with pd.ExcelWriter('planilha_bacteria_padronizada.xlsx') as xw:
    p.drop(columns='ACAO').loc[~remover].to_excel(xw, sheet_name='Metadata - Bacteria', index=False)
    p.loc[remover].to_excel(xw, sheet_name='Linhas a remover (ITS)', index=False)

# ---------------------------------------------------------------- diferenças finais vs planilha online
on = online.set_index('SAMPLE'); pp = p.set_index('SAMPLE')
fonte = rev_log.set_index(['SAMPLE', 'COLUNA'])[['TIPO', 'FONTE']]
fonte = fonte[~fonte.index.duplicated()]
rows = []
for s in pp.index:
    if remover[p.SAMPLE.eq(s)].iloc[0]:
        rows.append(dict(SAMPLE=s, BIOPROJECT=pp.at[s, 'BIOPROJECT'], SAMPLE_NAME=pp.at[s, 'SAMPLE_NAME'], COLUNA='(linha inteira)',
                         VALOR_ONLINE='presente', VALOR_NOVO='REMOVER da aba Bacteria', TIPO='REMOVER', FONTE=pp.at[s, 'ACAO']))
        continue
    for col in [x for x in online.columns if x != 'SAMPLE']:
        a = on.at[s, col]; a_ = NA if pd.isna(a) or str(a).strip() == '' else str(a).strip()
        b = pp.at[s, col]
        if a_ == b: continue
        if (s, col) in fonte.index:
            t, f = fonte.loc[(s, col)]
        else:
            t, f = 'FORMATO', 'padronização de unidade/formato/NA (ver PADRONIZACAO.md)'
        rows.append(dict(SAMPLE=s, BIOPROJECT=pp.at[s, 'BIOPROJECT'], SAMPLE_NAME=pp.at[s, 'SAMPLE_NAME'], COLUNA=col,
                         VALOR_ONLINE=a_, VALOR_NOVO=b, TIPO=t, FONTE=f))
D = pd.DataFrame(rows).sort_values(['BIOPROJECT', 'TIPO', 'COLUNA', 'SAMPLE_NAME'])
D.to_csv('correcoes_finais.tsv', sep='\t', index=False)
print('diferenças vs planilha online:', len(D)); print(D.groupby('TIPO').size().to_string())
print(D[D.TIPO == 'FORMATO'].groupby('COLUNA').size().sort_values(ascending=False).to_string())

# ---------------------------------------------------------------- relatório de padronização
U = {'POLYMER_SIZE': 'µm (cm × 10 000; mm × 1 000). Filmes: espessura; pedaços: "a x b"; partículas: diâmetro',
     'POLYMER_SIZE_METRIC': 'sempre "µm" (NA se não há tamanho)',
     'POLYMER_THICKNESS(µm)': 'espessura do filme em µm (NA para partículas, controles e quando o artigo não informa)',
     'POLYMER_PIECE_SIZE(µm)': 'tamanho do pedaço ("a x b") ou diâmetro da partícula, em µm (NA para mulch inteiro no campo ou não informado)', 'POLYMER_AROMATIC_RINGS': '1 = tem anel aromático (tereftalato: PET, PBAT e blends), 0 = não tem, NA = controle ou composição desconhecida',
     'DENSITY_(g/cm³)': 'g/cm³', 'MOLECULAR_WEIGHT_(g/mol)': 'g/mol, número inteiro, faixa "min-max"', 'SAMPLING_DEPTH': 'cm, "min-max"',
     'ANNUAL_RAINFALL(mm)': 'mm/ano', 'AVG_ANNUAL_TEMPERATURE': '°C (temperatura média anual do ar)',
     'SOIL_TEMPERATURE(C)': '°C (campo: média do solo; laboratório: temperatura de incubação)', 'WATER_CONTENT(%)': '% (gravimétrico ou % da capacidade de retenção, como no artigo)',
     'SOC(g/kg)': 'g/kg (carbono orgânico; quando o artigo dá matéria orgânica, SOC = MO / 1,724)', 'TN(g/kg)': 'g/kg', 'C/N': 'adimensional',
     'pH': 'adimensional (média; o desvio foi removido)', 'DOC(mg/kg)': 'mg/kg', 'DIN(mg/kg)': 'mg/kg (NH4⁺-N + NO3⁻-N)',
     'NH4(mg/kg)': 'mg/kg', 'NO3(mg/kg)': 'mg/kg', 'AP(mg/kg)': 'mg/kg', 'AK(mg/kg)': 'mg/kg', 'YEAR_PERIOD': 'ano ou "ano-ano"'}
w = ['# Padronização de unidades e formatos — aba "Metadata - Bacteria"\n',
     'Aplicada sobre a planilha revisada (`planilha_bacteria_revisada.tsv`). As saídas são `planilha_bacteria_padronizada.xlsx`, '
     'pronta para colar na planilha online (aba **Metadata - Bacteria** + aba com as linhas de ITS a remover), e `correcoes_finais.tsv`, '
     'com **todas** as diferenças em relação à planilha online atual (revisão por artigo + padronização).\n',
     '## Regras gerais\n',
     '* **Vazio = `NA`** em todas as colunas.',
     '* **Números:** ponto decimal (`15.14`, não `15,14`), sem `~` e sem separador de milhar.',
     '* **Média ± desvio:** fica só a média (ex.: `6,03 ± 0,36` → `6.03`). Os desvios estão no relatório da revisão.',
     '* **Faixa:** `min-max` (ex.: `489–525` → `489-525`). **Dimensões:** `a x b`.',
     '* **Controles sem plástico:** `POLYMER_TYPE = NONE` e propriedades do polímero `NA`.\n',
     '## Unidade de cada coluna\n', '| Coluna | Unidade / formato |', '|---|---|']
w += [f'| `{k}` | {v} |' for k, v in U.items()]
w += ['\n## Vocabulário unificado\n', '| Coluna | Antes | Depois |', '|---|---|---|']
w += [f'| `{col}` | {a} | {b} |' for col, m in VOC.items() for a, b in m.items()]
w += ['| `POLYMER_SIZE` | 4 x 4 cm; 2–5 × 2–5 mm; 25 x 25 cm; 1 mm | 40000 x 40000; 2000-5000 x 2000-5000; 250000 x 250000; 1000 (µm) |',
      '| `MOLECULAR_WEIGHT_(g/mol)` | 10⁴ – 10⁶; 6 x 10⁴ – 2 x 10⁵; 10,000 - 50,000 | 10000-1000000; 60000-200000; 10000-50000 |',
      '| `YEAR_PERIOD` | 2019/2020; 2019–2022 | 2019-2020; 2019-2022 |',
      '\n## Observação sobre POLYMER_SIZE\n',
      'A coluna mistura grandezas diferentes: **espessura** dos filmes de mulch (10–479 µm), **dimensão dos pedaços** de filme '
      '(40000 x 40000 µm) e **diâmetro** de partículas (30–250 µm). Agora a unidade é a mesma, mas, para comparar entre estudos, '
      'as colunas `POLYMER_THICKNESS(µm)` e `POLYMER_PIECE_SIZE(µm)`, logo após `POLYMER_SIZE`, separam as duas medidas. Exemplo: em PRJNA702448 o filme tem 50 µm de espessura '
      'e foi cortado em pedaços de 2000-5000 µm; em PRJNA630025 a espessura não é informada.\n',
      '## Resumo das diferenças em relação à planilha online\n', '| Tipo | Células |', '|---|---|']
w += [f'| {k} | {v} |' for k, v in D.groupby('TIPO').size().items()]
open('PADRONIZACAO.md', 'w').write('\n'.join(w) + '\n')
