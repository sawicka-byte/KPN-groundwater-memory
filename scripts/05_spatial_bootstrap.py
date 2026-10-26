from _recovery_common import *
import collections,math,warnings,argparse
parser=argparse.ArgumentParser()
parser.add_argument('--replicates',type=int,default=220)
args=parser.parse_args()
coords=pd.read_csv(BASE/'data_context/well_coordinates_epsg2180.csv').set_index('well')
assert q.well.isin(coords.index).all(),'Missing spatial coordinates'
rows=[]
for sc in (3,6,12):
 d=q[q.scale==sc].copy().reset_index(drop=True)
 t=d.time_months.to_numpy(float);ev=d.event.to_numpy(int);x=d[COV].to_numpy(float);w=d.well.to_numpy()
 orig=fit(d,robust=True)
 for width,shift in ((4000,0),(4000,2000),(8000,0),(8000,4000)):
  blocks=collections.defaultdict(list)
  for i,well in enumerate(w):
   c=coords.loc[well];key=(math.floor((c.x_epsg2180+shift)/width),math.floor((c.y_epsg2180+shift)/width));blocks[key].append(i)
  keys=sorted(blocks);rng=np.random.default_rng(46000+sc*100+width+shift);out=[];fail=0
  for z in range(args.replicates):
   ids=np.concatenate([np.asarray(blocks[keys[k]],int) for k in rng.integers(0,len(keys),size=len(keys))])
   if np.unique(x[ids,-1]).size<2:fail+=1;continue
   try:
    with warnings.catch_warnings():
     warnings.simplefilter('ignore')
     f=PHReg(t[ids],x[ids],status=ev[ids],ties='efron').fit(disp=0)
    v=float(np.exp(f.params[0]))
    if np.isfinite(v) and v>0:out.append(v)
    else:fail+=1
   except Exception:fail+=1
  rows.append(dict(scale=sc,grid_m=width,offset_m=shift,blocks=len(keys),B_requested=args.replicates,B_valid=len(out),B_failed=fail,HR_original=float(np.exp(orig.params[0])),CI_low=np.percentile(out,2.5) if out else np.nan,CI_high=np.percentile(out,97.5) if out else np.nan,frac_HR_ge_1=np.mean(np.asarray(out)>=1) if out else np.nan))
  pd.DataFrame(rows).to_csv(BASE/'outputs/spatial_block_bootstrap_S5.csv',index=False)
  print('Done:',sc,width,shift,'valid',len(out),flush=True)
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(OUT/'spatial_block_bootstrap_S5.csv',index=False)
print('Saved',OUT/'spatial_block_bootstrap_S5.csv')
