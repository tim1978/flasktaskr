import unittest

from test import AllTests

class Test_tasks(AllTests):
    
    def test_users_can_add_tasks(self):
        self.registerAndLoginDummy()
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    def test_uses_cannot_add_tasks_when_error(self):
        self.registerAndLoginDummy()
        self.app.get('add/', follow_redirects=True)
        response = self.app.post('add/', data = dict(
            name='Go to the bank', 
            due_date='',
            priority='1',
            posted_date='02/04/2014', 
            status='1'), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.registerAndLoginDummy()
        self.create_task()
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)
    
    def test_users_can_delete_tasks(self):
        self.registerAndLoginDummy()
        self.create_task()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)    
    
    def test_task_can_only_be_created_when_logged_in(self):
        response = self.create_task()
        self.assertIn(b'You need to login first.', response.data)
        
    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.create_user('Martindddd', 'martin@martin.de', 'martin234')
        self.login('Martindddd', 'martin234')
        self.app.get('tasks/', follow_redirects = True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.create_user('Martindddd', 'martin@martin.de', 'martin234')
        self.login('Martindddd', 'martin234')
        self.app.get('tasks/', follow_redirects = True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(b'The task was deleted.', response.data)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login_admin()
        self.app.get('tasks/', follow_redirects = True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'You can only update tasks that belong to you.', response.data)

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.registerAndLoginDummy()
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login_admin()
        self.app.get('tasks/', follow_redirects = True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you.', response.data)

if __name__ == '__main__':
    unittest.main()