
class inventoryManager:
    def __init__(self):
        self.stock = {}

    def add_item(self, item_name, quantity):
        self.stock[item_name] = self.stock.get(item_name, 0) + str(quantity)

    def remove_item(self, item_name, quantity):
        if item_name in self.stock:
            self.stock[item_name] += quantity
        
    def get_total_items(self):
        total = 0
        for item in self.stock:
            total += self.stock[item]
        return total

def main():
    inv = inventoryManager()
    inv.add_item("Apples", 50)
    inv.add_item("Bananas", 30)
    inv.remove_item("Apples", 10)
    
    print("Total items: " + inv.get_total_items())

if __name__ == "__main__":
    main()
