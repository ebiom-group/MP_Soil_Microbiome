"""Compara a aba 'Metadata - Bacteria' da planilha com os metadados depositados no NCBI/ENA
e gera as correções por amostra.

Fontes: dados_ncbi/runs_biosample.tsv (ENA filereport + atributos NCBI BioSample, baixados em 2026-09-29)
e os artigos originais citados em CORRECOES_METADADOS.md.

Saídas:
  correcoes_planilha.tsv            formato longo: uma linha por célula a alterar
  planilha_bacteria_corrigida.tsv   aba 'Metadata - Bacteria' inteira já corrigida (+ colunas novas)
  CORRECOES_METADADOS.md            relatório com as tabelas por projeto
"""
import numpy as np
import pandas as pd

X = '../results/dados_complementares/Database_Plastic-Soil.xlsx'
bac = pd.read_excel(X, 'Metadata - Bacteria')
ncbi = pd.read_csv('dados_ncbi/runs_biosample.tsv', sep='\t').set_index('run_accession')
conj = set(pd.read_csv('../results/conjunto_alex/meta.tsv', sep='\t').SAMPLE)

orig = bac.copy()
c = bac.copy().set_index('SAMPLE', drop=False)
n = c.SAMPLE_NAME.astype(str)
nc = ncbi.reindex(c.index)
motivo = {}          # (SAMPLE, coluna) -> fonte/motivo
novas = ['TRATAMENTO_ORIGINAL', 'TIPO_AMOSTRA', 'LOCAL', 'DATA_COLETA', 'GLIFOSATO', 'ADUBACAO_N',
         'DOSE_MP(%)', 'FOTOENVELHECIMENTO', 'TEMPO_INCUBACAO', 'ACAO']
for col in novas: c[col] = np.nan
c = c.astype(object)

PROPS = ['POLYMER_AROMATIC_RINGS', 'BIODEGRADABLE', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)',
         'CHEMICAL_COMPOSITION', 'HARDNESS', 'DEGRADABILITY_RATE', 'PLASTIC_GROUPPING']
ref = (orig.dropna(subset=['POLYMER_TYPE']).groupby('POLYMER_TYPE')[PROPS]
       .agg(lambda s: s.mode().iloc[0] if s.notna().any() else np.nan))

# lacunas da própria planilha: Naturecycle (starch/Polyester blend) é compostável/biodegradável
ref.loc['starch/Polyester blend', ['BIODEGRADABLE', 'PLASTIC_GROUPPING']] = ['Biodegradable', 'Biodegradable_polyester']

def setv(idx, col, val, fonte):
    for i in ([idx] if isinstance(idx, str) else list(idx)):
        v = val(i) if callable(val) else val
        cur = c.at[i, col]
        if (pd.isna(cur) and pd.isna(v)) or (not pd.isna(cur) and not pd.isna(v) and str(cur) == str(v)):
            continue
        c.at[i, col] = v
        if col == 'POLYMER_TYPE' and pd.isna(cur) and v == 'NONE': continue   # só padronização, não é erro
        if col not in novas: motivo[(i, col)] = fonte

def set_polimero(idx, pol, fonte):
    for i in ([idx] if isinstance(idx, str) else list(idx)):
        setv(i, 'POLYMER_TYPE', pol, fonte)
        if pol == 'NONE':
            for p in PROPS + ['POLYMER_COLOR']: setv(i, p, np.nan, fonte + ' (controle: sem propriedades de polímero)')
        elif pol in ref.index:
            for p in PROPS: setv(i, p, ref.at[pol, p], f'propriedades padrão de {pol} na planilha')

P = lambda proj: c.index[c.BIOPROJECT == proj]

# ---------------------------------------------------------------- PRJNA564156 (bulk, EUA)
F_564 = 'NCBI BioSample (título = tratamento; parcela mantém o mesmo tratamento nas 4 coletas)'
MULCH = {'BioAgri': 'starch/PBAT', 'Naturecycle': 'starch/Polyester blend', 'Organix': 'PLA/PBAT',
         'PLA/PHA': 'PLA/PHA', 'Polyethylene': 'PE', 'No Mulch': 'NONE', 'Weedguard': 'Cellulose paper'}
CLIMA = {'USA: Knoxville in Tennessee': 'Humid subtropical', 'USA: Mount Vernon in Washington State': 'Mediterranean'}
for proj in ['PRJNA564156', 'PRJNA631499']:
    for i in P(proj):
        if i not in nc.index or pd.isna(nc.at[i, 'title']): continue
        t = nc.at[i, 'title']; c.at[i, 'TRATAMENTO_ORIGINAL'] = t
        c.at[i, 'LOCAL'] = nc.at[i, 'geo_loc_name']; c.at[i, 'DATA_COLETA'] = nc.at[i, 'collection_date']
        pol = MULCH[t]
        if pol == 'Cellulose paper':
            setv(i, 'POLYMER_TYPE', 'Cellulose paper', F_564 + ' — WeedGuardPlus é mulch de papel (não é plástico)')
            setv(i, 'BIODEGRADABLE', 'Biodegradable', 'papel de celulose')
            setv(i, 'PLASTIC_GROUPPING', 'Non-plastic (paper)', 'papel de celulose')
            for p in ['POLYMER_AROMATIC_RINGS', 'DENSITY_(g/cm³)', 'MOLECULAR_WEIGHT_(g/mol)', 'CHEMICAL_COMPOSITION',
                      'HARDNESS', 'DEGRADABILITY_RATE', 'POLYMER_COLOR', 'POLYMER_SIZE']:
                setv(i, p, np.nan, 'papel de celulose: propriedades de plástico não se aplicam')
        else:
            set_polimero(i, pol, F_564)
        if nc.at[i, 'isolation_source'] == 'enrichment culture':
            c.at[i, 'TIPO_AMOSTRA'] = 'Cultura de enriquecimento (lab)'
            c.at[i, 'TEMPO_INCUBACAO'] = nc.at[i, 'Time of incubation']
            setv(i, 'EXPERIMENT_TYPE', 'Ex_situ', 'NCBI isolation_source = "enrichment culture" (incubação 3–6 semanas em laboratório)')
            setv(i, 'SOIL_FRACTION', 'Enrichment_culture', 'NCBI isolation_source = "enrichment culture"')
        else:
            c.at[i, 'TIPO_AMOSTRA'] = 'Solo de campo' if proj == 'PRJNA564156' else 'Plastisfera de campo'
        setv(i, 'CLIMATE', CLIMA[nc.at[i, 'geo_loc_name']], 'NCBI geo_loc_name (Knoxville-TN = subtropical úmido; Mount Vernon-WA = mediterrâneo)')

# ---------------------------------------------------------------- PRJNA702448 (PBSA, Alemanha)
F_702 = 'NCBI BioSample (isolation_source / env_local_scale)'
for i in P('PRJNA702448'):
    els = str(nc.at[i, 'env_local_scale']) if i in nc.index else ''
    c.at[i, 'TRATAMENTO_ORIGINAL'] = els.rsplit('_', 1)[0]
    c.at[i, 'ADUBACAO_N'] = 'Sim' if 'N fertilization' in els else 'Não'
    if 'PBSA' in els: set_polimero(i, 'PBSA', F_702 + ': tratamento com PBSA')
    else: set_polimero(i, 'NONE', F_702 + ': sem PBSA')
    frac = 'Plastosphere' if nc.at[i, 'isolation_source'] == 'PBSA_plastic' else 'Bulk'
    setv(i, 'SOIL_FRACTION', frac, F_702 + (': PBSA_plastic = plastisfera' if frac == 'Plastosphere' else ': soil'))
    setv(i, 'FERTILIZATION', 'Chemical' if 'N fertilization' in els else np.nan, F_702 + ': só tratamentos "N fertilization" receberam N')
    c.at[i, 'TIPO_AMOSTRA'] = 'Plastisfera (PBSA)' if frac == 'Plastosphere' else ('Solo inicial (T0)' if 'Initial' in els else 'Solo')

# ---------------------------------------------------------------- PRJNA1155845 (MP + glifosato, E. crypticus)
F_115 = 'NCBI experiment_title (gut/soil) + artigo: Enchytraeus crypticus, J. Hazard. Mater. 2025 (doi:10.1016/j.jhazmat.2025.137676)'
for i in P('PRJNA1155845'):
    if i.startswith('SRR30519'):
        c.at[i, 'ACAO'] = 'REMOVER da aba Bacteria — run de ITS (fungo); mover para aba Fungi'
        c.at[i, 'TIPO_AMOSTRA'] = 'ITS (fungo)'
        continue
    core = n[i].replace('S_', '', 1) if n[i].startswith('S_') else n[i]
    gut = nc.at[i, 'sample_title'] == 'gut'
    c.at[i, 'TIPO_AMOSTRA'] = 'Intestino de Enchytraeus crypticus' if gut else 'Solo'
    c.at[i, 'GLIFOSATO'] = 'Sim' if core.startswith(('Gly', 'GA', 'GE')) else 'Não'
    c.at[i, 'TRATAMENTO_ORIGINAL'] = {'Con': 'Controle', 'Gly': 'Glifosato', 'GA': 'PLA + glifosato', 'GE': 'PET + glifosato',
                                      'PLA': 'PLA', 'PET': 'PET'}[core.rstrip('0123456789')]
    setv(i, 'SOIL_FRACTION', 'Gut' if gut else 'Bulk', F_115)
    if gut: setv(i, 'ENV_TYPE', 'Invertebrate gut', F_115)
    if core.startswith(('Con', 'Gly')): set_polimero(i, 'NONE', F_115)

# ---------------------------------------------------------------- PRJEB59875 (duna costeira, Itália)
F_EB = 'Nome da amostra no ENA (E=Thinopyrum junceum, Sp=Sporobolus pumilus; C=controle, MB=Mater-Bi, PE=polietileno) + artigo Menicagli et al. 2023 (rizosfera)'
for i in P('PRJEB59875'):
    code = n[i].split()[1]; planta = 'Sporobolus pumilus' if code.startswith('Sp') else 'Thinopyrum junceum'
    trat = code[2:] if code.startswith('Sp') else code[1:]
    c.at[i, 'TRATAMENTO_ORIGINAL'] = {'C': 'Controle', 'MB': 'Sacola Mater-Bi', 'PE': 'Sacola de polietileno'}[trat]
    setv(i, 'CULTIVAR', planta, F_EB)
    setv(i, 'SOIL_FRACTION', 'Rhizosphere', 'Artigo: "Plastic litter changes the rhizosphere bacterial community..." — todas as amostras são rizosfera')
    set_polimero(i, {'C': 'NONE', 'MB': 'starch/PBAT', 'PE': 'HDPE'}[trat], F_EB + ('; Mater-Bi = amido/PBAT (mesma classe que BioAgri)' if trat == 'MB' else ''))
    if trat == 'C':
        for p in ['POLYMER_FORMAT', 'POLYMER_SIZE']: setv(i, p, np.nan, F_EB + ' (controle)')

# ---------------------------------------------------------------- PRJNA630025 (Rüthi et al. 2020)
for i in P('PRJNA630025'):
    if n[i].endswith('_fung'):
        c.at[i, 'ACAO'] = 'REMOVER da aba Bacteria — run de ITS (fungo, *_fung); já está na aba Fungi'
        c.at[i, 'TIPO_AMOSTRA'] = 'ITS (fungo)'
    else:
        c.at[i, 'LOCAL'] = nc.at[i, 'sample_alias'] if i in nc.index else np.nan
        c.at[i, 'ACAO'] = 'VERIFICAR polímero e fração no material suplementar de Rüthi et al. 2020 (NCBI não informa por amostra)'

# ---------------------------------------------------------------- PRJNA1054347 (mulch de milho)
for i in P('PRJNA1054347'):
    em = nc.at[i, 'env_medium'] if i in nc.index else None
    if n[i] in ('BM5', 'BM6'):
        c.at[i, 'ACAO'] = f'VERIFICAR: nome indica solo bulk, mas o NCBI diz env_medium="{em}"'
    if n[i] == 'M4':
        c.at[i, 'ACAO'] = 'VERIFICAR: SAMPLING_DEPTH = 0, as demais amostras têm 0-20'

# ---------------------------------------------------------------- PRJNA1021161 (dose/tempo/envelhecimento)
for i in P('PRJNA1021161'):
    src = nc.at[i, 'isolation_source'] if i in nc.index else ''
    c.at[i, 'TRATAMENTO_ORIGINAL'] = src
    if pd.notna(src):
        import re
        d = re.match(r'([\d.]+)%', src); c.at[i, 'DOSE_MP(%)'] = float(d.group(1)) if d else 0
        a = re.search(r'photoaged \((\d+) days\)', src); c.at[i, 'FOTOENVELHECIMENTO'] = f'{a.group(1)} dias' if a else ('virgem' if d else np.nan)
        t = re.search(r'treated for (\d+) days', src); c.at[i, 'TEMPO_INCUBACAO'] = f'{t.group(1)} dias' if t else '0 (solo inicial)'
    if 'Blank control' in str(src) or 'Untreated' in str(src): set_polimero(i, 'NONE', 'NCBI isolation_source (controle)')

# ---------------------------------------------------------------- PRJNA932786 (mesocosmo com minhoca)
for i in P('PRJNA932786'):
    c.at[i, 'TIPO_AMOSTRA'] = 'Solo (réplica "b"; "a" = intestino de minhoca, "c" = coprólito, não incluídos)'
    c.at[i, 'TRATAMENTO_ORIGINAL'] = nc.at[i, 'env_local_scale'] if i in nc.index else np.nan
    if str(c.at[i, 'POLYMER_TYPE']) == 'nan' or c.at[i, 'POLYMER_TYPE'] == 'NONE': set_polimero(i, 'NONE', 'NCBI env_local_scale = "No microplastics"')

# ---------------------------------------------------------------- vocabulário (todas as linhas)
for i in c.index:
    if c.at[i, 'BIODEGRADABLE'] == 'BIODEGRADABLE':
        setv(i, 'BIODEGRADABLE', 'Biodegradable', 'padronização de vocabulário (BIODEGRADABLE → Biodegradable)')
    if str(c.at[i, 'DENSITY_(g/cm³)']) == '0,94-0,167':
        setv(i, 'DENSITY_(g/cm³)', '0,94-0,97', 'erro de digitação (densidade do PE = 0,94–0,97 g/cm³)')
    if c.at[i, 'POLYMER_TYPE'] == 'starch/Polyester blend':
        for col in ['BIODEGRADABLE', 'PLASTIC_GROUPPING']:
            setv(i, col, ref.at['starch/Polyester blend', col], 'propriedade vazia para starch/Polyester blend (Naturecycle é compostável)')

# ---------------------------------------------------------------- linhas fora do conjunto
for i in c.index:
    if i not in conj and pd.isna(c.at[i, 'ACAO']):
        c.at[i, 'ACAO'] = 'Fora do conjunto_alex (não processado / falhou no QC) — conferir'

# ============================================================================ saídas
long = pd.DataFrame([dict(SAMPLE=i, BIOPROJECT=c.at[i, 'BIOPROJECT'], SAMPLE_NAME=c.at[i, 'SAMPLE_NAME'], COLUNA=col,
                          VALOR_ATUAL=orig.set_index('SAMPLE').at[i, col], VALOR_CORRETO=c.at[i, col], FONTE=f)
                     for (i, col), f in motivo.items()])
long = long.sort_values(['BIOPROJECT', 'SAMPLE_NAME', 'COLUNA'])
long.to_csv('correcoes_planilha.tsv', sep='\t', index=False)
c.to_csv('planilha_bacteria_corrigida.tsv', sep='\t', index=False)

def fmt(v):
    return '_(vazio)_' if pd.isna(v) or v == '' else str(v).replace('|', '/')

# ---- markdown
L = []
w = L.append
w('# Correções dos metadados — aba "Metadata - Bacteria"\n')
w('Comparação entre a planilha `Database_Plastic-Soil.xlsx` e os metadados depositados pelos autores no **NCBI BioSample / ENA** '
  '(baixados em 29/09/2026, cópia em `dados_ncbi/`) e nos artigos originais.\n')
w('* `correcoes_planilha.tsv`: uma linha por célula a alterar (SAMPLE, coluna, valor atual → correto, fonte). Dá para filtrar no Google Sheets.')
w('* `planilha_bacteria_corrigida.tsv`: a aba inteira já corrigida, com as colunas novas sugeridas no final.')
w('* `gerar_correcoes.py`: regenera tudo.\n')

w('## 1. Tipo de dado\n')
w('* **Todas as 553 amostras do `conjunto_alex` são 16S rRNA (bactérias).** São 314 em V4 (515F/806R) e 239 em V3‑V4. '
  'Na tabela final, 100 % dos ASVs estão classificados como *Bacteria*: arqueias, cloroplasto e mitocôndria foram removidos no pipeline. Não há fungos no conjunto.')
w('* A **aba "Metadata - Bacteria" tem 84 runs de fungos (ITS)** que não deveriam estar lá:')
w('  * **PRJNA630025**: 36 runs `*_fung` (ITS).')
w('  * **PRJNA1155845**: 48 runs `SRR30519516–SRR30519563` (ITS). Os de 16S são `SRR30517334–SRR30517381`.')
w('* ⚠️ **As abas e as configs do projeto‑09 estão trocadas.** As sequências de `SRR30517*` são 16S V4 típicas (251 pb, começam com TACG, 100 % classificadas no SILVA). '
  'As de `SRR30519*` são ITS (cerca de 217 pb, 47 % "Unassigned" no SILVA). Mas:')
w('  * `auto-bash/configs/projeto-09-bacteria.conf` usa **SRR30519** (ITS) como bactéria → **`results/projeto-09-bacteria` é, na verdade, ITS processado com SILVA** e precisa ser refeito.')
w('  * `projeto-09-fungo.conf` usa **SRR30517** (16S) como fungo.')
w('  * A aba **"Metadata - Fungi"** lista SRR30517 (16S) para PRJNA1155845. O certo seria SRR30519.')
w('  * O `conjunto_alex` usa o conjunto certo (SRR30517).')
w('* A aba "Metadata - Fungi" também lista, para **PRJNA1054347** (36) e **PRJNA702448** (31), os **mesmos runs da aba Bacteria**. '
  'Esses BioProjects só têm esses runs no NCBI, e eles são 16S, então os dados de ITS desses estudos precisam ser procurados em outro BioProject.\n')

w('## 2. Resumo por projeto\n')
w('| Projeto | Gravidade | Problema | Amostras afetadas | Fonte |')
w('|---|---|---|---|---|')
cnt = long.groupby('BIOPROJECT').SAMPLE.nunique()
resumo = [
 ('PRJNA564156', '🔴 alta', 'Polímero trocado em relação ao tratamento registrado no NCBI. A mesma parcela aparece com polímeros diferentes entre coletas (32 de 42 parcelas). Clima Knoxville/Mount Vernon invertido em 50 amostras. "Weedguard" (mulch de **papel**) não é plástico.', 'NCBI BioSample (título, parcela, local)'),
 ('PRJNA1155845', '🔴 alta', '**24 amostras são intestino de *Enchytraeus crypticus*, não solo** (as sem prefixo `S_`). Tratamento glifosato sem coluna própria. 48 runs de ITS na aba de bactérias.', 'NCBI + artigo (J. Hazard. Mater. 2025)'),
 ('PRJNA631499', '🔴 alta', '**46 amostras de 2016‑07 são culturas de enriquecimento em laboratório** (3 e 6 semanas), não plastisfera de campo. Clima invertido.', 'NCBI isolation_source'),
 ('PRJEB59875', '🔴 alta', 'Polímero e planta desalinhados em relação ao nome da amostra. Todas são **rizosfera** (não plastisfera).', 'Nome no ENA + artigo (Menicagli et al. 2023)'),
 ('PRJNA702448', '🟠 média', '`S_PS*`/`S_PSN*` são solo **com PBSA** (estavam como controle). `SOIL_FRACTION` vazio. Adubação N aparece em todas as amostras. Controles têm propriedades de PBSA.', 'NCBI env_local_scale'),
 ('PRJNA630025', '🟠 média', '36 runs de ITS na aba de bactérias. A correspondência entre nome (P/S/VPI) e polímero/fração **não pode ser verificada no NCBI** (só 2 BioSamples, um por local). A análise não encontrou diferença plastisfera × bulk, o que é suspeito.', 'ENA library_name; artigo Rüthi et al. 2020'),
 ('PRJNA1054347', '🟡 baixa', 'BM5 e BM6: nome = bulk, mas o NCBI diz rizosfera. M4 com profundidade 0 (demais 0‑20).', 'NCBI env_medium'),
 ('PRJNA1021161', '🟢 ok', 'Anotação correta. Dose, fotoenvelhecimento e tempo estão só no nome; foram sugeridas colunas.', 'NCBI isolation_source'),
 ('PRJNA932786', '🟢 ok', 'Correto (só réplicas "b" = solo). O artigo e a aba de projetos dizem **LDPE**; a planilha diz PE. Sugestão: usar LDPE.', 'NCBI env_medium'),
]
for p, g, prob, fonte in resumo:
    w(f'| {p} | {g} | {prob} | {int(cnt.get(p, 0))} | {fonte} |')
w('')
w('Linhas da aba que **não estão no `conjunto_alex`**: PRJNA853344 (2 runs, SRR19868794/95) e PRJNA631499 `BDM07160016PL`, `BDM07160014PL`. Verificar se falharam no QC.\n')

w('## 3. Colunas novas sugeridas\n')
w('| Coluna | Para quê | Projetos |')
w('|---|---|---|')
w('| `TRATAMENTO_ORIGINAL` | nome do tratamento como o autor depositou (ex.: BioAgri, Weedguard, "0.5% photoaged PE") | todos |')
w('| `TIPO_AMOSTRA` | solo / plastisfera / rizosfera / intestino / cultura de enriquecimento | todos |')
w('| `GLIFOSATO` | Sim/Não | PRJNA1155845 |')
w('| `ADUBACAO_N` | Sim/Não | PRJNA702448 |')
w('| `DOSE_MP(%)`, `FOTOENVELHECIMENTO`, `TEMPO_INCUBACAO` | desenho fatorial | PRJNA1021161, PRJNA631499 |')
w('| `LOCAL`, `DATA_COLETA` | local e data da coleta | PRJNA564156, PRJNA631499, PRJNA630025 |')
w('| `ACAO` | remover / verificar | onde aplicável |\n')
w('**Vocabulário a padronizar na planilha inteira:** `BIODEGRADABLE` escrito também como `BIODEGRADABLE` (maiúsculas); densidade do PE digitada como `0,94-0,167`; '
  '`starch/Polyester blend` e `Polyester blend` sem nenhuma propriedade; decimais misturando vírgula e ponto (`1,24` e `1.24`); controles ora `NONE`, ora vazio; '
  'a coluna se chama `PLASTIC_GROUPPING` (PP duplicado).\n')
w('Valores novos em colunas existentes: `SOIL_FRACTION` = `Gut` e `Enrichment_culture`; `POLYMER_TYPE` = `Cellulose paper` (Weedguard) e `NONE` para todos os controles (hoje há `NONE` e vazio misturados).\n')

w('## 4. Tabelas por projeto (valores corretos)\n')
w('Em negrito: células que mudam. O valor atual da planilha aparece entre colchetes.\n')
show = {
 'PRJNA564156': ['SAMPLE_NAME', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'BIODEGRADABLE', 'PLASTIC_GROUPPING', 'CLIMATE', 'LOCAL', 'DATA_COLETA'],
 'PRJNA631499': ['SAMPLE_NAME', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'SOIL_FRACTION', 'EXPERIMENT_TYPE', 'TEMPO_INCUBACAO', 'CLIMATE', 'LOCAL'],
 'PRJNA1155845': ['SAMPLE_NAME', 'TIPO_AMOSTRA', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'GLIFOSATO', 'SOIL_FRACTION', 'ENV_TYPE', 'ACAO'],
 'PRJEB59875': ['SAMPLE_NAME', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'CULTIVAR', 'SOIL_FRACTION', 'BIODEGRADABLE', 'PLASTIC_GROUPPING'],
 'PRJNA702448': ['SAMPLE_NAME', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'SOIL_FRACTION', 'FERTILIZATION', 'ADUBACAO_N', 'BIODEGRADABLE'],
 'PRJNA630025': ['SAMPLE_NAME', 'LOCAL', 'POLYMER_TYPE', 'SOIL_FRACTION', 'ACAO'],
 'PRJNA1054347': ['SAMPLE_NAME', 'POLYMER_TYPE', 'SOIL_FRACTION', 'SAMPLING_DEPTH', 'ACAO'],
 'PRJNA1021161': ['SAMPLE_NAME', 'POLYMER_TYPE', 'DOSE_MP(%)', 'FOTOENVELHECIMENTO', 'TEMPO_INCUBACAO'],
 'PRJNA932786': ['SAMPLE_NAME', 'TRATAMENTO_ORIGINAL', 'POLYMER_TYPE', 'TIPO_AMOSTRA'],
}
o = orig.set_index('SAMPLE')
for p, cols in show.items():
    d = c[c.BIOPROJECT == p].sort_values('SAMPLE_NAME', key=lambda s: s.astype(str))
    w(f'### {p}  ({len(d)} linhas na aba)\n')
    w('| SAMPLE | ' + ' | '.join(cols) + ' |'); w('|' + '---|' * (len(cols) + 1))
    for i, r in d.iterrows():
        cells = []
        for col in cols:
            if (i, col) in motivo:
                cells.append(f'**{fmt(r[col])}** [{fmt(o.at[i, col])}]')
            else:
                cells.append(fmt(r[col]))
        w(f'| {i} | ' + ' | '.join(cells) + ' |')
    w('')

w('## 5. Fontes\n')
w('* NCBI BioSample / ENA: atributos por amostra em `dados_ncbi/runs_biosample.tsv`.')
w('* PRJNA564156 / PRJNA631499: mesmo experimento de mulch biodegradável em Knoxville-TN e Mount Vernon-WA; título do BioSample = produto aplicado na parcela.')
w('* PRJNA1155845: *The combination of microplastics and glyphosate affects the microbiome of soil inhabitant Enchytraeus crypticus*. J. Hazard. Mater. 2025, doi:10.1016/j.jhazmat.2025.137676.')
w('* PRJEB59875: Menicagli et al. 2023, *Plastic litter changes the rhizosphere bacterial community of coastal dune plants* (PMID 37030390).')
w('* PRJNA630025: Rüthi et al. 2020, Front. Environ. Sci., doi:10.3389/fenvs.2020.562263.')
open('CORRECOES_METADADOS.md', 'w').write('\n'.join(L) + '\n')

print('células a corrigir:', len(long), '| amostras:', long.SAMPLE.nunique())
print(long.groupby(['BIOPROJECT', 'COLUNA']).size().to_string())
print(c.ACAO.value_counts().to_string())
