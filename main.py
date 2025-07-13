class product:
    def __init__(self, name, price, sku, quantity_in_stocks):
        self.name = name
        self.price  = price
        self.sku = sku
        self.quantity_in_stocks = quantity_in_stocks
        
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
                    
                    
class customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.cart = []
        
        
    def view_profile(self):
        print(f"customer_id: {self.customer_id}")
        print(f"name: {self.name}")
        print(f"email: {self.email}")
        
        
    def add_to_cart(self, product, quantity):
        self.cart.append((product, quantity))
        print(f"added {quantity} of {product.name} to cart.")
        
        
    def view_cart(self):
        if not self.cart:
            print("cart is empty. ")
        else:
            print("cart items: ")
            for item, quantity in self.cart:
                print(f"- {item.name}  (x{quantity}) - ${item.price} each")
                
    def clear_cart(self):
        self.cart = []
        print("cart has been cleared")   
        
        
        


