from Metatrader import *
from Datamine import *
from Trade_probability import *

import pandas_ta as ta




def add_df_eg(df, symbol):
    
    final_df = df
    df_eg = pd.DataFrame()

    # Loop to remove the last row and print the DataFrame each time
    while not df.empty:
        data = find_edge_and_growth(symbol, df)
        # Add the row to the DataFrame
        df_eg = df_eg._append(data, ignore_index=True)
        
        # Remove the last row
        df = df.drop(df.index[-1])  # Drops the last row
        print(".....")


    df_eg = df_eg.iloc[::-1].reset_index(drop=True)  # Reverse the DataFrame
    final_df = final_df.reset_index()  # Converts index to column if it's set as index
    df_eg = df_eg.reset_index()  # Converts index to column if it's set as index
  
    # Merge by index
    merged_df = pd.concat([final_df.reset_index(drop=True), df_eg.reset_index(drop=True)], axis=1)
    merged_df = merged_df.drop(columns=['symbol', 'index'])

    return merged_df



login = metatrader(89898149, '13781128Pp_', 'LiteFinance-MT5-Demo')
login.start_mt5()
symbol = "FDAX_l"
df = datamine('1d', symbol, "online", number_data=2000).df()
print(df)

# Remove a column by name
df = df.drop(columns=["volume", "spread", "real_volume"])
df = add_df_eg(df, symbol)


length = 14
atr_rate = 5
atr = ta.atr(high=df['high'], low=df['low'], close=df['close'], length=length)
df = pd.concat([df, atr], axis=1)

b_loss = 0
b_profit = 0
s_loss = 0
s_profit = 0

print(df)

for i in range(len(df)):
    # Buy positions
    if ((df.iloc[i]['edge_1'] == 100) and (df.iloc[i]['growth_1'] > 0)
            and (df.iloc[i]['edge_7'] > 30) and (df.iloc[i]['growth_7'] > 1) 
            and (df.iloc[i]['edge_30'] > 30) and (df.iloc[i]['growth_30'] > 3) 
            ):
        
        print("Buy:",df.iloc[i])
        data_n = i
        trade_price = df.iloc[i]['close']
        trade_atr = df.iloc[i]['ATRr_14']
        tp = trade_price + (atr_rate * trade_atr)
        sl = trade_price - (atr_rate * trade_atr)
        
        if not pd.isnull(df.loc[i, 'ATRr_14']):
            while True:
                now_price = df.iloc[data_n]['close']
                if now_price > tp:
                    b_profit += 1 
                    print("profit")
                    break

                elif now_price < sl:
                    b_loss += 1
                    print("loss")
                    break

                else:
                    if data_n < len(df) - 1:
                        data_n += 1
                        print("-------------------",data_n)
                    else:
                        print("position doesen't reach tp or sl.")
                        break


    # Sell position
    if ((df.iloc[i]['edge_1'] == -100) and (df.iloc[i]['growth_1'] < 0)
        and (df.iloc[i]['edge_7'] < -30) and (df.iloc[i]['growth_7'] < -1) 
        and (df.iloc[i]['edge_30'] < -30) and (df.iloc[i]['growth_30'] < -3) 
        ):
    
        print("Sell:",df.iloc[i])
        data_n = i
        trade_price = df.iloc[i]['close']
        trade_atr = df.iloc[i]['ATRr_14']
        tp = trade_price - (atr_rate * trade_atr)
        sl = trade_price + (atr_rate * trade_atr)
        
        if not pd.isnull(df.loc[i, 'ATRr_14']):
            while True:
                now_price = df.iloc[data_n]['close']
                price_change = trade_price - now_price
                if now_price < tp:
                    s_profit += 1 
                    print("profit")
                    break

                elif now_price > sl:
                    s_loss += 1
                    print("loss")
                    break

                else:
                    if data_n < len(df) - 1:
                        data_n += 1
                        print("-------------------",data_n)
                    else:
                        print("position doesen't reach tp or sl.")
                        break



print("number buy profit:",b_profit)
print("number buy loss:",b_loss)

print("number sell profit:",s_profit)
print("number sell loss:",s_loss)


print("number profit:",s_profit + b_profit)
print("number loss:",s_loss + b_loss)