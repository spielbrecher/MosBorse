from enum import Enum

class ORDER_TYPE(Enum):
    BUY = "buy"
    SELL = "sell"
    STOP_LIMIT = "stop limit"
    TAKE_PROFIT = "take profit"
