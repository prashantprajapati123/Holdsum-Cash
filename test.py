import requests
username = "test"
p1 = "passwordprime"
p2 = p1
email = "bla@gmail.bla"
employment = dict({"address":"usernasdfalkjame",
                "city":"ny", 
                "state":"ny",
                "zipCode":"11234",
                "role":"CEO",
                "employer":"test",
                "monthly_income":"123554",
                "income_frequency":"123",
                "next_pay_date":"1990-12-2"
                })
data = dict({"address":"usernasdfalkjame","city":"ny", "state":"ny", "SSN":"11234556",
    "DOB": "1990-12-2", "zipCode":"11234", "employment":employment})
print data
# token= "c189e554d6141429bc5664236a38414949487181"
r = requests.post("http://127.0.0.1:8000/user/profile/",
    data = data,

   headers={"Authorization": "Token c189e554d6141429bc5664236a38414949487181"}
   )

print (r.text)