# Test of signals to create "profile" on different types of user

Different use cases of ways of how to create profiles with signals.

## App: user_profile

"Normal" user_profile way of creating an extension of a user.
We want to add extra data to user and we do it as a_profile.
We do not care about different types of user.

The model will have a O2O relation with the user.

We will put the signal in models.py

## App: user_profile_2

Same as user_profile, but we will split the code in signals.py
and touch __init__ and apps.py

Following : https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html

## App: entities

We will have different types of users. And depending on which type
of user we are creating, we will create one or other class 
asociated object to the User class.

## App: entities_2

The same, but we only put signals in models.py
Not in the __init__.py or app.py

Following : https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html

## Results

### user_profile

    In [1]: User.objects.all()
    Out[1]: <QuerySet []>
    
    In [2]: Profile.objects.all()
    Out[2]: <QuerySet []>
    
    In [3]: Profile2.objects.all()
    Out[3]: <QuerySet []>
    
    In [4]: User.objects.create_user(email="u01@gmail.com",password="x", user_type=1)
    Out[4]: <User: u01@gmail.com>
    
    In [5]: User.objects.all()
    Out[5]: <QuerySet [<User: u01@gmail.com>]>
    
    In [6]: Profile.objects.all()
    Out[6]: <QuerySet [<Profile: Profile object (5)>]>
    
    In [7]: Profile2.objects.all()
    Out[7]: <QuerySet []>
    
-- LOG OUTPUT --

    10-23 20:58 signals.apps.authentication.models INFO     [authentication create_user]
    10-23 20:58 signals.apps.authentication.models INFO     [authentication _create_user]
    10-23 20:58 signals.apps.user_profile.models INFO     [user_profile receiver]
    10-23 20:58 signals.apps.user_profile.models INFO     [user_profile receiver if]
    10-23 20:58 signals.apps.user_profile.models INFO     [user_profile receiver save]
    
## user_profile_2

-- settings config -> INSTALLED APPS --

    #   'user_profile_2', # NOT WORKING
    #    'signals.apps.user_profile_2.apps.UserProfile2Config', # WORKING OK
    'user_profile_2.apps.UserProfile2Config', # WORKING OK

-- python manage.py shell -- 

    In [2]: User.objects.create_user(email="u01@gmail.com",password="x", user_type=1) 
    Out[2]: <User: u01@gmail.com>
    
    In [3]: Profile2.objects.all()
    Out[3]: <QuerySet [<Profile2: Profile2 object (1)>]>

## entities

-- settings config -> INSTALLED APPS --

    'signals.apps.entities',

-- python manage.py shell -- 

    In [1]: User.objects.create_user(email="u01@gmail.com",password="x", user_type=1)
    Out[1]: <User: u01@gmail.com>
    
    In [2]: User.objects.all()
    Out[2]: <QuerySet [<User: u01@gmail.com>]>
    
    In [3]: Person.objects.all()
    Out[3]: <QuerySet [<Person: >]>
    
    In [4]: Company.objects.all()
    Out[4]: <PersistentModelQuerySet []>
    
    In [5]: Company.objects.all().count()
    Out[5]: 0
    
    In [6]: Person.objects.all().count()
    Out[6]: 1

## entities_2

-- settings config -> INSTALLED APPS --

    'signals.apps.entities_2.apps.Entities2Config',

-- python manage.py shell -- 

    In [1]: User.objects.all().count()
    Out[1]: 0
    
    In [2]: Person2.objects.all().count()
    Out[2]: 0
    
    In [3]: User.objects.create_user(email="u01@gmail.com",password="x", user_type=1)
    Out[3]: <User: u01@gmail.com>
    
    In [4]: User.objects.all().count()
    Out[4]: 1
    
    In [5]: Person2.objects.all().count()
    Out[5]: 1
    
    In [6]: p = Person2.objects.first()  
    Out [6]: <Person2: u01@gmail.com> 
