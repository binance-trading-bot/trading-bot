import os
from time import sleep
import datetime
import pandas as pd
import numpy as np
from binance import ThreadedWebsocketManager
from binance.client import Client
print("here")
#init
api_key = 'TLnYum0nZJrY5uZAypPwmEOdxeAlVHdcY61ARLbwMXMUFJoInR5IzeAFrLe2XKhM'
api_secret = 'qsl7U0gNf9lQxSm6GFbplHEU6nu5nI2zQ6ZbHKTMesv3S4OUgnQKsS0ILWmWSf8E'
client = Client(api_key, api_secret)
# price = {'BTCUSDT': None, 'error':False}
# print("here0")
# def btc_pairs_trade(msg):
# 	''' define how to process incoming WebSocket messages '''
# 	if msg['e'] != 'error':
# 		price['BTCUSDT'] = float(msg['c'])
# 	else:
# 		price['error'] = True
#
#   #init and start websocket
# bsm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
# print("error")
# bsm.start()
# bsm.start_symbol_ticker_socket(symbol='BTCUSDT', callback=btc_pairs_trade)
# print("here1")
#
# print("here2")

#Main 
def candle_score(lst_0,lst_1,lst_2):    
    
	O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
	O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
	O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
	DojiSize = 0.1
    
	doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)
    
	hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    
	inverted_hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    
	bullish_reversal= (O_2 > C_2)&(O_1 > C_1)&doji
    
	bearish_reversal= (O_2 < C_2)&(O_1 < C_1)&doji
    
	evening_star=(C_2 > O_2) & (min(O_1, C_1) > C_2) & (O_0 < min(O_1, C_1)) & (C_0 < O_0 )
    
	morning_star=(C_2 < O_2) & (min(O_1, C_1) < C_2) & (O_0 > min(O_1, C_1)) & (C_0 > O_0 )
    
	shooting_Star_bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
	shooting_Star_bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
	bearish_harami=(C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))
    
	Bullish_Harami=(O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))
    
	Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 >= C_1) & (O_1 >= C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))
    
	Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 >= O_1) & (C_1 >= O_0) & ((C_0 - O_0) > (O_1 - C_1 ))
    
	Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)

	Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

	Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

	strCandle=''
	candle_score=0
    
	if doji:
		strCandle='doji'
	if evening_star:
		strCandle=strCandle+'/ '+'evening_star'
		candle_score=candle_score-1
	if morning_star:
		strCandle=strCandle+'/ '+'morning_star'
		candle_score=candle_score+1
	if shooting_Star_bearish:
		strCandle=strCandle+'/ '+'shooting_Star_bearish'
		candle_score=candle_score-1
	if shooting_Star_bullish:
		strCandle=strCandle+'/ '+'shooting_Star_bullish'
		candle_score=candle_score-1
	if    hammer:
		strCandle=strCandle+'/ '+'hammer'
	if    inverted_hammer:
		strCandle=strCandle+'/ '+'inverted_hammer'
	if    bearish_harami:
		strCandle=strCandle+'/ '+'bearish_harami'
		candle_score=candle_score-1
	if    Bullish_Harami:
		strCandle=strCandle+'/ '+'Bullish_Harami'
		candle_score=candle_score+1
	if    Bearish_Engulfing:
		strCandle=strCandle+'/ '+'Bearish_Engulfing'
		candle_score=candle_score-1
	if    bullish_reversal:
		strCandle=strCandle+'/ '+'Bullish_Engulfing'
		candle_score=candle_score+1
	if    bullish_reversal:
		strCandle=strCandle+'/ '+'bullish_reversal'
		candle_score=candle_score+1
	if    bearish_reversal:
		strCandle=strCandle+'/ '+'bearish_reversal'
		candle_score=candle_score-1
	if    Piercing_Line_bullish:
		strCandle=strCandle+'/ '+'Piercing_Line_bullish'
		candle_score=candle_score+1
	if    Hanging_Man_bearish:
		strCandle=strCandle+'/ '+'Hanging_Man_bearish'
		candle_score=candle_score-1
	if    Hanging_Man_bullish:
		strCandle=strCandle+'/ '+'Hanging_Man_bullish'
		candle_score=candle_score+1
        
    #return candle_score
	return candle_score,strCandle
  
def candle_df(df):
    #df_candle=first_letter_upper(df)
	df_candle=df.copy()
	df_candle['candle_score']=0
	df_candle['candle_pattern']=''


	for c in range(2,len(df_candle)):
		cscore,cpattern=0,''
		lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
		lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
		lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
		cscore,cpattern=candle_score(lst_0,lst_1,lst_2)    
		df_candle['candle_score'].iat[c]=cscore
		df_candle['candle_pattern'].iat[c]=cpattern
    
	df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
	return df_candle


#create order

# while not price['BTCUSDT']:
# 	# wait for WebSocket to start streaming data
# 	sleep(0.1)

while True:
	# error check to make sure WebSocket is working
	# if price['error']:
	# 	# stop and restart socket
	# 	bsm.stop()
	# 	sleep(2)
	# 	bsm.start()
	# 	price['error'] = False
	# else:
	to_dt = datetime.datetime.now().date()
	from_dt = to_dt - datetime.timedelta(days=14)
	klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_6HOUR, str(from_dt), str(to_dt))
	for x in range(len(klines)):
		klines[x]=klines[x][1:5]
		print(list)
	print(klines)
	# Create the pandas DataFrame
	df = pd.DataFrame(klines, columns=['Open', 'High','Low','Close'])
	print(klines)
	df = df.apply(pd.to_numeric, errors='coerce')
	df_candle = candle_df(df)
	df_candle_score=float(df_candle['candle_cumsum'].iloc[[-1]])
	if df_candle_score>1:
		try:
			order = client.order_market_buy(symbol='BTCUSDT', quantity=10)
			break
		except Exception as e:
			print(e)

	if df_candle_score<1:
		try:
			order = client.order_market_sell(symbol='BTCUSDT', quantity=10)
			break
		except Exception as e:
			print(e)
	sleep(0.2)


bsm.stop()

