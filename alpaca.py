#------- Alpaca ----------------
import alpaca_trade_api as tradeapi
import threading
import time, datetime
from WebScraimport WebScraper

api_key=""
api_secret=""
alpaca_api_base_url="https://paper-api.alpaca.markets"
url = url = 'https://finance.yahoo.com/gainers'
tradeapi=tradeapi.REST(api_key,api_secret,alpaca_api_base_url,'v2')
#
keltner_period=20
no_of_stocks_to_trade = 5

# class System:
#     def __init__(self):
#         self.alpaca=tradeapi.REST(api_key,api_secret,alpaca_api_base_url,'v2')
#         stockUniverse=WebScraper(url=url)
        
#         self.allStocks=[]
#         for stock in stockUniverse:
#             self.allStocks.append([stock,0])
            
#         self.long=[]
#         self.short=[]
#         self.position=0
#         self.longAmount=0
#         self.shortAmount=0
#         self.timeToClose=None
        
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
        # Find when mkt closes , so sell 15 mins before that
        clock=tradeapi.get_clock()
        closingTime=clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime=clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        self.timeToClose=closingTime - currTime

        if self.timeToClose < (60*15):
            print("Mkt closing soon, Closing positions")
            positions = tradeapi.list_positions()

            for position in positions():
                if (position.side=='long'):
                    orderSide='sell'
                else:
                    orderSide='buy'

                qty=abs(int(float(position.qty)))
                respSO=[]
                tSubmitOrder=threading.Thread(target=submitOrder(qty,position.symbol,orderSide,respSO))
                tSubmitOrder.start()
                tSubmitOrder.join()

            # Run script again after market close for next trading day.
            print("Sleeping until market close (15 minutes).")
            time.sleep(60 * 15)

        else:
            # Trading signals activated
            tSystem=threading.Thread(target=tradingSystem)
            tSystem.start()
            tSystem.join()
            time.sleep(60)

def account_info():
    # Get our account information.
    account = tradeapi.get_account()
    
    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')

    # Check how much money we can use to open new positions.
    print('${} is available as buying power.'.format(account.buying_power))
    

            
# Wait for mkt to open
def awaitMarketOpen():
    isOpen = tradeapi.get_clock().is_open
    while(not isOpen):
        clock = tradeapi.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        print(str(timeToOpen) + " minutes til market open.")
        time.sleep(60)
        isOpen = tradeapi.get_clock().is_open

# Determine position size of each asset
def position_sizing():
    account=tradeapi.get_account()
    cash_balance=account.buying_power()
    position_size=round(float(cash_balance)/no_of_stocks_to_trade)
    return position_size

def tradingSystem():
#         tAlgo=threading.Thread(target=self.Algo)
#         tAlgo.start()
#         tAlgo.join()
    # Clear existing orders again.
    orders = self.alpaca.list_orders(status="open")
    for order in orders:
        self.alpaca.cancel_order(order.id)

    assets=WebScraper(url=url)
    assets=[asset for asset in assets if asset.tradable]
    self.position=0
    self.index=0
    self.formatted_time = None
    while self.index<len(assets):
        barset=tradeapi.REST.get_barset(symbols=assets,
                                        timeframe='5m',
                                        limit=keltner_period,
                                        end=formatted_time)
        for symbol in assets:
            bars=barset[symbol]
            price=bars[-1].c
            if price > KeltnerChannel(20) and (self.position==0 or self.position==-1):
                tradeapi.REST.submit_order(symbol=symbol,
                                          qty=position_sizing(),
                                          side='buy',
                                          type='market',
                                          time_in_force='day')
                self.position+=1
                print('{} Shares of {} Bought at'.format(tradeapi.REST.get_position()[0],
                                                        symbol) )
            elif:
                price < KeltnerChannel(20) and (self.position==0 or self.position==1):
                    tradeapi.REST.submit_order(symbol=symbol,
                                          qty=tradeapi.REST.get_position()[0],
                                          side='sell',
                                          type='market',
                                          time_in_force='day')
                self.position-=1

                
if __name__ == '__main__':
    """
    check on your daily profit or loss by
    comparing your current balance to yesterday's balance.
    """
    # Get account info
    account = tradeapi.get_account()
      

    # Check our current balance vs. our balance at the last market close
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')
    print(f'Today\'s portfolio % change: ${balance_change*100/account.buying_power}%')
