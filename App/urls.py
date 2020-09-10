from django.urls import path
from App import views

app_name = 'App'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('marketwithparams/<int:typeid>/<int:childcid>/<order_rule>/', views.market_with_params, name='market_with_params'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),

    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('checkuser/', views.check_user, name="check_user"),

    path('logout/', views.logout, name="logout"),
    path('activate/', views.activate, name="activate"),

    path('addtocart/', views.add_to_cart, name="add_to_cart"),
    path('changecartstate/', views.change_cart_state, name="change_cart_state"),

    path('subshopping/', views.sub_shopping, name="sub_shopping"),

    path('allselect/', views.all_select, name="all_select"),

    path('makeorder/', views.make_order, name="make_order"),

    path('orderdetail/', views.order_detail, name="order_detail"),
    path('orderlistnotpay/', views.order_list_not_pay, name="order_list_not_pay"),

    path('payed/', views.payed, name="payed"),
    path('alipay/', views.alipay, name="alipay"),



]
