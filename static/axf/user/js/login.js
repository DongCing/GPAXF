// 登录密码摘要加密，避免浏览器端密码泄露
function parse_data() {

    var $password_input = $("#password_input");
    // val()获取文本框内的值,trim()去除头尾空格
    var password = $password_input.val().trim();
    // 摘要算法，进行密码安全
    $password_input.val(md5(password));

    return true;

}