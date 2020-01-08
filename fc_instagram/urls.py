from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.shortcuts import redirect

from contents.views import HomeView


# class NonUserTemplateView(TemplateView):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_anonymous:
#             return redirect('contents_home')

#         return super(NonUserTemplateView, self).dispatch(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include('apis.urls')),
    path('', HomeView.as_view(), name='contents_home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'),
         name='register'),
]
