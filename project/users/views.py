import random
import re
import uuid

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.

# 显示主页
from helper.demo_sms_send import send_sms
from users.forms import Reg_in, Log_in, Find_password, PersonModelFrom, Address_get
from users.models import Users, Shipaddress


# 判定是否登录的装饰器
def style(old_functioon):
    def inner(request,*args,**kwargs):
        if not request.session.get('tel'):
            # 跳转到登录页面
            return redirect('users:登录')
        else:
            # 表明已经存在session则继续调用原来的函数
            return old_functioon(request,*args,**kwargs)
    return inner


# 主页显示
@style
def show(request):
    tel = request.session.get('tel')
    constext = {
        'tel':tel
    }
    return render(request, 'users/member.html',context=constext)

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
            if Users.objects.filter(tel='{}'.format(clean_data.get('tel'))):
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
                # request.session['tel'] = request.POST.get('tel')
                # request.session.set_expiry(0)
                # 修改为直接跳转到登录页面进行登录
                return redirect('users:登录')
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
                request.session['tel'] = request.POST.get('tel')
                request.session.set_expiry(0)
                return redirect('users:主页')
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
            return redirect('users:登录')
        else:
            # 进行提示
            context = {
                'error':form.errors,
                'data':data,
            }
            return render(request, 'users/findback.html',context=context)
    else:
        return render(request, 'users/findback.html')

# 个人页面的修改
@style
def personpage(request):
    # 如果从session中没有获得tel,则表明没有登录,则需要跳转到登录页面
    datas = Users.objects.get(tel=request.session.get('tel'))
    if request.method == 'POST':
        data = request.POST
        form = PersonModelFrom(data)
        # 对数据进行检验
        if form.is_valid():
            # 如果写入的格式正确则进行数据库写入
            clean_data = form.cleaned_data
            Users.objects.filter(tel=request.session.get('tel')).update(**clean_data)
            # 之后跳转回当前页面
            # 从数据库中查询到数据进行传入

            return redirect('users:个人首页')
        else:
            # 输入有错则回显并提示
            context = {
                'data':datas
            }
            return render(request,'users/infor.html',context=context)
    else:
        # 进行数据显示
        context = {
            'data':datas
        }
        return render(request, 'users/infor.html',context=context)


# 收获地址显示函数
@style
def gladdress(request):
    return render(request, 'users/gladdress.html')


# 收货地址添加函数
@style
def address(request):
    if request.method == 'POST':
        # 进行表单的验证
        data = request.POST
        form = Address_get(data)
        if form.is_valid():
            # 验证通过后
            clean_data = form.cleaned_data
            # 由于最多只能有六个地址，所以这里需要先进行判定是否已经有六个地址
            users = Users.objects.get(tel=request.session.get('tel'))
            if len(users.shipaddress_set.filter(defaults=0)) == 6:
                # 表明已经有了6个地址,此时需要进行提示最多只有六条并不执行后面的语句
                context = {
                    'woring': '您已经拥有六条收货地址,请删除后再添加'
                }
                return render(request,'users/address.html',context=context)
            # 写入数据库前对数据前先对其是否是默认的选中地址进行判定
            if clean_data.get('defaults'):
                # 如果是选中的则先把数据库里面的默认清空,然后再添加,保持默认地址只有一个
                Shipaddress.objects.all().update(defaults=0)
                # 如果没有选则默认则直接添加
            # 将数据写入数据库
            Shipaddress.objects.create(linkusers=Users.objects.get(tel=request.session.get('tel')),**clean_data)
            # 添加成功后应该进行跳转
            return redirect('users:收货地址显示页')
        else:
            # 进行回显提示
            context = {
                'data':data,
                'error':form.errors,
            }
            return render(request,'users/address.html',context=context)
    else:
        return render(request, 'users/address.html')



from django_redis import *
def short_msg(request):
    # 当点击之后进行调用函数,返回的是json对象
    # 生成随机数
    # 先验证手机号的合法性
    tel = request.POST.get('tel')
    res = re.search('^1[3-9]\d{9}$', tel)
    if res:
        random_num = [str(random.randint(0,9)) for _ in range(4)]
        random_num = ''.join(random_num)
        # 产生随机数字之后进行写入数据库
        cnn = get_redis_connection('default')
        cnn.set(tel,random_num)
        cnn.expire(tel,300)
        # r = cnn.get(tel)
        print(random_num)
        # 向阿里法送短信验证请求
        __business_id = uuid.uuid1()
        # print(__business_id)
        params = "{\"code\":\"%s\",\"product\":\"老子就是做个短信验证而已\"}" % random_num
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        send_sms(__business_id,tel, "注册验证", "SMS_2245271", params)
        return JsonResponse({"key": 0})
    else:
        # 表单验证失败
        return JsonResponse({'key': 1})