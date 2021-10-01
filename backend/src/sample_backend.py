from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from random import randint
import random
import string


app = Flask(__name__)
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
         for user in users['users_list']:
            if (user['name'] == search_username) and (user['job'] == search_job):
               subdict['users_list'].append(user)
         return subdict
      elif search_username :
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
      
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd["id"] = ''.join(random.choice(string.ascii_lowercase) for i in range(3))+str(randint(100, 999)) # create random id
      users['users_list'].append(userToAdd)
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
