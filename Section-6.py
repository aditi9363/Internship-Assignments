Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
>>> #Ans 1
>>> class Student:
...     def __init__(self):
...         self.name = "Unknown"
...         self.age = 0
...         self.grade = "Not Assigned"
...     def get_name(self):
...         return self.name
...     def get_age(self):
...         return self.age
...     def get_grade(self):
...         return self.grade
...     def set_name(self, name):
...         self.name = name
...     def set_age(self, age):
...         self.age = age
...     def set_grade(self, grade):
...         self.grade = grade
...     def display(self):
...         print("Student Details:")
...         print("Name :", self.name)
...         print("Age :", self.age)
...         print("Grade :", self.grade)
... 
...         
>>> s1 = Student()
>>> s1.set_name("Virat")
>>> s1.set_age(24)
>>> s1.set_grade("A")
>>> s1.display()
Student Details:
Name : Virat
Age : 24
Grade : A
>>> print(s1.get_name())
Virat
>>> print(s1.get_age())
24
>>> print(s1.get_grade())
A


#Ans 2
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Grade:", self.grade)

        
student1 = Student("Ira", 18, "A")
student2 = Student("Raj", 19, "B")
student1.display()
Name: Ira
Age: 18
Grade: A
student2.display()
Name: Raj
Age: 19
Grade: B


#Ans 3
class Student:
    def __init__(self, name, age, grade):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        if not isinstance(grade, str):
            raise TypeError("Grade must be a string")
        self.name = name
        self.age = age
        self.grade = grade
    def set_age(self, age):
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
        self.age = age
    def display(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Grade:", self.grade)
        print("----------------------")

        
print("---Valid Input---")
---Valid Input---
try:
    student1 = Student("Rohit", 18, "A")
    student1.display()
except Exception as e:
    print("Error:", e)

    
Name: Rohit
Age: 18
Grade: A
----------------------
print("---Invalid Input(wrong type for age)---")
---Invalid Input(wrong type for age)---
try:
    student2 = Student("Isha", "18", "B")
    student2.display()
except Exception as e:
    print("Error:", e)

    
Error: Age must be an integer
print("---Invalid Input(out of range)---")
---Invalid Input(out of range)---
try:
    student3 = Student("Neha", 200, "A")
    student3.display()
except Exception as e:
    print("Error:", e)

    
Error: Age must be between 0 and 150
print("---Testing setter---")
---Testing setter---
try:
    student1.set_age(26)
    student1.display()
    student1.set_age("30")
except Exception as e:
    print("Error:", e)

    
Name: Rohit
Age: 26
Grade: A
----------------------
Error: Age must be an integer
