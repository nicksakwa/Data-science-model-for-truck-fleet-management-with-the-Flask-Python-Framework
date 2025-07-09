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