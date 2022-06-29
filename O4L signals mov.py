from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
from talib import BBANDS
from talib import SMA
from datetime import datetime
import concurrent.futures
from discord import Webhook, RequestsWebhookAdapter
print("ONLY FOR LEGENDS SIGNALS 0.04_300_12")
account = input("Email :")
password = input("password :")
mood = input("Mood  :")
I_want_money = IQ_Option(account, password)
check = I_want_money.connect()
I_want_money.change_balance(mood)
I_want_money.get_server_timestamp()
now = datetime.now()
if check:
        print("####   CONNECT  SUCCEFULY    #####")
else:
        print("connect failed")
def send_msj(message):
    webhook = Webhook.from_url("https://discord.com/api/webhooks/989158059022618655/hgkfCPkxufy_j5xmUsBG76ZslDftZc1sAZlpwjSXckvcMdlLnLwylHGPcn0r1K6lQQ1X", adapter=RequestsWebhookAdapter())
    webhook.send(message)
send_msj("################  %s/%s/%s  ################ " % (now.day, now.month, now.year))
def bbands(goal):
    print(f"##connect to {goal}")
    size = 300
    maxdict = 200
    I_want_money.start_candles_stream(goal, size, maxdict)
    while True:
        time.sleep(0.25)
        candles = I_want_money.get_realtime_candles(goal, size)
        inputs = {
            'open': np.array([]),
            'close': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
        }
        for timestamp in list(candles.keys()):
            open = inputs["open"] = np.append(inputs["open"], candles[timestamp]["open"])
            close = inputs["close"] = np.append(inputs["open"], candles[timestamp]["close"])
            high = inputs["high"] = np.append(inputs["open"], candles[timestamp]["max"])
            low = inputs["low"] = np.append(inputs["open"], candles[timestamp]["min"])
        upperband, middleband, lowerband = BBANDS(close * 10000000000000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        real_200 = SMA(close, timeperiod=200)
        up = upperband[-1]
        dn = lowerband[-1]
        md = middleband[-1]
        cls = close[-1] * 10000000000000
        rl_200 = real_200[-1] * 10000000000000
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:")
        if up < rl_200:
            if cls > up or cls == up :
                send_msj(f"## Sell {goal} ##{current_time} ")
                print(f"# sell {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn} ")
                time.sleep(size)
                continue
        if dn > rl_200:
            if cls < dn or cls == dn:
                send_msj(f"## Buy {goal} ##{current_time}")
                print(f"# buy {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn}")
                time.sleep(size)
                continue
        if now.strftime("%S") == "00" :
            print(f"# {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn}")

with concurrent.futures.ThreadPoolExecutor () as executor :
    goals = ["EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "EURJPY", "EURGBP", "AUDCAD", "GBPJPY", "AUDJPY",
             "CADJPY", "USDCAD", "EURAUD"]
    results = [executor.submit(bbands, goal) for goal in goals]