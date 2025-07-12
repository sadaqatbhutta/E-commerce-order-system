class product:
    def __init__(self, name, price, sku, quantity_in_stocs):
        self.name = name
        self.price  = price
        self.sku = sku
        self.quantity_in_stocks = quantity_in_stocs
        
    def display_info(self):
        print(f"product: {self.name}")
        print(f"price: {self.price}")
        print(f"sku: {self.sku}")
        print(f"quantity_in_stocks: {self.quantity_in_stocks}")
        
    def update_stocks(self, quantity_sold):
        if quantity_sold <= self.quantity_in_stocks:
            self.quantity_in_stocks -= quantity_sold
            print(f"{quantity_sold} items sold. remaining stock: {self.quantity_in_stocks}")
        else:
            print(f"Insufficient stock. only {self.quantity_in_stocks} items available. ")
                    