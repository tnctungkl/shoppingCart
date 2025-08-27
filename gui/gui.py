import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import ttk, messagebox, simpledialog
from tkinter import Toplevel
from ttkbootstrap import Style
from uis.themes import ThemeState
from uis import save
import json

class GUI:
    def __init__(self, root, cart, theme_state: ThemeState):
        self.root = root
        self.cart = cart
        self.theme = theme_state
        self.style = Style(theme=self.theme.name)
        self.root.title(f"Tungshoop {self.theme.emoji} – Shopping Cart")
        self.root.geometry("1640x860")

        self._build_widgets()
        self._refresh_products()
        self._refresh_cart()

    def _build_widgets(self):
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill=tk.BOTH, expand=True)

        topbar = ttk.Frame(container)
        topbar.pack(fill=tk.X, pady=(0,12))

        self.toggle_bttn = ttk.Button(topbar, text=f"Toggle Theme {self.theme.emoji}", command=self._toggle_theme)
        self.toggle_bttn.pack(side=tk.LEFT)

        self.save_bttn = ttk.Button(topbar, text="Save…", command=self._open_save_dialog)
        self.save_bttn.pack(side=tk.RIGHT, padx=5)

        self.checkout_bttn = ttk.Button(topbar, text="Checkout", command=self._checkout)
        self.checkout_bttn.pack(side=tk.RIGHT)

        main = ttk.Panedwindow(container, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True)

        prod_frame = ttk.Labelframe(main, text="Products")
        self.prod_tree = ttk.Treeview(prod_frame, columns=("id","name","price","stock","ship","weight","type"), show="headings")
        for col, w in zip(["id","name","price","stock","ship","weight","type"],[90,220,90,80,90,80,80]):
            self.prod_tree.heading(col, text=col.title())
            self.prod_tree.column(col, width=w, anchor=tk.W)
        self.prod_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        prod_actions = ttk.Frame(prod_frame)
        prod_actions.pack(fill=tk.X, padx=400, pady=(0,6))
        ttk.Button(prod_actions, text="Add to Cart", command=self._add_to_cart_dialog).pack(side=tk.LEFT)

        main.add(prod_frame, weight=1)

        cart_frame = ttk.Labelframe(main, text="Cart")
        self.cart_tree = ttk.Treeview(cart_frame, columns=("id","name","qty","unit","shipping","subtotal"), show="headings")
        for col, w in zip(["id","name","qty","unit","shipping","subtotal"],[90,220,80,90,90,100]):
            self.cart_tree.heading(col, text=col.title())
            self.cart_tree.column(col, width=w, anchor=tk.W)
        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        cart_actions = ttk.Frame(cart_frame)
        cart_actions.pack(fill=tk.X, padx=6, pady=(0,6))
        ttk.Button(cart_actions, text="Update Quantity", command=self._update_quantity_dialog).pack(side=tk.LEFT)
        ttk.Button(cart_actions, text="Remove Item", command=self._remove_item_dialog).pack(side=tk.LEFT, padx=6)
        ttk.Button(cart_actions, text="Clear Cart", command=self._clear_cart).pack(side=tk.LEFT)

        self.total_var = tk.StringVar(value="Total: ₺0")
        ttk.Label(cart_actions, textvariable=self.total_var).pack(side=tk.RIGHT)

        main.add(cart_frame, weight=1)

    def _toggle_theme(self):
        self.theme.toggle()
        self.style.theme_use(self.theme.name)
        self.root.title(f"Tungshoop {self.theme.emoji} – Shopping Cart")
        self.toggle_bttn.configure(text=f"Toggle Theme {self.theme.emoji}")

    def _open_save_dialog(self):
        snap = self.cart.get_cart_snapshot()
        if not snap.get("items"):
            messagebox.showinfo("Save", "Cart is empty.")
            return
        dlg = Toplevel(self.root)
        dlg.title("Save as …")
        dlg.geometry("4000x260")
        ttk.Label(dlg, text="Choose a save file format:").pack(pady=10)

        row = ttk.Frame(dlg)
        row.pack(pady=6)
        ttk.Button(row, text="EXCEL", command=lambda: self._do_save(save.save_excel, snap, dlg)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="PDF", command=lambda: self._do_save(save.save_pdf, snap, dlg)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="JSON", command=lambda: self._do_save(save.save_json, snap, dlg)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="DOCX", command=lambda: self._do_save(save.save_docx, snap, dlg)).pack(side=tk.LEFT, padx=6)

    def _do_save(self, fn, snapshot, dlg):
        filename = fn(snapshot)
        messagebox.showinfo("Saved", f"Exported to: {filename}")
        dlg.destroy()

    def _refresh_products(self):
        for i in self.prod_tree.get_children():
            self.prod_tree.delete(i)
        for p in self.cart.catalog.values():
            ptype = getattr(p, "_download_link", None)
            ptype = "digital" if ptype else ("physical" if getattr(p, "_weight", None) is not None else "generic")
            weight = getattr(p, "_weight", "-")
            self.prod_tree.insert("", tk.END, values=(p._product_id, p._name, p._price, p._quantity_available, p._shipping_cost, weight, ptype))

    def _refresh_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        for pid, item in self.cart._items.items():
            self.cart_tree.insert("", tk.END, values=(pid, item._product._name, item._quantity, item._product._price, item._product._shipping_cost, item.calculate_subtotal()))
        self.total_var.set(f"Total: ₺{self.cart.get_total()}")

    def _add_to_cart_dialog(self):
        sel = self.prod_tree.focus()
        if not sel:
            messagebox.showwarning("Add", "Select a product first.")
            return
        pid = self.prod_tree.item(sel, 'values')[0]
        qty = simpledialog.askinteger("Quantity", "Enter quantity:", minvalue=1, parent=self.root)
        if qty:
            ok = self.cart.add_item(pid, qty)
            if ok:
                self._refresh_products()
                self._refresh_cart()

    def _update_quantity_dialog(self):
        sel = self.cart_tree.focus()
        if not sel:
            messagebox.showwarning("Update", "Select a cart item.")
            return
        pid = self.cart_tree.item(sel, 'values')[0]
        qty = simpledialog.askinteger("New Quantity", "Enter new quantity (0 to remove):", minvalue=0, parent=self.root)
        if qty is not None:
            self.cart.update_quantity(pid, qty)
            self._refresh_products()
            self._refresh_cart()

    def _remove_item_dialog(self):
        sel = self.cart_tree.focus()
        if not sel:
            messagebox.showwarning("Remove", "Select a cart item.")
            return
        pid = self.cart_tree.item(sel, 'values')[0]
        self.cart.remove_item(pid)
        self._refresh_products()
        self._refresh_cart()

    def _clear_cart(self):
        if messagebox.askyesno("Clear", "Really, want to clear entire cart?"):
            self.cart.clear_cart()
            self._refresh_products()
            self._refresh_cart()

    def _checkout(self):
        if not self.cart._items:
            messagebox.showinfo("Checkout", "Cart is empty, Time to add some items!")
            return
        self.cart.display_cart()
        messagebox.showinfo("Checkout", "💳 Checkout complete. Thank you for shopping with us!")
        self.cart.clear_cart()
        self._refresh_products()
        self._refresh_cart()