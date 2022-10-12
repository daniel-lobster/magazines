from flask_app import flash, session
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model

DATABASE = 'magazines_schema2'


class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # FOREIGN KEY
        self.creator_id = data['creator_id']
        self.creator_first_name = data['creator_first_name']
        self.creator_last_name = data['creator_last_name']
        self.subscribers = []
    
    def __repr__(self):
        return f'<Magazine: {self.title}>'

    # create a magazine
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO magazines (title,description,creator_id) VALUES (%(title)s, %(description)s, %(creator_id)s);'
        magazine_id = connectToMySQL(DATABASE).query_db(query, data)
        return magazine_id

    # find all magazines (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from magazines join users on magazines.creator_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        #pprint(results)
        magazines = []
        for result in results:
            magazine_data={
                'id' : result['id'],
                'title' : result['title'],
                'description' : result['description'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                # FOREIGN KEY
                'creator_id' : result['creator_id'],
                'creator_first_name' : result['first_name'],
                'creator_last_name' : result['last_name']
            }
            magazines.append(Magazine(magazine_data))
        return magazines

    # find one magazine by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from magazines WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        magazine = Magazine(results[0])
        return magazine

    # find one magazine by id with subscribers
    @classmethod
    def find_by_id_with_subscribers(cls, data):
        query = 'SELECT * from magazines join users on magazines.creator_id = users.id WHERE magazines.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        result=results[0]
        magazine_data={
                'id' : result['id'],
                'title' : result['title'],
                'description' : result['description'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                # FOREIGN KEY
                'creator_id' : result['creator_id'],
                'creator_first_name' : result['first_name'],
                'creator_last_name' : result['last_name']
            }
        magazine = Magazine(magazine_data)
        query = 'SELECT * from magazines left join subscriptions on magazines.id = subscriptions.magazine_id join users on subscriptions.subscriber_id = users.id WHERE magazines.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        for result in results:
            magazine.subscribers.append(user_model.User(result))
        return magazine

    # update one magazine by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE magazines SET title = %(title)s, description = %(description)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one magazine by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM magazines WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    @classmethod
    def subscribe_to_magazine(cls, data):
        subscriber_data={
            'subscriber_id':session['user_id'],
            'magazine_id':data
        }
        query = 'INSERT INTO subscriptions (subscriber_id,magazine_id) VALUES (%(subscriber_id)s, %(magazine_id)s);'
        magazine_id = connectToMySQL(DATABASE).query_db(query, subscriber_data)
        return subscriber_data
    
    @classmethod
    def get_magazine_by_id_with_num_subscribers(cls, data):
        query = 'select * from magazines join subscriptions on magazines.id=subscriptions.magazine_id where magazines.id=%(id)s;'
        magazines_list = connectToMySQL(DATABASE).query_db(query, data)
        num_magazines= len(magazines_list)
        return num_magazines
