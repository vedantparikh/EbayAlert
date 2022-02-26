## eBay Alert System

### Commands

#### Running application via docker
Add relevant environment variables into `.env.docker`, `.env` and in `settings.py` file. 
Run the `docker-compose build` to build the docker image. 
Run the `docker-compose up` to run the docker image of the application.

#### Running locally without using docker. 
Run `sh setup_python_venv.sh` to set up the python virtualenv.
Run `source .venv/bin/activate` to activate the virtualenv.
Change Directory to `src/python/shore`. Run `python -m manage runserver`
Run `python -m manage migrate`
Run `python -m manage createsuperuser` After that enter your email and password.
Run `docker run --name my-redis -p 6379:6379 -d redis`
Run celery commands `celery -A shore.celery worker -l info` and `celery -A shore.celery beat -l info`

You should see that server will be running at `http://127.0.0.1:8000/`
You can Login with your credentials at `http://127.0.0.1:8000/admin/`

### API Specs

All the API Specs are documented using `drf-yasg` module and are served at: `http://127.0.0.1:8000/swagger/`


############################################################################################################
###                                                                                                      ###
###  I could not use the eBay developer API as I am having an authentication issue, also tried with the  ###
###  creating a new account with different email, however, could not pass eBay authentication on time.   ###
###  Here, I have used a different API which was available. The description about this API is as follows.###
###                                                                                                      ### 
############################################################################################################

Json response looks as below. 
```json
{
    "id": "4f5db194-3671-4b98-b494-93458f6512b1", 
    "name": "0-6", 
    "height": 6,
    "district": "LEHEL",
    "coordinates": [48.97047481858539, 11.17023357573369]
}
```
In our case I am considering the height as the product price, name as the product name and id as the product id.

This endpoint is having the limited search phrases which are mentioned below:
- AU
- GIESING
- LAIM
- LEHEL
- LUDWIGVORSTADT
- MAXVORSTADT
- NEUHAUSEN
- SCHWABING
- SENDLING

Please use these as the search phrases in the alert application.

All other logic remains the same in our application only handling different data.


## Architecture Decisions:

The application has Three Database Tables:

- User
- Subscription
- Product

### User Model:

Utilizes Django's User model.

- Id: UUID Primary Key.
- Email: Email Field. Has only email as a required field and has unique constraints to it.

### Subscription Model:

- Id: UUID Primary Key.
- Search Phrase: VarChar Field. Stores a search phrase (varchar). Search phrase information is used to query the eBay client and fetch
  the relevant information.
- Frequency: Integer Field. Stores frequency of the mails (integer). It is a choice field which is having options of 2, 15, 30.
  These are the interval times (minutes) for an email subscription.
- Is Reverse: Boolean Field. Stores boolean value if results obtained from the client should be displayed in reverse order or it should be in
  ascending order.
- User: A Foreign Key to the User model. This can be used to fetch relevant user information (i.e. email). Multiple subscriptions are possible for the single user.
- Created At: Datetime field. Stores creation timestamp of the instance.
- Updated At. Datetime field. Stores latest timestamp of an update operation.

### Product Model:

- Id: UUID Primary Key.
- Product Id: VarChar Field. Stores the unique Id obtained from the eBay client with the search phrase.
- Name: VarChar Field. Stores the name of the product.
- Price: Decimal Field. Stores the price of the product with two digits precision in decimal places.
- Subscription: Foreign Key Field: Stores for which subscription these products are stored.

## Insights of the implementation, use cases covered, and flexibility for future changes.

* The Subscription database Model is the core of the application. Through the subscription model, we can fetch users and
the products which are linked to them. One User can have multiple subscriptions. Each subscription instance contains the search
phrase in it. Also, Unique constraints are added which means that for the given user there should be a unique search phrase
that exists in the subscription database model.

* When the new subscription instance is created at the same time, the subscription emails (Periodic Tasks in Celery
context) are set. Periodic tasks are of two kinds; one gives the search phrase result of the product containing the name
and price of the products. The second one gives an update about the price decrease, no price change or new products which are
available within an interval of two days. Whenever the new subscription instance is created at the same time we are
fetching products from the eBay client and storing product prices and names in our database which is later being used as
a reference when we want to check whether the price has decreased or remained the same or if new products are available.
These processes are performed when the Periodic task for the second kind is triggered. At the same time, we are fetching
the products using search phrases and comparing their names and prices in our already existing database of products for
the given subscription and mailing users with the relevant information.

* When the update operation happens for the subscription instance at the same time, we are removing the relevant Periodic
task available and creating a new Periodic task with the new information of the subscription. If the update operation
contains changes in the search phrase then we are unlinking the products associated with the subscription and creating new
products and linking them with the given subscription instance.

* When the user is deleted, then all the relevant Periodic Task is also being deleted.

* Celery is being used as part of the scheduling of the alerts. Celery has a PeriodicTask table that stores the name of
the task (with unique constraint), interval schedule, start time and relevant information. As we also support Create, Update
and Delete operations we also need to create, update or delete our PeriodicTask instances. Hence, custom logic is required to
identify and filter the relevant PeriodicTask whenever the subscription is changed or deleted. The name field of the
PeriodicTask is created with the combination of Subscription Id, User Id and the type of email. This way we can filter
the periodic task whenever update and delete operation is performed in subscription and delete the relevant periodic task attached to the subscription. 
And at the same time create a new periodic task if the operation is Update. As we can filter all the periodic tasks based on User Id. 
This naming convention gives us the ability to delete all the subscriptions when the user is deleted. 
Also, if we are not going to continue one of the email services we can filter the periodic task on the basis of the
email service name and disable or delete the periodic tasks.

### Extra Features:

- All the endpoints have an optional trailing slash
- Product and Subscription database model has soft delete implemented.