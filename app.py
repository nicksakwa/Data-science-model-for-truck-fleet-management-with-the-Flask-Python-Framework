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

data_truck_paper={
    'Truck ID': truck_ids,
    'Price':np.random.uniform(10000, 60000, num_trucks)
}
df_truck_paper=pd.DataFrame(data_truck_paper)

def get_truck_evaluations():
    # Initialize a main DataFrame to consolidate all truck data
    df_master = pd.DataFrame({'Truck ID': truck_ids})

    # 1. Truck Finance Features
    df_master = df_master.merge(df_finance, on='Truck ID', how='left')
    df_master['Is Paid Off'] = df_master['Remaining Balance'] == 0
    df_master['Total Owed'] = df_master['Remaining Balance'] + df_master['Buyout Price']

    # 2. MaintenancePO_truck Features
    repairs_summary = df_repairs.groupby('Truck ID').agg(
        Total_Repair_Cost=('Total Cost', 'sum'),
        Num_Repairs=('Truck ID', 'count')
    ).reset_index()
    df_master = df_master.merge(repairs_summary, on='Truck ID', how='left')
    df_master['Total_Repair_Cost'] = df_master['Total_Repair_Cost'].fillna(0)
    df_master['Num_Repairs'] = df_master['Num_Repairs'].fillna(0)

    # 3. Vehicle Distance Traveled Features
    distance_summary = df_distance.groupby('Truck ID').agg(
        Total_Miles_Traveled=('Distance Traveled (miles)', 'sum'),
        Avg_Daily_Miles=('Distance Traveled (miles)', 'mean'),
        Std_Dev_Daily_Miles=('Distance Traveled (miles)', 'std'),
        Num_Idle_Days=('Distance Traveled (miles)', lambda x: (x == 0).sum())
    ).reset_index()
    df_master = df_master.merge(distance_summary, on='Truck ID', how='left')
    df_master['Total_Miles_Traveled'] = df_master['Total_Miles_Traveled'].fillna(0)
    df_master['Avg_Daily_Miles'] = df_master['Avg_Daily_Miles'].fillna(0)
    df_master['Std_Dev_Daily_Miles'] = df_master['Std_Dev_Daily_Miles'].fillna(0)
    df_master['Num_Idle_Days'] = df_master['Num_Idle_Days'].fillna(0)

    latest_date = df_distance['Date'].max()
    ten_weeks_ago = latest_date - pd.Timedelta(weeks=10)
    miles_10_weeks = df_distance[df_distance['Date'] >= ten_weeks_ago].groupby('Truck ID')['Distance Traveled (miles)'].sum().reset_index()
    miles_10_weeks.rename(columns={'Distance Traveled (miles)': 'Miles_Last_10_Weeks'}, inplace=True)
    df_master = df_master.merge(miles_10_weeks, on='Truck ID', how='left')
    df_master['Miles_Last_10_Weeks'] = df_master['Miles_Last_10_Weeks'].fillna(0)

    # 4. Truck Odometer Data Features
    latest_odometer = df_odometer.sort_values('Payroll Week', ascending=False).drop_duplicates('Truck ID')
    latest_odometer = latest_odometer[['Truck ID', 'Odometer Reading']]
    latest_odometer.rename(columns={'Odometer Reading': 'Latest_Odometer_Reading'}, inplace=True)
    df_master = df_master.merge(latest_odometer, on='Truck ID', how='left')
    df_master['Latest_Odometer_Reading'] = df_master['Latest_Odometer_Reading'].fillna(0)
    df_master['Odometer_Distance_Check'] = 'Good' # Placeholder

    # 5. Stub Data Features
    stub_summary = df_stub.groupby('Truck ID').agg(
        Num_Payroll_Entries=('Payroll Week', 'count'),
        Total_Collected_Amount=('Amount', 'sum')
    ).reset_index()
    df_master = df_master.merge(stub_summary, on='Truck ID', how='left')
    df_master['Num_Payroll_Entries'] = df_master['Num_Payroll_Entries'].fillna(0)
    df_master['Total_Collected_Amount'] = df_master['Total_Collected_Amount'].fillna(0)

    # 6. Truck Paper Features
    df_master = df_master.merge(df_truck_paper, on='Truck ID', how='left')
    df_master.rename(columns={'Price': 'Estimated_Resale_Value'}, inplace=True)
    df_master['Estimated_Resale_Value'] = df_master['Estimated_Resale_Value'].fillna(0)

    df_master['Potential_Gain_Loss_If_Sold'] = df_master['Estimated_Resale_Value'] - df_master['Total Owed']

    # --- Decision Logic ---
    total_repair_cost_q75 = df_master['Total_Repair_Cost'].quantile(0.75)
    miles_last_10_weeks_q25 = df_master['Miles_Last_10_Weeks'].quantile(0.25)
    num_payroll_entries_q25 = df_master['Num_Payroll_Entries'].quantile(0.25)
    latest_odometer_q75 = df_master['Latest_Odometer_Reading'].quantile(0.75)

    borderline_repair_cost_upper = df_master['Total_Repair_Cost'].quantile(0.60)
    borderline_repair_cost_lower = df_master['Total_Repair_Cost'].quantile(0.40)
    borderline_usage_upper = df_master['Num_Payroll_Entries'].quantile(0.60)
    borderline_usage_lower = df_master['Num_Payroll_Entries'].quantile(0.40)
    borderline_miles_upper = df_master['Miles_Last_10_Weeks'].quantile(0.60)
    borderline_miles_lower = df_master['Miles_Last_10_Weeks'].quantile(0.40)

    def make_truck_recommendation(row):
        high_mileage=row['latest_Odometer_Reading']> latest_odometer_q75
        high_repair_cost=row['Total_Repair_Cost']> total_repair_cost_q75
        low_usage = row['Num_Payroll_Entries'] < num_payroll_entries_q25
        resale_higher_than_owed = row['Potential_Gain_Loss_If_Sold'] > 0

        low_moderate_mileage = row['Latest_Odometer_Reading'] <= latest_odometer_q75
        actively_used = row['Num_Payroll_Entries'] >= num_payroll_entries_q25
        resale_lower_than_owed = row['Potential_Gain_Loss_If_Sold'] < 0

        if high_mileage and high_repair_cost and low_usage and resale_higher_than_owed:
            return 'Sell'
        if low_moderate_mileage and (not high_repair_cost) and actively_used and resale_lower_than_owed:
            return 'Keep'
        
        borderline_repair = (row['Total_Repair_Cost'] > borderline_repair_cost_lower) and \
                            (row['Total_Repair_Cost'] < borderline_repair_cost_upper)
        borderline_usage = (row['Num_Payroll_Entries'] > borderline_usage_lower) and \
                           (row['Num_Payroll_Entries'] < borderline_usage_upper)
        borderline_miles = (row['Miles_Last_10_Weeks'] > borderline_miles_lower) and \
                           (row['Miles_Last_10_Weeks'] < borderline_miles_upper)
         
        if borderline_repair or borderline_usage or borderline_miles or (low_usage and not high_repair_cost):
            return 'Inspect'
        return 'Inspect'
    
    df_master['Recommendation'] = df_master.apply(make_truck_recommendation, axis=1)
    return df_master

@app.route('/')
def index():
    # Get the processed data
    df_result = get_truck_evaluations()

    # Select and format columns for display
    display_columns = [
        'Truck ID', 'Ownership Type', 'Monthly Cost', 'Total Owed', 'Is Paid Off',
        'Total_Repair_Cost', 'Num_Repairs', 'Total_Miles_Traveled', 'Miles_Last_10_Weeks',
        'Num_Idle_Days', 'Latest_Odometer_Reading', 'Num_Payroll_Entries',
        'Total_Collected_Amount', 'Estimated_Resale_Value', 'Potential_Gain_Loss_If_Sold',
        'Recommendation'
    ]
    df_display = df_result[display_columns].round(2) # Round numerical columns for cleaner display

    # Convert DataFrame to an HTML table string
    # You can add CSS classes to the table for styling (e.g., 'class="table table-striped"')
    html_table = df_display.to_html(classes='data-table', index=False)

    # Generate summary of recommendations
    recommendation_summary = df_result['Recommendation'].value_counts().to_frame(name='Count').to_html(classes='summary-table')

    # Basic HTML template string
    # In a real Flask app, this would be in a separate .html file (e.g., templates/index.html)
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Truck Evaluation Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
            h1, h2 { color: #0056b3; }
            .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .data-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            .data-table th, .data-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            .data-table th { background-color: #e2e6ea; }
            .summary-table { margin-top: 30px; border-collapse: collapse; }
            .summary-table th, .summary-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            .summary-table th { background-color: #e2e6ea; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Truck Evaluation Dashboard</h1>
            <p>This dashboard provides recommendations for your truck fleet based on financial, mechanical, and operational data.</p>
            <p><strong>Note:</strong> This demonstration uses simulated data due to file access limitations.</p>

            <h2>Detailed Truck Evaluation</h2>
            {{ html_table | safe }}

            <h2>Summary of Recommendations</h2>
            {{ recommendation_summary | safe }}

            <h2>Explanation of Logic and Future Predictions</h2>
            <p>
                The recommendations (Keep, Sell, Inspect) are based on a set of rules combining mileage, repair costs, usage, and resale value against outstanding loans.
            </p>
            <h3>Addressing Specific Questions:</h3>
            <ul>
                <li><strong>Are we still getting value out of this truck?</strong> Evaluated by usage (payroll entries) and revenue collected versus repair costs.</li>
                <li><strong>Will keeping it cost us more than it’s worth?</strong> Assessed by the 'Potential_Gain_Loss_If_Sold' metric, comparing estimated resale value to total amount owed.</li>
                <li><strong>Is there enough data to clearly decide, or does this one need a closer look?</strong> Trucks with 'borderline' metrics or conflicting signals are flagged for 'Inspect'.</li>
                <li><strong>How much did we gain/lose, or How much Is predicted for this truck to get in the next X weeks?</strong> 'Potential_Gain_Loss_If_Sold' shows immediate gain/loss. Future predictions (next X weeks) would require advanced time-series and predictive maintenance models, which are beyond the scope of this demonstration but are critical for a full operational tool.</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(template, html_table=html_table, recommendation_summary=recommendation_summary)

if __name__ =='__main__'
    app.run(debug=True)
