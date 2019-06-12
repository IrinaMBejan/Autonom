from autonomus.models import User, Token

import uuid
import hashlib
import jwt

from datetime import datetime, timedelta
from enum import Enum


config = {
    'jwt_secret': 'super-secret-key-please-change',
    'token_expiration_seconds': 3600,
    'token_refresh_seconds': 1000,
    'jwt_algorithm': 'HS256'
}

class Roles(Enum):
    USER = 0,
    ADMIN = 1,
    NEWBIE = 2


def add_user(username, password, email, phone_number):
    """Inserts new user to the database. Use for register purposes."""
    user = User(
            username=username, 
            password=hash_password(password), 
            email=email, 
            type="user",
            tags=[],
            events=[])

    if phone_number:
        user.phone_numer = phone_number

    user.put()


def exists_user(email, password):
    """Verify if the user exists in the datastore"""
    query = User.query()
    query.add_filter('email', '=', email)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            return None
        elif check_password(ent.password, password):  
            return ent
    return None

def get_user(username):
    """Verify if the user exists in the datastore"""
    query = User.query()
    query.add_filter('username', '=', username)
    query_it = query.fetch()
    for ent in query_it:
        if ent is None:
            return None
        else:
            return ent

    return None


def get_users():
    return User.all()


def get_user_events(urlsafe):
    user = User.get(urlsafe)
    return user.events


def add_tag_to_user(user_urlsafe, key):
    user = User.get(user_urlsafe)
    if key not in user.tags:
        user.tags.append(key)
    user.put()


def remove_tag_from_user(user_urlsafe, key):
    user = User.get(user_urlsafe)
    if key in user.tags:
        user.tags.remove(key)
    user.put()


def add_event_to_user(user_urlsafe, key):
    user = User.get(user_urlsafe)
    if key not in user.events:
        user.events.append(key)
    user.put()


def remove_event_from_user(user_urlsafe, key):
    user = User.get(user_urlsafe)
    if key in user.events:
        user.events.remove(key)
    user.put()


def hash_password(password):
    """Encode password"""
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    """Check if password stored matches the given one"""
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def generate_token(user):
    """Generates token encoding user urlsafe and time"""

    payload = {
        'user_url': user.urlsafe,
        'exp': datetime.utcnow() + timedelta(seconds=config['token_expiration_seconds'])
    }
    return jwt.encode(payload, config['jwt_secret'], config['jwt_algorithm'])


def exists_token(token):
    """Checks whether the token exists in the database."""

    query = Token.query()
    query.add_filter('token', '=', token)
    query_list = list(query.fetch())

    if query_list:
        for token_entity in query_list:
            if token_entity:
                return True
    return False


def verify_token(authorization):
    """Checks if given token is valid"""
    try:
        token = authorization.split(' ')[1]
        decoding = jwt.decode(token, config['jwt_secret'], config['jwt_algorithm'])
        if not exists_token(token):
            return None

        return decoding['user_url']

    except jwt.InvalidTokenError:
        return None


def get_user_role(urlsafe):
    user = User.get(urlsafe)
    
    if user.type == "user":
        return Roles.USER

    if user.type == "admin":
        return Roles.ADMIN

    return Roles.NEWBIE
 

def get_user_tags(urlsafe):
    user = User.get(urlsafe)
    return user.tags


def update_token(jwt_token, user):
    """ Updates existing token for user or creates new one """

    query = Token.query()
    query.add_filter('user', '=', user.key)
    query_list = list(query.fetch())

    if query_list:
        for token_entity in query_list:
            token_entity.token = jwt_token.decode("utf-8")
            token_entity.put()
    else:
        token = Token(token=jwt_token.decode("utf-8"), user=user.key)
        token.put()


def remove_token(urlsafe):
    user = User.get(urlsafe)
 
    query = Token.query()
    query.add_filter('user', '=', user.key)
    query_list = list(query.fetch())

    if query_list:
        for token_entity in query_list:
            token_entity.remove()


def is_token_expired(token):
    """Checks if given token is valid"""
    try:
        decoding = jwt.decode(token, config['jwt_secret'], config['jwt_algorithm'])
        return False
    except jwt.ExpiredSignatureError:
        return True
