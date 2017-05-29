## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pip install virtualenv

$ virtualenv venv

$ source venv/bin/activate

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku open
```


## Documentation

#### Register/Login by Facebook
    - POST /auth/facebook/
        input:
            {
                "access_token": "[facebook access_token]"
            }
        output:
            {
                "key": "[backend token]"
            }
#### Register by email/password/username
    - POST /auth/registration/
        input:
            {
                "username": "[required]"
                "password1": "[required, must match password2]",
                "password2": "[required, must match password1]",
                "email": "[required]"
            }
        output:
            {
                "key": "[backend token]"
            }
#### Login with username/password
    - POST /auth/login/
        input:
            {
                "username": "[required]",
                "email": "[required]",
                "password": "[required]"
            }
        output:
            {
                "key": "[backend token]"
            }
#### Get/Patch User Info
    - GET /auth/user/
        header:
            {
                "Authorization": "Token [backend token]"
            }
        output:
            {
                "username": ,
                "email": ,
                "first_name": ,
                "last_name": 
            }
    - PUT/PATCH /auth/user/
        header:
            {
                "Authorization": "Token [backend token]"
            }
        input:
            {
                "username": ,
                "email": ,
                "first_name": ,
                "last_name": 
            }
        output:
            {
                "username": ,
                "email": ,
                "first_name": ,
                "last_name": 
            }
#### Change Password
    - POST /auth/password/change/
        header:
            {
                "Authorization": "Token [backend token]"
            }
        input:
            {
                "old_password": ,
                "new_password1": ,
                "new_password2": 
            }
#### Logout
    - POST /auth/logout/
        header:
            {
                "Authorization": "Token [backend token]"
            }

        
