class Broker:

    def __init__(self):
        self.log_file_name = "broker.log"
        self.log_file = open(self.log_file_name, "rw")

    def open_order(self, order):
        self.log_file.write("{}, {}, {}, {}, {}, {}".format(order.id, order.type, order.instrument, order.lots, order.datetime, order.isExecuted))
