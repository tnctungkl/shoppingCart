# 🛒 Tungshoop – Shopping Cart

**Tungshoop** is a feature-rich **Shopping Cart Management System** that provides both a **Graphical User Interface (GUI)** built with Tkinter + ttkbootstrap, and a **Command-Line Interface (CLI)** mode for terminal-based usage.  
The system integrates **PostgreSQL logging**, supports both **physical and digital products**, and enables **multi-format data exports (JSON, Excel, PDF, DOCX)**.  
This project demonstrates strong skills in **Python desktop development, database integration, and clean software design**, making it a valuable addition to any professional portfolio.

---

## 📂 Project Structure:

```
├── cart/
│   ├── cart.py
│   ├── product.py
├── database/
│   └── logger.py
├── gui/
│   ├── gui.py
├── uis/
│   ├── themes.py
│   └── save.py
├── jsons/
│   ├── infoProducts.json
│   └── cart.json
├── shppngCart.py
├── tungshoop_sql.sql
├── requirements.txt
└── .gitignore
```
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-brightgreen?logo=windows)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Essential Key Features:

- **Dual Interface Support**:  
  - 🌐 **GUI**: Modern, theme-based Tkinter application  
  - 💻 **CLI**: Lightweight terminal interface  
- **Product Management**: Supports physical & digital products (stock, pricing, shipping, license keys).  
- **Cart Operations**: Add, remove, update, clear, and checkout functionality.  
- **Export Options**: Save cart data as:  
  - 📄 JSON  (`.json`)
  - 📊 Excel (`.xlsx`)  
  - 📑 PDF  (`.pdf`)
  - 📝 Word (`.docx`)  
- **Theme Switching**: Toggle between 🌙 Dark and ☀ Light themes.  
- **Database Logging (PostgreSQL)**:  
  - User actions logged in real-time  
  - JSONB support for cart states  
  - Sequence & Trigger management for clean log handling  
- **CLI Menu**:
```
====== Tungshoop SHOPPING CART MENU ======
1.View Products
2.Add Product to Cart
3.View Cart
4.Update Quantity in Cart
5.Remove Item from Cart
6.Clear Cart
7.Checkout
8.Exit
```

---

## ⚙️ Installation & Setup:

### Requirements:
- Python **3.10+**
- PostgreSQL **17+**
- Dependencies listed in `requirements.txt`
- Dependencies:
  ```
  pip install -r requirements.txt
  ```

### Running the Application:
GUI Mode (default):
```
- python shppngCart.py
```

CLI Mode:
```
- python shppngCart.py --cli
```

---

## 📦 Database Configuration:

- Create a PostgreSQL database (e.g. **tungcart_db**).
- Run the provided **tungshoop_sql.sql** file to create required tables, functions and triggers.
- Update database credentials inside **shppngCart.py** in the **TUNGCART_DB** configuration block with dotenv secure protection.

---

## 💥 İmportant Reminder:

- Don't forget to change the database information in the code!

---

## 👑 Author:

        Tunç KUL
    Computer Engineer
