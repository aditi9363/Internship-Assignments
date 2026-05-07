Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

#Ans 1
def calculate_total(price, quantity=1):
    total = price * quantity
    return total

result1 = calculate_total(200)
result2 = calculate_total(200, 3)
print("Without passing quantity:", result1)
Without passing quantity: 200
print("With passing quantity:", result2)
With passing quantity: 600


#Ans 2
x = "Global Scope"
def outer_function():
    x = "Enclosing Scope"
    def inner_function():
        x = "Local Scope"
        print("Inside inner function:", x)     #Local Scope
    inner_function()
    print("Inside outer function:", x)       #Enclosing Scope

    
outer_function()
Inside inner function: Local Scope
Inside outer function: Enclosing Scope
>>> print("At global level:", x)      #Global Scope
At global level: Global Scope
>>> 
>>> 
>>> #Ans 3
>>> def outer_function():
...     greeting = "Hello Everyone, Good morning."
...     def inner_function():
...         print("Inner function says:", greeting)
...     inner_function()
... 
...     
>>> outer_function()
Inner function says: Hello Everyone, Good morning.
>>> 
>>> 
>>> #Ans 4
>>> #Global
>>> x = 10
>>> def modify_global():
...     global x
...     x = x + 5
... 
...     
>>> print("Before function call:", x)
Before function call: 10
>>> modify_global()
>>> print("After function call:", x)
After function call: 15
>>> 
>>> #Nonlocal
>>> def outer_function():
...     x = 20
...     def inner_function():
...         nonlocal x
...         x = x + 10
... 
...         
>>> print("Before inner function:", x)
Before inner function: 15
