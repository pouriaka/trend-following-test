from Metatrader import *
from Datamine import *


import mysql.connector
from sqlalchemy import create_engine
import pandas as pd



class Database:
    def __init__(self): 
        # Define connection parameters
        self.user = 'root'
        self.password = '$gpMFuBJ3Q1#U6^V'
        self.host = 'localhost'
        self.database = 'forex'

        # Create the database connection URL
        self.connection_string = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}'

        # Create SQLAlchemy engine
        self.engine = create_engine(self.connection_string)


    def save_dataframe(self, df: pd.DataFrame, table_name: str):
        try:
            # Save DataFrame to MySQL table
            df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)
            print(f"DataFrame successfully saved to table `{table_name}`")
        except Exception as e:
            print(f"An error occurred: {e}")


    def load_table(self, table_name: str) -> pd.DataFrame:
            try:
                # Load table from MySQL to a DataFrame
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, con=self.engine)
                print(f"Table `{table_name}` loaded successfully!")
                return df
            except Exception as e:
                print(f"An error occurred: {e}")
                return None



def find_edge_and_growth(symbol, df):
    # Selecting the last 1 days
    last_1_day = df.iloc[-1]

    # Counting red and green candles
    if (last_1_day['close'] > last_1_day['open']):
        edge_1 = 100
    else:
        edge_1 = -100

    # Calculate percentage change from the first day of the last week to the last day
    initial_price = last_1_day ['open']
    final_price = last_1_day ['close']
    last_1_days_change_pct = ((final_price - initial_price) / initial_price) * 100
    growth_1 = round(last_1_days_change_pct, 2)


    if len(df) >= 7:
        # Selecting the last 7 days
        last_7_days = df.iloc[-7:]

        # Counting red and green candles
        green_candles = (last_7_days['close'] > last_7_days['open']).sum()
        red_candles = (last_7_days['close'] < last_7_days['open']).sum()
        edge_7 = ((green_candles - red_candles)/7) * 100
        edge_7 = round(edge_7, 2)

        # Calculate percentage change from the first day of the last week to the last day
        initial_price = last_7_days ['close'].iloc[0]
        final_price = last_7_days ['close'].iloc[-1]
        last_7_days_change_pct = ((final_price - initial_price) / initial_price) * 100
        growth_7 = round(last_7_days_change_pct, 2)
    
    else:
        edge_7 = 0
        growth_7 = 0


    if len(df) >= 30:
        # Selecting the last 30 days
        last_30_days = df.iloc[-30:]

        # Counting red and green candles
        green_candles = (last_30_days['close'] > last_30_days['open']).sum()
        red_candles = (last_30_days['close'] < last_30_days['open']).sum()
        edge_30 = ((green_candles - red_candles)/30) * 100
        edge_30 = round(edge_30, 2)

        # Calculate percentage change from the first day of the last week to the last day
        initial_price = last_30_days ['close'].iloc[0]
        final_price = last_30_days ['close'].iloc[-1]
        last_30_days_change_pct = ((final_price - initial_price) / initial_price) * 100
        growth_30 = round(last_30_days_change_pct, 2)

    else:
        edge_30 = 0
        growth_30 = 0


    if len(df) >= 60:
        # Selecting the last 60 days
        last_60_days = df.iloc[-60:]

        # Counting red and green candles
        green_candles = (last_60_days['close'] > last_60_days['open']).sum()
        red_candles = (last_60_days['close'] < last_60_days['open']).sum()
        edge_60 = ((green_candles - red_candles)/60) * 100
        edge_60 = round(edge_60, 2)

        # Calculate percentage change from the first day of the last week to the last day
        initial_price = last_60_days ['close'].iloc[0]
        final_price = last_60_days ['close'].iloc[-1]
        last_60_days_change_pct = ((final_price - initial_price) / initial_price) * 100
        growth_60 = round(last_60_days_change_pct, 2)
    
    else:
        edge_60 = 0
        growth_60 = 0


    if len(df) >= 120:
        # Selecting the last 120 days
        last_120_days = df.iloc[-120:]

        # Counting red and green candles
        green_candles = (last_120_days['close'] > last_120_days['open']).sum()
        red_candles = (last_120_days['close'] < last_120_days['open']).sum()
        edge_120 = ((green_candles - red_candles)/120) * 100
        edge_120 = round(edge_120, 2)

        # Calculate percentage change from the first day of the last week to the last day
        initial_price = last_120_days ['close'].iloc[0]
        final_price = last_120_days ['close'].iloc[-1]
        last_120_days_change_pct = ((final_price - initial_price) / initial_price) * 100
        growth_120 = round(last_120_days_change_pct, 2)

    else:
        edge_120 = 0
        growth_120 = 0


    data_dic = {
        'symbol':symbol,
        'edge_1': edge_1,
        'growth_1': growth_1,
        'edge_7': edge_7,
        'growth_7': growth_7,
        'edge_30': edge_30,
        'growth_30': growth_30,
        'edge_60': edge_60,
        'growth_60': growth_60,
        'edge_120': edge_120,
        'growth_120': growth_120,
    }

    return data_dic






