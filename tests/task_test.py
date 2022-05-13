import logging

from app import db
from app.db.models import Task
from faker import Faker
import datetime

def test_adding_task(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(Task).count() == 0
        #showing how to add a record
        #create a record
        task = Task('test', 'this is a test', datetime.datetime(2022,5,19), 1,0)
        #add it to get ready to be committed
        db.session.add(task)
        #finding one user record by email
        user = Task.query.filter_by(title='test').first()
        log.info(task)
        #asserting that the user retrieved is correct
        assert task.title == 'test'
        
        #checking cascade delete
        db.session.delete(task)
        assert db.session.query(Task).count() == 0




