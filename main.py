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
        
        
class order:
    
    def __init__(self, order_id, customer, products):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.status = "pending"
        
    def calculate_total(self):
        total = 0
        for product, quantity in self.products:
            total += product.price * quantity
        return total
        
    def display_order(self):
        print(f"order_id: {self.order_id}")
        print(f"customer: {self.customer.name}")
        print("products in order:")
        for product, quantity in self.products:
            print(f"- {product.name} (x{quantity}) - ${product.price} each")
        print(f"total amount: ${self.calculate_total()}")
        print(f"status: {self.status}")
        
    def update_status(self, new_status):
        self.status = new_status
        print(f"order status updated to: {self.status}")
        
        
class OrderManager:
    def __init__(self):
        self.orders = []
        self.next_order_id = 1001

    def create_order(self, customer):
        if not customer.cart:
            print("cart is empty. cannot create order.")
            return None
        new_order = order(self.next_order_id, customer, customer.cart.copy())
        self.orders.append(new_order)
        self.next_order_id += 1
        customer.clear_cart()
        print(f"order {new_order.order_id} created successfully.")
        return new_order

    def find_order_by_id(self, order_id):
        for ord in self.orders:
            if ord.order_id == order_id:
                return ord
        print(f"order with id {order_id} not found.")
        return None

    def display_all_orders(self):
        if not self.orders:
            print("no orders found.")
        else:
            for ord in self.orders:
                print("-" * 30)
                ord.display_order()

        
# ---------------------------
# Testing OrderManager system
# ---------------------------

# Create some products
p1 = product("Laptop", 1200.00, "SKU123", 10)
p2 = product("Headphones", 150.00, "SKU456", 25)

# Create a customer
c1 = customer(1, "Alice Smith", "alice@example.com")

# Create the manager
order_system = OrderManager()

# Customer adds items to cart again
c1.add_to_cart(p1, 2)
c1.add_to_cart(p2, 1)

# Customer places order
new_order = order_system.create_order(c1)

# View the new order
if new_order:
    new_order.display_order()

# Add another order to test multiple
c1.add_to_cart(p2, 3)
order_system.create_order(c1)

# View all orders in the system
order_system.display_all_orders()

