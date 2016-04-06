import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    # execute prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG']=False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)
    
    def login_admin(self):
        return self.app.post('/', data=dict(
            name='Superman', password="LuiseLane"), follow_redirects=True)
        
    def register(self, name, email, password, confirm):
        return self.app.post('register/', data=dict(
            name=name, email=email, password=password, confirm=confirm), 
            follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)
    
    def registerAndLoginDummy(self):
        self.register('Michael', 'mik@teletabies.com', 'Tinkiwinki', 'Tinkiwinki')
        return self.login('Michael', 'Tinkiwinki')

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
    
    def create_admin_user(self):
        new_user = User(name='Superman', email="karel@krypton.uni", 
            password=bcrypt.generate_password_hash('LuiseLane'), role='admin')
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data = dict(
            name='Go to the bank', 
            due_date='02/05/2014',
            priority='1',
            posted_date='02/04/2014', 
            status='1'), follow_redirects=True)


    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list', response.data)



 


if __name__ == "__main__":
    unittest.main()
