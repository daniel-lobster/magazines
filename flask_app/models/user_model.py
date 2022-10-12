from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
# from flask_app.models.magazine_model import Magazine
from flask_app.models import magazine_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'magazines_schema2'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_magazines = []
    
    def __repr__(self):
        return f'<User: {self.email}>'

    # this static method validates the user's form input
    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['first_name']) < 3:
            flash('First name must be at least two characters.', 'first_name')
            is_valid = False
        if len(form['last_name']) < 3:
            flash('Last name must be at least two characters.', 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']): 
            flash('Invalid email address!', 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters.', 'password')
            is_valid = False
        if form['password']!=form['c_password']:
            flash('Confirmation password must match password.', 'password')
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        print(f'Created: <User {user_id}>')
        return user_id

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id_with_created_magazines(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        user = User(result[0])
        query = 'SELECT * from users left join magazines on users.id = magazines.creator_id WHERE users.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        for result in results:
            magazine_data={
                'id' : result['magazines.id'],
                'title' : result['title'],
                'description' : result['description'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                # FOREIGN KEY
                'creator_id' : result['creator_id'],
                'creator_first_name' : result['first_name'],
                'creator_last_name' : result['last_name']
            }
            print(magazine_data)
            user.created_magazines.append(magazine_model.Magazine(magazine_data))
        return user


    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True
