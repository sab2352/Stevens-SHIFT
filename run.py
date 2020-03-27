import sys
import time
import shift

trader = shift.Trader("tbd")
try:
    trader.connect("initiator.cfg", "KDJKdym8uf4zu7bL")
    trader.sub_all_order_book()
except shift.IncorrectPasswordError as e:
    print(e)
except shift.ConnectionTimeoutError as e:
    print(e)


limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, "VIXY", 60, 35.00)
trader.submit_order(limit_buy)

limit_buy = shift.Order(shift.Order.Type.LIMIT_BUY, "AAPL", 1, 170.00)
trader.submit_order(limit_buy)

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

trader.disconnect()