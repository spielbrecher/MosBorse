from OrderType import ORDER_TYPE

class Order:

    id: int
    type: ORDER_TYPE
    instrument: str
    lots: float
    datetime: str
    isExecuted: bool

    def __init__(self):
        pass

