from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import os
import json
from config_singleton import *

config = ConfigClass()
config.load_config_data("cnfig.yml")


class Context():

    def __init__(self, discount_strategy: DiscountStrategy, shipping_strategy: ShippingStrategy) -> None:
        """
        Usually, the Context accepts a strategy through the constructor, but
        also provides a setter to change it at runtime.
        """
        self._discount_strategy = discount_strategy
        self._shipping_strategy=shipping_strategy

    @property
    def discount_strategy(self) -> DiscountStrategy:
        """
        The Context maintains a reference to one of the Strategy objects. 
        """

        return self._strategy

    @discount_strategy.setter
    def discount_strategy(self, discount_strategy: DiscountStrategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """
        self._discount_strategy = discount_strategy

    @property
    def shipping_strategy(self) -> ShippingStrategy:
        """
        The Context maintains a reference to one of the Strategy objects. 
        """

        return self._strategy

    @shipping_strategy.setter
    def shipping_strategy(self, shipping_strategy: ShippingStrategy) -> None:
        """
        Usually, the Context allows replacing a Strategy object at runtime.
        """
        self._shipping_strategy = shipping_strategy
    

    def calculate_shipping(self,data) -> None:
        """
        The Context delegates some work to the Strategy object instead of
        implementing multiple versions of the algorithm on its own.
        """

        base_cost=0
        discount_applied=0
        final_cost=0

        for item in data:
            base_cost+=self._shipping_strategy.calculate_base_cost(item['weight_kg'])
            
        discount_applied=self._discount_strategy.calculate_discount(base_cost)
        
        final = {
            "base_cost": base_cost,
            "discount_applied": discount_applied,
            "final_cost": base_cost-discount_applied,
        }

        return final

    

# Estrategias de descuento
class ShippingStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.
    """

    @abstractmethod
    def calculate_base_cost(self, peso: float):
        pass


class LocalShippingStrategy(ShippingStrategy):
    def calculate_base_cost(self, peso: float) -> float:
        return config.local_fix + peso * config.local_var


class NationalShippingStrategy(ShippingStrategy):
    def calculate_base_cost(self, peso: float) -> float:
        return config.national_fix + peso * config.national_var
    
class InternationalShippingStrategy(ShippingStrategy):
    def calculate_base_cost(self, peso: float) -> float:
        return config.international_fix + peso * config.international_var
    


# Estrategias de descuento
class DiscountStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.
    """

    @abstractmethod
    def calculate_discount(self, value: float):
        pass

class NoDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, value: float) -> float:
        return 0


class PrimeUserStrategy(DiscountStrategy):
    def calculate_discount(self, value: float) -> float:
        return value* 0.15
    
class NewUserStrategy(DiscountStrategy):
    def calculate_discount(self, value: float) -> float:
        return 5
    



if __name__ == "__main__":
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, "input_test.json")

    with open(folder_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    context = Context(NoDiscountStrategy(),LocalShippingStrategy())

    if data['destination'] == 'international':
        context._shipping_strategy=InternationalShippingStrategy()
    elif data['destination'] == 'national':
        context._shipping_strategy=NationalShippingStrategy()
    else:
        context._shipping_strategy=LocalShippingStrategy()

    if data['coupon'] == 'PRIME_USER':
        context._discount_strategy=PrimeUserStrategy()
    elif data['coupon'] == 'NEW_USER':
        context._discount_strategy=NewUserStrategy()
    else:
        context._discount_strategy=NoDiscountStrategy()



    print(context.calculate_shipping(data['items']))