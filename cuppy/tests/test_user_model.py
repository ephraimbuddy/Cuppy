from . import BaseTest


class TestSetPassword(BaseTest):

    def test_password_hash_saved(self):
        user = self.makeUser(username="ephraim", email='example@example.com')
        self.assertFalse(user.password_hash)

        user.set_password("secret")
        self.assertTrue(user.password_hash)


class TestCheckPassword(BaseTest):

    def test_password_hash_not_set(self):
        user = self.makeUser(username="ephraim", email='example@example.com')
        self.assertFalse(user.password_hash)
        self.assertFalse(user.check_password('secret'))

    def test_correct_password(self):
        user = self.makeUser(username="ephraim", email='example@example.com')
        user.set_password('secret')
        self.assertTrue(user.password_hash)
        self.assertTrue(user.check_password('secret'))

    def test_incorrect_password(self):
        user = self.makeUser(username="ephraim", email='example@example.com')
        user.set_password('secret')
        self.assertTrue(user.password_hash)
        self.assertFalse(user.check_password('incorrect'))


class TestAuthUserLog(BaseTest):

    def test_AddUserLog(self):
        from cuppy.models.users import AuthUserLog
        from sqlalchemy.sql import func
        user = self.makeUser(username="ephraim", email='example@example.com')
        user.set_password('secret')
        log = AuthUserLog(
            user = user,
            time = func.now(),
            event="R"
        )
        self.assertEqual(user.user_log[0].time,log.time)


class TestActivityLog(BaseTest):

    def test_userActivity(self):
        from cuppy.models.users import UserActivity
        from sqlalchemy.sql import func
        user = self.makeUser(username="ephraim", email='example@example.com')
        user.set_password('secret')
        ac = UserActivity(
            user=user,
            description="Added a user",
            time=func.now()
        )
        self.assertEqual(ac.time,user.activities[0].time)
