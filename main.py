import json

class product:
    def __init__(self, name, price, sku, quantity_in_stocks):
        self.name = name
        self.price = price
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
            print(f"Insufficient stock. only {self.quantity_in_stocks} items available.")


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
            print("cart is empty.")
        else:
            print("cart items:")
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

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer.customer_id,
            "products": [
                {
                    "sku": product.sku,
                    "quantity": quantity
                }
                for product, quantity in self.products
            ],
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data, customers, products):
        # find customer by ID
        customer_obj = next((c for c in customers if c.customer_id == data["customer_id"]), None)
        # find product objects
        product_list = []
        for item in data["products"]:
            prod_obj = next((p for p in products if p.sku == item["sku"]), None)
            if prod_obj:
                product_list.append((prod_obj, item["quantity"]))

        order_obj = cls(data["order_id"], customer_obj, product_list)
        order_obj.status = data["status"]
        return order_obj


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

    def save_orders_to_file(self, filename):
        data = [o.to_dict() for o in self.orders]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"All orders saved to {filename}")

    def load_orders_from_file(self, filename, customers, products):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.orders = [order.from_dict(item, customers, products) for item in data]
            if self.orders:
                self.next_order_id = max(o.order_id for o in self.orders) + 1
            print(f"Loaded {len(self.orders)} orders from {filename}")
        except FileNotFoundError:
            print(f"No existing file found at {filename}.")


class Payment:
    def __init__(self, payment_id, order, amount, method):
        self.payment_id = payment_id
        self.order = order
        self.amount = amount
        self.method = method
        self.status = "unpaid"

    def process_payment(self):
        if self.amount == self.order.calculate_total():
            self.status = "paid"
            self.order.update_status("paid")
            print(f"Payment of ${self.amount} successful using {self.method}.")
        else:
            print("Payment failed: Amount does not match order total.")


# ------------------------------------------
# Example usage / Testing
# ------------------------------------------

if __name__ == "__main__":
    # Define products
    p1 = product("Laptop", 1200, "SKU001", 10)
    p2 = product("Mouse", 25, "SKU002", 50)
    products_list = [p1, p2]

    # Define customers
    c1 = customer(1, "Alice", "alice@example.com")
    customers_list = [c1]

    # Define order manager
    order_system = OrderManager()

    # Customer adds items and places order
    c1.add_to_cart(p2, 3)
    second_order = order_system.create_order(c1)

    if second_order:
        payment2 = Payment("PAY1002", second_order, second_order.calculate_total(), "PayPal")
        payment2.process_payment()

    # SAVE orders to JSON
    order_system.save_orders_to_file("orders.json")

    # LOAD orders back
    print("\n--- Loading orders from file ---")
    order_system.load_orders_from_file("orders.json", customers_list, products_list)
    order_system.display_all_orders()
