$(function () {
    // 在未付款订单列表点击订单，跳转到订单详情支付界面
    $(".order").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        window.open('/axf/orderdetail/?orderid=' + order_id, "_self");

    })

})