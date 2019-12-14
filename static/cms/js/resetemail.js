$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if(!email){
            xtalert.alertInfoToast('请输入邮箱');
        }
        zlajax.get({
           'url': '/cms/email_captcha/',
            'data': {'email':email},
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('邮件已发送成功！请注意查收！');
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail':function (error) {
                xtalert.alertNetworkError();
            }
        });
    });
});


$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜，修改邮箱成功！')
                }else{
                    xtalert.alertInfo(data['message']);
                }
            },
            'fail':function (data) {
                xtalert.alertNetworkError();
            }
        });

    });
});


// 我是测试代码