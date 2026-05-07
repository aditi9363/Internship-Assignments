Python 3.12.3 (tags/v3.12.3:f6650f9, Apr  9 2024, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.

#Ans 1
age = 21
print(age, type(age))
21 <class 'int'>
price = 432.50
print(price, type(price))
432.5 <class 'float'>
name = "Riya"
print(name, type(name))
Riya <class 'str'>
fruits = ["apple","banana","cherry","mango"]
print(fruits, type(fruits))
['apple', 'banana', 'cherry', 'mango'] <class 'list'>
coordinates = (10,20,30)
print(coordinates, type(coordinates))
(10, 20, 30) <class 'tuple'>
student = {"name" : "Riya", "age" : 24, "marks" : 70}
print(student, type(student))
{'name': 'Riya', 'age': 24, 'marks': 70} <class 'dict'>
unique_numbers = {1,2,3,4,5}
print(unique_numbers, type(unique_numbers))
{1, 2, 3, 4, 5} <class 'set'>


#Ans 2 - Container data types are list,tuple,dictionary and set.Container data types are those that can store multiple values in a single variable.
fruits = ["apple","mango","banana","cherry"]
print(fruits)
['apple', 'mango', 'banana', 'cherry']
#list - stores a collection of fruit names
coordinates = (10,20,30)
print(coordinates)
(10, 20, 30)
#tuple - stores fixed coordinate values
student = {"name" : "Ovi", "age" : 24, "marks" : 80}
print(student)
{'name': 'Ovi', 'age': 24, 'marks': 80}
#dictionary - stores student details in key-value pairs
unique_numbers = {1,2,3,4,5}
print(unique_numbers)
{1, 2, 3, 4, 5}
#set - stores unique numbers


#Ans 3
data = 50
print(data, type(data))
50 <class 'int'>
data = 75.5
print(data, type(data))
75.5 <class 'float'>
data = "Hello world"
print(data, type(data))
Hello world <class 'str'>
data = [10,20,30,40]
print(data, type(data))
[10, 20, 30, 40] <class 'list'>
#Here we are using one variable(data) again and again.But storing different types of data in the same variable, python automatically changes the type. this is called dynamic typing


#Ans 4
#LIST
fruits = ["apple","banana","apple","cherry"]
print(fruits)
['apple', 'banana', 'apple', 'cherry']
fruits.append("mango")
print(fruits)
['apple', 'banana', 'apple', 'cherry', 'mango']
#list - ordered, allows duplicates, mutable(can change)
#TUPLE
numbers = (1, 2, 2, 3)
print(numbers)
(1, 2, 2, 3)
#numbers.append(4) - not allowed
#tuple - ordered, allows duplicates, immutable(cannot change)
#DICTIONARY
student = {"name" : "Riya", "age" : 19, "marks" : 78}
print(student)
{'name': 'Riya', 'age': 19, 'marks': 78}
student["age"] = 25
print(student)
{'name': 'Riya', 'age': 25, 'marks': 78}
#dictionary - ordered, duplicates not allowed(keys must be unique), mutable(can change)
#SET
unique_numbers = {1, 2, 2, 3}
print(unique_numbers)
{1, 2, 3}
unique_numbers.add(4)
print(unique_numbers)
{1, 2, 3, 4}
#set - unordered(no fix order), duplicates not allowed(automatically removed), mutable(can change)


#Ans 5
age = 26
price = 99.9
name = "Ira"
fruits = ["apple", "mango", "cherry"]
numbers = (11, 22, 33)
student = {"name" : "Riya", "age" : 30, "marks" : 82}
unique = {1, 2, 3}
print(type(age))
<class 'int'>
print(type(price))
<class 'float'>
print(type(name))
<class 'str'>
print(type(fruits))
<class 'list'>
print(type(numbers))
<class 'tuple'>
print(type(student))
<class 'dict'>
print(type(unique))
<class 'set'>
#Here type() shows the class name of data type.


#Ans 6
value = 50
print(type(value))
<class 'int'>
value = "hello world"
print(type(value))
<class 'str'>
value = ["apple" ,"cherry", "guava"]
print(type(value))
<class 'list'>
#Observation - Same variable 'value' stores different types of data (int -> str -> list).Python automatically changes the type, this is called dynamic typing.


#Ans 7
#int
x = 20
x = int(20)
x = 0

#float
f = 10.5
f = float(10.5)
f = 0.0

#string
s = "hello"
s = str("hello")
s = ""
s += "world"

#list
l = [1, 2, 3]
l = list([1, 2, 3])
l = []
l.append(4)

#tuple
t = (1, 2)
t = tuple([1,2])
t = ()          #cannot add later

#dictionary
d = {"a":1}
d = dict(a=1)
d = {}
d["b"] = 2

#set
st = {11, 22}
st = set([11, 22])
st = set()
st.add(33)


#Ans 8
#STRING
text = "HelloWorld"
print(len(text))
10

print(text[0:5])
Hello
print(text[0:10:2])
Hlool
newtext = text + "123"
print(newtext)
HelloWorld123

#LIST
nums = [3, 2, 5, 6]
print(len(nums))
4
print(nums[1:3])
[2, 5]
nums2 = [10, 20]
print(nums + nums2)
[3, 2, 5, 6, 10, 20]
nums.append(11)
print(nums)
[3, 2, 5, 6, 11]
nums.sort()
print(nums)
[2, 3, 5, 6, 11]
mixed = [1, "hi", 55.5]
print(mixed)
[1, 'hi', 55.5]
matrix = [[1, 2], [3, 4]]
for row in matrix:
    for item in row:
        print(item)

        
1
2
3
4

#TUPLE
t = (6, 2, 8,1)
print(len(t))
4
print(t[1:3])
(2, 8)
print(t[0])
6
t2 = (3, 9)
print(t + t2)
(6, 2, 8, 1, 3, 9)
temp = list(t)
temp.sort()
t_sorted = tuple(temp)
print(t_sorted)
(1, 2, 6, 8)

#DICTIONARY
student = {"name" : "Ira", "age" : 20, "marks" : 85}
print(len(student))
3
student["city"] = "Pune"
print(student)
{'name': 'Ira', 'age': 20, 'marks': 85, 'city': 'Pune'}
print(student["name"])           #access value using key
Ira
print(student.keys())
dict_keys(['name', 'age', 'marks', 'city'])
print(student.values())
dict_values(['Ira', 20, 85, 'Pune'])
student["age"] = 23
print(student)
{'name': 'Ira', 'age': 23, 'marks': 85, 'city': 'Pune'}
for key,value in student.items():
    print(key, value)

    
name Ira
age 23
marks 85
city Pune

#SET
s1 = {10, 20, 30}
s2 = {40, 50, 60}
print(len(s1))
3
s1.add(40)
print(s1)
{40, 10, 20, 30}
s1.remove(20)
print(s1)
{40, 10, 30}
s1.pop()
40
print(s1)
{10, 30}
print(s1.union(s2))
{50, 40, 10, 60, 30}
print(s1.intersection(s2))
set()

>>> 
>>> #Ans 9
>>> #list -> tuple
>>> my_list = [1, 2, 3]
>>> my_tuple = tuple(my_list)
>>> print(my_list, type(my_list))
[1, 2, 3] <class 'list'>
>>> print(my_tuple, type(my_tuple))
(1, 2, 3) <class 'tuple'>
>>> 
>>> #tuple -> list
>>> new_list = list(my_tuple)
>>> print(new_list, type(new_list))
[1, 2, 3] <class 'list'>
>>> 
>>> #dict.keys() and dict.values() -> list
>>> student = {"name" : "Ovi", "age" : 28, "marks" : 62}
>>> keys_list = list(student.keys())
>>> values_list = list(student.values())
>>> print(keys_list, type(keys_list))
['name', 'age', 'marks'] <class 'list'>
>>> print(values_list, type(values_list))
['Ovi', 28, 62] <class 'list'>
>>> 
>>> #int -> float
>>> a = 15
>>> b = float(a)
>>> print(b, type(b))
15.0 <class 'float'>
>>> 
>>> #float -> int
>>> c = 25.6
>>> d = int(c)
>>> print(d, type(d))
25 <class 'int'>
>>> 
>>> #int -> str
>>> num = 100
>>> num_str = str(num)
>>> print(num_str, type(num_str))
100 <class 'str'>
