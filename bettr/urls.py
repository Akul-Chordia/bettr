"""
URL configuration for bettr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# bettr/urls.py


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from bets import views  # Import your views

urlpatterns = [
    path('admin/' , admin.site.urls) ,
    path('' , views.index , name='index') ,  # Set the index view to the home ('') URL
    path('login/' , views.login_view , name='login') ,  # Use views.login_view directly
    path('notifications/' , views.notification_view , name='notifications') ,
    path('logout/' , views.logout_view , name='logout') ,
    path('profile/' , views.profile_view , name='profile') ,
    path('signup/' , views.create_user_profile , name='signup') ,
    path('bet/' , views.bet_view , name='bet') ,
    path('make_bet/' , views.make_bet , name='make_bet') ,
    path('wallet/' , views.wallet , name='wallet') ,
    path('my-bets/' , views.my_bets_view , name='my_bets') ,
    path('profile/' , views.profile_view , name='profile') ,
    path('validate_bet/' , views.validate_bet , name='validate_bet') ,
    path('claim_verification/' , views.claim_dispute , name='claim_verification') ,
    path('arbitration_request/' , views.arbitrator_rule , name='arbitration_request') ,
    path('claim_bet/' , views.claim_bet , name='claim_bet') ,
    path('add_money/' , views.add_money , name='add_money') ,
    path('withdraw_money/' , views.withdraw_money , name='withdraw_money')

]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
