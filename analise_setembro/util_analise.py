"""Funções compartilhadas pelas análises de comparação (analise_v2_comparacoes.ipynb)."""
from pathlib import Path

import numpy as np
import pandas as pd
import skbio
from scipy import stats
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.ordination import pcoa
from statsmodels.stats.multitest import multipletests

DATA = Path('../results/conjunto_alex')
DEPTH = 12000


def carregar(seed=42):
    """Contagens, taxonomia, árvore, metadados corrigidos, tabela rarefeita e diversidade alfa (todas as 553 amostras)."""
    asv = pd.read_csv(DATA / 'asv_table.tsv', sep='\t', index_col=0).astype(int)
    tax = pd.read_csv(DATA / 'taxonomy.tsv', sep='\t', index_col=0).reindex(asv.index)
    tree = skbio.TreeNode.read(str(DATA / 'tree.nwk'))
    meta = pd.read_csv('meta_corrigida.tsv', sep='\t', index_col=0).loc[asv.columns]

    def lowest(row):
        for r in ['Genus', 'Family', 'Order', 'Class', 'Phylum']:
            if pd.notna(row[r]):
                return row[r] if r == 'Genus' else f'{row[r]} (NC)'
        return 'Não classificado'
    tax['LABEL'] = tax.apply(lowest, axis=1)

    rng = np.random.default_rng(seed)
    rare = pd.DataFrame(np.column_stack([rng.multivariate_hypergeometric(asv[s].values, DEPTH) for s in asv.columns]),
                        index=asv.index, columns=asv.columns)
    rare = rare.loc[rare.sum(1) > 0]
    ids, M = list(rare.columns), rare.T.values
    alpha = pd.DataFrame({
        'Riqueza': alpha_diversity('observed_features', M, ids),
        'Shannon': alpha_diversity('shannon', M, ids),
        'Pielou': alpha_diversity('pielou_e', M, ids),
        'FaithPD': alpha_diversity('faith_pd', M, ids, taxa=list(rare.index), tree=tree, validate=False),
    })
    gcounts = asv.groupby(tax.LABEL).sum().drop(index='Não classificado', errors='ignore')
    return asv, tax, tree, meta, rare, alpha, gcounts


# ------------------------------------------------------------------ PERMANOVA
def _design(meta, terms):
    X = [np.ones((len(meta), 1))]; mats = []; dfs = []
    for t in terms:
        col = meta[t]
        if pd.api.types.is_numeric_dtype(col):
            col = col.fillna(col.mean()); Xt = ((col - col.mean()) / (col.std() or 1)).values[:, None]
        else:
            Xt = pd.get_dummies(col.astype(object).fillna('NA').astype(str), drop_first=True).values.astype(float)
        before = np.linalg.matrix_rank(np.hstack(X)); X.append(Xt); M = np.hstack(X)
        dfs.append(np.linalg.matrix_rank(M) - before); mats.append(M @ np.linalg.pinv(M))
    return mats, np.array(dfs, dtype=float)


def permanova(D, meta, terms, perms=999, strata=None, seed=0):
    """PERMANOVA sequencial (SS tipo I, como adonis2 by='terms'); permutação opcional restrita a estratos."""
    D = np.asarray(D); n = len(D); J = np.eye(n) - 1 / n; G = J @ (-0.5 * D ** 2) @ J; SST = np.trace(G)
    Hs, dfs = _design(meta, terms)
    keep = dfs > 0
    def stat(Gm):
        tr = [np.sum(H * Gm) for H in Hs]; ss = np.diff([0] + tr); res = SST - tr[-1]
        return ss, res, n - 1 - dfs.sum()
    ss, res, dfr = stat(G)
    with np.errstate(divide='ignore', invalid='ignore'):
        F = np.where(keep, (ss / dfs) / (res / dfr), np.nan)
    rng = np.random.default_rng(seed); cnt = np.zeros(len(terms))
    groups = [np.arange(n)] if strata is None else [np.where(np.asarray(strata) == s)[0] for s in np.unique(strata)]
    for _ in range(perms):
        p = np.arange(n)
        for g in groups: p[g] = rng.permutation(g)
        s2, r2, _ = stat(G[np.ix_(p, p)])
        with np.errstate(divide='ignore', invalid='ignore'):
            cnt += np.nan_to_num(((s2 / dfs) / (r2 / dfr)) >= F - 1e-12)
    out = pd.DataFrame({'gl': dfs, 'R2': ss / SST, 'F': F, 'p': np.where(keep, (cnt + 1) / (perms + 1), np.nan)}, index=terms)
    out.loc['Residual'] = [dfr, res / SST, np.nan, np.nan]
    return out


def dist(rare, samples, metric='braycurtis', tree=None, level=None, tax=None):
    X = rare[samples]
    if level == 'genus':
        X = (X / X.sum()).groupby(tax.reindex(X.index).LABEL).sum()
    X = X.loc[X.sum(1) > 0]
    kw = dict(taxa=list(X.index), tree=tree, validate=False) if 'unifrac' in metric else {}
    return beta_diversity(metric, X.T.values, ids=list(samples), **kw)


def dispersao(D, groups):
    o = pcoa(skbio.DistanceMatrix(np.asarray(D), ids=[str(i) for i in range(len(D))]), method='eigh')
    X = o.samples.values[:, o.eigvals.values > 0]; groups = np.asarray(groups); d = np.zeros(len(D))
    for g in np.unique(groups):
        idx = groups == g; d[idx] = np.linalg.norm(X[idx] - X[idx].mean(0), axis=1)
    return pd.Series(d), stats.kruskal(*[d[groups == g] for g in np.unique(groups)]).pvalue


# ------------------------------------------------------------------ efeitos
def hedges_g(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); nx, ny = len(x), len(y)
    sp = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    g = (1 - 3 / (4 * (nx + ny) - 9)) * (x.mean() - y.mean()) / sp
    return g, (nx + ny) / (nx * ny) + g ** 2 / (2 * (nx + ny))


def dersimonian_laird(g, v):
    g, v = np.asarray(g), np.asarray(v); w = 1 / v
    fe = (w * g).sum() / w.sum(); Q = (w * (g - fe) ** 2).sum(); k = len(g)
    tau2 = max(0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    ws = 1 / (v + tau2); mu = (ws * g).sum() / ws.sum(); se = np.sqrt(1 / ws.sum())
    return mu, se, 2 * stats.norm.sf(abs(mu / se)), (max(0, (Q - (k - 1)) / Q) if Q > 0 else 0)


def clr(df):
    L = np.log(df + 0.5); return L - L.mean(0)


def da(gcounts, a, b, prev=0.2):
    """Abundância diferencial de gêneros: CLR + Mann-Whitney + BH. a, b = listas de amostras."""
    X = gcounts[list(a) + list(b)]; X = X.loc[(X > 0).mean(1) >= prev]
    C = clr(X); Ca, Cb = C[list(a)], C[list(b)]
    diff = Ca.mean(1) - Cb.mean(1)
    p = np.array([stats.mannwhitneyu(Ca.loc[g], Cb.loc[g]).pvalue for g in C.index])
    q = multipletests(p, method='fdr_bh')[1]
    return pd.DataFrame({'dCLR': diff, 'p': p, 'q': q}).sort_values('p')


def resumo_contraste(nome, a, b, rare, alpha, gcounts, strata=None, meta=None, extra_terms=(), perms=999):
    """Métricas padronizadas de um contraste A × B: PERMANOVA (BC, ASV), g de Shannon/riqueza, nº de gêneros DA."""
    s = list(a) + list(b)
    mm = pd.DataFrame({'GRUPO': ['A'] * len(a) + ['B'] * len(b)}, index=s)
    if meta is not None:
        for t in extra_terms: mm[t] = meta.loc[s, t].values
    D = dist(rare, s).data
    r = permanova(D, mm, list(extra_terms) + ['GRUPO'], perms=perms, strata=strata)
    gS, _ = hedges_g(alpha.loc[a, 'Shannon'], alpha.loc[b, 'Shannon'])
    gR, _ = hedges_g(alpha.loc[a, 'Riqueza'], alpha.loc[b, 'Riqueza'])
    d = da(gcounts, a, b)
    return dict(contraste=nome, n_A=len(a), n_B=len(b), R2=r.at['GRUPO', 'R2'], p_perm=r.at['GRUPO', 'p'],
                g_Shannon=gS, g_Riqueza=gR, pct_Riqueza=100 * (alpha.loc[a, 'Riqueza'].median() / alpha.loc[b, 'Riqueza'].median() - 1),
                n_generos_q05=int((d.q < .05).sum()), n_generos_testados=len(d),
                p_disp=dispersao(D, mm.GRUPO)[1]), d
