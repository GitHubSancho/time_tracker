# tracker/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .forms import TimeRecordForm
from .models import TimeRecord, User  # 导入 TimeRecord 模型


def record_time(request):
    if request.method == 'POST' and request.headers.get(
            'x-requested-with') == 'XMLHttpRequest':
        form = TimeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            latest_records = TimeRecord.objects.order_by('-start_datetime')[:10]
            records_html = render(request, 'tracker/partials/records_list.html',
                                  {
                                      'records': latest_records
                                  }).content.decode('utf-8')
            return JsonResponse({
                'status': 'success',
                'message': '记录已成功保存',
                'records_html': records_html
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = TimeRecordForm()
        records = TimeRecord.objects.order_by(
            '-start_datetime')[:10]  # 获取最新的十条记录
        return render(request, 'tracker/record_time.html', {
            'form': form,
            'records': records
        })


def success_view(request):
    return render(request, 'tracker/success.html')  # 假设你有一个 success.html 模板


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember') == 'true'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                # 设置会话为两周后过期
                request.session.set_expiry(1209600)  # 1209600 秒 = 14 天
                # 设置Cookie保存用户名
                response = redirect('home')
                response.set_cookie('username', username, max_age=1209600)
                return response
            else:
                # 设置会话在浏览器关闭时过期
                request.session.set_expiry(0)
                return redirect('home')
        else:
            messages.error(request, '用户名或密码错误')  # 添加错误消息
            return render(request, 'tracker/login.html')
    else:
        # 如果存在记住我的Cookie，则填充用户名
        initial_data = {'username': request.COOKIES.get('username', '')}
        return render(request, 'tracker/login.html',
                      {'initial_data': initial_data})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 使用 create_user 方法创建并保存用户
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                invite_code=form.cleaned_data['invite_code'])
            login(request, user)
            message = '注册成功！'
            # 清空消息
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'tracker/signup.html', {
                'form': form,
                'message': message
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            # 清空消息
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'tracker/signup.html', {
                'form': form,
                'errors': errors
            })
    else:
        form = SignUpForm()
        # 清空消息
        storage = messages.get_messages(request)
        storage.used = True
    return render(request, 'tracker/signup.html', {'form': form})


def home_view(request):
    """ 首页 """
    return render(request, 'tracker/home.html')