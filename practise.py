#连接数据库：
from flask import render_template
#import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand


#pymysql.install_as_MySQLdb() #这个和 import pymysql 不写的话，下面的 mysql 替换成 mysql+pymysql 即可

app = Flask(__name__)  #定义 app 对象 是 Flask 类定义的对象
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://vigoryu:123456@119.45.191.60:3306/work'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#每次请求结束后都会自动提交数据库中的变动
db = SQLAlchemy(app) #db 对象是 SQLAlchemy 类的实例，且把app 传过去了，表示程序使用的数据库
manger = Manager(app)  # 将 app 传给Manger 并且赋值给了 manger, 用装饰器 @manger.command 去使底下定义的东西能成为一个命令去执行
# 初始化 db 迁移工具
migrate = Migrate(app,db) # 和app绑定是肯定的，因为是做迁移肯定是要数据库相关的
manger.add_command('db',MigrateCommand) # 这一步是增加一个新的命令是因为要操作数据，这个命令叫 db
# 创建了一个迁移的命令 db 然后这个db 后面还有好多 命令 骚操作

#模型定义
class Student(db.Model):
    '''User 模型'''
    __tablename__ = 'student_2'  # 表的名字
    # 定义表中的字段，与直接在数据库中定义有所区别
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False,unique=True)
    gender = db.Column(db.Enum('男','女','保密'))
    city = db.Column(db.String(10),nullable=False)
    birthday = db.Column(db.Date,default='1990-08-09')
    money = db.Column(db.Float)

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.Enum('男', '女', '保密'))
    city = db.Column(db.String(10), nullable=False)

@app.route('/')
def home():
    user = Student.query.all()  # 从数据库中取数据
    return render_template('home.html',user=user)

@manger.command
def add_table():
    '''添加表结构'''
    db.create_all()

@manger.command
def add_data():
    '''添加初始数据'''
    u1 = Student(name='tom',gender='男',city='北京',birthday='1989-03-04',money=888)
    u2 = Student(name='lucy', gender='女', city='上海',
                 birthday='1995-9-12',  money=736)
    u3 = Student(name='jack', gender='男', city='武汉',
                 birthday='1998-5-14',money=8632)
    u4 = Student(name='bob', gender='男', city='苏州',
                 birthday='1994-3-9', money=1986)
    u5 = Student(name='lily', gender='女', city='南京',
                 birthday='1992-3-17', )
    u6 = Student(name='eva', gender='女', city='芜湖',
                 birthday='1987-7-28',  money=862)
    u7 = Student(name='alex', gender='男', city='成都',
                 birthday='1974-2-5', )
    u8 = Student(name='jam', gender='男', city='太原',
                 birthday='1999-5-26', money=871)
    u9 = Student(name='rob', gender='男', city='青岛',
                 birthday='1997-5-9')
    u10 = Student(name='ella', gender='女', city='大连',
                  birthday='1999-9-7', money=8128)
    db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,u9,u10])
    db.session.commit()


# 创建数据表
if __name__ == '__main__':
    manger.run()

