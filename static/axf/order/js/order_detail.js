$(function () {
    // 订单支付
    $("#alipay").click(function () {

        console.log("支付");

        var orderid = $(this).attr("orderid");

        $.getJSON("/axf/payed/", {"orderid": orderid}, function(data) {
            console.log(data);

            if (data['status'] === 200){
                window.open('/axf/mine', '_self')
            }
        })

    })

})