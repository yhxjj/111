"""Synthetic-only environment checks. No experimental input or network access."""
import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--out', required=True)
args = parser.parse_args()
out = Path(args.out).resolve()
out.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(out / 'cache' / 'matplotlib')
os.environ['XDG_CACHE_HOME'] = str(out / 'cache')
import socket
def offline(*args, **kwargs):
    raise RuntimeError('Network is disabled for this synthetic test')
socket.create_connection = offline
import requests
requests.sessions.Session.request = offline
import importlib.metadata as metadata
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
from patsy import dmatrices
import gseapy as gp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# The shared style is loaded from the explicitly read omics-plotting Skill.
root = Path(__file__).resolve().parents[2]
skill = (root / '.sciagent-skills/skills/data-visualization/omics-plotting/SKILL.md').read_text()
style_block = skill.split('## Shared style')[1].split('```python\n')[1].split('```')[0]
exec(style_block, globals())
figdir = out / 'figures'
figdir.mkdir(exist_ok=True)
rng = np.random.default_rng(20261102)
# 16 independent synthetic samples, 80 artificial log2 intensity features.
groups = np.repeat(['SIM_Control', 'SIM_Treatment'], 8)
x = rng.normal(10, 0.45, (16, 80))
x[8:, :12] += 1.8
x[8:, 12:24] -= 1.8
x[8:, 24:] += rng.normal(0, 0.25, (8, 56))
genes = [f'SIM_GENE_{i:03}' for i in range(80)]
pd.DataFrame(x, columns=genes).assign(group=groups).to_csv(out/'SIMULATED_log2_intensities.csv', index=False)
t = stats.ttest_ind(x[8:], x[:8], axis=0, equal_var=False)
q = multipletests(t.pvalue, method='fdr_bh')[1]
assert np.isfinite(t.statistic).all() and np.isfinite(q).all()
assert ((q >= 0) & (q <= 1)).all() and (q >= t.pvalue - 1e-12).all()
np.testing.assert_allclose(multipletests([.01, .04, .03, .002], method='fdr_bh')[1], [.02, .04, .04, .008])
fc = x[8:].mean(0)-x[:8].mean(0)
res = pd.DataFrame({'gene':genes, 'log2FoldChange':fc, 'welch_t':t.statistic, 'pvalue':t.pvalue, 'padj':q})
res.to_csv(out/'SIMULATED_welch_bh.csv', index=False)
modeldata = pd.DataFrame({'value':x[:,0], 'group':groups, 'batch':np.tile(['B1','B2'],8)})
design_y, design_x = dmatrices('value ~ C(group) + C(batch)', data=modeldata, return_type='dataframe')
assert design_x.shape == (16, 3) and design_y.shape == (16, 1)
fit = smf.ols('value ~ C(group) + C(batch)', data=modeldata).fit(cov_type='HC3')
assert np.isfinite(fit.params).all() and np.isfinite(fit.conf_int()).all().all()
(out/'SIMULATED_ols_hc3.txt').write_text(fit.summary().as_text())
pca = PCA(n_components=2)
coords = pca.fit_transform(StandardScaler().fit_transform(x))
assert coords.shape == (16,2) and np.isfinite(coords).all()
pd.DataFrame(coords, columns=['PC1','PC2']).assign(group=groups).to_csv(out/'SIMULATED_pca.csv',index=False)
fig,ax=plt.subplots(figsize=(6,5))
sns.scatterplot(x=coords[:,0], y=coords[:,1], hue=groups, palette=['#204897','#e34948'], ax=ax)
ax.set(xlabel=f'PC1 ({pca.explained_variance_ratio_[0]:.1%})', ylabel=f'PC2 ({pca.explained_variance_ratio_[1]:.1%})', title='SIMULATED PCA (n=8 per group)')
for ext in ['png','pdf']: fig.savefig(figdir/f'SIMULATED_pca.{ext}')
plt.close(fig)
up=(fc>=1)&(q<.05); dn=(fc<=-1)&(q<.05); ns=~(up|dn)
fig,ax=plt.subplots(figsize=(6,5))
for mask,color,label in [(ns,NS,'NS'),(dn,DOWN,'Down'),(up,UP,'Up')]:
    ax.scatter(fc[mask],-np.log10(np.clip(q[mask],1e-300,1)),color=color,label=f'{label} ({mask.sum()})',s=20)
for v in [-1,1]: ax.axvline(v,ls='--',color='.5',lw=.8)
ax.axhline(-np.log10(.05),ls='--',color='.5',lw=.8)
ax.set(xlabel='Treatment - Control (log2 intensity)',ylabel='-log10 BH-adjusted p',title='SIMULATED volcano |log2FC| >= 1; q < 0.05')
ax.legend()
for ext in ['png','pdf']: fig.savefig(figdir/f'SIMULATED_volcano.{ext}')
plt.close(fig)
# Artificial gene sets, deliberately unrelated to any organism or pathway.
sets={'SIMULATED_SET_UP':genes[:12], 'SIMULATED_SET_DOWN':genes[12:24], 'SIMULATED_SET_MIXED':genes[::5]}
gmt=out/'SIMULATED_ONLY.gmt'
gmt.write_text(''.join(k+'\tSIMULATED_NOT_SPECIES_ANNOTATION\t'+'\t'.join(v)+'\n' for k,v in sets.items()))
ora = gp.enrich(gene_list=list(np.array(genes)[up]), gene_sets=str(gmt), background=genes, outdir=None, no_plot=True)
assert not ora.results.empty
ora.results.to_csv(out/'SIMULATED_local_ORA.csv', index=False)
ranked = pd.Series(t.statistic,index=genes).sort_values(ascending=False)
pre = gp.prerank(rnk=ranked,gene_sets=str(gmt),min_size=5,max_size=40,permutation_num=100,threads=1,seed=20261102,outdir=None,no_plot=True,verbose=False)
assert not pre.res2d.empty and np.isfinite(pre.res2d['NES'].astype(float)).all()
pre.res2d.to_csv(out/'SIMULATED_local_GSEA.csv', index=False)
versions={n:metadata.version(n) for n in ['numpy','pandas','scipy','statsmodels','patsy','gseapy','matplotlib','seaborn','scikit-learn','openpyxl','requests']}
summary={'data':'SIMULATED ONLY; no species annotation; no biological conclusions', 'seed':20261102,'versions':versions,'tests':{'welch_bh':'PASS','bh_known_values':'PASS','ols_formula_patsy_hc3':'PASS','pca_png_pdf':'PASS','volcano_png_pdf':'PASS','offline_ora_local_gmt':'PASS','offline_prerank_local_gmt':'PASS'},'pca_explained_variance_ratio':pca.explained_variance_ratio_.tolist(),'ora_terms':len(ora.results),'gsea_terms':len(pre.res2d),'gsea_permutations':100}
(out/'test_results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
