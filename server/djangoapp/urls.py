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

    path(route='', view=views.get_dealerships, name='home'),
    path('about/',views.AboutPageView.as_view(),name='about'),
    path('contact/',views.ContactPageView.as_view(),name='contact'),
    path('reviews/', views.ReviewPageView.as_view(),name='reviews'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path(route='dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    path('dealer/<int:id>/add-review/', views.add_review, name='add_review'),
    path(route='dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    path(route='dealer/<int:id>/review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)