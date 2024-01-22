#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

menu = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

question = ("What would you like to drink? Espresso is $1.50, Latte is $2.50, Cappuccino is $3.00. Type espresso, "
            "latte, or cappuccino:")
turn_off = "off"
show_report = "report"
profit = 0.00


def main():
    configure_logger()
    is_on = True
    has_resources = True
    while is_on:
        choice = input(question)
        if choice == turn_off:
            is_on = False
            break
        elif choice == show_report:
            print_report()
            break
        elif check_valid_choice(choice):
            if is_resource_sufficient(menu[choice]["ingredients"]) and process_coins(menu[choice]):
                make_coffee(menu[choice])
                print("Enjoy your " + choice + "!")


def configure_logger():
    """
    Configure the logger with a RotatingFileHandler and a StreamHandler.
    File name is coffe.log, maxBytes is 102400 (100KB), backupCount=10
    """
    # eventually move this to the logging-config.ini file
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    file_handler = RotatingFileHandler('coffee.log', maxBytes=102400, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # write to standard out so it ends up in container logs
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def check_valid_choice(choice):
    if choice not in menu.keys():
        print("Valid choices are: ")
        print(menu.keys())
        return False
    return True


def is_resource_sufficient(order_ingredients):
    is_enough = True
    for item in order_ingredients:
        if order_ingredients[item] >= resources[item]:
            print("Sorry there is not enough " + item)
            is_enough = False
    return is_enough


def process_coins(item):
    price = item["cost"]
    price_format = "${:,.2f}".format(price)
    print("Please insert " + price_format + " in coins.")
    quarters = int(input("How many quarters?"))
    dimes = int(input("How many dimes?"))
    nickels = int(input("How many nickels?"))
    pennies = int(input("How many pennies?"))
    quarters_total = quarters * 0.25
    dimes_total = dimes * 0.10
    nickels_total = nickels * 0.05
    pennies_total = pennies * 0.01
    total_inserted = quarters_total + dimes_total + nickels_total + pennies_total
    total_inserted_currency = "${:,.2f}".format(total_inserted)
    if price > total_inserted:
        print("Sorry, that's not enough. You inserted " + total_inserted_currency + ". Transaction canceled. Money "
                                                                                    "refunded")
        return False
    if price < total_inserted:
        change = total_inserted - price
        currency_string = "${:,.2f}".format(change)
        print("Here is your change: " + currency_string)
    return True


def make_coffee(item):
    resources["water"] = resources["water"] - item["water"]
    resources["milk"] = resources["milk"] - item["milk"]
    resources["coffee"] = resources["coffee"] - item["coffee"]


def print_report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
