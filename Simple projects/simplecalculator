#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 23:40:35 2024

@author: vaishnav
"""

print("This is a calculator.")
status = 0
while status == 0:
    try:
        a = float(input("Enter your first number: "))
        b = float(input("Enter your second number: "))
        c = input("Select your operator: \n + for addition \n - for subtraction\n * for multiplication\n / for division\n")

        if c == "+":
            print(a, '+', b, '=', a + b)
        elif c == "-":
            print(a, '-', b, '=', a - b)
        elif c == "*":
            print(a, '*', b, '=', a * b)
        elif c == "/":
            if b != 0:
                print(a, '/', b, '=', a / b)
            else:
                print("Error: Division by zero")
        else:
            print("Invalid operation")
    except ValueError:
        print("Invalid input. Please enter a valid number")
    else:
        d = input("Do you want to continue?(y/n):\n")
        if d == "y":
            status = 0
        elif d == "n":
            status = 1
        else:
            print("Invalid response. Exiting!")
            status = 1
    
        
