# sales-module-implementation-project
This public repo documents the planning and development of a full Sales Management Module for Odoo (Session 1 Task). We leverage Python/Odoo framework, focusing on robust functionalities, strict Git branching structure (main stable, feature/*), and Python best practices for submission. Ready for implementation.

# Sales Module Implementation Project  
A complete OOP-based Sales & Invoicing system built in **Python**, demonstrating real business logic similar to ERP systems (like Odoo, SAP, Dynamics).  
The project showcases clean architecture, class modeling, workflow automation, and strong object-oriented practices.

---

## Project Overview  
This project simulates a **full sales lifecycle**, starting from product selection → creating sale orders → confirming orders → generating invoices → updating customer records → managing stock levels.

---

## System Architecture  
The project contains the following main models:

### **1. BaseModel**
A shared abstract base class that provides:
- Unique ID generation  
- Standard `name` attribute  
- Reusable initialization logic  

All models inherit from this class.

---

### **2. Customer**
Represents the buyer.  
Stores:
- Name & email  
- All created **Sale Orders**  
- All **Invoices** generated  
Provides:  
- `add_order()`  
- `add_invoice()`  
- `show_invoices()`  
- `cancel_order()`  

---

### **3. Product**
Represents an inventory item.  
Tracks:
- Name  
- Price  
- Stock quantity  

Methods:
- `reduce_stock()`  
- `increase_stock()`  
- `set_price()`  

---

### **4. SaleOrder**
Represents the customer’s purchase request.  
Stores:
- Customer  
- Order state (draft → confirmed → cancelled)  
- One-to-many list of SaleOrderLine  

Important methods:
- `add_line()`  
- `compute_total()`  
- `confirm()`  
- `cancel()`  

Upon confirmation:
✔ Stock is reduced  
✔ Invoice is automatically created  
✔ Invoice is posted  
✔ Customer invoice history updates  

---

### **5. SaleOrderLine**
Represents a single product line inside a SaleOrder.  
Contains:
- Product  
- Quantity  
- Subtotal property  

---

### **6. Invoice**
Represents the financial document.  
Stores:
- Customer  
- Sale order reference  
- Lines (InvoiceLine)  
- State (draft → posted)  

Methods:
- `add_line()`  
- `post()`  
- `total` (property)

---

### **7. InvoiceLine**
Represents a single billed product.  
Contains:
- Product  
- Quantity  
- Fixed unit price  
- Subtotal property  

---

##  Business Workflow  
1. User creates a **Sale Order**  
2. Adds products to order  
3. User confirms the order  
4. System automatically:  
- Deducts stock  
- Creates an Invoice  
- Adds Invoice Lines  
- Posts the Invoice  
- Saves Invoice under customer's history  

5. User can view all invoices  
6. User can cancel a confirmed order (stock restored)

---

##  Main Application (main.py)
The program includes a full menu-driven interface:

- Add customers  
- List products  
- Create sale orders  
- Confirm / cancel orders  
- View customer invoices  

Each menu action calls the appropriate class methods — keeping business logic inside models (clean OOP separation).

---


