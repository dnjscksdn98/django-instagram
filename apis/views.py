from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login


class BaseView(View):  # 베이스 API
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result)


class UserCreateView(BaseView):  # 유저 생성 API
    @method_decorator(csrf_exempt)  # post 사용시 필요, 보안을 위해
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):  # 유저 생성
        username = request.POST.get('username', '')
        # 예외 처리
        if not username:
            self.response(message='아이디를 입력해주세요', status=400)

        password = request.POST.get('password', '')
        if not password:
            self.response(message='패스워드를 입력해주세요', status=400)

        email = request.POST.get('email', '')
        if not email:
            try:
                validate_email(email)  # 이메일 폼 검증
            except ValidationError:  # 검증 오류
                self.response(message='올바른 이메일을 입력해주세요', status=400)

        try:  # 예외 처리
            user = User.objects.create_user(  # 유저 생성
                username,
                password,
                email
            )
        except IntegrityError:  # 유효하지 않을 겨우 에러 발생
            # status=400 : 잘못된 요청
            # BaseView의 response호출
            return self.response(message='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id': user.id})


class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요', status=400)

        password = request.POST.get('password', '')
        if not password:
            return self.response(message='패스워드를 입력해주세요', status=400)

        # 유효하면 User를 반환하고, 그렇지 않으면 None을 반환
        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(message='입력 정보를 확인해주세요', status=400)

        login(request, user)  # 로그인

        return self.response
