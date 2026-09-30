# CLI Bank ATM

A terminal-based banking system written in pure Python.

## Features
- Account registration with randomly generated 7-digit IDs
- Secure PIN authentication (4-6 digits)
- Two accounts per user: Main Account + Investment Account
- Deposit / Withdraw
- Transfer money between your own accounts
- Transfer money to other users
- Persistent storage using JSON
- Input validation and basic error handling

## How to Run

1. Clone the repository
2. Make sure you have Python 3.8+ installed
3. Copy the example data:
   ```bash
   cp CLI_users_example.json CLI_users.json
4. Run the program:
   ```bash
   python bank.py

## Project Structure

cli-bank-atm/
 - bank.py
 - CLI_users.json
 - .gitignore
 - README.md

## Future Plans

 - Refactor to Object-Oriented Programming (OOP)
 - Add better error handling
 - Add transaction history
 - Possibly a simple GUI later

## Author
Kanat
