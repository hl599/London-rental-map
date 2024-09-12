import pandas as pd

dates = pd.date_range('2021-07-31','2024-04-01', freq='MS').strftime("%Y-%m").tolist()

df = pd.DataFrame()

for date in dates:
    df_temp = pd.read_csv(f"import/crime_data/{date}/{date}-metropolitan-street.csv")
    df = pd.concat([df, df_temp], ignore_index = True)

df.to_csv('build/crime_data.csv')
