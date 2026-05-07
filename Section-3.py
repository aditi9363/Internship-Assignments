Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

#Ans 1
try :
    print("Trying to divide a number by zero...")
    result = 10 / 0
except ZeroDivisionError:
    print("Oops! You cannot divide a number by zero.")
else :
    print("Division successful! Result is:", result)
finally :
    print("This block always runs(cleanup or final messages.)")

    
Trying to divide a number by zero...
Oops! You cannot divide a number by zero.
This block always runs(cleanup or final messages.)


#Ans 2
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except TypeError:
        print("Error: Please provide numeric values only.")
    else:
        print("Division successful! Result is:", result)
    finally:
        print("Operation completed.\n")

        
safe_divide(25, 2)
Division successful! Result is: 12.5
Operation completed.

safe_divide(25, 0)
Error: Cannot divide by zero.
Operation completed.

safe_divide(25, "a")
Error: Please provide numeric values only.
Operation completed.

>>> 
>>> 
>>> #Ans 3
>>> try:
...     num = int(input("Enter an integer: "))
... except ValueError:
...     print("Invalid input! Please enter a valid integer.")
... else:
...     square = num ** 2
...     print("Square of the number is:", square)
... 
...     
Enter an integer: 8
Square of the number is: 64
>>> 
>>> 
>>> #Ans 4
>>> class NegativeNumberError(Exception):
...     pass
... 
>>> def check_number(num):
...     if num < 0:
...         raise NegativeNumberError("Negative numbers are not allowed!")
...     else:
...         print("Valid number entered:", num)
... 
...         
>>> try:
...     n = int(input("Enter a number: "))
...     check_number(n)
... except NegativeNumberError as e:
...     print("Custom Error:", e)
... except ValueError:
...     print("Invalid input! Please enter an integer.")
... 
...     
Enter a number: -5
Custom Error: Negative numbers are not allowed!
