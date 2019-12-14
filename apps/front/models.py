from exts import db
from datetime import datetime
import shortuuid
import enum
from werkzeug.security import generate_password_hash,check_password_hash

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)   # pip install shortuuid 不能再使用自增长
    telephone = db.Column(db.String(100),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signatuer = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs): #password __init__
        if 'password' in kwargs:
            self.password = kwargs.get('password') #其他父类来操作
            kwargs.pop('password')
        super(FrontUser, self).__init__(*args,**kwargs)


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self,newpwd):
        result = check_password_hash(self._password,newpwd)
        return result