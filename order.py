import types

class Order(object):
    """docstring for Order"""
    def __init__(self, nendoroids, market):
        super(Order, self).__init__()

        self.market = market
        self.nendoroids = nendoroids
        self.product_price = 0
        self.shipping_fee = 0
        self.total_price = 0

        if isinstance(market.shipping_fee, dict):
            pass
        elif isinstance(market.shipping_fee, types.FunctionType):
            pass
        elif isinstance(market.shipping_fee, int):
            pass

    def update(self):
        self.product_price = 0
        self.shipping_fee = 0
        self.total_price = 0
        for product in nendoroids:
           pass

