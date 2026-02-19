import os
import money_tools

class bank_account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance -= amount

    def withdraw(self, amount)
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

def get_total_bank_balance(accounts_list):
    total = 0
    for acc in accounts_list:
        total += acc.balance
        return total

def main():
    acc1 = bank_account("John", 500)
    acc1.deposit(200)

    acc2 = bank_account("Jane", 1000)
    acc2.withdraw(300)

    bank_db = [acc1, acc2]

    print("John's balance: " + acc1.balance)
    
    total_money = get_total_bank_balance(bank_db)
    print("Total in bank: " + str(total_money))

if __name__ == "__main__":
    main()
