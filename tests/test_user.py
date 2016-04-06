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

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.register('Michaela', 'mika@teletabies.com', 'Tippsy66', 'Tippsy66')
        response=self.login('Michaela', 'Tippsy66')
        self.assertNotIn(b'Delete', response.data)
        self.assertNotIn(b'Mark as complete', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.register('Michael', 'mik@teletabies.com', 'Tinkiwinki', 'Tinkiwinki')
        self.login('Michael', 'Tinkiwinki')
        response=self.create_task()
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)

    def test_admin_users_can_see_task_modify_links_for_all_tasks(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'LuiseLane')
        response=self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)




if __name__ == '__main__':
        unittest.main()    