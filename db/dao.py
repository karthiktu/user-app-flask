from hashlib import md5
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.exc import NoResultFound

Base = declarative_base()

class User(Base, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id', 'name', 'displayName', 'email', 'phone')

    id = Column(Integer, primary_key=True)
    name =  Column(String(50), unique=True)
    displayName =  Column(String(100))
    email = Column(String(100))
    phone = Column(String(100))
    password = Column(String(100))
    roles = relationship('Role', secondary='user_roles')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)


class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))


engine = create_engine('sqlite:///myexample.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

admin_role = Role(name='Admin')

user1 = User()
user1.displayName= 'Karthik TU'
user1.email = 'tukarthik@gmail.com'
user1.name = 'tukarthik'
user1.phone = '9894682558'
user1.password = md5(b'123456').hexdigest()

user1.roles = [admin_role]

def getAllUsers():
    with Session() as session:
        return {'users' : [x.to_dict() for x in session.query(User).all() ]}

def getUser(id):
    with Session() as session:
        return session.query(User).filter(User.id == id).one().to_dict()

def getUserByName(name):
    with Session() as session:
        return session.query(User).filter(User.name == name).one().to_dict()


def createUser(name, displayName, email, phone, password):
    user1 = User()
    user1.displayName= displayName
    user1.email = email
    user1.name = name
    user1.phone = phone
    user1.password = password
    with Session() as session:
        session.add(user1)
        session.commit()
        return user1.to_dict()

def updateUser(name, displayName, email, phone):
    with Session() as session:
        try:
            user = session.query(User).filter(User.name == name).one()
            if displayName is not None:
                user.displayName = displayName
            if email is not None:
                user.email = email
            if phone is not None:
                user.phone = phone
            session.commit()
            return user.to_dict()
        except Exception as e:
            return str(e)

def deleteUser(id):
    with Session() as session:
        try:
            session.query(User).filter(User.id == id).delete()
            session.commit()
            return '', 200
        except Exception as e:
            return str(e), 500

def getPasswordRolesForUser(username):
    with Session() as session:
        try:
            user = session.query(User).filter(User.name == username.decode("utf-8") ).one()
        except NoResultFound:
            return None, None
        return user.password, [ r.name for r in user.roles ]


with Session() as session:
    session.add(admin_role)
    session.add(user1)
    session.commit()





