from _recovery_common import *
from scipy.stats import spearmanr
from scipy.stats import norm
OUT=BASE/'outputs';OUT.mkdir(exist_ok=True)
results=[]; scho=[]; loo=[]; split=[]
for sc in (3,6,12):
 d=q[q.scale==sc].copy().reset_index(drop=True)
 model=fit(d,robust=True)
 b,se=model.params[0],model.bse[0]
 results.append(dict(scale=sc,n=len(d),recoveries=int(d.event.sum()),wells=d.well.nunique(),HR=np.exp(b),CI_low=np.exp(b-1.96*se),CI_high=np.exp(b+1.96*se)))
 residual=model.schoenfeld_residuals
 for j,v in enumerate(COV):
  ok=(d.event.to_numpy()==1)&np.isfinite(residual[:,j]);rho,p=spearmanr(np.log(d.time_months.to_numpy()[ok]),residual[ok,j])
  scho.append(dict(scale=sc,term=v,n=int(ok.sum()),rho=rho,p_nominal=p))
 for well in sorted(d.well.unique()):
  z=d[d.well!=well]
  try: loo.append(dict(scale=sc,excluded_well=well,HR=np.exp(fit(z).params[0])))
  except Exception: loo.append(dict(scale=sc,excluded_well=well,HR=np.nan))
 # Prespecified t=6 start-stop extended Cox; interactions for memory, duration and minimum SGI
 t=[];entry=[];event=[];X=[];groups=[]
 for r in d.itertuples(index=False):
  x=np.array([r.memory_z,r.log_duration,r.drought_min_sgi,r.dune],float)
  if r.time_months<=6:
   t.append(r.time_months);entry.append(0);event.append(r.event);X.append(list(x)+[0,0,0]);groups.append(r.well)
  else:
   t.append(6);entry.append(0);event.append(0);X.append(list(x)+[0,0,0]);groups.append(r.well)
   t.append(r.time_months);entry.append(6);event.append(r.event);X.append(list(x)+list(x[:3]));groups.append(r.well)
 f=PHReg(np.asarray(t,float),np.asarray(X,float),status=np.asarray(event,int),entry=np.asarray(entry,float),ties='efron').fit(groups=np.asarray(groups),disp=0)
 cov=f.cov_params()
 for j,name in enumerate(['memory_z','log_duration','drought_min_sgi']):
  for label,idx in [('first_6_months',j),('change_after_6',j+4)]:
   beta=f.params[idx];se=f.bse[idx]
   split.append(dict(scale=sc,term=name,period=label,HR=np.exp(beta),CI_low=np.exp(beta-1.96*se),CI_high=np.exp(beta+1.96*se),p_nominal=2*norm.sf(abs(beta/se))))
  beta=f.params[j]+f.params[j+4];se=np.sqrt(cov[j,j]+cov[j+4,j+4]+2*cov[j,j+4])
  split.append(dict(scale=sc,term=name,period='after_6_months',HR=np.exp(beta),CI_low=np.exp(beta-1.96*se),CI_high=np.exp(beta+1.96*se),p_nominal=2*norm.sf(abs(beta/se))))
for name,rows in [('cox_primary.csv',results),('schoenfeld_screen_S3.csv',scho),('cox_split_6mo_S4.csv',split),('cox_leave_one_well_out.csv',loo)]:
 pd.DataFrame(rows).to_csv(OUT/name,index=False)
print(pd.DataFrame(results).to_string(index=False));print('Wrote S3 / S4 screening tables and LOO.')
