from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from random import randint
import json
import random
import string


app = Flask(__name__)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

#client = pymongo.MongoClient("mongodb+srv://dkim:Picard2738@cluster0.t8smq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#db = client.users
#users_list = db.users_list

#connect and create a db named as mydb
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/users"
#initializing the client for mongodb
mongo_cli = PyMongo(app)
#creating the customer collection
db = mongo_cli.db

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      subdict = {'users_list' : []}
      if search_username and search_job:
         find_by_user_and_job(search_username, search_job)
      elif search_username :
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      else: 
         #cursor = db.users_list.find({})
         #list_cur = list(cursor)
         #json_data = dumps(list_cur)
         #subdict['users_list'] = json_data
         return users
      
   elif request.method == 'POST':
      userToAdd = request.get_json()
      users['users_list'].append(userToAdd)
      result = db.users_list.insert_one({"name":userToAdd.get("name"), "job":userToAdd.get("job")}) # insert user into database
      userToAdd["id"] = str(result.inserted_id) # give id to fetched value
      resp = jsonify(userToAdd)
      resp.status_code = 201 #200 is the default code for a normal response
      return resp

   elif request.method == 'DELETE':
      userToDelete = request.get_json()
      for user in users['users_list']:
         if user['id'] == userToDelete["id"]:
            users['users_list'].remove(userToDelete)
      resp = jsonify(success=True)
      resp.status_code = 204
      return resp

@app.route('/users/<id>')
def get_user(id):
   if id :
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users

   