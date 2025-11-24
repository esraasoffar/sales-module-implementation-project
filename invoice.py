from base import BaseModel
from invoice_line import InvoiceLine

class Invoice(BaseModel):
    def __init__(self, name, customer, sale_order):
        super().__init__(name)
        self.customer = customer
        self.sale_order = sale_order
        self.lines = []
        self.state = "draft"

    def add_line(self, product, quantity):
        if self.state == "posted":
            raise Exception("Cannot add lines to a posted invoice.")
        line = InvoiceLine(
            name=f"Line for {product.name}",
            product=product,
            quantity=quantity,
            unit_price=product.price,
            invoice=self,
        )
        self.lines.append(line)

    @property
    def total(self):
        return sum(line.subtotal for line in self.lines)

    def post(self):
        self.state = "posted"