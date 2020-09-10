$(function () {

    $("#not_login").click(function () {
        // 未登录，定义点击登录事件
        window.open('/axf/login/', '_self');
    })

    $("#regis").click(function () {
        window.open('/axf/register/',"_self");
    })

    $("#not_pay").click(function () {
        // 未付款点击事件
        window.open('/axf/orderlistnotpay/', "_self")

    })

})