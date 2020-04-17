import sys
import time
import shift
import datetime


trader = shift.Trader("tbd")
try:
    trader.connect("initiator.cfg", "KDJKdym8uf4zu7bL")
    trader.sub_all_order_book()
except shift.IncorrectPasswordError as e:
    print(e)
except shift.ConnectionTimeoutError as e:
    print(e)


print("Buying Power\tTotal Shares\tTotal P&L\tTimestamp")
print(
    "%12.2f\t%12d\t%9.2f\t%26s"
    % (
        trader.get_portfolio_summary().get_total_bp(),
        trader.get_portfolio_summary().get_total_shares(),
        trader.get_portfolio_summary().get_total_realized_pl(),
        trader.get_portfolio_summary().get_timestamp(),
    )
)


tickets = ['MCD', 'NKE', 'PG', 'WMT']
rangePERCENT = [0.0126, 0.0159, 0.0133, 0.0135]
openPrice = []
increment = [0, 0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.04, 0.005, 0.07]

time.sleep(5)

for i in range(4):
    a = trader.get_best_price(tickets[i])

    openPrice.append((a.get_bid_price() + a.get_ask_price())/ 2)

    limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, tickets[i], 1, openPrice[0]+0.01)
    trader.submit_order(limit_buy)

    for k in increment:
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, tickets[i], 1, openPrice[i]*(1-rangePERCENT[i]/2-k))
        trader.submit_order(limit_buy)

        limit_sell = shift.Order(shift.Order.Type.LIMIT_SELL, tickets[i], 1, openPrice[i]*(1+rangePERCENT[i]/2+k))
        trader.submit_order(limit_sell)


tickets = ['AAPL', 'CSCO', 'MSFT', 'IBM']
rangePERCENT = [0.0174, 0.0167, 0.015, 0.014]
openPrice = []
increment = [0, 0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.04, 0.005, 0.07]
for i in range(4):
    a = trader.get_best_price(tickets[i])

    openPrice.append((a.get_bid_price() + a.get_ask_price()) / 2)

    limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, tickets[i], 1, openPrice[0]+0.01)
    trader.submit_order(limit_buy)

    for k in increment:
        limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, tickets[i], 1, openPrice[i]*(1-rangePERCENT[i]/2-k))
        trader.submit_order(limit_buy)

print(
    "Symbol\t\t\t\tType\t  Price\t\tSize\tExecuted\tID\t\t\t\t\t\t\t\t\t\t\t\t\t\t Status\t\tTimestamp"
)
for order in trader.get_submitted_orders():
    if order.status == shift.Order.Status.FILLED:
        price = order.executed_price
    else:
        price = order.price
    print(
        "%6s\t%16s\t%7.2f\t\t%4d\t\t%4d\t%36s\t%23s\t\t%26s"
        % (
            order.symbol,
            order.type,
            price,
            order.size,
            order.executed_size,
            order.id,
            order.status,
            order.timestamp,
        )
    )

while True:
    current_time = time.strftime("%H/%M")
    if current_time == '15/55':
        for item in trader.get_portfolio_items().values():
            shares = sum(item.get_shares())
            sell_all = shift.Order(shift.Order.Type.MARKET_SELL, item.get_symbol(), shares)
            trader.submit_order(sell_all)
        exit(1)


