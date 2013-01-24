from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from arattai import settings
import re

login_form_widget_attrs = { 'class': 'required login' }
username_re = re.compile(r'^[\w\s ]+$', re.UNICODE)

class StrippedNonEmptyCharField(forms.CharField):
	def clean(self, value):
		value = value.strip()
		if self.required and value == '':
			raise forms.ValidationError(_('this field is required'))
		return value

class UserNameField(StrippedNonEmptyCharField):
	def __init__(self, db_model=User, db_field='username', must_exist=False, skip_clean=False, label=_('choose a username'), **kw):
		self.must_exist = must_exist
		self.skip_clean = skip_clean
		self.db_model = db_model
		self.db_field = db_field
		error_message={'required': _('user name is required'),
'taken': _("sorry, this name is taken, please choose another"),
'forbidden': _("sorry, this name is not allowed, please choose another"),
'missing': _('sorry, tere is no user with this name'),
'multiple-taken': _('sorry, we have serious error - user name is taken by sevaral users'),
'invalid': _('user name can only consist of letters, empty space and underscore'),
'toshort': _('user name is to short, please use at least %d characters') % settings.MIN_USERNAME_LENGTH}
		super(UserNameField, self).__init__(widget=forms.TextInput(attrs=login_form_widget_attrs), label=label, error_messages=error_message, **kw)

		if 'error_messages' in kw:
			error_messages.update(kw['error_messages'])
			del kw['error_messages']
			super(UserNameField, self).__init__(max_length=30, widget=forms.TextInput(attrs=login_form_widget_attrs), label=label, error_mesages=error_messages, **kw)

	def clean(self, username):
		""" validate username """
		if self.skip_clean == True:
			return username
		
        	if hasattr(self, 'user_instance') and isinstance(self.user_instance, User):
	            if username == self.user_instance.username:
	                return username

        	try:
            		username = super(UserNameField, self).clean(username)
        	except forms.ValidationError:
            		raise forms.ValidationError(self.error_messages['required'])
		
        	if len(username) < settings.MIN_USERNAME_LENGTH:
            		raise forms.ValidationError(self.error_messages['toshort'])

        	if self.required and not username_re.match(username):
            		raise forms.ValidationError(self.error_messages['invalid'])

        	if username in settings.RESERVED_USERNAMES:
            		raise forms.ValidationError(self.error_messages['forbidden'])

        	try:
            		user = self.db_model.objects.get(
                    	**{'%s' % self.db_field : username}
            		)
            		if user:
                		if self.must_exist:
                    			return username
                		else:
                    			raise forms.ValidationError(self.error_messages['taken'])
        	except self.db_model.DoesNotExist:
            		if self.must_exist:
                		raise forms.ValidationError(self.error_messages['missing'])
            		else:
                		return username
        	except self.db_model.MultipleObjectsReturned:
            		raise forms.ValidationError(self.error_messages['multiple-taken'])

class UserEmailField(forms.EmailField):
    def __init__(self,skip_clean=False,**kw):
        self.skip_clean = skip_clean
        super(UserEmailField,self).__init__(widget=forms.TextInput(attrs=dict(login_form_widget_attrs,
            maxlength=200)), label=mark_safe(_('your email address')),
            error_messages={'required':_('email address is required'),
                            'invalid':_('please enter a valid email address'),
                            'taken':_('this email is already used by someone else, please choose another'),
                            },
            **kw
            )

    def clean(self,email):
        """ validate if email exist in database
        from legacy register
        return: raise error if it exist """
        email = super(UserEmailField,self).clean(email.strip())
        if self.skip_clean:
            return email
        if settings.EMAIL_UNIQUE == True:
            try:
                user = User.objects.get(email = email)
                raise forms.ValidationError(self.error_messages['taken'])
            except User.DoesNotExist:
                return email
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(self.error_messages['taken'])
        else:
            return email 


class UserFirstNameField(forms.CharField):
	def clean(self, value):
		value = value.strip()
		if self.required and value == '':
			raise forms.ValidationError(_('this field is required'))
		return value

class UserLastNameField(forms.CharField):
	def clean(self, value):
		value = value.strip()
		if self.required and value == '':
			raise forms.ValidationError(_('this field is required'))
		return value

class RegistrationForm(forms.Form):
	email = UserEmailField()
	username = UserNameField()
	first_name = UserFirstNameField()
	last_name = UserLastNameField()
        password = forms.CharField( widget=forms.PasswordInput(render_value=False), label="Your Password" )

	#def __init__(self, *args, **kwargs):
	#	super(RegistrationForm, self).__init__(*args, **kwargs)
