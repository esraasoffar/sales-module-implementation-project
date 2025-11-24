from base import BaseModel

class InvoiceLine(BaseModel):
    def _init_(self, name, product, quantity, unit_price, invoice):
        super().__init__(name)
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price
        self.invoice = invoice

    @property
    def subtotal(self):
        return self.quantity * self.unit_price