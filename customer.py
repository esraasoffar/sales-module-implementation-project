from base import BaseModel

class Customer(BaseModel):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email
        self.invoices = []
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def add_invoice(self, invoice):
        self.invoices.append(invoice)

    def show_invoices(self):
        if not self.invoices:
            print(f"No invoices recorded for {self.name}.")
            return

        for i, inv in enumerate(self.invoices, start=1):
            print(f"{i}. Invoice: {inv.name} | Total: {inv.total} | State: {inv.state}")

    def change_info(self, new_name=None, new_email=None):
        if new_name:
            self.name = new_name
        if new_email:
            self.email = new_email

    def cancel_order(self, order):
        if order in self.orders:
            self.orders.remove(order)