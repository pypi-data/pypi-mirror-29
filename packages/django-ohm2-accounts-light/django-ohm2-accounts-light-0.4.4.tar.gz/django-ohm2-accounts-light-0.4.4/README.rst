django-ohm2-handlers-light source code
=============================


Installation:

#. Create a Python +3.5 virtualenv

#. Install dependencies::

    - ohm2_handlers_light
    - rest_framework

#. Add 'ohm2_accounts_light' to installed apps::

    INSTALLED_APPS = [
      '''
      'ohm2_accounts_light',
      ...
    ]

#. Create tables::

    ./manage.py migrate




Models
------

handlers_light comes with two basic models::
	#from ohm2_handlers_light.models import BaseModel

	class PasswordReset(BaseModel):
		user = models.ForeignKey(User)

		last_sent_date = models.DateTimeField(null = True, blank = True, default = None)
		activation_date = models.DateTimeField(null = True, blank = True, default = None)
		ip_address = models.GenericIPAddressField(null = True, blank = True, default = "")
		code = models.CharField(max_length = settings.STRING_NORMAL, unique = True)


		def send_again(self):
			if self.last_sent_date and not h_utils.is_older_than_now(self.last_sent_date, seconds = settings.MINIMUM_PASSWORD_RESET_DELAY):
				return False
			return True

		def __str__(self):
			return self.user.username


Pipelines
---------

Use this pipelines to handle cascade-functions.

Signup (ohm2_accounts_light.pipelines.signup.default)::
	
	# 1: user = ohm2_accounts_light_utils.create_user(username, email, password)
	# 2: ohm2_accounts_light_utils.run_signup_pipeline(request, user, username, email, password)


Login (ohm2_accounts_light.pipelines.login.default)::
	
	# 1: auth_user = authenticate(username, password)
	# 2: ohm2_accounts_light_utils.run_login_pipeline(request, auth_user)

	
Logout (ohm2_accounts_light.pipelines.logout.default)::
	
	# 1: ohm2_accounts_light_utils.run_logout_pipeline(request)



Behavior can be change on the settins.py like this::

	OHM2_ACCOUNTS_LIGHT_SIGNUP_PIPELINE = (
		'your_app.pipelines.signup.pipeline_1',
		'your_app.pipelines.signup.pipeline_2',
	)

	OHM2_ACCOUNTS_LIGHT_LOGIN_PIPELINE = (
		'your_app.pipelines.login.pipeline_1',
		'your_app.pipelines.login.pipeline_2',
	)

	OHM2_ACCOUNTS_LIGHT_LOGOUT_PIPELINE = (
		'your_app.pipelines.logout.pipeline_1',
		'your_app.pipelines.logout.pipeline_2',
	)





Variables
---------

OHM2_ACCOUNTS_LIGHT_CHECK_PASSWORD_SECURE: check if user password is secure (default: True)
OHM2_ACCOUNTS_LIGHT_SIGNUPS_ENABLED: signup enabled (disabled) (default: True)
OHM2_ACCOUNTS_LIGHT_ENABLE_EMAIL_LOGIN: users are able to login using their email address (default: True)
OHM2_ACCOUNTS_LIGHT_UNIQUE_USER_EMAILS: if True, users must have unique email addresses (default: True)
OHM2_ACCOUNTS_LIGHT_SIGNUP_PIPELINE: sets the signup pipeline
OHM2_ACCOUNTS_LIGHT_LOGIN_PIPELINE: sets the login pipeline
OHM2_ACCOUNTS_LIGHT_LOGOUT_PIPELINE: sets the logout pipeline



API - v1
--------

Add 'ohm2_accounts_light.api.v1.urls' to your 'urls.py'.

Signup (ohm2_accounts_light.api.v1.views.signup)::
	
	Runs the signup pipeline checking this variables::

		1.- CHECK_PASSWORD_SECURE: if True, check user's password using 'ohm2_accounts_light.utils.is_password_secure'.
		2.- SIGNUPS_ENABLED: if True, signups are allowed. If False, no signups will take place.


Login(ohm2_accounts_light.api.v1.views.login)::
	
	Runs the login pipeline checking this variables::

		1.- ENABLE_EMAIL_LOGIN: if True, will try to use username as email address.
		2.- UNIQUE_USER_EMAILS: if True, will get user objects using 'h_utils.get_db' function


Logout(ohm2_accounts_light.api.v1.views.logout)::
	
	Runs the logout pipeline.


	