#Create a student dictionary and add first_name, last_name, gender, age, marital status, skills, country, city and address as keys for the dictionary

student = {}
student['first_name'] = 'Mohammed'
student['last_name'] = 'Harshin'
student['gender'] = 'Male'
student['age'] = 25
student['marital status'] = 'Single'
student['skills'] = []
student['country'] = 'India'
student['city'] = 'Malappuram'
print("Student",student)
student['skills'].append('HTML')
student['skills'].append('CSS')
student['skills'].append('Python')
print("Student",student)
print("Length of Std dictionary:",len(student))
print('values_of_skill:',student['skills'])

values_of_dict = student.values()
dict_as_keys = student.keys()
print(dict_as_keys)
print(values_of_dict)
print("dict to list using items()",student.items())
print("removed item:",student.pop('city'))
print("Student",student)
