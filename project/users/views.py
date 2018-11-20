from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

# 显示主页
from users.forms import Reg_in, Log_in, Find_password
from users.models import Users


def show(request):
    return render(request, 'users/member.html')

# 注册页面
def reg_in(request):
    # 如果是提交判断失败的需要进行分类的处理
    if request.method == 'POST':
        # 如果使用的是提交方式
        data = request.POST
        form = Reg_in(data)
        if form.is_valid():
            # 如果验证成功,需要进一步验证密码与再次输入的是否一致
            clean_data = form.cleaned_data
            # 对用户名进行判断,防止在数据库中已经注册
            if str(clean_data.get('tel')) == str(Users.objects.get(tel='{}'.format(clean_data.get('tel'))).tel):
                # 如果该用户已经注册过则进行跳转回原来界面,并构造错误让其显示
                mes = {'tel': ['该用户已经注册']}
                context = {
                    'error': mes
                }
                return render(request, 'users/reg.html',context=context)

            if clean_data.get('password') == clean_data.get('re_password'):
                # 密码没有问题则进行写入数据库
                # 写入数据库进行md5加密
                password = clean_data.get('password')
                import hashlib
                ha = hashlib.md5(password.encode('utf-8'))
                password = ha.hexdigest()
                # 写入数据库
                Users.objects.create(tel=clean_data.get('tel'),password=password)
                # 直接登录跳转到个人中心并添加session
                request.session['tel'] = request.POST.get('tel')
                # request.session.set_expriy(0)
                return render(request,'users/member.html')
            else:
                # 密码验证没有通过则回到原始界面
                mes = {'re_password':['两次密码输入不一致']}
                context = {
                    'error':mes
                }
                return render(request, 'users/reg.html',context=context)
        else:
            # 格式存在不正确的,那么需要回显示
            context = {
                'error':form.errors,
                'data':data,
            }
            return render(request,'users/reg.html',context=context)
    return render(request,'users/reg.html')

# 登录页面
def log_in(request):
    # 导入登录页面
    # 如果是采用的POST登录则需要进行表单验证
    if request.method == 'POST':
        # 需要对提交的信息进行验证
        data = request.POST
        form = Log_in(data)
        if form.is_valid():
            # 如果输入没有错误再执行
            clean_data = form.cleaned_data
            password = clean_data.get('password')
            # 进行哈希转换
            import hashlib
            ha = hashlib.md5(password.encode('utf-8'))
            password = ha.hexdigest()
            # 进行数据库查询
            if Users.objects.filter(tel=clean_data.get('tel'),password=password):
                # 如果找到了则表明用户输入正确进行跳转到个人主页
                return render(request,'users/member.html')
            else:
                # 如果错误则表明用户名密码不正确,需要进行重新输入并提示
                mes = {'tel': ['用户名或者密码不正确']}
                context = {
                    'error': mes,
                    'data':request.POST
                }
                return render(request, 'users/login.html',context=context)
        else:
            # 如果存在普通错误需要回显示提示
            context = {
                'error':form.errors,
                'data':request.POST
            }
            return render(request, 'users/login.html',context=context)
    else:
        # 其他方式登录则进行直接显示
        return render(request, 'users/login.html')

# 密码找回
def findback(request):
    if request.method == 'POST':
        # 使用的是POST方式则进行数据的改写
        data = request.POST
        form = Find_password(data)
        if form.is_valid():
            # 如果数据没问题执行则进行数据判断
            clean_data = form.cleaned_data
            # 对用户是否存在判断
            if not Users.objects.filter(tel=clean_data.get('tel')):
                # 表示用户名不存在
                context = {
                    'error':{'tel':['用户名不存在']},
                    'data':data,
                }
                return render(request, 'users/findback.html',context=context)
            # 对两次输入密码是否一致的判断
            if not clean_data.get('password') == clean_data.get('re_password'):
                # 两次密码输入不正确
                context = {
                    'error': {'password': ['两次密码输入不一致']},
                    'data': data,
                }
                return render(request, 'users/findback.html',context=context)
            # 之前的都没有错误则执行数据库的更新
            # 对密码进行哈希处理
            import hashlib
            ha = hashlib.md5(clean_data.get('password').encode('utf-8'))
            password = ha.hexdigest()
            Users.objects.filter(tel=clean_data.get('tel')).update(password=password)
            # 最后跳转回登录页
            return render(request,'users/login.html')
        else:
            # 进行提示
            context = {
                'error':form.errors,
                'data':data,
            }
            return render(request, 'users/findback.html',context=context)
    else:
        return render(request, 'users/findback.html')