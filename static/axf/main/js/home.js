
$(function () {

    initTopSwiper()

    initSwiperMenu()

})

function initTopSwiper() {
        // 初始化轮播
        var swiper = new Swiper("#topSwiper",{
        loop: true,
        autoplay: 3000,
            //分页器
        pagination: '.swiper-pagination',
    });
}

function initSwiperMenu() {
        var swiper = new Swiper("#swiperMenu",{
        // 三个循环轮播
        slidesPerView: 3,
    });
}