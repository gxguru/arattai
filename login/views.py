# Create your views here.

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext

from django.http import HttpResponseRedirect
from arattai.models import BlogModel, UserModel, CommentModel
from django.contrib.auth.models import User

from django.core import validators

from validations import RegistrationForm

def login_user(request):
	state=""
	username = password = ""
	
	if request.POST:
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				state = "welcome %s" % username
				return HttpResponseRedirect('/arattai/mainpage/?username='+username)
			else:
				state = "Account is not active. Email the admin"
		else:
			state = "Login failed password=%s" % password
	return render_to_response('auth.html', {"state": state, "username": username}, context_instance=RequestContext(request))

#This method gets registered in the settings.py TEMPLATE_REGISTER file and this dictionary will be 
#available as part of request object.
def user_info(request):
	user = str(request.user).strip()
        print "guru user_info.user=", user
	if user != 'AnonymousUser':
	        user_data = User.objects.get(username=unicode(user))
	else:
		return {"user_id": -1, "username": user, "first_name": user}
	return {"user_id": user_data.id, "username": user_data.username, "first_name": user_data.first_name}


def mainpage(request):
        user_data = User.objects.get(username=unicode(request.user))
	print "mainpage: user_data.username=%s" % user_data.username
	if user_data is not None:
		return render_to_response('mainpage.html', {"username": user_data.username}, context_instance=RequestContext(request))

def savepage(request, page_name):
        content = request.POST['content']
        try:
                page = BlogModel.objects.filter(blog_name=blog_name)
		user = UserModel.objects.filter(user_id=user_id)
                page.content = content
        except wikipage.DoesNotExist:
                page = BlogModel(blog_name=blog_name, content=markdown.markdown(content))
        page.save()
        return HttpResponseRedirect("/arattai/"+ page_name+ "/")

def register(request):
	if request.POST:
		form1 = RegistrationForm(request.POST)
		
        #help taken from the following websites
        #https://docs.djangoproject.com/en/dev/ref/forms/validation/
        #https://docs.djangoproject.com/en/1.2/ref/validators/
		if form1.is_valid():
			user_ = User(username=form1.cleaned_data['username'], email=form1.cleaned_data['email'])
			user_.first_name = form1.cleaned_data['first_name']
			user_.last_name = form1.cleaned_data['last_name']
			user_.is_superuser = False
			user_.is_staff = False
			user_.set_password(form1.cleaned_data['password'])
			user_.save()			

		return render_to_response('auth.html', {"state": state, "username": username}, context_instance=RequestContext(request))
		#return HttpResponseRedirect('/arattai/mainpage/?username='+form1.cleaned_data['username'])
	else:
		return render_to_response('register.html', {"username": ""}, context_instance=RequestContext(request))
