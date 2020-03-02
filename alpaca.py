#------- Alpaca ----------------
import alpaca_trade_api as tradeapi
import threading
import time, datetime
from app.py import WebScraper

api_key=""
api_secret=""
alpaca_api_base_url="https://paper-api.alpaca.markets"
url = url = 'https://finance.yahoo.com/gainers'

#
keltner_period=20

class System:
    def __init__(self):
        self.alpaca=tradeapi.REST(api_key,api_secret,alpaca_api_base_url,'v2')
        stockUniverse=WebScraper(url=url)
        
        self.allStocks=[]
        for stock in stockUniverse:
            self.allStocks.append([stock,0])
            
        self.long=[]
        self.short=[]
        self.position=0
        self.longAmount=0
        self.shortAmount=0
        self.timeToClose=None
        
    def run(self):
        orders=self.alpaca.list_orders(status='open')
        for order in orders:
            self.alpaca.cancel_order(order_id)
        
        # Wait for opening
        tAMO=threading.Thread(target=self.awaitMarketOpen)
        tAMO.start()
        tAMO.join()
        print('Mkt opened')
        
        # Check for signals every minute, making necessary trades
        while True:
            # Find when mkt closes , so sell 15 mins before that
            clock=self.alpaca.get_clock()
            closingTime=clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime=clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            self.timeToClose=closingTime - currTime
            
            if self.timeToClose < (60*15):
                print("Mkt closing soon, Closing positions")
                positions = self.alpaca.list_positions()

                for position in positions():
                    if (position.side=='long'):
                        orderSide='sell'
                    else:
                        orderSide='buy'

                    qty=abs(int(float(position.qty)))
                    respSO=[]
                    tSubmitOrder=threading.Thread(target=self.submitOrder(qty,position.symbol,orderSide,respSO))
                    tSubmitOrder.start()
                    tSubmitOrder.join()
               
                # Run script again after market close for next trading day.
                print("Sleeping until market close (15 minutes).")
                time.sleep(60 * 15)
                
            else:
                # Trading signals activated
                tSystem=threading.Thread(target=self.tradingSystem)
                tSystem.start()
                tSystem.join()
                time.sleep(60)
                
    
    # Wait for mkt to open
    def awaitMarketOpen(self):
        isOpen = self.alpaca.get_clock().is_open
        while(not isOpen):
            clock = self.alpaca.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currTime) / 60)
            print(str(timeToOpen) + " minutes til market open.")
            time.sleep(60)
            isOpen = self.alpaca.get_clock().is_open
            
            
    def tradingSystem(self):
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
                                              qty=trading_size,
                                              side='buy',
                                              type='market',
                                              time_in_force='day')
                    self.position+=1
                    print('{} Shares of {} Bought at'.format(tradeapi.REST.get_position(),
                                                            tradeapi.REST.) )
                elif:
                    price < KeltnerChannel(20) and (self.position==0 or self.position==1):
                        tradeapi.REST.submit_order(symbol=symbol,
                                              qty=trading_size,
                                              side='sell',
                                              type='market',
                                              time_in_force='day')
                    self.position-=1
                    
