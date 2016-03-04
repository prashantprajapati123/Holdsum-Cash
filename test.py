import requests
username = 'test'
p1 = 'passwordprime'
p2 = p1
email = "bla@gmail.bla"
token= '84e2c8c006fe6c47132586e78e2331a9bf315075'
r = requests.get('https://holdsum.herokuapp.com/auth/user/'
    ,headers={'Authorization': 'Token 84e2c8c006fe6c47132586e78e2331a9bf315075'})
print (r.text)