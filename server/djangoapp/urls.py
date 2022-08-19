from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView

app_name = 'djangoapp'


urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path('',views.HomePageView.as_view(),name='home'),
    path('about/',views.AboutPageView.as_view(),name='about'),
    path('contact/',views.ContactPageView.as_view(),name='contact'),
    path('login/',views.LoginPageView.as_view(),name='login'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)