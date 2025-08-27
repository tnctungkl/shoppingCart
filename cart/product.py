from __future__ import annotations
import random
import string
import json

class Product:
    def __init__(self, product_id, name, price, quantity_available, shipping_cost=0):
        self._product_id = product_id
        self._name = name
        self._price = float(price)
        self._quantity_available = int(quantity_available)
        self._shipping_cost = float(shipping_cost)

    def decrease_quantity(self, amount: int) -> bool:
        if 0 < amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    def increase_quantity(self, amount: int) -> None:
        if amount > 0:
            self._quantity_available += amount

    def display_details(self) -> str:
        return f"[{self._product_id}] {self._name} | Price: ₺{self._price} | Stock: {self._quantity_available}"

    def to_dict(self) -> dict:
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_available": self._quantity_available,
            "shipping_cost": self._shipping_cost,
        }

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, weight, shipping_cost=999):
        super().__init__(product_id, name, price, quantity_available, shipping_cost)
        self._weight = float(weight)

    def display_details(self) -> str:
        return f"{super().display_details()} | Weight: {self._weight}kg | Shipping: ₺{self._shipping_cost}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "type": "physical",
            "weight": self._weight,
        })
        return d

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, quantity_available, download_link):
        super().__init__(product_id, name, price, quantity_available, shipping_cost=0)
        self._download_link = download_link
        self._license_key = self._generate_license_key()

    def _generate_license_key(self) -> str:
        chars = string.ascii_uppercase + string.digits
        active_key = ''.join(random.choices(chars, k=12))
        return f"KEY-{active_key}"

    def display_details(self) -> str:
        return (f"[{self._product_id}] {self._name} | Price: ₺{self._price} "
                f"| Stock: {self._quantity_available} | Link: {self._download_link}")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "type": "digital",
            "download_link": self._download_link,
            "license_key": self._license_key,
        })
        return d