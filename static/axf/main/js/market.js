$(function () {
    $("#all_types").click(function () {
        console.log("All Type");

        var $all_types_container = $("#all_types_container");

        $all_types_container.show();

        var $all_type = $(this);

        var $span = $all_type.find("span").find("span");

        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");

        var $sort_rule_container = $(sort_rule_container);

        $sort_rule_container.slideUp();

        var $sort_rule = $("#sort_rule");

        var $span_sort_rule = $sort_rule.find("span").find("span");

        $span.removeClass("glyphico-chevron-up").addClass("glphicon-chevron-down");

    })

    // 点击展示区,下拉菜单收回,下箭头图标变为上箭头
    $("#all_types_container").click(function () {

        var $all_type_container = $(this);

        $all_type_container.hide();

        var $all_type = $("#all_types");

        var $span = $all_type.find("span").find("span");

        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#sort_rule").click(function () {
        console.log("Sort Rule");

        var $sort_rule_container = $("#sort_rule_container");

        $sort_rule_container.show();

        var $sort_rule = $(this);

        var $span = $sort_rule.find("span").find("span");

        $span.removeClass("glyphico-chevron-down").addClass("glphicon-chevron-up");

        var $all_type_container = $("#all_type_container");

        $all_type_container.hide();

        var $all_type = $("#all_types");

        var $span_all_type = $all_type.find("span").find("span");

        $span_all_type.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#sort_rule_container").click(function(){

        var $sort_rule_container = $(this);

        $sort_rule_container.slideUp();

        var $sort_rule = $("#sort_rule");

        var $span = $sort_rule.find("span").find("span");

        $span.removeClass("glyphico-chevron-up").addClass("glphicon-chevron-down");

    })

    // 商品点击+-事件
    $(".subShopping").click(function () {
        console.log('sub');
    })

    $(".addShopping").click(function () {
        console.log('add');
        // 在HTML上级元素goods中获取goodsid，js中接收，再传到views中
        var $add = $(this);

        var goodsid = $add.attr("goodsid");

        // 将goods.id通过ajax发送给服务器，加入购物车，（地址，参数，返回结果）
        $.get('/axf/addtocart/', {"goodsid": goodsid}, function (data) {
            console.log(data);

            if (data['status'] === 302){
                window.open('/axf/login/', "_self");
            }else if (data['status'] === 200){
                // 查找add在HTML中的兄弟（上一个）节点span
                // .html改变元素内的内容，实现商品的添加数字变化
                $add.prev('span').html(data['c_goods_num'])
            }
        })
    })

})