import pandas as pd
import numpy as np
from flask import Flask, render_template_string

app=Flask(__name__)
np.random.seed(42)
num_trucks=20
truck_ids=[f'TRUCK_{i:03d}'for i in range(1, num_trucks + 1)]

data_finance={
    'Truck ID': truck_ids,
    'Monthly Cost':np.random.uniform(500, 2000, num_trucks),
    'Remaining Balance':np.random.uniform(0, 50000, num_trucks),
    'Buyout Price':np.random.uniform(0, 10000, num_trucks),
    'Ownership Type': np.random.choice(['Owned', 'Lease','Financed'], num_trucks, p=[0.3, 0.4, 0.3])
}
df_finance=pd.DataFrame(data_finance)
df_finance.loc[df_finance['Ownership Type']=='Owned',['Remaining balance', 'Buyout Price']]=0

repair_data=[]
for truck_id in truck_ids:
    num_repairs= np.random.randint(0,10)
    for _ in range(num repairs):
        repair_data.append({
            'Truck ID': truck_id,
            'Date':pd.to_datetime('2024-01-01')+ pd.to_timedelta(np.random.randint(0,180), unit='D'),
            'Total Cost':np.random.uniform(50,5000),
            'Odometer Reading':np.random.randint(50000, 500000)
        })
    df_repairs= pd.DataFrame(repairs_data)
    df_repairs['Date']= pd.to_datetime(df_repairs['Date'])