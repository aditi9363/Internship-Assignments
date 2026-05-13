Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

#Ans 1
with open("student_data.txt", "w") as file:
    file.write("Virat - 94\n")
    file.write("Ira - 87\n")
    file.write("Rohit - 80\n")
    file.write("Anvi - 73\n")
    file.write("Ovi - 69\n")

    
11
9
11
10
9
print("Data written successfully into student_data.txt")
Data written successfully into student_data.txt


#Ans2
with open("student_data.txt", "r") as file:
    content = file.read()

    
print("Using read():")
Using read():
print(content)
Virat - 94
Ira - 87
Rohit - 80
Anvi - 73
Ovi - 69

with open("student_data.txt", "r") as file:
    lines = file.readlines()

    
print("Using readlines():")
Using readlines():
>>> print(lines)
['Virat - 94\n', 'Ira - 87\n', 'Rohit - 80\n', 'Anvi - 73\n', 'Ovi - 69\n']
>>> 
>>> 
>>> #Ans 3
>>> with open("student_data.txt", "r") as file:
...     for line_number, line in enumerate(file, start=1):
...         print(line_number, ":", line.strip())
... 
...         
1 : Virat - 94
2 : Ira - 87
3 : Rohit - 80
4 : Anvi - 73
5 : Ovi - 69
>>> 
>>> 
>>> #Ans 4
>>> with open("student_data.txt", "a") as file:
...     file.write("Om - 97\n")
...     file.write("Neha - 70\n")
... 
...     
8
10
>>> with open("student_data.txt", "r") as file:
...     content = file.read()
... 
...     
>>> print(content)
Virat - 94
Ira - 87
Rohit - 80
Anvi - 73
Ovi - 69
Om - 97
Neha - 70

