# Create your views here.
from django.http import HttpResponse
from django.http import Http404  
from django.shortcuts import get_object_or_404, render_to_response
from djsite.helloworld.models import UserInfo

def index(request):
	return render_to_response("helloworld/index.html")
	
def pageview(request, page_name):
	try:
		return render_to_response("helloworld/%s.html" % page_name)
	except:
		raise Http404
	
def interest(request):
	try:
		u = UserInfo.objects.get(email=request.POST['email'])
		return render_to_response("helloworld/error.html", {'error_message':"You have already signed up! We'll let you know when we're ready for you!"})
	except UserInfo.DoesNotExist:
		try:
			u = UserInfo(email=request.POST['email'])
			u.save()
			return render_to_response("helloworld/thanks.html")
		except KeyError:
			return render_to_response("helloworld/error.html", {'error_message':"No form data entered"})
		return render_to_response("helloworld/thanks.html")