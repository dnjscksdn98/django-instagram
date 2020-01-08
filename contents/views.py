from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):  # 홈, TemplateView: 해당 템플릿으로 렌더링해줌
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    template_name = 'home.html'  # 렌더링 해줄 html 지정
