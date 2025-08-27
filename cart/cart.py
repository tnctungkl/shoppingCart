from __future__ import annotations
from typing import Dict
from pathlib import Path
import json
from cart.product import Product, PhysicalProduct, DigitalProduct

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = int(quantity)

    def calculate_subtotal(self) -> float:
        return (self._quantity * self._product._price) + (
            self._product._shipping_cost if isinstance(self._product, PhysicalProduct) else 0
        )

    def __str__(self) -> str:
        return (
            f"Item: {self._product._name} | Quantity: {self._quantity} "
            f"| Unit Price: ₺{self._product._price} "
            f"| Subtotal: ₺{self.calculate_subtotal()}"
        )

class ShoppingCart:
    def __init__(self, catalog_file="jsons/infoProducts.json", cart_file="jsons/cart.json", db_logger=None):
        self._product_catalog_file = catalog_file
        self._cart_state_file = cart_file
        Path(self._cart_state_file).parent.mkdir(parents=True, exist_ok=True)
        self._items: Dict[str, CartItem] = {}
        self.catalog = self._load_catalog()
        self.db = db_logger
        self._load_cart_state()

    def _log(self, action: str, status: str):
        if not self.db:
            return
        self.db.log_action(action=action, status=status, cart_state=self.get_cart_snapshot())

    def get_cart_snapshot(self) -> dict:
        return {
            "items": [
                {
                    "product_id": prdctID,
                    "name": item._product._name,
                    "quantity": item._quantity,
                    "price": item._product._price,
                    "shipping": item._product._shipping_cost,
                    "subtotal": item.calculate_subtotal(),
                }
                for prdctID, item in self._items.items()
            ],
            "total": self.get_total(),
        }

    def _load_catalog(self) -> dict:
        catalog = {}
        try:
            with open(self._product_catalog_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if item.get("type") == "physical":
                        p = PhysicalProduct(
                            item["product_id"], item["name"], item["price"], item["quantity_available"], item.get("weight", 1), item.get("shipping_cost", 999)
                        )
                    elif item.get("type") == "digital":
                        p = DigitalProduct(
                            item["product_id"], item["name"], item["price"], item["quantity_available"], item["download_link"]
                        )
                    else:
                        p = Product(item["product_id"], item["name"], item["price"], item["quantity_available"], item.get("shipping_cost", 0))
                    catalog[p._product_id] = p
        except FileNotFoundError:
            print("⚠️ Product catalog not found. Please, ensure catalog file (.json file) exists!")
        return catalog

    def _save_catalog(self) -> None:
        with open(self._product_catalog_file, "w", encoding="utf-8") as f:
            data = [p.to_dict() for p in self.catalog.values()]
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_cart_state(self) -> None:
        try:
            if not Path(self._cart_state_file).exists() or Path(self._cart_state_file).stat().st_size == 0:
                with open(self._cart_state_file, "w", encoding="utf-8") as f:
                    json.dump([], f)
            with open(self._cart_state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    pid = item["product_id"]
                    qty = item["quantity"]
                    if pid in self.catalog:
                        self._items[pid] = CartItem(self.catalog[pid], qty)
        except (FileNotFoundError, json.JSONDecodeError):
            self._items = {}

    def _save_cart_state(self) -> None:
        with open(self._cart_state_file, "w", encoding="utf-8") as f:
            data = [{"product_id": prdctID, "quantity": item._quantity} for prdctID, item in self._items.items()]
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_item(self, product_id: str, quantity: int) -> bool:
        try:
            if product_id in self.catalog:
                product = self.catalog[product_id]
                if product._quantity_available >= quantity > 0:
                    if product_id in self._items:
                        self._items[product_id]._quantity += quantity
                    else:
                        self._items[product_id] = CartItem(product, quantity)
                    product.decrease_quantity(quantity)
                    self._save_cart_state()
                    print(f"✅ {quantity}x '{product._name}' successfully added to cart.")
                    self._log("add_item", "success")
                    return True
                else:
                    print("⚠️ Not enough stock available, for now!")
                    self._log("add_item", "failed")
            else:
                print("⚠️ Invalid product ID, Please try again!")
                self._log("add_item", "failed")
        except Exception as e:
            print(f"❌ Error: {e}")
            self._log("add_item", "error")
        return False

    def update_quantity(self, product_id: str, new_quantity: int) -> bool:
        if product_id in self._items:
            cart_item = self._items[product_id]
            current_state = cart_item._quantity
            product = cart_item._product
            diff = int(new_quantity) - current_state
            if diff > 0 and product._quantity_available >= diff:
                product.decrease_quantity(diff)
                cart_item._quantity = int(new_quantity)
            elif diff < 0:
                product.increase_quantity(-diff)
                cart_item._quantity = int(new_quantity)
            if new_quantity == 0:
                del self._items[product_id]
            self._save_cart_state()
            print("✅ Quantity successfully updated.")
            self._log("update_quantity", "success")
            return True
        print("⚠️ Item not found in cart, Please check again!")
        self._log("update_quantity", "failed")
        return False

    def remove_item(self, product_id: str) -> bool:
        if product_id in self._items:
            item = self._items.pop(product_id)
            item._product.increase_quantity(item._quantity)
            self._save_cart_state()
            print("✅ Item successfully removed from cart.")
            self._log("remove_item", "success")
            return True
        print("⚠️ Item not found in cart, Please check again!")
        self._log("remove_item", "failed")
        return False

    def clear_cart(self) -> None:
        self._items.clear()
        self._save_cart_state()
        print("🗑️ All Cart cleared.")
        self._log("clear_cart", "success")

    def get_total(self) -> float:
        return sum(item.calculate_subtotal() for item in self._items.values())

    def display_cart(self) -> None:
        if not self._items:
            print("🛒 Your cart is empty, Time to add some items!")
            return
        print("\n-=*=--=*=--=*=--=*=--=*=- FINAL CART CONTENTS -=*=--=*=--=*=--=*=--=*=-")
        for item in self._items.values():
            print(item)
        print(f"Total Amount: ₺{self.get_total()}\n")

    def display_products(self) -> None:
        if not self.catalog:
            print("⚠️ Catalog is empty!")
            return
        print("\n-*-*-*-*-*- PRODUCT CATALOG -*-*-*-*-*-")
        for product in self.catalog.values():
            print(product.display_details())