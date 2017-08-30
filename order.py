import types

class Order(object):
    """docstring for Order"""
    def __init__(self, nendoroids, market):
        super(Order, self).__init__()
        
        if isinstance(market.shipping_fee, dict):
            pass
        elif isinstance(market.shipping_fee, types.FunctionType):
            pass
        elif isinstance(market.shipping_fee, int):
            pass
