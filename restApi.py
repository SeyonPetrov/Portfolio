from flask_restful import reqparse, abort, Resource
from flask import Flask, jsonify, url_for
from data import db_session
from data.users import User
import requests
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
db_session.global_init('db/owners12.db')


par = reqparse.RequestParser()
par.add_argument('phone_num', required=True)
par.add_argument('name', required=True)
par.add_argument('age', required=True, type=int)
par.add_argument('place_job_study', required=True)
par.add_argument('sex', required=True)
par.add_argument('address', required=True)
par.add_argument('email', required=True)
par.add_argument('hashed_password', required=True)


def generator():
    length = '10'
    api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
    response = requests.get(api_url, headers={'X-Api-Key': 'fg4oSPFJZ1Xy+8uIlK3Csg==ViW2Xa7h9Q1MzVgN'})
    if response:
        return response.json()['random_password']
    return None


def abort_if_not_found(user_id):
    sess = db_session.create_session()
    user = sess.query(User).filter(User.unic_code == str(user_id))
    if not user:
        abort(404, message=f'User {user_id} not found')


class UsersResource(Resource):
    def get(self, user_code):
        abort_if_not_found(user_code)
        user = db_session.create_session().query(User).filter(User.unic_code == str(user_code))
        return jsonify({'user': user.to_dict(only=('name', 'age', 'sex', 'place_job_study'))})

    def delete(self, user_id):
        abort_if_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).filter(User.unic_code == str(user_id))
        sess.delete(user)
        sess.commit()
        return jsonify({'ALL': 'GOOD'})


class UsersListRes(Resource):
    def get(self):
        users = db_session.create_session().query(User).all()
        return jsonify({'all_users': [
            x.to_dict(only=('name', 'age', 'sex', 'place_job_study')) for x in users
        ]})

    def post(self):
        args = par.parse_args()
        sess = db_session.create_session()

        user = User(
            email=args['email'],
            name=args['name'],
            place_job_study=args['place_job_study'],
            address=args['address'],
            age=args['age'],
            phone_num=args['phone_num'],
            sex=args['sex'],
            avatar=str(url_for('static', filename=f'images/2021056-0.jpeg')),
            unic_code=str(generator())
        )
        user.set_password(args['hashed_password'])
        sess.add(user)
        sess.commit()
        return jsonify({'ALL': 'GOOD'})