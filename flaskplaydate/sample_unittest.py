import unittest
from types import SimpleNamespace
from .routes import account
from . import routes
from . import app

class AccountRouteTests(unittest.TestCase):
    def test_account_get_populates_form_and_renders(self):
        fake_user = SimpleNamespace(username="olduser", email="old@example.com", image_file="pic.png")

        last_form = {}

        class FakeField:
            def __init__(self):
                self.data = None

        class FakeForm:
            def __init__(self):
                last_form['inst'] = self
                self.picture = FakeField()
                self.username = FakeField()
                self.email = FakeField()

            def validate_on_submit(self):
                return False

        def fake_render_template(*args, **kwargs):
            return {"rendered": args, "context": kwargs}

        def fake_url_for(endpoint, **kwargs):
            return "/static/" + kwargs.get("filename", "")

        # patch module-level names in routes
        orig_UpdateAccountForm = routes.UpdateAccountForm
        orig_render_template = routes.render_template
        orig_url_for = routes.url_for
        orig_current_user = routes.current_user

        try:
            routes.UpdateAccountForm = FakeForm
            routes.render_template = fake_render_template
            routes.url_for = fake_url_for
            routes.current_user = fake_user

            with app.test_request_context("/account", method="GET"):
                result = account()

            # verify render_template was called (we return our sentinel)
            self.assertIsInstance(result, dict)
            # verify the form instance was populated from current_user in GET branch
            form = last_form.get("inst")
            self.assertIsNotNone(form)
            self.assertEqual(form.picture.data, "pic.png")
            self.assertEqual(form.username.data, "olduser")
            self.assertEqual(form.email.data, "old@example.com")
        finally:
            routes.UpdateAccountForm = orig_UpdateAccountForm
            routes.render_template = orig_render_template
            routes.url_for = orig_url_for
            routes.current_user = orig_current_user

    def test_account_post_updates_user_and_redirects(self):
        fake_user = SimpleNamespace(username="olduser", email="old@example.com", image_file="pic.png")

        commit_called = {"flag": False}

        class FakeFormPost:
            def __init__(self):
                self.picture = SimpleNamespace(data=None)
                self.username = SimpleNamespace(data="newuser")
                self.email = SimpleNamespace(data="new@example.com")

            def validate_on_submit(self):
                return True

        def fake_commit():
            commit_called["flag"] = True

        def fake_redirect(target):
            return ("redirected-to", target)

        def fake_url_for(name, **kwargs):
            return "/account"

        orig_UpdateAccountForm = routes.UpdateAccountForm
        orig_db_session = getattr(routes, "db").session if hasattr(routes, "db") else None
        orig_redirect = routes.redirect
        orig_url_for = routes.url_for
        orig_current_user = routes.current_user

        # patch what's necessary
        try:
            routes.UpdateAccountForm = FakeFormPost
            if hasattr(routes, "db"):
                routes.db.session.commit = fake_commit
            routes.redirect = fake_redirect
            routes.url_for = fake_url_for
            routes.current_user = fake_user

            with app.test_request_context("/account", method="POST"):
                result = account()

            # after POST, user attributes should be updated and commit called
            self.assertEqual(fake_user.username, "newuser")
            self.assertEqual(fake_user.email, "new@example.com")
            self.assertTrue(commit_called["flag"] or (orig_db_session is None))
            # result should be our fake redirect sentinel
            self.assertEqual(result, ("redirected-to", "/account"))
        finally:
            routes.UpdateAccountForm = orig_UpdateAccountForm
            if orig_db_session is not None:
                routes.db.session = orig_db_session
            routes.redirect = orig_redirect
            routes.url_for = orig_url_for
            routes.current_user = orig_current_user


if __name__ == "__main__":
    unittest.main()