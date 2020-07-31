//以post方式请求(csrf)
//以post方式请求(csrf)
function CharMode(iN) {
    if (iN >= 48 && iN <= 57) //数字
        return 1;
    if (iN >= 65 && iN <= 90) //大写字母
        return 2;
    if (iN >= 97 && iN <= 122) //小写
        return 4;
    else
        return 8; //特殊字符
}

//bitTotal函数
//计算出当前密码当中一共有多少种模式
function bitTotal(num) {
    modes = 0;
    for (i = 0; i < 4; i++) {
        if (num & 1) modes++;
        num >>>= 1;
    }
    return modes;
}

//checkStrong函数
//返回密码的强度级别
function checkStrong(sPW) {
    if (sPW.length <= 4)
        return 0; //密码太短
    Modes = 0;
    for (i = 0; i < sPW.length; i++) {
        //测试每一个字符的类别并统计一共有多少种模式.
        Modes |= CharMode(sPW.charCodeAt(i));
    }
    return bitTotal(Modes);
}

function pwStrength1() {    //光标不在输入框时，执行下面动作
    $('.passwordtishi').hide()  //隐藏安全程度提示
}

function pwStrength(pwd) {    //监听键盘事件
    O_color = "#eeeeee";
    L_color = "#FF0000";
    M_color = "#FF9900";
    H_color = "#33CC00";
    if (pwd == null || pwd == "") {   //如果键盘输入为空，或者未输入
        Lcolor = Mcolor = Hcolor = O_color;
        $('.passwordtishi').hide()
    } else {  //如果输入值
        $('.passwordtishi').show();
        // 计算输入密码的强度
        S_level = checkStrong(pwd);
        switch (S_level) {
            case 0:
                Lcolor = Mcolor = Hcolor = O_color;
            case 1:
                Lcolor = L_color;
                Mcolor = Hcolor = O_color;
                break;
            case 2:
                Lcolor = O_color;
                Mcolor = M_color
                Hcolor = O_color;
                break;
            default:
                Lcolor = Mcolor = O_color;
                Hcolor = H_color;
        }
    }
    //设置安全提示框背景颜色
    document.getElementById("strength_L").style.background = Lcolor;
    document.getElementById("strength_M").style.background = Mcolor;
    document.getElementById("strength_H").style.background = Hcolor;
    return;
}

function time(o) {
    if (wait == 0) {
        o.removeAttribute("disabled");
        $("#btnemail").css("background", "dodgerblue");
        o.value = "发送验证码到邮箱";
        wait = 60;
    } else {
        o.setAttribute("disabled", true);
        $("#btnemail").css("background", "#A9A9A9");
        o.value = wait + "秒后可以重新发送";
        wait--;
        setTimeout(function () {
                time(o)
            },
            1000)
    }
}

