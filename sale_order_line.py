from base import BaseModel

class SaleOrderLine:
    def _init_(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        self.product = product
        self.quantity = quantity
        self.unit_price = product.price
        self.subtotal = self.unit_price * self.quantity

    def _str_(self):
        return (
            f"SaleOrderLine(product='{self.product.name}', "
            f"qty={self.quantity}, unit_price={self.unit_price}, "
            f"subtotal={self.subtotal})"
        )