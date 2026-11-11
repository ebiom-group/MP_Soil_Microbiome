"""Seção 9 do notebook principal: t-SNE, modelos lineares, heatmaps, ISA (IndVal) e db-RDA (Bray–Curtis).
Importado por build_notebook.py (usa as funções md() e code() de lá)."""


def adicionar(md, code):
    md(r"""
## 9. Análises adicionais: t‑SNE, modelos lineares, heatmaps, ISA e db‑RDA

| Análise | Pergunta | Onde |
|---|---|---|
| **t‑SNE** (Bray–Curtis) | como as amostras se agrupam, visto de forma não linear | 9.1 |
| **Modelos lineares** | diversidade alfa com interações; gêneros que respondem ao tratamento (efeito fixo de estrato, estilo MaAsLin2) | 9.2 |
| **Heatmaps** | padrões de abundância dos gêneros‑chave; R² por projeto × fator | 9.3 |
| **ISA / IndVal** | quais gêneros são *indicadores* de cada compartimento/classe de plástico/polímero | 9.4 |
| **db‑RDA** (Bray–Curtis) | ordenação restrita: quanto da composição os fatores explicam e em que direção | 9.5 |
""")

    # ------------------------------------------------------------------ 9.1 t-SNE
    md(r"""
### 9.1 t‑SNE sobre Bray–Curtis
t‑SNE com distância pré‑computada (Bray–Curtis). Serve **só para visualização**: distâncias entre grupos distantes e
tamanhos de cluster não têm interpretação quantitativa. Testamos 3 perplexidades para verificar se os agrupamentos são estáveis.
""")
    code(r"""
from sklearn.manifold import TSNE
def tsne(D, perplexity=30, seed=42):
    return TSNE(n_components=2, metric='precomputed', init='random', perplexity=perplexity,
                random_state=seed, max_iter=2000).fit_transform(np.asarray(D))

TS = pd.DataFrame(tsne(bc_gen.data), index=gen_rel.columns, columns=['tSNE1', 'tSNE2']).join(meta)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
for ax, (hue, st) in zip(axes.flat, [('BIOPROJECT', 'REGIAO'), ('COMPARTIMENTO', None), ('CLASSE', None), ('COUNTRY', None)]):
    sns.scatterplot(data=TS, x='tSNE1', y='tSNE2', hue=hue, style=st, s=20, alpha=.85, ax=ax, palette='tab10')
    ax.set_title(f't-SNE (Bray–Curtis, gênero, perplexidade 30) — {hue}'); ax.legend(fontsize=7)
savefig('09_tsne_global')

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for ax, perp in zip(axes, [10, 30, 50]):
    e = pd.DataFrame(tsne(bc_gen.data, perp), index=gen_rel.columns, columns=['t1', 't2']).join(meta)
    sns.scatterplot(data=e, x='t1', y='t2', hue='BIOPROJECT', style='COMPARTIMENTO', s=14, ax=ax, legend=(perp == 50))
    ax.set_title(f'perplexidade {perp}')
axes[-1].legend(fontsize=6, bbox_to_anchor=(1, 1)); savefig('09_tsne_perplexidade')
""")
    code(r"""
# t-SNE dentro dos desenhos com plástico e controle (ASV, rarefeito): o tratamento aparece quando o estudo é fixado?
fig, axes = plt.subplots(2, 4, figsize=(22, 10))
for ax, (pj, mm) in zip(axes.flat, [(p, d) for p, d in meta.groupby('BIOPROJECT') if len(d) >= 12]):
    s = list(mm.index); X = rare[s]; X = X.loc[X.sum(1) > 0]
    D = beta_diversity('braycurtis', X.T.values, ids=s).data
    e = pd.DataFrame(tsne(D, perplexity=min(30, (len(s) - 1) // 3)), index=s, columns=['t1', 't2']).join(meta)
    sns.scatterplot(data=e, x='t1', y='t2', hue='POLYMER', style='COMPARTIMENTO', s=40, ax=ax, palette='tab10')
    ax.set_title(pj, fontsize=10); ax.legend(fontsize=6)
savefig('09_tsne_por_projeto')
""")

    # ------------------------------------------------------------------ 9.2 modelos lineares
    md(r"""
### 9.2 Modelos lineares

**(a) Diversidade alfa.** Dois modelos, nos estratos que têm controle (sem papel):
* **ANOVA tipo II** com projeto como efeito fixo: `métrica ~ projeto + CLASSE × fração`
* **Modelo misto** com interação: `métrica ~ CLASSE × fração + (1 | projeto)`

**(b) Gêneros (estilo MaAsLin2).** Para cada gênero (prevalência ≥ 25 %): `CLR ~ CLASSE + estrato` (estrato = projeto × fração como
efeito fixo, ou seja, compara plástico e controle **dentro** de cada estrato). Coeficientes vs. controle, FDR (BH).
""")
    code(r"""
from statsmodels.stats.anova import anova_lm
sub = A[A.ESTRATO.isin(ef.projeto.unique()) & A.CLASSE.ne('Papel')].copy()
sub['CLASSE'] = pd.Categorical(sub.CLASSE, ['Controle', 'Biodegradável', 'Não biodegradável'])
rows, anovas = [], {}
for mt in ['Riqueza', 'Shannon', 'FaithPD', 'Pielou']:
    sub['y'] = (sub[mt] - sub[mt].mean()) / sub[mt].std()
    ols = smf.ols('y ~ C(BIOPROJECT) + CLASSE * SOIL_FRACTION', sub).fit()
    anovas[mt] = anova_lm(ols, typ=2)
    lmm = smf.mixedlm('y ~ CLASSE * SOIL_FRACTION', sub, groups=sub.BIOPROJECT).fit(reml=True)
    for t in lmm.params.index:
        if t.startswith('CLASSE'):
            rows.append(dict(metrica=mt, termo=t, coef_DP=lmm.params[t], IC95_inf=lmm.conf_int().loc[t, 0],
                             IC95_sup=lmm.conf_int().loc[t, 1], p=lmm.pvalues[t]))
LM_alfa = pd.DataFrame(rows); LM_alfa.round(4).to_csv(TAB / '09_lm_alfa_misto.csv', index=False)
AN = pd.concat({k: v[['F', 'PR(>F)']] for k, v in anovas.items()}, axis=1); AN.round(4).to_csv(TAB / '09_lm_alfa_anova.csv')
print('ANOVA tipo II (projeto como efeito fixo):'); display(AN.round(4))
print('Modelo misto (coeficientes em desvios-padrão, referência = Controle na fração Bulk):'); display(LM_alfa.round(3))

fig, ax = plt.subplots(figsize=(9, 5))
d = LM_alfa.copy(); d['lbl'] = d.metrica + ' | ' + d.termo.str.replace('CLASSE[T.', '', regex=False).str.replace(']', '', regex=False)
d = d.iloc[::-1].reset_index(drop=True)
ax.errorbar(d.coef_DP, d.index, xerr=[d.coef_DP - d.IC95_inf, d.IC95_sup - d.coef_DP], fmt='o', c='k', capsize=3)
ax.set_yticks(d.index, d.lbl, fontsize=7); ax.axvline(0, ls='--', c='grey'); ax.set_xlabel('coeficiente (DP) vs controle')
ax.set_title('Modelo linear misto da diversidade alfa'); savefig('09_lm_alfa_coef')
""")
    code(r"""
def lm_generos(samples, termo='CLASSE', ref='Controle', bloco='ESTRATO', prev=0.25):
    '''OLS vetorizado para todos os gêneros: CLR ~ termo + bloco (efeito fixo). Retorna coef, EP, p, q por nível.'''
    mm = meta.loc[samples]; X = gcounts[samples]; X = X.loc[(X > 0).mean(1) >= prev]
    Y = clr(X).T.values                                                     # amostras × gêneros
    lv = [l for l in mm[termo].unique() if l != ref]
    Xd = np.column_stack([np.ones(len(mm))] + [(mm[termo] == l).values.astype(float) for l in lv] +
                         [pd.get_dummies(mm[bloco], drop_first=True).values.astype(float)])
    XtX_inv = np.linalg.pinv(Xd.T @ Xd); B = XtX_inv @ Xd.T @ Y
    res = Y - Xd @ B; dfr = len(mm) - np.linalg.matrix_rank(Xd); s2 = (res ** 2).sum(0) / dfr
    out = []
    for i, l in enumerate(lv, start=1):
        se = np.sqrt(XtX_inv[i, i] * s2); t = B[i] / se; p = 2 * stats.t.sf(np.abs(t), dfr)
        out.append(pd.DataFrame({'nivel': l, 'coef': B[i], 'EP': se, 't': t, 'p': p}, index=X.index))
    out = pd.concat(out); out['q'] = out.groupby('nivel').p.transform(lambda p: multipletests(p, method='fdr_bh')[1])
    return out.join(tax_g[['Phylum', 'Family']])

s_ctrl = list(sub.index)
LMG = lm_generos(s_ctrl); LMG.round(4).to_csv(TAB / '09_lm_generos.csv')
for nv, d in LMG.groupby('nivel'):
    print(f'{nv} vs Controle: {(d.q < .05).sum()} de {len(d)} gêneros com q < 0.05 (↑ {((d.q < .05) & (d.coef > 0)).sum()} / ↓ {((d.q < .05) & (d.coef < 0)).sum()})')
display(LMG[LMG.q < .05].sort_values('coef').round(3).groupby('nivel').head(12))

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
for ax, (nv, d) in zip(axes, LMG.groupby('nivel')):
    sig = d.q < .05
    ax.scatter(d.coef, -np.log10(d.p), s=8, c=np.where(sig, np.where(d.coef > 0, 'firebrick', 'steelblue'), 'lightgrey'))
    for g, r in d[sig].sort_values('p').head(10).iterrows(): ax.annotate(g, (r.coef, -np.log10(r.p)), fontsize=6)
    ax.axvline(0, c='k', lw=.6); ax.set_title(f'{nv} vs Controle'); ax.set_xlabel('coeficiente (Δ CLR)')
axes[0].set_ylabel('-log10(p)'); savefig('09_lm_generos_volcano')
""")

    # ------------------------------------------------------------------ 9.3 heatmaps
    md("### 9.3 Heatmaps")
    code(r"""
# (a) R² da PERMANOVA por projeto × fator (Bray–Curtis, ASV)
H = PP[PP.metrica == 'braycurtis'].pivot_table(index='projeto', columns='termo', values='R2')
Hp = PP[PP.metrica == 'braycurtis'].pivot_table(index='projeto', columns='termo', values='p')
annot = H.map(lambda v: '' if pd.isna(v) else f'{v:.2f}') + Hp.map(lambda p: '' if pd.isna(p) else ('***' if p < .001 else '**' if p < .01 else '*' if p < .05 else ''))
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(H, annot=annot, fmt='', cmap='rocket_r', vmin=0, vmax=.5, ax=ax, cbar_kws={'label': 'R²'}, linewidths=.5, linecolor='white')
ax.set_title('R² da PERMANOVA por projeto e fator (* p<0,05, ** p<0,01, *** p<0,001)'); savefig('09_heatmap_R2_permanova')
""")
    code(r"""
# (b) gêneros-chave (linear model q<0,05 + núcleo da plastisfera): CLR médio padronizado por compartimento × classe
chave = list(dict.fromkeys(list(LMG[LMG.q < .05].index) + list(plast.index[:30])))
chave = [g for g in chave if g in gcounts.index]
C_all = clr(gcounts.loc[gcounts.index.isin(chave) | ((gcounts > 0).mean(1) >= .2)]).loc[chave]
grp = meta.COMPARTIMENTO + ' | ' + meta.CLASSE
Hm = C_all.T.groupby(grp).mean().T
Hm = Hm[[c for c in Hm.columns if (grp == c).sum() >= 5]]
Hz = Hm.sub(Hm.mean(1), axis=0).div(Hm.std(1), axis=0)
row_col = pd.Series(['#c0392b' if g in plast.index and plast.at[g, 'direcao'].startswith('enr') else
                     '#2e86c1' if g in plast.index else '#7f8c8d' for g in Hz.index], index=Hz.index)
cg = sns.clustermap(Hz, cmap='RdBu_r', center=0, figsize=(11, max(8, .22 * len(Hz))), row_colors=row_col,
                    xticklabels=True, yticklabels=True, cbar_kws={'label': 'CLR médio (z)'}, dendrogram_ratio=(.12, .08))
cg.ax_heatmap.tick_params(axis='y', labelsize=6); cg.ax_heatmap.tick_params(axis='x', labelsize=8, rotation=60)
cg.fig.suptitle('Gêneros-chave: modelo linear (cinza) e núcleo da plastisfera (vermelho ↑ / azul ↓)', y=1.01)
plt.savefig(FIG / '09_heatmap_generos_chave.png', dpi=150); plt.show()
""")

    # ------------------------------------------------------------------ 9.4 ISA
    md(r"""
### 9.4 Indicator Species Analysis (ISA, IndVal.g)
IndVal de Dufrêne & Legendre (versão **IndVal.g**, corrigida para tamanhos de grupo desiguais):
`IndVal = √(A × B)`, onde **A** = especificidade (quanto da abundância média do gênero está naquele grupo) e
**B** = fidelidade (fração das amostras do grupo em que o gênero ocorre). Significância por 999 permutações dos rótulos
**restritas dentro de cada estudo/desenho**, e FDR (BH). Nível de gênero, abundância relativa.
""")
    code(r"""
def indval(samples, grupo, strata=None, perms=999, prev=0.05, seed=0):
    mm = meta.loc[samples]; X = gcounts[samples]; X = (X / X.sum()); X = X.loc[(X > 0).mean(1) >= prev]
    M = X.T.values; g = mm[grupo].astype(str).values; G = np.unique(g)
    def stat(lbl):
        mean = np.stack([M[lbl == k].mean(0) for k in G]); A_ = mean / np.clip(mean.sum(0, keepdims=True), 1e-300, None)
        B_ = np.stack([(M[lbl == k] > 0).mean(0) for k in G]); return np.sqrt(A_ * B_), A_, B_
    IV, A_, B_ = stat(g); best = IV.argmax(0); obs = IV.max(0)
    rng = np.random.default_rng(seed); cnt = np.ones(M.shape[1])
    blocks = [np.arange(len(g))] if strata is None else [np.where(mm[strata].values == s)[0] for s in mm[strata].unique()]
    for _ in range(perms):
        gp = g.copy()
        for b in blocks: gp[b] = rng.permutation(g[b])
        cnt += stat(gp)[0].max(0) >= obs - 1e-12
    r = pd.DataFrame({'grupo': G[best], 'IndVal': obs, 'A_especificidade': A_[best, range(len(best))],
                      'B_fidelidade': B_[best, range(len(best))], 'p': cnt / (perms + 1)}, index=X.index)
    r['q'] = multipletests(r.p, method='fdr_bh')[1]
    return r.join(tax_g[['Phylum', 'Family']]).sort_values(['grupo', 'IndVal'], ascending=[True, False])

def mostra_isa(r, n=12, nome=''):
    s = r[(r.q < .05) & (r.IndVal >= .5)]
    print(f'{nome}: {len(s)} indicadores (q<0,05 e IndVal≥0,5) —', s.grupo.value_counts().to_dict())
    display(s.groupby('grupo').head(n).round(3))

# (i) compartimento: desenhos com plastisfera e solo com o mesmo plástico
meta['DESENHO'] = np.select([meta.COLETA.eq('2016-09') & meta.SITIO.eq('Knoxville-TN'), meta.COLETA.eq('2016-09') & meta.SITIO.eq('MountVernon-WA'),
                             meta.BIOPROJECT.eq('PRJNA702448'), meta.BIOPROJECT.eq('PRJNA630025')], ['EUA-TN', 'EUA-WA', 'PBSA-DE', 'Alpes/Artico'], '')
s_i = list(meta.index[meta.DESENHO.ne('') & meta.CLASSE.isin(['Biodegradável', 'Não biodegradável'])])
ISA_comp = indval(s_i, 'COMPARTIMENTO', strata='DESENHO'); ISA_comp.round(4).to_csv(TAB / '09_isa_compartimento.csv')
mostra_isa(ISA_comp, nome='Compartimento (plastisfera × solo)')
""")
    code(r"""
# (ii) classe do plástico no solo/rizosfera (estratos com controle), permutação dentro do estrato
ISA_classe = indval(s_ctrl, 'CLASSE', strata='ESTRATO'); ISA_classe.round(4).to_csv(TAB / '09_isa_classe.csv')
mostra_isa(ISA_classe, nome='Classe (controle / biodegradável / não biodegradável)')
# (iii) polímero na plastisfera de campo (PRJNA631499), permutação dentro do sítio
s_pl = list(meta.index[meta.BIOPROJECT.eq('PRJNA631499')])
ISA_pol = indval(s_pl, 'POLYMER', strata='SITIO'); ISA_pol.round(4).to_csv(TAB / '09_isa_polimero_plastisfera.csv')
mostra_isa(ISA_pol, nome='Polímero na plastisfera de campo')
""")
    code(r"""
fig, axes = plt.subplots(1, 3, figsize=(20, 7))
for ax, (r, t) in zip(axes, [(ISA_comp, 'Compartimento'), (ISA_classe, 'Classe de plástico'), (ISA_pol, 'Polímero (plastisfera)')]):
    top = r[(r.q < .05)].sort_values('IndVal', ascending=False).groupby('grupo').head(8).sort_values(['grupo', 'IndVal'])
    if top.empty: ax.set_title(f'{t}: nenhum indicador significativo'); continue
    sns.barplot(data=top.reset_index(), y='LABEL' if 'LABEL' in top.reset_index() else 'index', x='IndVal', hue='grupo', dodge=False, ax=ax)
    ax.set_title(f'ISA — {t}'); ax.set_ylabel(''); ax.tick_params(axis='y', labelsize=7); ax.legend(fontsize=7)
savefig('09_isa_indicadores')
""")

    # ------------------------------------------------------------------ 9.5 db-RDA
    md(r"""
### 9.5 db‑RDA (análise de redundância baseada em distância, Bray–Curtis)
Implementação equivalente a `vegan::capscale/dbrda`: PCoA da matriz de Bray–Curtis (eixos com autovalor positivo) →
regressão multivariada nas variáveis explicativas → PCA dos valores ajustados (eixos **CAP**). Testes por permutação
(999) do modelo e de cada termo (**marginal**, isto é, condicionado aos demais). Versão **parcial** remove primeiro o efeito do projeto.
""")
    code(r"""
def _dm(mm, terms):
    cols = []
    for t in terms:
        c = mm[t]
        if pd.api.types.is_numeric_dtype(c):
            c = c.fillna(c.mean()); cols.append(((c - c.mean()) / (c.std() or 1)).values[:, None])
        else:
            cols.append(pd.get_dummies(c.astype(object).fillna('NA').astype(str), drop_first=True).values.astype(float))
    return np.hstack(cols) if cols else np.zeros((len(mm), 0))

def dbrda(D, mm, constr, cond=(), perms=999, strata=None, seed=0):
    D = np.asarray(D); n = len(D); J = np.eye(n) - 1 / n; G = J @ (-0.5 * D ** 2) @ J
    w, V = np.linalg.eigh(G); pos = w > 1e-10 * w.max()
    Y = V[:, pos] * np.sqrt(w[pos]); inercia_neg = -w[w < 0].sum()
    tot = (Y ** 2).sum()
    Z = _dm(mm, cond); Z = Z - Z.mean(0) if Z.size else Z
    def resid(M, Zm):
        return M - Zm @ np.linalg.pinv(Zm) @ M if Zm.size else M
    Yr = resid(Y, Z); inercia_cond = tot - (Yr ** 2).sum()
    def ajuste(Ym, Xm):
        Xm = resid(Xm - Xm.mean(0), Z); H = Xm @ np.linalg.pinv(Xm); F_ = H @ Ym
        return F_, np.linalg.matrix_rank(Xm)
    X = _dm(mm, constr); Yfit, df = ajuste(Yr, X)
    ss_c = (Yfit ** 2).sum(); ss_r = ((Yr - Yfit) ** 2).sum(); dfr = n - 1 - (np.linalg.matrix_rank(Z) if Z.size else 0) - df
    Fobs = (ss_c / df) / (ss_r / dfr)
    rng = np.random.default_rng(seed)
    blocks = [np.arange(n)] if strata is None else [np.where(np.asarray(strata) == s)[0] for s in np.unique(strata)]
    def perm_p(Ym, Xm, d_, Fo):
        c = 1
        for _ in range(perms):
            p = np.arange(n)
            for b in blocks: p[b] = rng.permutation(b)
            Yp = Ym[p]; Fp_, _ = ajuste(Yp, Xm); sc = (Fp_ ** 2).sum(); sr = ((Yp - Fp_) ** 2).sum()
            c += (sc / d_) / (sr / dfr) >= Fo - 1e-12
        return c / (perms + 1)
    p_modelo = perm_p(Yr, X, df, Fobs)
    termos = []
    for t in constr:                                            # teste marginal de cada termo
        outros = [u for u in constr if u != t]
        Zt = np.hstack([Z, _dm(mm, outros)]) if (Z.size or outros) else Z
        Zt = Zt - Zt.mean(0) if Zt.size else Zt
        Yt = resid(Y, Zt); Xt = resid(_dm(mm, [t]) - _dm(mm, [t]).mean(0), Zt)
        Ht = Xt @ np.linalg.pinv(Xt); Ft = Ht @ Yt; dft = np.linalg.matrix_rank(Xt)
        if dft == 0:
            termos.append(dict(termo=t, gl=0, R2_marginal=0.0, F=np.nan, p=np.nan)); continue
        sct = (Ft ** 2).sum(); srt = ((Yt - Ft) ** 2).sum()
        Fo = (sct / dft) / (srt / dfr); c = 1
        for _ in range(perms):
            p = np.arange(n)
            for b in blocks: p[b] = rng.permutation(b)
            Yp = Yt[p]; Fp_ = Ht @ Yp; c += ((Fp_ ** 2).sum() / dft) / (((Yp - Fp_) ** 2).sum() / dfr) >= Fo - 1e-12
        termos.append(dict(termo=t, gl=dft, R2_marginal=sct / tot, F=Fo, p=c / (perms + 1)))
    U, S, Vt = np.linalg.svd(Yfit, full_matrices=False)
    k = int(min(df, (S > 1e-10).sum())); eig = S[:k] ** 2
    lc = Yfit @ Vt[:k].T; wa = Yr @ Vt[:k].T
    Xs = resid(X - X.mean(0), Z)
    return dict(R2_restrito=ss_c / tot, R2_condicional=inercia_cond / tot, F=Fobs, gl=df, p=p_modelo,
                prop_eixos=eig / tot, lc=lc, wa=wa, X=Xs, termos=pd.DataFrame(termos).set_index('termo'),
                inercia_neg_rel=inercia_neg / (tot + inercia_neg))

def resumo_dbrda(r, nome):
    print(f"{nome}: restrito R² = {r['R2_restrito']:.3f} (F = {r['F']:.2f}, p = {r['p']:.3f})"
          + (f"; condicional (removido) = {r['R2_condicional']:.3f}" if r['R2_condicional'] > 1e-9 else '')
          + f"; CAP1 = {r['prop_eixos'][0]*100:.1f}%" + (f", CAP2 = {r['prop_eixos'][1]*100:.1f}%" if len(r['prop_eixos']) > 1 else '')
          + f"; inércia negativa = {r['inercia_neg_rel']*100:.1f}%")
    display(r['termos'].round(4))

def plot_dbrda(r, mm, hue, style=None, ax=None, title='', generos=None, abund=None, n_gen=8):
    k = r['wa'].shape[1]
    d = pd.DataFrame(r['wa'][:, :2] if k >= 2 else np.column_stack([r['wa'][:, 0], np.zeros(len(mm))]),
                     index=mm.index, columns=['CAP1', 'CAP2']).join(mm[[hue] + ([style] if style else [])])
    sns.scatterplot(data=d, x='CAP1', y='CAP2', hue=hue, style=style, s=28, alpha=.8, ax=ax, palette='tab10')
    cen = d.groupby(hue)[['CAP1', 'CAP2']].mean()
    ax.scatter(cen.CAP1, cen.CAP2, marker='X', s=160, c='k')
    for lv, rr in cen.iterrows(): ax.annotate(str(lv), (rr.CAP1, rr.CAP2), fontsize=7, weight='bold')
    if abund is not None:                                     # gêneros: correlação com CAP1/CAP2 (setas)
        Cb = clr(abund[mm.index]); Cb = Cb.loc[(abund[mm.index] > 0).mean(1) >= .25]
        cor = pd.DataFrame({ax_: Cb.T.corrwith(d[ax_]) for ax_ in ['CAP1', 'CAP2']})
        top = cor.pow(2).sum(1).sort_values(ascending=False).head(n_gen).index
        sc = np.abs(d[['CAP1', 'CAP2']]).max().min() * .9
        for g_ in top:
            ax.arrow(0, 0, cor.at[g_, 'CAP1'] * sc, cor.at[g_, 'CAP2'] * sc, color='dimgrey', alpha=.7, head_width=sc * .03)
            ax.annotate(g_, (cor.at[g_, 'CAP1'] * sc * 1.08, cor.at[g_, 'CAP2'] * sc * 1.08), fontsize=6, color='dimgrey')
    pe = r['prop_eixos'] * 100
    ax.set_xlabel(f'CAP1 ({pe[0]:.1f}%)'); ax.set_ylabel(f'CAP2 ({pe[1]:.1f}%)' if len(pe) > 1 else 'CAP2')
    ax.set_title(title, fontsize=10); ax.legend(fontsize=6)
""")
    code(r"""
# (a) db-RDA PARCIAL global (gênero): efeito de fração + classe, removido o efeito do projeto
mt_ = meta.loc[gen_rel.columns]
r_glob = dbrda(bc_gen.data, mt_, ['SOIL_FRACTION', 'CLASSE'], cond=['BIOPROJECT'], perms=199, strata=mt_.BIOPROJECT.values)
resumo_dbrda(r_glob, 'db-RDA parcial global | Condition(projeto)')
fig, ax = plt.subplots(1, 2, figsize=(15, 6))
plot_dbrda(r_glob, mt_, 'COMPARTIMENTO', None, ax[0], 'db-RDA parcial — compartimento (projeto removido)', abund=gcounts)
plot_dbrda(r_glob, mt_, 'CLASSE', 'COMPARTIMENTO', ax[1], 'db-RDA parcial — classe')
savefig('09_dbrda_global_parcial')
""")
    code(r"""
# (b) db-RDA ambiental: variáveis de solo/clima (amostras com dados completos). ATENÇÃO: confundido com o projeto.
env_v = ['pH', 'SOC(g/kg)', 'C/N', 'ANNUAL_RAINFALL(mm)', 'AVG_ANNUAL_TEMPERATURE']
ok = mt_[env_v].notna().all(1); s_env = list(mt_.index[ok])
idx = [list(gen_rel.columns).index(s) for s in s_env]
mm_env = mt_.loc[s_env].rename(columns=lambda c: c.replace('(', '_').replace(')', '').replace('/', '_'))
env_c = [c.replace('(', '_').replace(')', '').replace('/', '_') for c in env_v]
Xv = mm_env[env_c]; vif = pd.Series(np.diag(np.linalg.pinv(np.corrcoef(Xv.values, rowvar=False))), index=env_c)
print('Projetos com dados completos:', mm_env.BIOPROJECT.value_counts().to_dict()); print('VIF:', vif.round(1).to_dict())
r_env = dbrda(bc_gen.data[np.ix_(idx, idx)], mm_env, env_c, perms=199)
resumo_dbrda(r_env, 'db-RDA ambiental (permutação livre — n efetivo = nº de locais!)')
fig, ax = plt.subplots(figsize=(8, 6))
plot_dbrda(r_env, mm_env, 'BIOPROJECT', 'COMPARTIMENTO', ax, 'db-RDA ambiental (Bray–Curtis, gênero)')
lcs = np.abs(r_env['wa'][:, :2]).max(0).min() * .9
for j, v in enumerate(env_c):
    c1 = np.corrcoef(r_env['X'][:, j], r_env['lc'][:, 0])[0, 1]; c2 = np.corrcoef(r_env['X'][:, j], r_env['lc'][:, 1])[0, 1]
    ax.arrow(0, 0, c1 * lcs, c2 * lcs, color='darkred', head_width=lcs * .03); ax.annotate(v, (c1 * lcs * 1.1, c2 * lcs * 1.1), color='darkred', fontsize=8)
savefig('09_dbrda_ambiental')
""")
    code(r"""
# (c) db-RDA dentro de projetos (ASV, rarefeito, Bray–Curtis)
casos = [('PRJNA564156', ['POLYMER'], ['SITIO', 'COLETA'], 'SITIO'),
         ('PRJNA1054347', ['SOIL_FRACTION', 'POLYMER'], [], None),
         ('PRJNA631499', ['POLYMER'], ['SITIO'], 'SITIO'),
         ('PRJNA702448', ['NITROGENIO', 'SOIL_FRACTION', 'TRAT'], [], None),
         ('PRJNA1155845', ['GLIFOSATO', 'POLYMER'], [], None),
         ('PRJNA1021161', ['DIAS', 'POLYMER', 'ENVELHECIMENTO'], [], None)]
DB = {}
fig, axes = plt.subplots(2, 3, figsize=(21, 12))
for ax, (pj, constr, cond, st) in zip(axes.flat, casos):
    s = list(meta.index[meta.BIOPROJECT == pj]); mm = meta.loc[s].copy()
    X = rare[s]; X = X.loc[X.sum(1) > 0]
    D = beta_diversity('braycurtis', X.T.values, ids=s).data
    r = dbrda(D, mm, constr, cond=cond, perms=499, strata=(mm[cond[0]].values if cond else None))
    DB[pj] = r; resumo_dbrda(r, f'{pj} | constr={constr} | cond={cond}')
    plot_dbrda(r, mm, 'POLYMER' if 'POLYMER' in constr else 'TRAT', st or (constr[0] if constr[0] != 'POLYMER' else None), ax,
               f"{pj}: R² restrito = {r['R2_restrito']:.2f}, p = {r['p']:.3f}", abund=gcounts, n_gen=6)
savefig('09_dbrda_por_projeto')
pd.concat({k: v['termos'] for k, v in DB.items()}).round(4).to_csv(TAB / '09_dbrda_por_projeto_termos.csv')
""")
