
from django.urls import path, re_path, include
from rest_framework.authtoken.views import obtain_auth_token 
from django.views.generic import RedirectView


urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  ls
    path('api/', include('lms.urls')),
    path('', RedirectView.as_view(url='api/', permanent=False)),

]

