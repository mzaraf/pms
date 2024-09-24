
from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordChangeForm(SetPasswordForm):
    """
    A form for changing the password without requiring the old password.
    Inherits from SetPasswordForm, which only asks for the new password and confirmation.
    """
    pass