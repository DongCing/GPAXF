// 获取屏幕尺寸,将底层单位设置成屏幕的十分之一
// 注释后,项目效果无变化,实用效果存疑
$( function(){
    document.documentElement.style.fontSize = innerWidth / 10 + "px";
})