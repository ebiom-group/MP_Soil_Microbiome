"""Gera meta_corrigida.tsv: metadados do conjunto_alex com as correções de gerar_correcoes.py aplicadas
e colunas derivadas usadas nas análises.

Uso: .venv/bin/python gerar_correcoes.py && .venv/bin/python preparar_metadados.py
"""
import numpy as np
import pandas as pd

meta = pd.read_csv('../results/conjunto_alex/meta.tsv', sep='\t', index_col=0)
corr = pd.read_csv('planilha_bacteria_corrigida.tsv', sep='\t').set_index('SAMPLE').reindex(meta.index)

# colunas categóricas corrigidas (as numéricas continuam as do meta.tsv, que já vêm parseadas)
for col in ['POLYMER_TYPE', 'SOIL_FRACTION', 'CLIMATE', 'CULTIVAR', 'BIODEGRADABLE', 'DEGRADABILITY_RATE', 'HARDNESS',
            'CHEMICAL_COMPOSITION', 'ENV_TYPE', 'EXPERIMENT_TYPE', 'FERTILIZATION']:
    meta[col] = corr[col]
meta['PLASTIC_GROUPING'] = corr['PLASTIC_GROUPPING']
for col in ['TRATAMENTO_ORIGINAL', 'TIPO_AMOSTRA', 'LOCAL', 'DATA_COLETA', 'GLIFOSATO', 'ADUBACAO_N',
            'DOSE_MP(%)', 'FOTOENVELHECIMENTO', 'TEMPO_INCUBACAO']:
    meta[col] = corr[col]

m = meta
m['POLYMER'] = m.POLYMER_TYPE.replace({'NONE': 'Controle', 'Cellulose paper': 'Papel'}).fillna('Controle')
m['TRAT'] = np.select([m.POLYMER.eq('Controle'), m.POLYMER.eq('Papel')], ['Controle', 'Papel'], 'Plástico')
m['CLASSE'] = np.select([m.POLYMER.eq('Controle'), m.POLYMER.eq('Papel'), m.BIODEGRADABLE.eq('Biodegradable')],
                        ['Controle', 'Papel', 'Biodegradável'], 'Não biodegradável')
m['COMPARTIMENTO'] = m.SOIL_FRACTION.map({'Bulk': 'Solo', 'Plastosphere': 'Plastisfera', 'Rhizosphere': 'Rizosfera',
                                         'Gut': 'Intestino', 'Enrichment_culture': 'Enriquecimento'})
m['REGIAO'] = m['16S_REGION']
m['ESTRATO'] = m.BIOPROJECT + ' | ' + m.SOIL_FRACTION

n = m.SAMPLE_NAME.astype(str)
# coleta (EUA): data depositada no NCBI
us = m.BIOPROJECT.isin(['PRJNA564156', 'PRJNA631499'])
m.loc[us, 'COLETA'] = m.loc[us, 'DATA_COLETA']
m.loc[us, 'SITIO'] = m.loc[us, 'LOCAL'].map({'USA: Knoxville in Tennessee': 'Knoxville-TN',
                                             'USA: Mount Vernon in Washington State': 'MountVernon-WA'})
m.loc[m.BIOPROJECT.eq('PRJNA630025'), 'SITIO'] = m.loc[m.BIOPROJECT.eq('PRJNA630025'), 'COUNTRY'].map(
    {'Switzerland': 'Alpes-CH', 'Greenland': 'Artico-GL'})
m['INCUBACAO_SEMANAS'] = m.TEMPO_INCUBACAO.where(m.SOIL_FRACTION.eq('Enrichment_culture')).str.extract(r'(\d+)')[0].astype(float)

# PRJNA1021161
p = m.BIOPROJECT.eq('PRJNA1021161')
m.loc[p, 'DOSE'] = m.loc[p, 'DOSE_MP(%)'].astype(float)
m.loc[p, 'ENVELHECIMENTO'] = m.loc[p, 'FOTOENVELHECIMENTO'].fillna('controle')
m.loc[p, 'DIAS'] = m.loc[p, 'TEMPO_INCUBACAO'].str.extract(r'^(\d+)')[0].astype(float)

# PRJNA702448
p = m.BIOPROJECT.eq('PRJNA702448')
m.loc[p, 'NITROGENIO'] = np.where(m.loc[p, 'ADUBACAO_N'].eq('Sim'), 'N+', 'N-')

m.to_csv('meta_corrigida.tsv', sep='\t')
print(m.shape)
print(pd.crosstab(m.BIOPROJECT, m.COMPARTIMENTO))
print(pd.crosstab(m.POLYMER, m.CLASSE))
