import unittest
import os
from shipping import *
import json

context = Context(NoDiscountStrategy(),LocalShippingStrategy())

class TestApp(unittest.TestCase):

    def test_shipping(self):

        expected_output={
            "base_cost": 62.5,
            "discount_applied": 9.375,
            "final_cost": 53.125
        }

        current_dir = os.getcwd()
        folder_path = os.path.join(current_dir,"input_test.json")

        with open(folder_path, "r", encoding="utf-8") as f:
            data = json.load(f)

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

        self.assertDictEqual(expected_output,context.calculate_shipping(data['items']))

if __name__ == '__main__':
    unittest.main()