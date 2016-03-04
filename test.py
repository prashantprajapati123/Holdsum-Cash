import requests
username = 'test'
p1 = 'passwordprime'
p2 = p1
email = "bla@gmail.bla"
r = requests.post('https://holdsum.herokuapp.com/auth/registration/'
    , json = {'username':username, 'password1': p1, 
    'password2': p2, 'email':email
    })
print (r.text)