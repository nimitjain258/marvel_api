# marvel_api
Access marvel API to store data then create a new API to retrieve this data from our computer.

## Creating our own API

This A3 REST API allows to interact with the data.csv dataset, retrieving data from it, creating new entries or deleting existing data. For these last two actions though you will need an Authentification.

# 1. How to access this API?
Fot the A3 API to work you will need to execute the code on the API_creation_code.py .py file.

You can do this either by openning a new terminal window and launching the script by running API_creation_code.py. (CHANGE NAME), or by creating a jupyter notebook and copy pasting the code on the .py file to run it.

To be able to run such code, you will need to have previously installed Python's flask, flask_restful, flask_jwt_extended, flask_bcrypt and beautifulsoup4 libraries. You can do so by uncommenting the following cells.

After you execute the code, the A3 API should be running on your local port 5000, so if you head over to http://127.0.0.1:5000/ or http://localhost:5000/, you should see the message "Welcome to the 'A3 API'! Possible endpoints are: '/characters', '/signup', '/login' and '/tokenuptime'".

From that point on, for every request that you want to make to the API, you should use the base URL: http://127.0.0.1:5000/ (or what is the same http://localhost:5000/).

# 2. Dataset
The dataset with wich the A3 API interacts includes the fields below:

Character Name refers to each Marvel Character's name in str form
Character ID refers to each Character's unique identifier, in str form
Total Available Events refers to the total amount of events each character is part of, in int form
Total Available Series refers to the total number of series each character is part of, in int form
Total Available Comics refers to the total number of events each character is part of, in int form
Price of the Most Expensive Comic refers to the price of the most expensive comic that each character is on, in float form and USD value

# 3. Authentification
To access the A3 API and simply retrieve data from it, you don't need any form of authentification.

However, if you want to create new entries into the dataset or delete/change existing ones you will need to sign up and log in. The authentification schema that this API uses is an OAuth system, by which everytime that you log in, you will recieve an access token with a limited duration to work with.

Sign Up
The first time that you wish to log in, you will need to create an account (sign up) with your email and a password of your choice.

This can be done by running the code following code on your Jupyter Notebook:

sign_up = requests.post(http://localhost:5000/signup , params = {"email": "your@email", "password": "yourPassword"})

Log In
To Log In, you will use your email and password that you signed up with, and as a result you will recieve an access token, which will be different every single time that you Log In.

This can be done by running the code following code on your Jupyter Notebook:

log_in = requests.get(http://localhost:5000/login , params = {"email": "your@email", "password": "yourPassword"})

The json result of this request will include the status and response as well as you access token. This can be accessed in similar fassion to the response by parsing 'token' as a dictionary key:

token = log_in["token"]

Your token is valid for 1 hour!. After that, a new sign-up is required.

# 4. Resources
You can access 4 resources using the API:

Characters: contains the information on several Marvel Characters and their IDs, number of comics, series and events they appear on, and the price of their most expensive comic.

Sign Up: allows you to create a user name and password, to be able to log in.

Log In: when logged in, you will recieve a token that will allow you to modify the data in the dataframe.

TokenUpTime: allows you to see your remaining uptime after log in through a token.

# 5. Making Requests
Types of requests available

Format of attributes within the requests

Examples of each request

The A3 API will most likely run on your local port 5000, so the basic url for your requests will be: http://localhost:5000/. Within this URL, you can access the 4 different resources through their different endpoints ('/characters', '/signup', '/login' and '/tokenuptime'), which will allow you to perform different requests.

The basic format of any request will be: request.[method](url = basicURL/endpoint, params = {}) where params corresponds to the different parameters that the request should take into account, in a dictionary format.

# 5.1 Sign Up Endpoint:
This endpoint is used to create a new account. The only action available here is a post request, wherby your chosen email and password information for the account will be stored in the API's database to recognize you when you log in.

This can be done by running the following code on your Jupyter Notebook:

requests.post("http://localhost:5000/signup" , params = {"email": "your@email", "password": "yourPassword"})

# 5.2 Log In Endpoint:
This endpoint is used to log in into your existing user, to be able to manipulate the Characters dataset. The only action available here is a get request, whereby your email and password are checked, and you get an access token as a result, with validity of 1 hour.

This can be done by running the following code on your Jupyter Notebook:

requests.get("http://localhost:5000/login" , params = {"email": "your@email", "password": "yourPassword"})

# 5.3 Token Up Time Endpoint:
This endpoint can be used to check the remaining uptime of your access token. The only action available here is a get request, whereby the validity of the access token that you provide is checked. You will get as a result the remaining valid time that the token has left, and once this time expires, you will be logged out of the API.

This can be done by running the following code on your Jupyter Notebook:

requests.get("http://localhost:5000/tokenuptime" , headers = {"Authorization": "Bearer" + "yourToken"})

# 5.4 Characters Endpoint:
Within the Characters Resource, you will be able to make:

Get request: to retrieve data of Characters from the Dataset
Post request: to add data of new Marvel Characters to the Dataset
Delete request: to eliminate data on existing Characters from the Dataset
Get Method:
This method allows you to retrieve information on one or multiple Marvel characters of your choice from the Dataset using either the character's id or name. However, using both identifiers simultaneously is prohibited.

This can be done by running the following code on your Jupyter Notebook:

requests.get("http://localhost:5000/characters" , params = {"character_name": ["Abyss", "3-D Man"]})

Post Method:
This method allows you to add one Marvel character of your choice to the Dataset. In order to do so, you must indicate the character id as parameter of the request. Other character attributes may also be included in the request's parameters, but are not necessary. On the other hand, you must indicate your access token as header in order to execute this request.

This can be done by running the following code on your Jupyter Notebook:

requests.post("http://localhost:5000/characters" , params = {"character_id": "1009151"}, headers ={"Authorization": "Bearer"+"yourToken"})

Put Method:
This method allows you to modify the price of one or multiple characters contained in the Dataset. In order to do so, you must indicate as parameters either the character(s) name(s) or id(s), as well as the desired new price(s) and currency(ies). In order to carry out this request, you are obligated to provide your access token as header as well .

This can be done by running the following code on your Jupyter Notebook:

requests.put("http://localhost:5000/characters" , params = {"character_id": ["1017851","1011031"], "new_price":["3.99", "9.99"], "currency":["USD","USD"]}, headers ={"Authorization": "Bearer"+"yourToken"})

Delete Method:
This method allows you to delete one or multiple entries from the Dataset. In order to do so, all that is required is that you indicate either the id(s) or the name(s) of the character(s) you wish to remove in the parameters of your request, in addition to your given access token as header. Please note that if you use both character id and character name identifiers simultaneously, fail to indicate any parameters, or fail to indicate a header containing your access token, your request will return an error.

This can be done by running the following code on your Jupyter Notebook:

requests.delete("http://localhost:5000/characters" , params = {"character_name": ["Agent Brand", "Adam Warlock"]}, headers = {"Authorization": "Bearer" + "yourToken"}})

# 6. Results
The A3 API uses conventional HTTP response codes to indicate the success or failure of an API request. In general, codes in the range 2xx indicate success, while codes in the 4xx range indicate an error that failed given the information provided (e.g., a required parameter was omitted, a charge failed, etc.).

The most common results you will get are:

200: indicates that your request was successful
400: indicates that you omitted a required parameter to perform the request or that you are giving two substitutory parameters at the same time
401: when trying to log in, indicates you are using the wrong email or password
404: indicates you are trying to interact with a Character that doesn't exist
409: indicates you are trying to add a resource (Character or email when signing up) that already exists
