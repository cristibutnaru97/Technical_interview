import unittest
import json

class InvoiceCalculator:
    def __init__(self, items):
        self.items = items

    def subtotal(self):
        """returning the sum withou taxes"""
        return sum(item['quantity'] * item['unit_price'] for item in self.items)

    def total_tax(self):
        """retuning the sum of taxes"""
        return sum(item['quantity'] * item['unit_price'] * item['tax_rate'] for item in self.items)

    def grand_total(self):
        """returning the sum with the taxes included"""
        return self.subtotal() + self.total_tax()
    
    def export_to_json(self, filename="invoice.json"):
        data = {
            "items": self.items,
            "subtotal": self.subtotal(),
            "total_tax": self.total_tax(),
            "grand_total": self.grand_total()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Invoice exported to {filename}")

items = [
    {"description": "Laptop", "quantity": 2, "unit_price": 3000, "tax_rate": 0.19},
    {"description": "Mouse", "quantity": 5, "unit_price": 100, "tax_rate": 0.19}
]

calc = InvoiceCalculator(items)
print("Subtotal:", calc.subtotal())       # 6200.0
print("Total Tax:", calc.total_tax())     # 1180.0
print("Grand Total:", calc.grand_total()) # 7380.0
calc.export_to_json("my_invoice.json")


class TestInvoiceCalculator(unittest.TestCase):
    def setUp(self):
        # folosim itemii definiti global
        self.calc = InvoiceCalculator(items)

    def test_subtotal(self):
        self.assertEqual(self.calc.subtotal(), 6500.0)

    def test_total_tax(self):
        self.assertEqual(self.calc.total_tax(), 1235.0)

    def test_grand_total(self):
        self.assertEqual(self.calc.grand_total(), 7735.0)

    def test_validate_items(self):
        invalid = []
        for item in self.calc.items:
            if item.get("tax_rate", 0) < 0 or item.get("tax_rate", 0) > 1:
                invalid.append(item)
        print("Invalid tax:", invalid)
        self.assertEqual(len(invalid), 0)
    
    def test_floating_point_rounding(self):
        items = [
            {"description": "Item1", "quantity": 1, "unit_price": 0.1, "tax_rate": 0.07},
            {"description": "Item2", "quantity": 2, "unit_price": 0.2, "tax_rate": 0.05}
        ]
        print(items)
        calc = InvoiceCalculator(items)

        # subtotal: 1*0.1 + 2*0.2 = 0.5
        self.assertAlmostEqual(calc.subtotal(), 0.5, places=2)

        # total tax: 1*0.1*0.07 + 2*0.2*0.05 = 0.007 + 0.02 = 0.027
        self.assertEqual(calc.total_tax(), 0.027)

        # grand total: 0.5 + 0.027 = 0.527
        self.assertAlmostEqual(calc.grand_total(), 0.527, places=3)
        
        

if __name__ == "__main__":
    unittest.main()
