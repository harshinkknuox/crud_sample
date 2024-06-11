person = {
    'first_name':'Asabeneh',
    'last_name':'Yetayeh',
    'age':250,
    'country':'Finland',
    'is_marred':True,
    'skills':['JavaScript', 'React', 'Node', 'MongoDB', 'Python'],
    'address':{
        'street':'Space street',
        'zipcode':'02210'
    }
    }
person['job title'] = 'Python Dev' #creating new key & values

person['skills'].append('HTML') #adding to skill key HTML value
person["first_name"] = 'Harshin' #editing or renaming first_name
person["age"] = 18
person.pop('is_marred')
keys = person.keys()

values = person.values()



#Tuples - We can change tuples to lists and lists to tuples. Tuple is immutable if we want to modify a tuple we should change it to a list.

tpl = ('item1', 'item2', 'item3','item4')
all_items = tpl[0:4]        
all_items = tpl[0:] 
print('all_items==',all_items)#all_items== ('item1', 'item2', 'item3', 'item4')     
middle_two_items = tpl[1:3]
print('==',middle_two_items) #== ('item2', 'item3')
tpl_list = list(tpl)
print(tpl_list)
tpl_list[0]= 'hi'
tpl_list = tuple(tpl_list)
print(tpl_list)
