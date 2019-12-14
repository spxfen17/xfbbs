from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from xfbbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel,PostModel

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission
FrontUser = front_models.FrontUser

app = create_app()
manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)



@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(password,username,email):
    user = CMSUser(password=password,username=username,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

@manager.command
def create_role():
    #1.访问者
    visitor = CMSRole(name='访问者',desc='只能访问相关信息，不能修改')
    visitor.permissions = CMSPermission.VISITOR
    #2.运营人员（修改个人信息，管理帖子，管理评论，管理前台用户）)
    operator = CMSRole(name='运营',desc='管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.FRONTUSER|CMSPermission.COMMENTER
    #3.管理员（拥有所有权限）
    admin = CMSRole(name='管理者',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.CMSUSER|CMSPermission.BOARDER|CMSPermission.FRONTUSER
    # 4.开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s'%role)
    else:
        print("%s邮箱没有这个用户!"%email)

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()



#测试代码
@manager.command
def create_test_post():
    for x in range(1,20):
        title = 'flask%s' % x
        content = '内容%s' % x
        board = BoardModel.query.filter_by(id=12).first()
        post = PostModel(title=title,content=content)
        post.board = board
        db.session.add(post)
        db.session.commit()
    print("恭喜！测试帖子添加成功")

#测试代码
@manager.command
def test_permission():
    user = CMSUser.query.filter_by(id = 2).first()
    if user.has_permission(CMSPermission.VISITOR):
        print('有')
    else:
        print('无')

if __name__ == '__main__':
    manager.run()
