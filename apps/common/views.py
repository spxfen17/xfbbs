from flask import Blueprint,request,make_response,jsonify
from utils import restful,xfcache
from exts import alidayu
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from io import BytesIO
import qiniu


bp = Blueprint('common',__name__,url_prefix='/c')

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码！')
#     # 生成4位验证码
#     captcha = Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         # return restful.params_error(message='短信验证码发送错误！')
#         return restful.success()


# 加密版
# telephone
# timestamp
# md5(timestamp+telephone+salt)
@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        if alidayu.send_sms(telephone,code=captcha):
            xfcache.set(telephone,captcha)
            return restful.success()
        else:
            # return restful.params_error()
            return restful.success()
    else:
        return restful.params_error(message='参数错误！')

#图形验证码
@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_grap_captcha()
    xfcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png') #指定格式为png
    out.seek(0)           #把指针指到开始位置
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

@bp.route('/uptoken/')
def uptoken():
    access_key = 'L5ghsvMRi2IO_enJO2DB-jIUWqC-2iX9kVcQHOXl'
    secret_key = 'Vv4iWYAA0DffsCJSzpmD4SN-bFKqzX84TwTsXPEt'
    q = qiniu.Auth(access_key,secret_key)

    bucket_name = 'xfbbs'
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken':token})
