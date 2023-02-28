### CC Assignment 1 Part 2 ### 

# base_url: http://localhost:5000/

# Standard library imports
import datetime
import requests
import time

# Third party imports
from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
import hashlib
import pandas as pd
import func

# Marvel API variables
pub_api_key = "083374c8f8fd31f9528c00e4fe42a485"
priv_api_key = "ea6ee0d1facc073193349ace751e1d5da7c2bb8d"
ts = str(time.time())

hash_val = (ts + priv_api_key + pub_api_key).encode()
md5_hash = hashlib.md5(hash_val).hexdigest()

# Fixer Exchange Rate API variablesimport requests
fixer_key = "Dn2W8TWFJAQ22OP3aXUit4zeUJbzHR6f"

# API building blocks/objects
app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "Shrek-is-love, Shrek4life!"



# Main API Functionality
class Base(Resource):

    def get(self):

        return {"status": 200, 
                "response": ("Welcome to the 'A3 API'! Possible "
                + "endpoints are: '/characters', '/signup', '/login' "
                + "and '/tokenuptime'")}, 200

class Characters(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("character_id", type = str, 
                            help = "Missing argument 'character_id'", 
                            required = True, location = "args")
        parser.add_argument("character_name", type = str, 
                            help = "Missing argument 'character_name'", 
                            required = False, location = "args")
        args = parser.parse_args()
        df = pd.read_csv('data.csv', dtype = {"Character Name": "string", 
                                              "Character ID": "string"})
       
    

    
    
    
        Function(a = ['1011334'],c = ['1011334','1017100','1009144','1010699','1009146','1016823','1009148'], d = ['Hello','jdhfjsj'])
        
        

    @jwt_required()
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type = str, 
                            help = "Access token is required", required = True, 
                            location = "headers")
        parser.add_argument("character_id", type = str, 
                            help = "Missing argument 'character_id'", 
                            required = True, location = "args")
        parser.add_argument("character_name", type = str, 
                            help = "Missing argument 'character_name'", 
                            required = False, location = "args")
        parser.add_argument("available_events", type = int, 
                            help = "Missing argument 'available_events'", 
                            required = False, location = "args")
        parser.add_argument("available_series", type = int, 
                            help = "Missing argument 'available_series'", 
                            required = False, location = "args")
        parser.add_argument("available_comics", type = int, 
                            help = "Missing argument 'available_comics'", 
                            required = False, location = "args")
        parser.add_argument("price_of_comic", type = float, 
                            help = "Missing argument 'price_of_comic'", 
                            required = False, location = "args")
        args = parser.parse_args()

        df = pd.read_csv('data.csv', dtype = {"Character Name": "string", 
                                              "Character ID": "string"})

        if args["character_id"] in list(df["Character ID"]):
            return {"status": 409, "response": (f"'{args['character_id']}' ",
                                                f"already exists.")}, 409

        elif all(args[x] is None for x in ("character_name", "available_events", 
                                           "available_series", "available_comics", 
                                           "price_of_comic")):
            url = "http://gateway.marvel.com/v1/public/characters/" + args["character_id"]
            params = {
                "apikey": pub_api_key,
                "ts": ts,
                "hash": md5_hash,
            }
            response = requests.get(url = url, params = params)

            if response.status_code == 404:
                return {"status": 404, "response": (f"character_id '{args['character_id']}' "
                                                    + f"is not a valid Marvel Character ID "
                                                    + f"(could not be found)")}, 404
            else:
                response = response.json()
                response = dict(response)["data"]["results"]

                comics = "http://gateway.marvel.com/v1/public/characters/" \
                         + args["character_id"] + "/comics"
                comics = requests.get(url = comics, params = params).json()
                comics = dict(comics)["data"]["results"]

                if response[0]["comics"]["available"] == 0:
                    max_price = 0.0          
                else:
                    url_price = "http://gateway.marvel.com/v1/public/characters/" \
                                + args["character_id"] + "/comics"
                    offset = 0
                    num_comics = response[0]["comics"]["available"]
                    
                    price_info = []
                    prices = []

                    while num_comics > 0:
                        params_price = {'apikey': pub_api_key, 'ts': ts, 
                                        'hash': md5_hash, 'limit': 100, 
                                        'offset': offset}
                        response_price = requests.get(url = url_price, 
                                         params = params_price).json()
                        price_data = response_price['data']['results']

                        for n in price_data:
                            price_info.append(n['prices'])                        
                            for x in price_info:
                                for y in x:
                                    prices.append(y['price'])
                                        
                        offset = offset + 100
                        num_comics = num_comics - 100
                    
                    max_price = max(prices)

                entry = pd.DataFrame({
                    "Character ID": [args["character_id"]],
                    "Character Name": response[0]["name"],
                    "Total Available Events": response[0]["events"]["available"],
                    "Total Available Series": response[0]["series"]["available"],
                    "Total Available Comics": response[0]["comics"]["available"],
                    "Price of the Most Expensive Comic": max_price})

                df = df.append(entry, ignore_index = True)
                df.to_csv("data.csv", index = False)
                df = df.to_dict(orient = "records")
                return {"status": 200, "response": df}, 200

        else:
            entry = pd.DataFrame({
                "Character ID": [args["character_id"]],
                "Character Name": [args["character_name"]],
                "Total Available Events": [args["available_events"]],
                "Total Available Series": [args["available_series"]],
                "Total Available Comics": [args["available_comics"]],
                "Price of the Most Expensive Comic": [args["price_of_comic"]]})

            df = df.append(entry, ignore_index = True)
            df.to_csv("data.csv", index = False)
            entry = df.loc[df["Character ID"] == args["character_id"]]
            entry = entry.to_dict(orient = "records")
            return {"status": 200, "response": entry}, 200

    @jwt_required()
    def put(self):

        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type = str, 
                            help = "Access token is required", required = True, 
                            location = "headers")
        parser.add_argument("character_id", type = str, action = "append", 
                            help = "Missing argument 'character_id'", 
                            required = False, location = "args")
        parser.add_argument("character_name", type = str, action = "append", 
                            help = "Missing argument 'character_name'", 
                            required = False, location = "args")
        parser.add_argument("new_price", type = str, action = "append", 
                            help = "Missing argument 'new_price'", 
                            required = True, location = "args")
        parser.add_argument("currency", type = str, action = "append", 
                            help = "Missing argument 'currency'", 
                            required = True, location = "args")
        args = parser.parse_args()

        df = pd.read_csv("data.csv", dtype = {"Character Name": "string", 
                                              "Character ID": "string"})

        if (args["character_id"] is not None) and (args["character_name"] is not None):
            return {"status": 400, "response": ("Please enter 1 unique identifier only. "
                                                + "Either 'character_id' or 'character_name'")}, 400
        
        elif (args["character_id"] is None) and (args["character_name"] is None):
            return {"status": 400, "response": ("Please enter at least 1 unique identifier. "
                                                + "Either 'character_id' or 'character_name'")}, 400

        elif args["character_id"] is not None:
            i = 0
            if all(item in list(df["Character ID"]) for item in args["character_id"]):

                while i < len(args["character_id"]):
                    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={args['currency'][i]}&base=USD"
                    payload = {}
                    headers = {"apikey": fixer_key}
                    response = requests.get(url, headers = headers, data = payload)
                    if response.status_code == 404:
                        return {"status": 404, "response": (f"Check that your currency "
                                                            + f"has the format 'XXX' and exists")}, 404
                    else:
                        response = response.json()
                        price_in_usd = float(args["new_price"][i]) / response["rates"][args["currency"][i]]
                        df.loc[(df["Character ID"] == args["character_id"][i]),"Price of the Most Expensive Comic"] = price_in_usd
                         
                        i += 1

                df.to_csv("data.csv", index = False)   
                df = df.to_dict(orient = "records")
                return {"status": 200, "response": df}, 200

            else:
                return {"status": 404, "response": (f"One or multiple given "
                                                    + f"Character names dont exist")}, 404

        elif args["character_name"] is not None:
            i = 0
            if all(item in list(df["Character Name"]) for item in args["character_name"]):

                while i < len(args["character_name"]):
                    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={args['currency'][i]}&base=USD"
                    payload = {}
                    headers = {"apikey": fixer_key}
                    response = requests.get(url, headers = headers, data = payload)
                    if response.status_code == 404:
                        return {"status": 404, "response": (f"Check that your currency "
                                                            + f"has the format 'XXX' and exists")}, 404
                    else:
                        response = response.json()
                        price_in_usd = float(args["new_price"][i]) / response["rates"][args["currency"][i]]
                        df.loc[(df["Character Name"] == args["character_name"][i]),"Price of the Most Expensive Comic"] = price_in_usd
                         
                        i += 1

                df.to_csv("data.csv", index = False)   
                df = df.to_dict(orient = "records")
                return {"status": 200, "response": df}, 200

            else:
                return {"status": 404, "response": (f"One or multiple given "
                                                    + f"Character names dont exist")}, 404

    @jwt_required()
    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type = str, help = "Access token is required", 
                            required = True, location = "headers")
        parser.add_argument("character_id", type = str, action = "append", 
                            help = "Missing argument 'character_id'", 
                            required = False, location = "args")
        parser.add_argument("character_name", type = str, action = "append", 
                            help = "Missing argument 'character_name'", 
                            required = False, location = "args")
        args = parser.parse_args()

        df = pd.read_csv("data.csv", dtype = {"Character Name": "string", 
                                              "Character ID": "string"})

        if (args["character_id"] is not None) and (args["character_name"] is not None):
            return {"status": 400, "response": ("Please enter 1 unique identifier only. "
                                                + "Either 'character_id' or 'character_name'")}, 400

        elif (args["character_id"] is None) and (args["character_name"] is None):
            return {"status": 400, "response": ("Please enter at least 1 unique identifier. "
                                                + "Either 'character_id' or 'character_name'")}, 400
        
        elif args["character_id"] is not None:
            if all(item in list(df["Character ID"]) for item in args["character_id"]):
                df = df.loc[-df["Character ID"].isin(args["character_id"])]
                df.to_csv("data.csv", index = False)
                df = df.to_dict(orient = "records")
                return {"status": 200, "response": df}, 200
            else:
                return {"status": 404, "response": (f"One or multiple given Character "
                                                    + f"ID(s) dont exist")}, 404
                    

        elif args["character_name"] is not None:
            if all(item in list(df["Character Name"]) for item in args["character_name"]):
                df = df.loc[-df["Character Name"].isin(args["character_name"])]
                df.to_csv("data.csv", index = False)
                df = df.to_dict(orient = "records")
                return {"status": 200, "response": df}, 200
            else:
                return {"status": 404, "response": (f"One or multiple given Character "
                                                    + f"names dont exist")}, 404

# Authentification scheme and login
user_data = pd.DataFrame(columns = ["email", "password"])
user_data.to_csv('users.csv', index = False)

def hash_password(password):

        return generate_password_hash(password).decode('utf8')

class SignUp(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("email", type = str, help = "Missing argument 'email'", 
                            required = True, location = "args")
        parser.add_argument("password", type = str, help = "Missing argument 'password'", 
                            required = True, location = "args")
        args = parser.parse_args()

        df = pd.read_csv('users.csv')

        if args["email"] in list(df["email"]):
            return {"status": 409, "response": f"{args['email']} already exists."}, 409
        else:
            entry = pd.DataFrame({
                "email": [args["email"]],
                "password": [hash_password(args["password"])]
            })
            df = df.append(entry, ignore_index = True)
            df.to_csv("users.csv", index = False)
            return {"status": 200, "response": "Successfully signed up"}, 200

class LogIn(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("email", type = str, help = "Missing argument email", 
                            required = True, location = "args")
        parser.add_argument("password", type = str, help = "Missing argument password", 
                            required = True, location = "args")
        args = parser.parse_args()

        df = pd.read_csv('users.csv')
        
        if args["email"] not in list(df["email"]):
            return {"status": 401, "response": "Invalid email"}, 401
        else: 
            password = df.loc[df["email"] == args["email"], "password"][0]
            if check_password_hash(password, args["password"]):
                expires = datetime.timedelta(hours = 1)
                access_token = create_access_token(identity = str(df.loc[df["email"] == args["email"]].index[0]), 
                                                   expires_delta = expires)
                return {"status": 200, "response": "Successfully logged in", 
                        "token": access_token}, 200
            else:
                return {"status": 401, "response": "Invalid password."}, 401

class TokenUptime(Resource):

    @jwt_required()
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("Authorization", type = str, help = "Access token is required", 
                            required = True, location = "headers")
        parser.parse_args()

        init = get_jwt()["iat"]
        expiry = get_jwt()["exp"]
        user_time = (expiry - init) / 60
        remaining = round((expiry - time.time()) / 60)

        return {"status": 200, "response": (f"Your token is valid for {user_time} "
                                            + f"minutes after login. Remaining uptime: "
                                            + f"{remaining} minutes")}, 200

api.add_resource(Base, "/")
api.add_resource(Characters, "/characters", endpoint = "characters")
api.add_resource(SignUp, "/signup", endpoint = "signup")
api.add_resource(LogIn, "/login", endpoint = "login")
api.add_resource(TokenUptime, "/tokenuptime", endpoint = "tokenuptime")

if __name__ == "__main__":
    app.run(debug=True)