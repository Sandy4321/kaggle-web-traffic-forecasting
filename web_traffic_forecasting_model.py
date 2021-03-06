#==============================================================================
# Import packages
#==============================================================================

from datetime import datetime     
import numpy as np
import pandas as pd
from fbprophet import Prophet

#==============================================================================
# Import data
#==============================================================================

print('======================================================================')
print('Script started at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Read the initial CSV files into dataframes
df_train = pd.read_csv('train_2.csv', index_col='Page', header=0)
df_key = pd.read_csv('key_2.csv', index_col='Page', header=0)

#==============================================================================
# Data preprocessing
#==============================================================================

site_name = df_train.index
df_train = df_train.transpose()

df_train = df_train.fillna(method='ffill') # Forward fill missing data
df_train = df_train.fillna(method='bfill') # Then backfill missing data
df_train = np.log(df_train[df_train != 0]) # Take the log transform
df_train = df_train.fillna(0) # Fill NaNs with zeros

#==============================================================================
# Run model
#==============================================================================

# Parameters

# For a quick trial run, change end_idx to a smaller number (e.g., to make
# predictions on the first 100 websites, set end_idx to 99). If you want to 
# run the model on just a single article, I recommend setting the start and end
# indexes to 9033 and 9034, respectively. This particular Wikipedia artcile is 
# the bio page of Elon Musk, which I reference in the README file.
#
#start_idx = 9033
#end_idx = 9034

start_idx = 0
#end_idx = df_train.shape[1]
end_idx = 99

# Start and end dates of predictions
date_format = "%m/%d/%Y"
first_date = datetime.strptime('9/1/2017', date_format) # First prediction date for Prophet
start_date = datetime.strptime('9/13/2017', date_format) # First prediction date for Kaggle
end_date = datetime.strptime('11/13/2017', date_format) # Last prediction date Prophet & Kaggle
prediction_period = (end_date - first_date).days + 1
prediction_subperiod = (end_date - start_date).days + 1

# Initialization
index = pd.date_range(start=start_date, end=end_date, freq='D')
df_pred = pd.DataFrame()

# This section loops through each individual Wikipedia article and makes a 
# prediction only if the article has historical traffic data. If an article 
# doesn't have any historical data, then assume zeros for future dates as well.

for i in range(start_idx, end_idx):

    df = df_train.iloc[:,i]
    
    # Format input for Prophet model
    df = df.reset_index()
    df.columns.values[:] = ['ds', 'y']

    if np.sum(df['y']) > 0: 
    
        # Include yearly seasonality    
        model = Prophet(yearly_seasonality=True)
        model.fit(df)
        
        # Make daily forecasts until end of prediction period
        future = model.make_future_dataframe(periods=prediction_period)
        forecast = model.predict(future)
        
        forecast.index = forecast['ds']
        
        # For speed, comment out the following two plot visualizations
        #model.plot(forecast)
        #model.plot_components(forecast)
    
        pred = pd.DataFrame(forecast['yhat'][forecast['ds'] >= start_date])

    else:
    
        pred = pd.DataFrame(np.zeros((prediction_subperiod,1)), index=index, columns=['yhat'])    
    
    pred.rename(columns = {'yhat':site_name[i]}, inplace=True)
    
    df_pred = pd.concat([df_pred, pred], axis=1)
    
    # Keep track of forecasts
    print(i) if i % 10 == 0 else False
        
#==============================================================================
# Create submission file
#==============================================================================

# Unstack the dataframe
df_final = pd.DataFrame(df_pred.unstack())
df_final.rename(columns = {0:'Visits'}, inplace=True)
df_final.reset_index(inplace=True)
df_final['key'] = df_final['level_0'] + '_' + df_final['ds'].astype(str)

# Merge df_final with df_key
df_final = pd.merge(df_final, df_key, how='inner', left_on='key', 
                    right_on=None, left_index=False, right_index=True)

# Override negative predictions with zeros
df_final['Visits'] = df_final['Visits'].apply(lambda x: 0 if x < 0 else x)

# Exponentiate the predicitions and then round up to zero decimal places
df_final['Visits'] = np.round(np.exp(df_final['Visits']), decimals=0)

# Create the submission file
df_submission = df_final.to_csv('submission_2.csv', index=False, 
                                columns=['Id','Visits'])

end_run_time = datetime.now()

print('Script completed at', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print('======================================================================')

#==============================================================================
# The End
#==============================================================================