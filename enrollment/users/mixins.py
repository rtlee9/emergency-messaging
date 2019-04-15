from django.contrib.auth.mixins import UserPassesTestMixin


class StaffRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is staff."""

    def test_func(self):
        if not self.request.user.is_staff:
            self.raise_exception = True
            self.permission_denied_message = """
            Staff access required. Please email admin to aprove accesss.
            """
            return False
        return True
