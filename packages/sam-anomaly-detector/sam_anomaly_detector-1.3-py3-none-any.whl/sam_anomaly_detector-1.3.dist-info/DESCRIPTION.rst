Time series forecasting and anomaly detection library on top of fbprophet

.. code:: python
    import pandas as pd
    from psycopg2 import connect
    from sam_anomaly_detector import Forecaster
    df_data = pd.read_csv('dataset.csv', columns=['ds', 'y'])
    json_data = df_data.to_json(orient='records')
    anomalies = Detector().forecast_today(dataset=json_data)
    print(anomalies)


- Input data should be a panda DataFrame having time and aggregated data
- Passed columns to forecaster should be 'ds' for 'time' and 'y' for 'aggregated data'
- Output is a panda DataFrame of anomalies. Important columns are:
    - actual: today's actual value
    - yhat_lower: forecast lower boundary
    - yhat: : forecastted value
    - yhat_upper: forecast upper boundary
    - std: standard diviation from boundaries. negative value means how far it is from 'yhat_lower',
             positive value means how far it is from 'yhat_upper'


