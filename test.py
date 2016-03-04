import requests
access_token = 'CAAXzctM9yiEBAJmOztKaToBr54FqaZA6OnhUjv5cuRg5sphoB9hJVEdFjPPO6NeuLMZBLZCQ7JM5ZBylJy0CWy4YBfwjlcPfjKhGyqWLYEyZBR2CTQ1S0AvesS13BwadvZATMC78z6ykzJMX96ICnbiLc5z3jUbKjsfbaBSDvN2WgrbboVCz7ZB39aWNkKCZCj0MmU62xCI2ZBgZDZD'
r = requests.post('https://holdsum.herokuapp.com/auth/facebook/', json = {'access_token':access_token})
print (r.text)