from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render

from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from main.models import Contact



def index(request):

	if request.method == "POST":
		full_name = request.POST.get("full_name")
		email = request.POST.get("email")
		message = request.POST.get("message")

		contact = Contact.objects.create(full_name=full_name, email=email, message=message)
		contact.save()

		messages.success(request, "Message Sent Successfully!")
		return HttpResponseRedirect(reverse("main:index"))


	else:
		context = {
				
	            }
		
		return render(request, "main/index.html", context )
