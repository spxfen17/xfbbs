from flask import (
    Blueprint,
    render_template,
    views,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm
)
from .models import CMSUser,CMSPermission
from ..models import BannerModel,BoardModel
from .decorators import login_required,permission_required
import config
from exts import db,mail
from utils import restful,xfcache
from flask_mail import Message
import string,random


bp = Blueprint('cms',__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    #/email_captcha/?email=xxx.qq@.com
    email = request.args.get('email')
    if not email:
        return restful.params_error("请传递邮箱参数")
    source = list(string.ascii_letters) #(a-z,A-Z)
    # source.extend([0,1,2,3,4,5,6,7,8,9])
    captcha = "".join(random.sample(source,6))
    #给这个邮箱发送邮件
    message = Message("xfbbs论坛邮箱验证码",recipients=[email],body="您的邮箱验证码是：%s"%captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    xfcache.set(email,captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')




# 板块管理的添加编辑删除
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards':board_models
    }
    return render_template('cms/cms_boards.html',**context)


@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个板块！")
    else:
        return restful.params_error(message=form.get_error())



@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message="请输入板块的id！")

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message="没有这个板块！")

    db.session.delete(board)
    db.session.commit()
    return restful.success()





# 轮播图的添加编辑删除
@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个轮播图！")
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请输入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()

class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或者密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)


class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))




