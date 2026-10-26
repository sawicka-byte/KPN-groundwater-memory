from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
e=pd.read_csv(BASE/'data_processed/drought_events.csv');r=pd.read_csv(BASE/'data_processed/recovery_events.csv')
s=e.groupby('SGI_scale').agg(all_runs=('Well','size'),completed=('Fully_observed_episode','sum'))
t=r.groupby('scale').agg(recovery_eligible=('recovery_eligible','sum'))
a=s.join(t)
extra=r.query('recovery_eligible==1 and left_uncertain==1').groupby('scale').size()
a['left_uncertain_but_exit_observed']=extra
a['difference_eligible_minus_complete']=a.recovery_eligible-a.completed
assert a.completed.sum()==961 and a.recovery_eligible.sum()==982
assert a.left_uncertain_but_exit_observed.sum()==21
assert (a.difference_eligible_minus_complete==a.left_uncertain_but_exit_observed).all()
print(a.to_string());print('Total:',a.sum().to_dict())
a.to_csv(BASE/'outputs/drought_to_recovery_eligibility.csv')
