from bs4 import BeautifulSoup
import requests
import alpaca_trade_api as tradeapi
import threading
import time, datetime
import pandas as pd

url = 'https://finance.yahoo.com/gainers'

def WebScraper(url):
    r=requests.get(url)

    soup=BeautifulSoup(r.content)

    stock_list=[]
    for i in range(21,31,1):
        ind_stock=str(soup.find_all('a')[i]['href'])
        idx=ind_stock.find('=')
        stk=ind_stock[idx+1:]
        stock_list.append(stk)

    return stock_list

WebScraper(url=url)
#========================================================
#----------------------- Alpaca ------------------------
#========================================================
# from WebScraper import WebScraper
api_key=""
api_secret=""
alpaca_api_base_url="https://paper-api.alpaca.markets"
url = url = 'https://finance.yahoo.com/gainers'

timeframe = '5min'
keltner_period=20
kelt_mult=1.0
no_of_stocks_to_trade = 5

daily_stock_list = WebScraper(url=url)
tradeapi=tradeapi.REST(api_key,api_secret,alpaca_api_base_url,'v2')

# ----- Historical Data for Analysis-----
def historical_data(timeframe):
    for stock in daily_stock_list:
        hist_data=tradeapi.alpha_vantage.historic_quotes(stock,adjusted=True,
                                                         cadence=timeframe,
                                                         output_format='pandas')
        return hist_data

# OHLC Data for all stocks in daily list
stock_data=historical_data(timeframe=timeframe) 
# ------------------------------------------

# -------- Algorithm-Keltner Channel-------------
def KeltnerChannel(df, n):
    MA=pd.Series(pd.rolling(df['Close']).mean())
    RangeMA = pd.Series(pd.rolling(df['High'] - df['Low']).mean())
    Upper=MA + RangeMA * kelt_mult
    Lower=MA - RangeMA * kelt_mult
    df = df.join(Upper)
    df = df.join(Lower)
    return df
# ----------------------------------

# def calc_Keltner(timeframe):
#     for stock in daily_stock_list:
#         KeltnerChannel



# ---- Account info, check trading permissions, Cash Balance ------
def account_info():
    # Get our account information.
    account = tradeapi.get_account()
    
    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    # Check Cash Balance.
    print('${} is available as Cash Balance.'.format(account.buying_power))
    
            
# Wait for mkt to open
def awaitMarketOpen():
    isOpen = tradeapi.get_clock().is_open
    while(not isOpen):
        clock = tradeapi.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        print(str(timeToOpen) + " minutes till market open.")
        time.sleep(60)
        isOpen = tradeapi.get_clock().is_open

# Determine position size of each asset
def position_sizing():
    account=tradeapi.get_account()
    cash_balance=account.buying_power()
    position_size=round(float(cash_balance)/no_of_stocks_to_trade)
    return position_size

# Submit an order if quantity is above 0.
def submitOrder(qty, stock, side, resp):
    if(qty != 0):
        try:
            tradeapi.submit_order(stock, qty, side, "market", "day")
            print("Market order of | " + str(qty) + " of " + stock + " " + side + " | completed.")
            resp.append(True)
        except:
            print("Order of | " + str(qty) + " of " + stock + " " + side + " | did not go through.")
            resp.append(False)
    else:
        print("Quantity is 0, order of | " + str(qty) + " of " + stock + " " + side + " | not completed.")
        resp.append(True)

# Get a list of all Open positions 5 Mins before Close
def check_Open_Positions_5m_before_close_and_exit():
    
    clock=tradeapi.get_clock()
    closingTime=clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
    currTime=clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    timeToClose=closingTime - currTime

    try:
        if timeToClose < (60*5):
            # List of all open positions
            porfolio=tradeapi.list_positions()

            print("Mkt closing soon, Closing positions")

            for position in portfolio:
                print('\n{} Shares of {}'.format(position.qty, position.symbol))
            
    except:
        if portfolio is Null:
            print ('No Open positions')
    

# Order Management System
def OMS():
#         tAlgo=threading.Thread(target=self.Algo)
#         tAlgo.start()
#         tAlgo.join()
    # Clear existing orders again.
    orders = tradeapi.list_orders(status="open")
    for order in orders:
        tradeapi.cancel_order(order.id)

    assets=WebScraper(url=url)
    assets=[asset for asset in assets if asset.tradable]
    position=0
    index=0
    formatted_time = None
    while index<len(assets):
        barset=tradeapi.get_barset(symbols=assets,
                                        timeframe=timeframe,
                                        limit=keltner_period,
                                        end=formatted_time)
        for symbol in assets:
            bars=barset[symbol]
            price=bars[-1].c
            if price > KeltnerChannel(df=stock_data,n=keltner_period) and (position==0):
                tradeapi.submit_order(symbol=symbol,qty=position_sizing(),
                                      side='buy',type='market',time_in_force='day')
                position+=1
                curr_position=tradeapi.get_position(symbol)
                curr_position=int(abs(curr_position.qty))
                print('\nFresh Buy position')
                print('{} Shares of {} Bought at'.format(curr_position,symbol))
            elif:
                price > KeltnerChannel(df=stock_data,n=keltner_period) and (position==-1):
                    curr_position=tradeapi.get_position(symbol)
                    curr_position=int(abs(curr_position.qty))
                    
                    tradeapi.submit_order(symbol=symbol,qty=curr_position,
                                          side='buy',type='market',time_in_force='day')
                    position+=1
                    print('\nCover the existing short position')
                    print('{} Shares of {} Bought at'.format(curr_position,symbol))
            elif:
                price < KeltnerChannel(df=stock_data,n=keltner_period) and (position==0):
                    tradeapi.submit_order(symbol=symbol,qty=position_sizing(),
                                          side='sell',type='market',time_in_force='day')
                    position-=1
                    curr_position=tradeapi.get_position(symbol)
                    curr_position=int(abs(curr_position.qty))
                    print('\nFresh Short position')
                    print('{} Shares of {} Sold at'.format(curr_position,symbol))
            
            elif:
                price < KeltnerChannel(df=stock_data,n=keltner_period) and (position==1):
                    curr_position=tradeapi.get_position(symbol)
                    curr_position=int(abs(curr_position.qty))
                    print('\nExit the existing Long position')
                    print('{} Shares of {} Sold at'.format(curr_position,
                                                            symbol) )
                    tradeapi.submit_order(symbol=symbol,qty=curr_position,
                                          side='sell',type='market',time_in_force='day')
                    position-=1

                    
def run():
    orders=tradeapi.list_orders(status='open')
    for order in orders:
        tradeapi.cancel_order(order_id)

    # Wait for opening
    tAMO=threading.Thread(target=awaitMarketOpen)
    tAMO.start()
    tAMO.join()
    print('Mkt opened')

    # Check for signals every minute, making necessary trades
    while True:
        # Cover All positions 15 mins before Mkt close
        clock=tradeapi.get_clock()
        closingTime=clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime=clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToClose=closingTime - currTime

        if timeToClose < (60*15):
            print("Mkt closing soon, Closing positions")
            positions = tradeapi.list_positions()

            for position in positions():
                if (position.side=='long'):
                    orderSide='sell'
                else:
                    orderSide='buy'

                qty=abs(int(float(position.qty)))
                resp_stock_orders=[]
                tSubmitOrder=threading.Thread(target=submitOrder(qty,position.symbol,
                                                                 orderSide,resp_stock_orders))
                tSubmitOrder.start()
                tSubmitOrder.join()

            # Run script again after market close for next trading day.
#             print("Sleeping until market close (15 minutes).")
#             time.sleep(60 * 15)

        else:
            # Trading signals activated
            tSystem=threading.Thread(target=OMS)
            tSystem.start()
            tSystem.join()
            time.sleep(60)
            
            
# Equity Balance Everyday - Daily P&L                    
def daily_PnL():
    # Get account info
    account = tradeapi.get_account()    
    
    # Check Daily P&L by comparing current balance to yesterday's balance
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s P&L: ${balance_change}')
    print(f'Today\'s Equity % change: ${balance_change*100/account.buying_power}%') 
                
if __name__ == '__main__':
    stock_data=historical_data(timeframe=timeframe)
    account_info()
    run()
    check_Open_Positions_5m_before_close_and_exit()
    daily_PnL()
    
