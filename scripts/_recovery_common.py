from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.duration.hazard_regression import PHReg
BASE = Path(__file__).resolve().parents[1]
rec=pd.read_csv(BASE/'data_processed/recovery_events.csv')
mem=pd.read_csv(BASE/'data_processed/groundwater_memory.csv')
q=rec.query('recovery_eligible == 1 and group in ["D", "M"]').merge(mem[['well','detrended_M12']],on='well',validate='many_to_one')
q=q[q.time_months.notna() & q.drought_duration.gt(0) & q.drought_min_sgi.notna()].copy()
q['event']=(q.outcome=='recovered').astype(int)
q['memory_z']=(q.detrended_M12-mem.query('group in ["D", "M"]').detrended_M12.mean())/mem.query('group in ["D", "M"]').detrended_M12.std(ddof=1)
q['log_duration']=np.log(q.drought_duration)
q['dune']=(q.group=='D').astype(int)
COV=['memory_z','log_duration','drought_min_sgi','dune']
def fit(data, robust=False):
 return PHReg(data.time_months.to_numpy(float),data[COV].to_numpy(float),status=data.event.to_numpy(int),ties='efron').fit(groups=data.well.to_numpy() if robust else None,disp=0)
