import logging

from app import db
from app.db.models import User
from faker import Faker

def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        #showing how to add a record
        #create a record
        user = User('ksl29@njit.edu', 'Password@123', 'Kadeem', 'Lewis',0)
        #add it to get ready to be committed
        db.session.add(user)
        #finding one user record by email
        user = User.query.filter_by(email='ksl29@njit.edu').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'ksl29@njit.edu'
        
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
