   # import json, time, re and random(account_id creation)
import json
import random
import time
import re
from datetime import datetime
date_format = "%Y-%m-%d %H:%M:%S"

class InsufficientFundsError(Exception):
    pass
class InvalidAccountID(Exception):
    pass
class InvalidTypeIn(Exception):
    pass

class User:
    def __init__(self, name, account_id, pin, main_acc=0, invest_acc=0, history = None):
        self.name = name
        self.account_id = account_id
        self._pin = pin
        self.main_acc = main_acc
        self.invest_acc = invest_acc
        if history == None:
            history = []
        self._history = history

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
            "invest_acc" : self.invest_acc,
            "history" : self._history
        }

    def _add_history(self, type, amount, account, timestamp, balance_after, counterparty=None):
        record = {'type': type, 'amount': amount, 'account': account, 'timestamp': timestamp, 'balance after': balance_after, 'counterparty': counterparty}
        self._history.append(record)
        self._history = self._history[-10:]
        return self._history

    def get_history(self):
        return self._history

 # define deposit method
    def deposit(self, acc_type, amount):
        if amount <= 0:
            return InvalidTypeIn
        else:
            if acc_type == "Main Account":
                self.main_acc += amount
                self._add_history('deposit', amount, acc_type, datetime.now().strftime(date_format), self.main_acc, None)
                return self.main_acc
            elif acc_type == "Investment Account":
                self.invest_acc += amount
                self._add_history('deposit', amount, acc_type, datetime.now().strftime(date_format), self.invest_acc, None)
                return self.invest_acc

 # define withdraw method
    def withdraw(self, acc_type, amount):
        if amount <= 0:
            return InvalidTypeIn
        else:
            if acc_type == "Main Account" and amount <= self.main_acc:
                self.main_acc -= amount
                self._add_history('withdraw', amount, acc_type, datetime.now().strftime(date_format), self.main_acc, None)
                return self.main_acc
            elif acc_type == "Investment Account" and amount <= self.invest_acc:
                self.invest_acc -= amount
                self._add_history('withdraw', amount, acc_type, datetime.now().strftime(date_format), self.invest_acc, None)
                return self.invest_acc
            else:
                return InvalidTypeIn

    def transfer_acc(self, amount, acc_choice):
        if acc_choice == "Main Account":
            if amount <= 0 or amount > self.invest_acc:
                return InvalidTypeIn
            else:
                self.main_acc += amount
                self.invest_acc -= amount
                self._add_history('Transfer Internal', amount, 'Investment Account', datetime.now().strftime(date_format), self.invest_acc, acc_choice)
                return self.main_acc, self.invest_acc
        elif acc_choice == "Investment Account":
            if amount <= 0 or amount > self.main_acc:
                return InvalidTypeIn
            else:
                self.main_acc -= amount
                self.invest_acc += amount
                self._add_history('Transfer Internal', amount, 'Main Account', datetime.now().strftime(date_format), self.main_acc, acc_choice)
                return self.invest_acc, self.main_acc
class Bank:
    def __init__(self, filename='users.json'):
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
                main_acc=details["main_acc"],
                invest_acc=details["invest_acc"],
                history=details["history"]
            )

    def transfer_user(self, person1, person2, am):
        if am < 0 or am > person1.main_acc:
            return InvalidTypeIn
        elif am <= person1.main_acc:
            person1.main_acc -= am
            person2.main_acc += am
            person1._add_history('Transfer Out', am, 'Main Account', datetime.now().strftime(date_format), person1.main_acc, person2.name)
            person2._add_history('Transfer In', am, 'Main Account', datetime.now().strftime(date_format), person2.main_acc, person1.name)
            return person1.main_acc

    def save_data(self):
        data_to_save ={}
        for acc_id, user_obj in self.users.items():
            data_to_save[acc_id] = user_obj.to_dict()

        with open(self.filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

def acc_type_choice(name):
    while True:
        acc_type = input(f"--------------------CLI-Bank-ATM--------------------\n"
                        f" {name}, please choose an account(1-3).         \n"
                        f" 1. [Main Account]                                   \n"
                        f" 2. [Investment Account]                             \n"
                        f" 3. [Back]                                           \n"
                        f"-----------------------------------------------------\n")
        if acc_type == "1":
            return "Main Account"
        elif acc_type == "2":
            return "Investment Account"
        elif acc_type == "3":
            return acc_type
        else:
            print(f"Error! Please enter a valid operational index(1-3)!")

def main():
    my_bank = Bank()
    my_bank.load_data()
    while True:
        break_all = False
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
                            f" Please enter your account ID(7 digits)(q to quit): ")
                if accid in my_bank.users:
                    current_user = my_bank.users[accid]
                    while True:
                        pin_attempt = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                        f" {current_user.name}, please enter your              \n"
                        f" account PIN(4-6 digits)(q to quit): "))
                        pin_check = current_user.check_pin(pin_attempt)
                        if pin_check:
                            while True:
                                break_all = False
                                mainmenu = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f" Welcome, {current_user.name}!                      \n"
                                                f" Please choose an operation to proceed with(1-5)!   \n"
                                                f" 1. [Check Balance]                                 \n"
                                                f" 2. [Deposit]                                       \n"
                                                f" 3. [Withdraw]                                      \n"
                                                f" 4. [Transfer]                                      \n"
                                                f" 5. [Transaction History]                           \n"
                                                f" 6. [Log out]                                       \n"
                                                f" 7. [Exit]                                          \n"
                                                f"----------------------------------------------------\n")
                                if mainmenu == "1":
                                    acc_type = acc_type_choice(current_user.name)
                                    if acc_type == "3":
                                        pass
                                    elif acc_type == "Main Account":
                                        acc_am = current_user.main_acc
                                        print(f"--------------------CLI-Bank-ATM--------------------\n"
                                              f" {current_user.name}, your current {acc_type}       \n"
                                              f" balance: ${acc_am:.2f}.                                \n")
                                        time.sleep(3)
                                    elif acc_type == "Investment Account":
                                        acc_am = current_user.invest_acc
                                        print(f"--------------------CLI-Bank-ATM--------------------\n"
                                              f" {current_user.name}, your current {acc_type}       \n"
                                              f" balance: ${acc_am:.2f}.                                \n")
                                        my_bank.save_data()
                                        time.sleep(3)
                                elif mainmenu == "2":
                                    acc_type = acc_type_choice(current_user.name)
                                    if acc_type == "3":
                                        pass
                                    elif acc_type == "Main Account":
                                            while True:
                                                am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                        f"-----------------------DEPOSIT----------------------\n"
                                                        f" {current_user.name}, please enter an amount to     \n"
                                                        f" deposit to your {acc_type}(q to quit): "))
                                                if am == "q":
                                                    break
                                                else:
                                                    try:
                                                        fam = float(am)
                                                        result = current_user.deposit(acc_type, fam)
                                                        if result == InvalidTypeIn:
                                                            print(" You must enter a valid amount to deposit!")
                                                        else:
                                                            print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                f"-----------------------DEPOSIT----------------------\n"
                                                                f" Deposit successful!                                \n"
                                                                f" You have successfully deposited ${fam:.2f} to your       \n"
                                                                f" {acc_type}.                                        \n"
                                                                f" Your current {acc_type} balance: ${result:.2f}     \n"
                                                                f"----------------------------------------------------")
                                                            my_bank.save_data()
                                                            time.sleep(3)
                                                            break
                                                    except ValueError:
                                                        print(" You must enter a valid amount to deposit!")
                                    elif acc_type == "Investment Account":
                                            while True:
                                                am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                        f"-----------------------DEPOSIT----------------------\n"
                                                        f" {current_user.name}, please enter an amount to     \n"
                                                        f" deposit to your {acc_type}(q to quit): "))
                                                if am == "q":
                                                    break
                                                else:
                                                    try:
                                                        fam = float(am)
                                                        result = current_user.deposit(acc_type, fam)
                                                        if result == InvalidTypeIn:
                                                            print(" You must enter a valid amount to deposit!")
                                                        else:
                                                            print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                f"-----------------------DEPOSIT----------------------\n"
                                                                f" Withdraw successful!                                \n"
                                                                f" You have successfully deposited ${fam:.2f} to your       \n"
                                                                f" {acc_type}.                                        \n"
                                                                f" Your current {acc_type} balance: ${result:.2f}     \n"
                                                                f"----------------------------------------------------")
                                                            my_bank.save_data()
                                                            time.sleep(3)
                                                            break
                                                    except ValueError:
                                                        print(" You must enter a valid amount to deposit!")
                                elif mainmenu == "3":
                                    acc_type = acc_type_choice(current_user.name)
                                    if acc_type == "3":
                                        pass
                                    elif acc_type == "Main Account":
                                            while True:
                                                am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f"----------------------WITHDRAW----------------------\n"
                                                f" {current_user.name}, please enter an amount to     \n"
                                                f" withdraw from your {acc_type}(q to quit).          \n"
                                                f" Current {acc_type} balance: ${current_user.main_acc:.2f}. \n"
                                                f" : "))
                                                if am == "q":
                                                    break
                                                else:
                                                    try:
                                                        fam = float(am)
                                                        result = current_user.withdraw(acc_type, fam)
                                                        if result == InvalidTypeIn:
                                                            print(f" You must enter a valid amount to withdraw!\n"
                                                                  f" (Amount must be a positive number, not exceeding your current balance). \n"
                                                                  f" Your current {acc_type} balance: ${current_user.main_acc:.2f}.")
                                                        else:
                                                            print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                f"----------------------WITHDRAW----------------------\n"
                                                                f" Withdraw successful!                                \n"
                                                                f" You have successfully withdrawn ${fam:.2f} from your       \n"
                                                                f" {acc_type}.                                        \n"
                                                                f" Your current {acc_type} balance: ${result:.2f}     \n"
                                                                f"----------------------------------------------------")
                                                            my_bank.save_data()
                                                            time.sleep(3)
                                                            break
                                                    except ValueError:
                                                            print(f" You must enter a valid amount to withdraw!(positive number, not exceeding your current balance).\n"
                                                                  f" Your current {acc_type} balance: ${current_user.main_acc:.2f}.")
                                    elif acc_type == "Investment Account":
                                            while True:
                                                am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f"----------------------WITHDRAW----------------------\n"
                                                f" {current_user.name}, please enter an amount to     \n"
                                                f" withdraw from your {acc_type}(q to quit).          \n"
                                                f" Current {acc_type} balance: ${current_user.invest_acc:.2f}. \n"
                                                f" : "))
                                                if am == "q":
                                                    break
                                                else:
                                                    try:
                                                        fam = float(am)
                                                        result = current_user.withdraw(acc_type, fam)
                                                        if result == InvalidTypeIn:
                                                            print(f" You must enter a valid amount to withdraw!\n"
                                                                  f" (Amount must be a positive number, not exceeding your current balance). \n"
                                                                  f" Your current {acc_type} balance: ${current_user.invest_acc:.2f}.")
                                                        else:
                                                            print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                f"----------------------WITHDRAW----------------------\n"
                                                                f" Withdraw successful!                                \n"
                                                                f" You have successfully withdrawn ${fam:.2f} from your       \n"
                                                                f" {acc_type}.                                        \n"
                                                                f" Your current {acc_type} balance: ${result:.2f}     \n"
                                                                f"----------------------------------------------------")
                                                            my_bank.save_data()
                                                            time.sleep(3)
                                                            break
                                                    except ValueError:
                                                            print(f" You must enter a valid amount to withdraw!(positive number, not exceeding your current balance).\n"
                                                                  f" Your current {acc_type} balance: ${current_user.invest_acc:.2f}.")
                                elif mainmenu == "4":
                                    while True:
                                        tranop = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                         f" Please enter what transfer option would you like   \n"
                                         f" to choose(1-3).                                    \n"
                                         f" 1. [To my Account]                                 \n"
                                         f" 2. [To User]                                       \n"
                                         f" 3. [Back]                                          \n"
                                         f"----------------------------------------------------\n")
                                        if tranop == "3":
                                            break
                                        elif tranop == "1":
                                            acc_choice = acc_type_choice(current_user.name)
                                            if acc_choice == "3":
                                                pass
                                            elif acc_choice == "Main Account":
                                                acc_type1 = "Main Account"
                                                acc_type2 = "Investment Account"
                                                acc_key1 = current_user.main_acc
                                                acc_key2 = current_user.invest_acc
                                                while True:
                                                    am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                    f"--------------TRANSFER-TO-ACCOUNT----------------------\n"
                                                    f" {current_user.name}, please enter an amount to     \n"
                                                    f" transfer from your {acc_type2} to your {acc_type1}(q to quit).          \n"
                                                    f" Current {acc_type2} balance: ${acc_key2:.2f}. \n"
                                                    f" Current {acc_type1} balance: ${acc_key1:.2f}. \n"
                                                    f" : "))
                                                    if am == "q":
                                                        break
                                                    else:
                                                        try:
                                                            fam = float(am)
                                                            result1, result2 = current_user.transfer_acc(fam, acc_choice)
                                                            if result1 == InvalidTypeIn:
                                                                print(f" You must enter a valid amount to transfer!\n"
                                                                    f" (Amount must be a positive number, not exceeding your current balance). \n"
                                                                    f" Your current {acc_type2} balance: ${acc_key2:.2f}.")
                                                            else:
                                                                print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                 f"--------------TRANSFER-TO-ACCOUNT----------------------\n"
                                                                    f" Transfer successful!                                \n"
                                                                    f" You have successfully transfered ${fam:.2f} from your       \n"
                                                                    f" {acc_type2} to your {acc_type1}.                                        \n"
                                                                    f" Your current {acc_type1} balance: ${result1:.2f}     \n"
                                                                    f" Your current {acc_type2} balance: ${result2:.2f}  \n"
                                                                    f"----------------------------------------------------")
                                                                my_bank.save_data()
                                                                time.sleep(3)
                                                                break_all = True
                                                                break
                                                        except ValueError:
                                                                print(f" You must enter a valid amount to withdraw!(positive number, not exceeding your current balance).\n"
                                                                    f" Your current {acc_type2} balance: ${acc_key2:.2f}.")
                                            elif acc_choice == "Investment Account":
                                                acc_type2 = "Main Account"
                                                acc_type1 = "Investment Account"
                                                acc_key2 = current_user.main_acc
                                                acc_key1 = current_user.invest_acc
                                                while True:
                                                    am = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                    f"--------------TRANSFER-TO-ACCOUNT----------------------\n"
                                                    f" {current_user.name}, please enter an amount to     \n"
                                                    f" transfer from your {acc_type2} to your {acc_type1}(q to quit).          \n"
                                                    f" Current {acc_type2} balance: ${acc_key2:.2f}. \n"
                                                    f" Current {acc_type1} balance: ${acc_key1:.2f}. \n"
                                                    f" : "))
                                                    if am == "q":
                                                        break
                                                    else:
                                                        try:
                                                            fam = float(am)
                                                            result1, result2 = current_user.transfer_acc(fam, acc_choice)
                                                            if result1 == InvalidTypeIn:
                                                                print(f" You must enter a valid amount to transfer!\n"
                                                                    f" (Amount must be a positive number, not exceeding your current balance). \n"
                                                                    f" Your current {acc_type2} balance: ${acc_key2:.2f}.")
                                                            else:
                                                                print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                 f"--------------TRANSFER-TO-ACCOUNT----------------------\n"
                                                                    f" Transfer successful!                                \n"
                                                                    f" You have successfully transfered ${fam:.2f} from your       \n"
                                                                    f" {acc_type2} to your {acc_type1}.                                        \n"
                                                                    f" Your current {acc_type1} balance: ${result1:.2f}     \n"
                                                                    f" Your current {acc_type2} balance: ${result2:.2f}  \n"
                                                                    f"----------------------------------------------------")
                                                                my_bank.save_data()
                                                                time.sleep(3)
                                                                break_all = True
                                                                break
                                                        except ValueError:
                                                                print(f" You must enter a valid amount to withdraw!(positive number, not exceeding your current balance).\n"
                                                                    f" Your current {acc_type2} balance: ${acc_key2:.2f}.")
                                        elif tranop == "2":
                                            while True:
                                                userid = (input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f" {current_user.name}, please enter preferable user's\n"
                                                f" account ID(7 digits)(q to quit): "))
                                                if userid == "q":
                                                    break
                                                elif userid in my_bank.users:
                                                    other_user = my_bank.users[userid]
                                                    while True:
                                                        am = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                                        f" {current_user.name}, please enter an amount to    \n"
                                                        f" transfer to {other_user.name}(q to quit).             \n"
                                                        f" Current Main Account balance: ${current_user.main_acc:.2f}. \n"
                                                        f" (NOTICE: amount will be withdrawn from your Main Account) \n"
                                                        f" : ")
                                                        if am == "q":
                                                            break
                                                        elif type(am) == int or float:
                                                            fam = float(am)
                                                            result = my_bank.transfer_user(current_user, other_user, fam)
                                                            if result == InvalidTypeIn:
                                                                print(f" You must enter a valid amount to transfer! \n"
                                                                      f" Amount must be above zero and below your current balance. \n"
                                                                      f" Your current Main Account balance: ${current_user.main_acc:.2f}.\n"
                                                                      f"-------------------------------------\n"
                                                                      f" : ")
                                                                    
                                                            else:
                                                                print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                                 f" {current_user.name}, you have successfully transfered \n"
                                                                 f" ${fam:.2f} to {other_user.name}!  \n"
                                                                 f" Your current Main Account balance: ${current_user.main_acc:.2f} \n"
                                                                 f"---------------------------------------------------\n")
                                                                my_bank.save_data()
                                                                time.sleep(3)
                                                                break_all = True
                                                                break
                                                        else:
                                                            print(" You must enter a valid amount to transfer! \n")
                                                else:
                                                    print(" User account ID was not found! \n"
                                                          " Please enter an existing account ID! \n")
                                                if break_all == True:
                                                    break
                                        else:
                                            print("You must enter a valid operational index(1-3)!")
                                        if break_all == True:
                                            break
                                elif mainmenu == "5":
                                    while True:
                                        i = 1
                                        history = current_user.get_history()
                                        print(f"--------------------CLI-Bank-ATM--------------------\n"
                                                f"-----------------TRANSACTION-HISTORY----------------\n")
                                        for dict in history:
                                            type, amount, account, timestamp, balance_after, counterparty = dict["type"], dict["amount"], dict["account"], dict["timestamp"], dict["balance after"], dict["counterparty"]
                                            print(
                                                f" {i}. Type: {type} | Amount: ${amount:.2f}              \n"
                                                f" Account: {account} | Time: {timestamp}             \n"
                                                f" Balance After: {balance_after:.2f} | Counterparty: {counterparty}\n"
                                                f"----------------------------------------------------\n")
                                            i = i + 1
                                        back = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                         f" Press any key to quit: ")
                                        if back:
                                            break
                                elif mainmenu == "6":
                                    break_all = True
                                    break
                                elif mainmenu == "7":
                                    exit()
                                else:
                                    print('You must enter a valid operation index(1-7)!')
                        elif pin_attempt == "q":
                            break
                        elif pin_check == False:
                            print(f"-------------------------------------------------------\n"
                                  f" Error! You must enter a valid account PIN(4-6 digits)!")
                        if break_all:
                            break 
                elif accid == "q":
                    print("q printed, breaking . . .")
                    break
                else:
                    print(f"--------------------------------------------------\n"
                          f" Error! Please enter a valid account ID(7 digits)!")
                if break_all:
                    break
        elif welcome_choice == "2":
            while True:
                newname = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                f" Please enter your name(q to quit): ")
                if newname == "q":
                    break
                if re.search(r'[^a-zA-Z\s]', newname):
                    print(" You must enter a valid name! \n"
                            " No special characters and numbers allowed! \n")
                else:
                    while True:
                        PIN_input = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                        f"----------------ACCOUNT-REGISTRATION----------------\n"
                                        f"{newname.strip()}, please create your PIN(4-6 digits only)(q to quit):")
                        if PIN_input == "q":
                            return False
                        if len(PIN_input) not in range(4,7):
                            print("PIN is too long or too short! Please enter a valid PIN.")
                        elif re.search(r'[^0-9]', PIN_input):
                            print("Invalid PIN!\n"
                                "You must enter digits only!")
                        else:
                            account_id = str(random.randint(1000000, 9999999))
                            if account_id not in my_bank.users:
                                break            
                    new_user = User(newname.strip(), account_id, PIN_input, 0, 0, None )
                    print(f"--------------------CLI-Bank-ATM--------------------\n"
                            f" You have successfully registered, {newname}!       \n"
                            f" Your assigned account ID is {account_id}.")
                    my_bank.users[account_id] = new_user
                    my_bank.save_data()
                    break
        elif welcome_choice == "3":
            exit() 
        else:
            print(f"----------------------------------------------------\n"
                  f" Error! Please enter a valid operational index(1-3)!")                   

if __name__ == '__main__':
    main()