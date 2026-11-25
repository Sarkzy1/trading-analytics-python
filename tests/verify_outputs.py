"""Verify key outputs of the synthetic trading journal capstone."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/processed/trading_journal_cleaned.csv'
assert path.is_file(), 'Run the notebook before checking outputs.'
df=pd.read_csv(path,parse_dates=['Trade_Date']).sort_values(['Trade_Date','Trade_ID'])
assert len(df)==39 and df['Trade_ID'].is_unique
cols=['Realized_PnL_USD','Entry_Price','Exit_Price','Position_Size_Lots']
assert np.isfinite(df[cols].to_numpy(float)).all()
assert (df[['Entry_Price','Exit_Price','Position_Size_Lots']]>0).all().all()
p=df['Realized_PnL_USD'].to_numpy(float)
assert math.isclose(p.sum(),-215.46,abs_tol=0.01)
assert math.isclose(100*(p>0).mean(),48.7179487179,abs_tol=0.01)
peak=np.maximum(0,np.maximum.accumulate(np.cumsum(p)))
assert math.isclose((peak-np.cumsum(p)).max(),427.88,abs_tol=0.01)
unflagged=df.loc[df['Quality_Status']=='Passed_Checks']
assert len(unflagged)==35 and math.isclose(unflagged['Realized_PnL_USD'].sum(),-194.46,abs_tol=0.01)
for file in ['figures/trading_dashboard.png','figures/trading_dashboard.pdf','reports/analytical_report.md','reports/analytical_report.pdf','reports/data_quality_report.csv']:
    assert (ROOT/file).stat().st_size>100
assert (ROOT/'reports/analytical_report.md').read_text()==(ROOT/'reports/analytical_report_reviewed.md').read_text()
print('PASS: metrics, dashboard, audit outputs and reviewed report')
