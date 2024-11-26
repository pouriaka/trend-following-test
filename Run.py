
from Trade_probability import *
from Backtest import *



login = metatrader(89898149, '*********', 'LiteFinance-MT5-Demo')
login.start_mt5()

symbol_list = []

# Get all available symbols
symbols = mt5.symbols_get()

# Check if any symbols were retrieved
if symbols:
    # Print symbol names
    for symbol in symbols:
        symbol_list.append(symbol.name)
else:
    print("No symbols found.")


df_data = pd.DataFrame()

for symbol in symbol_list:
    df = datamine('1d', symbol, "online", number_data=200).df()
    data = find_edge_and_growth(symbol, df)
    print(data)
    # Add the row to the DataFrame
    df_data = df_data._append(data, ignore_index=True)

print(df_data)
Database().save_dataframe(df_data, 'symbol_edge_and_growth')


#-----------------------------------------------------------------------------------------------------------


# df = Database().load_table('symbol_edge_and_growth')

# long term filter ---------------------
# filtered_df = df[(df['edge_1'] == 100) & (df['growth_1'] > 0.2)
#                  &(df['edge_7'] > 30) & (df['growth_7'] > 3) 
#                  & (df['edge_30'] > 30) & (df['growth_30'] > 5) 
#                  & (df['edge_60'] > 20) & (df['growth_60'] > 10)
#                  & (df['edge_120'] > 20) & (df['growth_120'] > 15)]

# filtered_df = df[(df['edge_1'] == -100) & (df['growth_1'] < -0.2)
#                  &(df['edge_7'] < -20) & (df['growth_7'] < 0) 
#                  & (df['edge_30'] < -20) & (df['growth_30'] < 0) 
#                  & (df['edge_60'] < -20) & (df['growth_60'] < 0)
#                  & (df['edge_120'] < -20) & (df['growth_120'] < 0)]


# short term filter ---------------------
# filtered_df = df[(df['edge_1'] == 100) & (df['growth_1'] > 0.2)
#                  &(df['edge_7'] > 40) & (df['growth_7'] > 4) 
#                  & (df['edge_30'] > 40) & (df['growth_30'] > 10) 
#                  ]

# filtered_df = df[(df['edge_1'] == -100) & (df['growth_1'] < -0.2)
#                  &(df['edge_7'] < -30) & (df['growth_7'] < -3) 
#                  & (df['edge_30'] < -30) & (df['growth_30'] < -5) 
#                 ]

# print(filtered_df)
