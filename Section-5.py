Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

#Ans 1
import sys
sys.argv = ["args_demo.py", "apple", "banana", "mango"]
print("Script name is:", sys.argv[0])
Script name is: args_demo.py
for index, arg in enumerate(sys.argv):
    print(f"Index {index} : {arg}")

    
Index 0 : args_demo.py
Index 1 : apple
Index 2 : banana
Index 3 : mango


#Ans 2
import sys
sys.argv = ["sum.py", "10", "20", "30"]
>>> if len(sys.argv) == 1:
...     print("No numbers provided. Please pass numbers as arguments.")
... else:
...     total = 0
...     for arg in sys.argv[1:]:
...         total += int(arg)
...     print("Sum of given numbers is:", total)
... 
...     
Sum of given numbers is: 60
>>> 
>>> 
>>> #Ans 3
>>> import sys
>>> sys.argv = ["calc.py", "20", "+", "15"]
>>> if len(sys.argv) != 4:
...     print("Usage: python calc.py <number1> <operator> <number2>")
... else:
...     num1 = float(sys.argv[1])
...     operator = sys.argv[2]
...     num2 = float(sys.argv[3])
...     if operator == "+":
...         result = num1 + num2
...     elif operator == "-":
...         result = num1 - num2
...     elif operator == "*":
...         result = num1 * num2
...     elif operator == "/":
...         if num2 == 0:
...             print("Error: Division by zero is not allowed")
...         else:
...             result = num1 / num2
...     else:
...         print("Error: Invalid operator. Use +, -, *, /")
...     if 'result' in locals():
...         print("Result:", result)
... 
...         
Result: 35.0
