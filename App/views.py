import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods
from App.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND
from App.views_helper import hash_str, send_email_activate, get_total_price
from GPAXF.settings import MEDIA_KEY_PREFIX, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY, ALIPAY_APPID


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuy = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    # 切片获取想要操作的图片
    main_shop0_1 = main_shops[0:1]

    main_shop1_3 = main_shops[1:3]

    main_shop3_7 = main_shops[3:7]

    main_shop7_11 = main_shops[7:11]

    main_shows = MainShow.objects.all()

    data = {
        "title": "HOME",
        "main_wheels": main_wheels,
        "main_navs": main_navs,
        "main_mustbuy": main_mustbuy,
        "main_shop0_1": main_shop0_1,
        "main_shop1_3": main_shop1_3,
        "main_shop3_7": main_shop3_7,
        "main_shop7_11": main_shop7_11,
        "main_shows": main_shows,
    }

    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={
        "typeid": 104749,
        "childcid": 0,
        "order_rule": 0,
    }))


def market_with_params(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()

    # 根据传入的 typeid 筛选出商品列表,并将其显示在内容区
    goods_list = Goods.objects.filter(categoryid=typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)

    # 根据传入的规则.对字段进行排序
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    foodtype = foodtypes.get(typeid=typeid)
    """
        对数据进行切割,得到分类列表
        
        全部分类:0#进口水果:103534#国产水果:103533
        切割  #
            ['全部分类:0', '进口水果:103534', '国产水果:103533']
        切割  :
            [['全部分类', '0'], ['进口水果', '103534'], ['国产水果', '103533']]
    """
    foodtypechildnames = foodtype.childtypenames

    foodtypechildname_list = foodtypechildnames.split("#")

    foodtype_childname_list = []

    for foodtypechildname in foodtypechildname_list:
        foodtype_childname_list.append(foodtypechildname.split(":"))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_UP],
    ]

    data = {
        "title": "MARKET",
        "foodtypes": foodtypes,
        "goods_list": goods_list,
        # 侧边拦选中黄标签判断
        "typeid": int(typeid),
        "foodtype_childname_list": foodtype_childname_list,
        "childcid": childcid,
        "order_rule_list": order_rule_list,
        "order_rule_view": order_rule,
    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)

    # 存在未选中状态，all_select为 not真 =》假
    is_all_select = not carts.filter(c_is_select=False).exists()

    data = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(),
    }

    return render(request, "main/cart.html", context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        "title": "我的",
        "is_login": False
    }

    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url

        # 个人页面,订单状态
        data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        data['order_not_receive'] = Order.objects.filter(o_user=user).filter(
            o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == "GET":

        data = {
            "title": "Register",

        }

        return render(request, 'user/register.html', context=data)

    elif request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")

        # 密码摘要加密
        # password = hash_str(password)
        # Django内置加密
        password = make_password(password)

        user = AXFUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon

        user.save()

        # 使用uuid生成唯一标识字符串
        u_token = uuid.uuid4().hex

        # 存入缓存中
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username, email, u_token)

        return redirect(reverse("axf:login"))


def login(request):
    if request.method == "GET":

        error_message = request.session.get('error_message')

        data = {
            "title": "登陆"
        }

        # 删除session，避免页面刷新重复出现；将error_message展现在login页面
        if error_message:
            del request.session['error_message']
            data['error_message'] = error_message

        return render(request, 'user/login.html', context=data)

    elif request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # 校验密码
        users = AXFUser.objects.filter(u_username=username)

        if users.exists():
            user = users.first()
            # 用户密码，数据安全后的密码
            if check_password(password, user.u_password):

                # 密码正确后，验证是否已激活
                if user.is_active:
                    # 存储用户登录状态
                    request.session['user_id'] = user.id
                    return redirect(reverse('axf:mine'))
                else:
                    print('Not Activate')
                    request.session['error_message'] = 'Not Activate'
                    return redirect(reverse('axf:login'))
            else:
                print("密码错误")
                request.session['error_message'] = 'Password Error'
                return redirect(reverse('axf:login'))
        print("用户不存在")
        request.session['error_message'] = 'User Does Not Exist'
        return redirect(reverse('axf:login'))


def check_user(request):
    username = request.GET.get("username")

    users = AXFUser.objects.filter(u_username=username)

    data = {
        "status": HTTP_OK,
        "msg": 'user can use',
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass

    return JsonResponse(data=data)


def logout(request):
    request.session.flush()

    return redirect(reverse('axf:mine'))


# 激活
def activate(request):
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:
        # 删除token，邮件只能使用一次
        cache.delete(u_token)

        user = AXFUser.objects.get(pk=user_id)

        user.is_active = True

        user.save()
        return redirect(reverse('axf:login'))

    return render(request, 'user/activate_fail.html')


# 购物车
def add_to_cart(request):
    goodsid = request.GET.get('goodsid')

    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user

    cart_obj.save()

    data = {
        'status': 200,
        'mag': 'add success',
        'c_goods_num': cart_obj.c_goods_num,
    }

    return JsonResponse(data=data)


# 购物车中商品勾选
def change_cart_state(request):
    cart_id = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_select = not cart_obj.c_is_select

    cart_obj.save()

    # 当购物车中商品勾选状态改变时，判定全选勾选框是否勾选
    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(),
    }

    return JsonResponse(data=data)


# 购物车中商品减
def sub_shopping(request):
    cartid = request.GET.get("cartid")

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': 'ok',
    }

    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num

    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    data['total_price'] = get_total_price()

    return JsonResponse(data=data)


def all_select(request):
    cart_list = request.GET.get('cart_list')
    # 将接收的’#‘字符串，还原成列表
    cart_list = cart_list.split("#")

    carts = Cart.objects.filter(pk__in=cart_list)

    for cart_obj in carts:
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'total_price': get_total_price(),
    }

    return JsonResponse(data=data)


# 生成订单
def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order()

    order.o_user = request.user

    order.o_price = get_total_price()

    order.save()

    # 生成订单并删除购物车中数据
    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()

    data = {
        "status": 200,
        "msg": 'ok',
        'order_id': order.id,
    }

    return JsonResponse(data)


def order_detail(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    data = {
        'title': "订单详情",
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    # 筛选出未付款的订单
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):
    order_id = request.GET.get("orderid")

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    data = {
        'status': 200,
        'msg': 'payed success',
    }

    return JsonResponse(data)


def alipay(request):
    # 构建支付客户端
    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        # 私钥
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )

    # 使用alipay进行支付请求的发起
    subject = "Macbook pro"
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no="20161112",    # 订单编号
        total_amount=0.01,  # 金额
        subject=subject,    # 主题
        return_url="https://www.baidu.com",
        notify_url="https://www.baidu.com"  # 可选, 不填则使用默认notify url
    )

    # 客户端操作
    return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

