import sys
import time

import shift

# check connection
# create trader object
trader = shift.Trader("democlient")

# connect and subscribe to all available order books
try:
    trader.connect("initiator.cfg", "password")
    trader.sub_all_order_book()
except shift.IncorrectPasswordError as e:
    print(e)
except shift.ConnectionTimeoutError as e:
    print(e)

# buy 1 share of AAPL with 10.00 as limit price;
# buy 10 share of xom with 10.00 as limit price;
trader = shift.Trader
limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, "AAPL", 1, 10.00)
trader.submit_order(limit_buy)

xom_limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, "XOM", 10, 10.00)
trader.submit_order(xom_limit_buy)

# market order
aapl_market_buy = shift.Order(shift.Order.Type.MARKET_BUY, "AAPL", 1)
trader.submit_order(aapl_market_buy)

xom_market_buy = shift.Order(shift.Order.Type.MARKET_BUY, "XOM", 1)
trader.submit_order(xom_market_buy)

# print our portfolio;
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

print()

print("Symbol\t\tShares\t\tPrice\t\t  P&L\tTimestamp")
for item in trader.get_portfolio_items().values():
    print(
        "%6s\t\t%6d\t%9.2f\t%9.2f\t%26s"
        % (
            item.get_symbol(),
            item.get_shares(),
            item.get_price(),
            item.get_realized_pl(),
            item.get_timestamp(),
        )
    )

# market sell
    aapl_market_sell = shift.Order(shift.Order.Type.MARKET_SELL, "AAPL", 1)
    trader.submit_order(aapl_market_sell)

    xom_market_sell = shift.Order(shift.Order.Type.MARKET_SELL, "XOM", 1)
    trader.submit_order(xom_market_sell)

# show infromations of our order
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

# disconnect
trader.disconnect()
