    # import json, time, re and random(account_id creation)
import json
import random
import time
import re

    # open json file as userdata
with open ("CLI_users.json", "r") as f:
    userdata = json.load(f)

    # create certain functions for certain operations
    # define save data
def save_data():
    with open("CLI_users.json", "w") as f:
        json.dump(userdata, f, indent=4)
    time.sleep(3)

    # define registration of account
def account_registration():
    while True:
        name_input = input(f"--------------------CLI-Bank-ATM--------------------\n"
                    f"----------------ACCOUNT-REGISTRATION----------------\n"
                    f"Please enter your name(q to quit):")
        if name_input == "q":
            return False
        
        if re.search(r'[^a-zA-Z\s]', name_input):
            print("You must enter a valid name! \n"
                "No special characters and numbers allowed!") 
        else:
            while True:
                PIN_input = input(f"--------------------CLI-Bank-ATM--------------------\n"
                                f"----------------ACCOUNT-REGISTRATION----------------\n"
                                f"{name_input.strip()}, please create your PIN(4-6 digits only)(q to quit):")
                if PIN_input == "q":
                    return False
                if len(PIN_input) not in range(4,7):
                    print("PIN is too long or too short! Please enter a valid PIN.")
                elif re.search(r'[^0-9]', PIN_input):
                    print("Invalid PIN!\n"
                        "You must enter digits only!")
                else:
                    account_id = str(random.randint(1000000, 9999999))
                    if account_id not in userdata:
                        break            
            new_user = {account_id : {'name' : name_input.strip(), 'PIN' : PIN_input, 'main_acc' : 0, 'invest_acc' : 0 }}
            userdata.update(new_user)
            print(f"--------------------CLI-Bank-ATM--------------------\n"
                    f" You have successfully registered, {name_input}!       \n"
                    f" Your assigned account ID is {account_id}.")
            save_data()
            return False 
    # define PIN check
def check_PIN(account_id):
    while True:
        PIN = input(f"--------------------CLI-Bank-ATM--------------------\n"
                    f"----------------------PIN-CHECK---------------------\n"
                    f"   Welcome, {userdata[account_id]["name"]}!         \n"
                    f"   Please enter your PIN(4-6 digits)(q to quit)     \n"
                    f"                                                    \n"
                    f"----------------------------------------------------\n")
        if PIN == "q":
            return False
        try:
            if PIN == userdata[account_id]["PIN"]:
                    return 
            else:
                  print("Incorrect PIN! \n"
                        "You must enter a valid PIN(4-6 digits only!)")
        except ValueError as e:
              print(f"Error! {e}")

    # define main menu
def mainmenu(account_id):
    while True:
        print(f"----------------CLI-Bank-ATM-----------------\n"
              f"--------------------MENU---------------------\n"
              f"Welcome back, {userdata[account_id]["name"]}!\n"
              f"Please select an operation to run:           \n"
              f"-- 1. Check Balance                          \n"
              f"-- 2. Deposit money                          \n"
              f"-- 3. Withdraw money                         \n"
              f"-- 4. Transfer Money                         \n"
              f"-- 5. Log out                                \n"
              f"-- 6. Exit                                   \n"
              f"---------------------------------------------\n")
        oper_input = input('What operation would you like to choose(1-5): ')
        if oper_input == "1":
            check_balance(account_id)
        elif oper_input == "2":
            deposit(account_id)
        elif oper_input == "3":
            withdraw(account_id)
        elif oper_input == "4":
            transfer(account_id)
        elif oper_input == "5":
            return False
        elif oper_input == "6":
            exit()
        else:
            print("Invalid operation index! \n"
                    "You must enter a valid operation index(1-5 only!)") 

    # define account choice
def account_pick(account_id):
    while True:
        print(f"----------------CLI-Bank-ATM-----------------\n"
          f"---------------ACCOUNT-CHOICE----------------\n"
          f"{userdata[account_id]["name"]}, what account \n"
          f" would you like to choose:                   \n"
          f"-- 1. Main account                           \n"
          f"-- 2. Investment account                     \n"
          f"-- 3. Go back                                \n"
          f"---------------------------------------------\n")
        acc_pick = input('What account would you like to choose(1-3): ')
        if acc_pick == "1":
            return 'MA'
        elif acc_pick == "2":
            return 'IA'
        elif acc_pick == "3":
            return False
        else:
            print("Incorrect operation index! \n"
                    "You must enter a valid operation index(1-3 only!)")

    # define checkbalance
def check_balance(account_id):
    acc_pick = account_pick(account_id)
    if acc_pick == "MA":
        print(f"-------------------------CLI-Bank-ATM--------------------------\n"
              f"Your Main account balance: ${userdata[account_id]["main_acc"]:.2f}.\n"
              f"---------------------------------------------------------------\n")
        time.sleep(2)
    elif acc_pick == "IA":
        print(f"-----------------------------CLI-Bank-ATM-------------------------------\n"
              f"Your Investement account balance: ${userdata[account_id]["invest_acc"]:.2f}.\n"
              f"------------------------------------------------------------------------\n")
        time.sleep(2)

    # define deposit function
def deposit(account_id):
    acc_pick = account_pick(account_id)
    if acc_pick == "MA":
        deposit_operation(account_id, acc_pick)
    elif acc_pick == "IA":
        deposit_operation(account_id, acc_pick)
    else:
        return
    
    # define deposit operation
def deposit_operation(account_id, acc_pick):
    while True:
        key = 'main_acc' if acc_pick == "MA" else 'invest_acc'
        text_key = 'Main Account' if acc_pick == "MA" else 'Investment Account'
        depam = input(f"--------------------------CLI-Bank-ATM----------------------------\n"
                    f"Current {text_key} balance: ${userdata[account_id][key]:.2f}.\n"
                    f"Please enter an amount for deposit(digits only!)(q to quit):\n")
        if depam == "q":
            return False
        try:
            amount = float(depam)
            if amount <= 0:
                print("Error! Please enter a positive amount to deposit!")
            else:
                userdata[account_id][key] += float(amount)
                print(f"You have successfully deposited ${amount:.2f} to your {text_key}!       \n"
                    f"Your current {text_key} balance: ${userdata[account_id][key]:.2f}.")
                save_data()
                return False 
        except ValueError:
            print("Error! Please enter a valid deposit amount!")
        
    # define withdraw function
def withdraw(account_id):
    acc_pick = account_pick(account_id)
    if acc_pick == "MA":
        withdraw_operation(account_id, acc_pick)
    if acc_pick == "IA":
        withdraw_operation(account_id, acc_pick)

    # define withdraw operation
def withdraw_operation(account_id, acc_pick):
    while True:
        key = 'main_acc' if acc_pick == "MA" else 'invest_acc'
        text_key = 'Main Account' if acc_pick == "MA" else 'Investment Account'
        withdam = input(f"--------------------------CLI-Bank-ATM----------------------------\n"
                        f"Current {text_key} balance: ${userdata[account_id][key]:.2f}.\n"
                        f"Please enter an amount to withdraw(digits only!)(q to quit):\n")
        if withdam == "q":
            return False
        try:
            amount = float(withdam)
            if amount <= 0:
                print("Error! Please enter a positive amount to withdraw!")
            elif amount > userdata[account_id][key]:
                print("Error! Insufficient funds!")
            else:
                userdata[account_id][key] -= float(amount)
                print(f"You have successfully withdrawn ${amount:.2f} from your {text_key}!       \n"
                    f"Your current {text_key} balance: ${userdata[account_id]["main_acc"]:.2f}.")
                save_data()
                return False 
        except ValueError:
            print("Error! Please enter a valid withdraw amount!")

    # define transfer between accounts and users of the same bank
def transferoption(account_id):
    while True:
        print("-----------------CLI-Bank-ATM-----------------\n"
          f"------------------TRANSFER-------------------\n"
          f"{userdata[account_id]["name"]}, what transfer\n"
          f" option would you like to choose:            \n"
          f"-- 1. To my another account                  \n"
          f"-- 2. To another user                        \n"
          f"-- 3. Go back                                \n"
          f"---------------------------------------------\n")
        tran_op_pick = input('What transfer option would you like to choose(1-3): ')
        if tran_op_pick == "1":
            return "Acc"
        elif tran_op_pick == "2":
            return "User"
        elif tran_op_pick == "3":
            return False
        else:
            print("Incorrect operation index! \n"
                    "You must enter a valid operation index(1-3 only!)")

def transferoptionacc(account_id):
    while True:
        print("-----------------CLI-Bank-ATM-----------------\n"
            f"------------------TRANSFER-------------------\n"
            f"{userdata[account_id]["name"]}, what account \n"
            f"would you like to transfer to:               \n"
            f"-- 1. To my main account                     \n"
            f"-- 2. To my investment account               \n"
            f"-- 3. Go back                                \n"
            f"---------------------------------------------\n")
        tran_acc_op_pick = input('What account would you like to transfer to(1-3): ')
        if tran_acc_op_pick == "1":
            return "MA"
        elif tran_acc_op_pick == "2":
            return "IA"
        elif tran_acc_op_pick == "3":
            return False
        else:
            print("Incorrect operation index! \n"
                    "You must enter a valid operation index(1-3 only!)")
                
    # define transfer
def transfer(account_id):
    op_tran = transferoption(account_id)
    if op_tran == "Acc":
        acc_pick = transferoptionacc(account_id)
        if acc_pick == False:
            return False
        else:
            transfer_b_accounts(account_id, acc_pick)

    elif op_tran == "User":
        while True:
            userid = input(f"--------------TRANSFER-TO-USER---------------\n"
                           f"{userdata[account_id]["name"]}, please enter \n"
                           f"user's account ID(7 digits) to proceed with  \n"
                           f"transfer(q to go back).                      \n"
                           f"---------------------------------------------\n")
            if userid == "q":
                        return False
            if userid == account_id:
                print("You can't transfer to yourself!")
            else:
                try:
                    if userid in userdata:
                        while True:
                            amount = input(f"--------------TRANSFER-TO-USER---------------\n"
                                            f"{userdata[account_id]["name"]}, please enter  \n"
                                            f"an amount to transfer to {userdata[userid]["name"]} \n"
                                            f"(q to quit):                                  \n"
                                            f" Your Main account balance:                   \n"
                                            f"  ${userdata[account_id]["main_acc"]:.2f}.        \n"
                                            f"--------------------------------------------- \n")
                            if amount == "q":
                                return False
                            try:
                                am = float(amount)
                                if am <= 0:
                                    print("Please enter a positive amount to transfer!")
                                elif am > userdata[account_id]["main_acc"]:
                                    print("Error! Insuffiecient funds!")
                                else:
                                    userdata[account_id]["main_acc"] -= float(am)
                                    userdata[userid]["main_acc"] += float(am)
                                    print(f"--------------------------------CLI-Bank-ATM---------------------------------\n"
                                        f"You have successfully transfered ${am} to {userdata[userid]["name"]}'s Account!\n"
                                        f"Your current Main Account balance: ${userdata[account_id]["main_acc"]:.2f}.      \n"
                                        f"-----------------------------------------------------------------------------")
                                    save_data()
                                    return False
                            except ValueError as e:
                                    print(f"Error! {e}")
                    else:
                        print("Used ID has not been found! \n"
                            "Please enter a valid user ID!")
                except ValueError as e:
                    print(f"Error! {e}")
                        
                    if len(userid.replace(" ", "")) == 7 and userid.isalpha() == False and userid.replace(" ", "") not in userdata and userid.replace(" ", "") != "":
                        print("Error! You typed in a wrong user ID!")
    else:
          return False         

    # define transfer between user's own accounts
def transfer_b_accounts(account_id, acc_pick):
    while True:
        key = 'main_acc' if acc_pick == "MA" else 'invest_acc'
        key_2 = 'invest_acc' if acc_pick == "MA" else 'main_acc'
        text_key = 'Main Account' if acc_pick == "MA" else 'Investment Account'
        text_key_2 = 'Investment Account' if acc_pick == "MA" else 'Main Account'
        amount = input(f"--------------------------------CLI-Bank-ATM---------------------------------\n"
                        f"Current {text_key} balance: ${userdata[account_id][key]:.2f}.           \n"
                        f"Current {text_key_2} balance: ${userdata[account_id][key_2]:.2f}.   \n"
                        f"Please enter an amount to transfer to {text_key}(digits only!)(q to quit):\n ")
        if amount == "q":
            return False
        try:
            amount = float(amount)
            if amount <= 0:
                print("Please enter a positive amount to transfer!")
            elif amount > userdata[account_id][key_2]:
                print("Error! Insufficient funds!")
            else:
                userdata[account_id][key_2] -= float(amount)
                userdata[account_id][key] += float(amount)
                print(f"--------------------------------CLI-Bank-ATM---------------------------------\n"
                    f"You have successfully transfered ${amount} to your {text_key}!           \n"
                    f"Your current {text_key} balance: ${userdata[account_id][key]:.2f}.      \n"
                    f"Your current {text_key_2} balance: ${userdata[account_id][key_2]:.2f}.\n"
                    f"-----------------------------------------------------------------------------")
                save_data()
                return False
        except ValueError as e:
                print(f"Error! {e}")
                  
    # login system
while True:
    print(f"--------------------CLI-Bank-ATM--------------------\n"
        f"                                                      \n"
        f"                    1. [Log in]                       \n"
        f"                    2. [Create Account]               \n"
        f"                    3. [Exit]                         \n")
    welcomechoice = input(
        f"Please enter(1-3):                \n"
        f"------------------------------------------------------\n")
    if welcomechoice == "1":
        while True:
            account_id = input(f"--------------------CLI-Bank-ATM--------------------\n"
                            f"Please enter your account ID(7 digits)(q to quit):")
            if account_id == "q":
                break
            try:
                if account_id in userdata:
                    PIN_check = check_PIN(account_id)
                    if PIN_check == False:
                        break
                    else:
                        mainmenu(account_id)
                else:
                    print("You must enter a valid account ID(7 digits only!)") 
            except ValueError as e:
                print(f"Error: {e}")
    elif welcomechoice == "2":
        newus = account_registration()
    elif welcomechoice == "3":
        exit()
    else:
        print("You must enter a valid operation index(1-3 only!)")