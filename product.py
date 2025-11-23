from base import BaseModel

class Product(BaseModel):
    def _init_(self, name, price, quantity):
        super()._init_(name)
        self.price = price
        self.quantity = quantity   


    def reduce_stock(self, qty):
        
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        if qty > self.quantity:
            raise ValueError(
                f"Not enough stock for {self.name}. "
                f"Available: {self.quantity}, Requested: {qty}"
            )

        self.quantity -= qty
        print(f"[INFO] Stock updated: {self.name} = {self.quantity}")

    def increase_stock(self, qty):
        
        if qty <= 0:
            raise ValueError("Quantity must be positive.")
        self.quantity += qty

    def set_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = new_price

    def get_price(self):
        return self.price

    def _str_(self):
        return (
            f"Product(id={self.id}, name='{self.name}', "
            f"price={self.price}, quantity={self.quantity})"
        )
