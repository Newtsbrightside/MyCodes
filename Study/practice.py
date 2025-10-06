#A Tuple Is
tupl = (1, 2, 3)
print(type(tupl))
print(tupl)
#A List Is
lst = [1, 2, 3]
print(type(lst))
print(lst)
#A Set Is
st = {1, 2, 3}
print(type(st))
print(st)
#A Dictionary Is
dct = {'a': 1, 'b': 2, 'c': 3}
print(type(dct))
print(dct)
print(type((1))) # This is not a tuple
print(type((1,))) # This is a tuple
print(type([1])) # This is a list
print(type({1})) # This is a set
print(type({1: 'a'})) # This is a dictionary
print(type({})) # This is a dictionary
print(type(set())) # This is a set
print(type([])) # This is a list
print(type(())) # This is a tuple
def f1(a,b,c):
    print(a,b)
nums = (1,2,3)
#f1(nums) # This will give an error
f1(*nums) # This will work
f1(1,2,3) # This will work
f1(*[1,2,3]) # This will work
f1(*{1,2,3}) # This will work
f1(**{'a':1,'b':2,'c':3}) # This will work
f1(*{'a':1,'b':2,'c':3}) # This will work
#f1(**{'x':1,'y':2,'z':3}) # This will give an error
f1(*{1:'a',2:'b',3:'c'}) # This will work
#f1({1:'a',2:'b',3:'c'}) # This will give an error
a = {1,2,3}
print(sorted(a)[2])
print(type(sorted(a)))
print(sorted(a))
a = {1: 'a', 2: 'b', 3: 'c'}
print(a[2])
a = (1,2,3)
print(a[2])
a = [1,2,3,4,5]
b = [-1,-2,-3,-4,-5]
zipped = zip(a,b)
print(type(zipped))
print(zipped)
print(type(dict(zipped)))
name = ['Asep', 'Budi', 'Caca']
n = enumerate (name)
for i in n:
    print(i)
name = dict(enumerate(name))
print(type(name))
print(name)