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

    distance_data = []
    start_date=pd.to_datetime('2024-01-01')
    end_date=pd.to_datetime('2024-06-30')
    date_range =pd.date_range(start=start_date, end=end_date, freq='D')

    for truck_id in truck_ids:
        idle_prob=np.random.uniform(0.1,0.5)
        for date in date_range:
            if np.random.rand() > idle_prob:
                distance_date.append({
                    'Truck ID': truck_id,
                    'Date': date,
                    'Distance Traveled (miles)':np.random.uniform(50, 600)
                })
            else:
                distance_data.append({
                    'Truck ID': truck_id,
                    'Date': date,
                    'Distance Traveled (miles)':0
                })
    df_distance=pd.DataFrame(distance_data)
    df_distance['Date']=pd.to_datetime(df_distance['Date'])

odometer_data=[]
payroll_weeks=pd.date_range(start='2024-01-01', end='2024-06-30', freq='W')
for truck_id in truck ids:
    current_odometer=np.random.randint(10000, 100000)
    for week_start in payroll_weeks:
        current_odometer+=np.random.randint(500, 3000)
        odometer_data.append({
            'Truck ID': truck_id,
            'Payroll week': week_start,
            'odometer Reading': current_odometer
        })
df_odometer= pd.DataFrame(odometer_data)
df_odometer['Payroll week']=pd.to_datetime(df_odometer['Payroll week'])

stub_data=[]
for truck_id in truck_ids:
    num_entries=np.random.randint(10, 30)
    for _ in range(num_entries):
        stud_data.append({
            'Truck ID': truck_id,
            'Payroll Week':pd.to_datetime('2024-01-01')+ pd.to_timedelta(np.random.randit(0,180), unit='D')
            'Amount':np.random.uniform(1000, 10000)
        })
df_stub=pd.DataFrame(stub_data)
df_stub['Payroll Week']=pd.to_datetime(df_stub['Payroll Week'])