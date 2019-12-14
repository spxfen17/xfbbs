from wtforms import StringField,IntegerField
from wtforms.validators import Email,Length,InputRequired,EqualTo
from ..forms import BaseForm
from utils import xfcache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired('请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确的格式密码')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确的旧格式密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确的新格式密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='新旧密码不一样请重新输入！')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email('请输入正确的邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = xfcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("邮箱验证码错误！")

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("不能修改为当前使用的邮箱！")

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称!')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图链接!')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接!')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级!')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！'),Length(2,15,message='长度应在2-15个字符之间')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[IntegerField('请输入板块的id！')])














