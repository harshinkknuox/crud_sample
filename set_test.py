# Adding Items to a Set.
# Once a set is created we cannot change any items and we can also add additional items.
# Unordered.


fruits = {'banana', 'orange', 'mango', 'lemon'}
print(len(fruits))
print('mango' in fruits)
fruits.add('lime')
print("added:",fruits)
fruits.update(['watermelon','carrot'])
print("updated:",fruits)
vegetables = ('tomato', 'potato', 'cabbage','onion', 'carrot')
fruits.update(vegetables)
print("updateddd:",fruits)
# fruits.remove('tomato')
removed_item = fruits.pop()#removes a random item
print("popped:",fruits)
print("removed_item:",removed_item)#print the removed random item

# Converting List to Set
# We can convert list to set and set to list. Converting list to set removes duplicates and only unique items will be reserved.

list_fruits = ['banana', 'orange', 'mango', 'lemon','orange', 'banana']
age = [22, 19, 24, 25, 26, 24, 25, 24]
print("length of age",len(age))
set_fruits = set(list_fruits)
print("List to set :",set_fruits) #list Coverted to Set and Duplicates removed Autmtcly 
it_companies = {'NUOX','IBM','Wipro','EDU','Apple'}
print(len(it_companies))
it_companies.add('Netflix')
print("added:",it_companies)

age_set = set(age)
print("age_set",age_set)
print("length of age_set",len(age_set))

