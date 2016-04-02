import unittest

from project import db
from project.models import User
from test import AllTests

class Test_user(AllTests):

    # each test should start with 'test'
    def test_user_setup(self):
        new_user = self.create_user("michael", "midfkja@dfa.dar", "michaelknop")
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        response = self.registerAndLoginDummy()
        self.assertIn(b'Welcome!', response.data)


    def test_logged_in_user_can_logout(self):
        self.registerAndLoginDummy()
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertIn(b'You need to login first.', response.data)

    def test_default_user_role(self):
        db.session.add(User("Johnny", "john@doe.com", "johnny"))
        db.session.commit()
        users = db.session.query(User).all()
        print users
        for user in users:
            self.assertEquals(user.role, 'user')

    def test_user_cannot_register_twice(self):
        self.register('Michael', 'mik@teletabies.com', 'Tinkiwinki', 'Tinkiwinki')
        response = self.register('Michael', 'mik@teletabies.com', 'Tinkiwinki', 'Tinkiwinki')
        self.assertIn(b'That username and/or email already exist.', response.data)

if __name__ == '__main__':
        unittest.main()    