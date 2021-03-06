$(function () {

    // 购物车中商品勾选
    $(".confirm").click(function () {

        console.log("change state");

        var $confirm = $(this);

        var $li = $confirm.parents("li");

        var cartid = $li.attr('cartid');

        $.getJSON("/axf/changecartstate/", {'cartid': cartid}, function (data) {

            console.log(data);

            if (data['status'] === 200) {

                $("#total_price").html(data['total_price']);

                if (data['c_is_select']) {
                    $confirm.find("span").find("span").html("√")
                } else {
                    $confirm.find("span").find("span").html("")
                }

                // 判定全选框勾选状态，有商品为勾选就显示未勾选
                if (data['is_all_select']) {

                    $(".all_select span span").html("√");
                } else {

                    $(".all_select span span").html("");
                }
            }

        })

    })

    // 购物车中点击 - 的事件
    $(".subShopping").click(function () {

        var $sub = $(this);

        var $li = $sub.parents("li");

        var cartid = $li.attr("cartid");

        $.getJSON("/axf/subshopping/", {"cartid": cartid}, function (data) {
            console.log(data);

            if (data['status'] === 200) {

                $("#total_price").html(data['total_price']);

                if (data['c_goods_num'] > 0) {
                    var $span = $sub.next("span");
                    $span.html(data['c_goods_num']);
                } else {
                    $li.remove();
                }
            }
        })

    })

    // 将选中和未选中分类,点击全选时改变选中状态
    $(".all_select").click(function () {

        var $all_select = $(this);

        // 分类未选中和选中
        var select_list = [];

        var unselect_list = [];

        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            // 判断勾选框中是否有内容，并进行分类
            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid);
            } else {
                unselect_list.push(cartid);
            }
        })

        if (unselect_list.length > 0) {
            // 无法传输 列表类型
            // 将列表中的元素用 # 连接
            $.getJSON("/axf/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data);
                // 商品和全选按钮变为选中状态
                if (data['status'] === 200) {
                    $(".confirm").find("span").find("span").html("√");
                    $all_select.find("span").find("span").html("√");

                    $("#total_price").html(data['total_price']);
                }
            })
        } else {
            if (select_list.length > 0) {
                $.getJSON("/axf/allselect/", {"cart_list": select_list.join("#")}, function (data) {
                    console.log(data);
                    if (data['status'] === 200) {
                        $(".confirm").find("span").find("span").html("");
                        $all_select.find("span").find("span").html("");

                        $("#total_price").html(data['total_price']);
                    }
                })
            }
        }
    })

    // 生成订单
    $("#make_order").click(function () {

        var select_list = [];

        var unselect_list = [];

        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            // 判断勾选框中是否有内容，并进行分类
            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid);
            } else {
                unselect_list.push(cartid);
            }
        })

        if (select_list.length === 0){
            return
        }
        $.getJSON("/axf/makeorder/", function (data) {
            console.log(data);

            if (data['status'] === 200){
                window.open('/axf/orderdetail/?orderid=' + data['order_id'], "_self");
            }

        })

    })

})