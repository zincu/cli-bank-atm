   # import json, time, re and random(account_id creation)
import json
import random
import time
import re

class InsufficientFundsError(Exception):
    pass
class InvalidAccountID(Exception):
    pass
class InvalidTypeIn(Exception):
    pass

class User:
    def __init__(self, name, account_id, pin, main_acc=0, invest_acc=0):
        self.name = name
        self.account_id = account_id
        self._pin = pin
        self.main_acc = main_acc
        self.invest_acc = invest_acc

    def check_pin(self, attempt: str) -> bool:
        return self._pin == attempt 

    def check_accountid(self, attempt: str) -> bool:
       return attempt in Bank.users

    def check_balance(self, acc_type):
        if acc_type == "Main Account":
            return self.main_acc
        elif acc_type == "Investment Account":
            return self.invest_acc
        elif acc_type == "3":
            return 
        else:
            return False

    def to_dict(self):
        return {
            "name" : self.name,
            "PIN" : self._pin,
            "main_acc" : self.main_acc,
            "invest_acc" : self.invest_acc
        }

    def deposit(self, acc_type, amount):
        if acc_type == "Main Account":
            acckey = self.main_acc
            return acckey + amount if 0 < amount else InvalidTypeIn 
        elif acc_type == "Investment Account":
            acckey = self.invest_acc
            return acckey + amount if 0 < amount else InvalidTypeIn 
        else:
            raise InvalidTypeIn("You must enter a valid account type!")


    def withdraw(self, acc_type, amount):
        if acc_type == "Main Account":
            acckey = self.main_acc
            return acckey - amount(f"-----------------------------WITHDRAW-----------------------------"
                                   f"You have successfully withdrawn ${amount} from your {acc_type}! \n"
                                   f"Your current {acc_type} balanse: ${acckey}.                     \n"
                                   f"------------------------------------------------------------------") if 0 < amount <= acckey else InsufficientFundsError(f"Error! Insufficient funds on {acc_type}!")
        elif acc_type == "Investment Account":
            acckey = self.invest_acc
            return acckey - amount(f"-----------------------------WITHDRAW-----------------------------"
                                   f"You have successfully withdrawn ${amount} from your {acc_type}! \n"
                                   f"Your current {acc_type} balanse: ${acckey}.                     \n"
                                   f"------------------------------------------------------------------") if 0 < amount <= acckey else InsufficientFundsError(f"Error! Insufficient funds on {acc_type}!")
        else:
            raise InvalidTypeIn("You must enter a valid account type!")

class Bank:
    def __init__(self, filename='CLIv1.1_users.json'):
        self.filename = filename
        self.users = {}
        self.load_data()

    def load_data(self):
        with open(self.filename, "r") as f:
            raw_data = json.load(f)

        for acc_id, details in raw_data.items():
            self.users[acc_id] = User(
                account_id=acc_id,
                name=details["name"],
                pin=details["PIN"],
            )

    def save_data(self):
        data_to_save ={}
        for acc_id, user_obj in self.users.items():
            data_to_save[acc_id] = user_obj.to_dict()

        with open(self.filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

def acc_type_choice():
    acc_type = input(f"--------------------CLI-Bank-ATM--------------------\n"
                    f" Please choose an account(1-3).                     \n"
                    f" 1. [Main Account]                                  \n"
                    f" 2. [Investment Account]                            \n"
                    f" 3. [Back]                                          \n"
                    f"----------------------------------------------------\n")
    if acc_type == "1":
        return "Main Account"
    elif acc_type == "2":
        return "Investment Account"
    elif acc_type == "3":
        return acc_type
    else:
        return

def main():
    my_bank = Bank()

    while True:
        welcome_choice = input(f"--------------------CLI-Bank-ATM--------------------\n"
                               f"                                                    \n"
                               f"                    1. [Log in]                     \n"
                               f"                    2. [Create Account]             \n"
                               f"                    3. [Exit]                       \n"
                               f" Please enter(1-3):                                 \n"
                               f"----------------------------------------------------\n")
        if welcome_choice == "1":
            while True:
                accid = input(f"--------------------CLI-Bank-ATM--------------------\n"
                            f"Plese enter your account id: ")
                if accid in my_bank.users:
                    current_user = my_bank.users[accid]
                    while True:
                        if current_user.check_pin(input(f"--------------------CLI-Bank-ATM--------------------\n"
                        f" Please enter your PIN: ")):
                            while True:
                                mainmenu = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f" Welcome, {current_user.name}!                      \n"
                                                f" Please choose an operation to proceed with(1-5)!   \n"
                                                f" 1. [Check Balance]                                 \n"
                                                f" 2. [Deposit]                                       \n"
                                                f" 3. [Withdraw]                                      \n"
                                                f" 4. [Transfer]                                      \n"
                                                f" 5. [Exit]                                          \n"
                                                f"----------------------------------------------------\n")
                                if mainmenu == "1":
                                    acc_type =acc_type_choice()
                                    if acc_type == "3":
                                        pass
                                    else:
                                        am = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f"-----------------------DEPOSIT----------------------\n"
                                                f" {current_user.name}, please enter an amount to     \n"
                                                f" deposit to your {acc_type}(q to quit): ")
                                        try:
                                            result = current_user.deposit(acc_type, am)
                                            print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f"-----------------------DEPOSIT----------------------\n"
                                                f" Deposit successful!                                \n"
                                                f" You have successfully deposited {am:.2f} to your       \n"
                                                f" {acc_type}.                                        \n"
                                                f" Your current {acc_type} balance: ${result:.2f}     \n"
                                                f"----------------------------------------------------")
                                        except:
                                            print("Error! main menu > deposit")
                                    
                           


            


if __name__ == '__main__':
    main()
