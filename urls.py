from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("Signup.html", views.Signup, name="Signup"),
			path("SignupAction", views.SignupAction, name="SignupAction"),	    	
			path("UserLogin.html", views.UserLogin, name="UserLogin"),
			path("UserLoginAction", views.UserLoginAction, name="UserLoginAction"),
			path("UpdateProfile", views.UpdateProfile, name="UpdateProfile"),
			path("UpdateProfileAction", views.UpdateProfileAction, name="UpdateProfileAction"),
			path("GenerateResume", views.GenerateResume, name="GenerateResume"),
			path("GenerateResumeAction", views.GenerateResumeAction, name="GenerateResumeAction"),
			path("ViewPrevious", views.ViewPrevious, name="ViewPrevious"),
			path("ViewShared", views.ViewShared, name="ViewShared"),
			path("Download", views.Download, name="Download"),
]