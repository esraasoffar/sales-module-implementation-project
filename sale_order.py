from base import BaseModel
from sale_order_line import SaleOrderLine  

class SaleOrder(BaseModel):
    def __init__(self, customer):
        super().__init__(name=f"SO_for{customer}") 
        #Calls BaseModel constructor and sets the name to a string like "SO_for_Alice".
        self.customer = customer
        self.lines = []
        self.state = "draft"


    def add_line(self, product, quantity):
        if self.state != "draft":
            raise ValueError("Cannot add lines to a confirmed order.")
         #Prevents modifying the order after it is confirmed. Only allowed while state == "draft".

        line = SaleOrderLine(product, quantity)
        self.lines.append(line)
        print(f"[INFO] Added line: {line}")

    
    def compute_total(self):
        return sum(line.subtotal for line in self.lines)

 
    def confirm(self):
        if self.state != "draft":
            raise ValueError("Order already confirmed.")
         #Prevents re-confirming /confirming non-draft orders.

        for line in self.lines:
            if line.quantity > line.product.quantity:
                raise ValueError(
                    f"Not enough stock for {line.product.name}. "
                    f"Available: {line.product.quantity}, Required: {line.quantity}"
                )

        for line in self.lines:
            line.product.reduce_stock(line.quantity)

        self.state = "confirmed"
        print(f"[ORDER CONFIRMED] Total = {self.compute_total()}")

    def __str__(self):
        details = "\n".join(str(line) for line in self.lines)
         #sticks all the line texts together with a new line between each one.
        return (
            f"SaleOrder(id={self.id}, customer='{self.customer}', "
            f"state='{self.state}', total={self.compute_total()})\n"
            f"Lines:\n{details}"
        )