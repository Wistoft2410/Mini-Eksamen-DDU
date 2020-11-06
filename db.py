from peewee import *

USER = 'nejjyigpsyjcqc'
PASSWORD = 'f7345217f875c8a617f3aff8f2812e35a6f55ef9178bf177a9c1247978b2f223'
HOST = 'ec2-52-208-175-161.eu-west-1.compute.amazonaws.com'
PORT = 5432

DB = PostgresqlDatabase('dae8653ftqev6r', 
                                   user=USER, 
                                   password=PASSWORD, 
                                   host=HOST, 
                                   port=PORT)


class Class(Model):
    name = CharField()

    class Meta:
        database = DB


class Student(Model):
    username = CharField()
    #email = CharField()
    #password = CharField()
    #Class = ForeignKeyField(Class, backref="students")

    class Meta:
        database = DB

#class Question(Model):
#    questionText = CharField()
#    answer1 = CharField()
#    answer2 = CharField()
#    answer1true = BooleanField()

class simpleQuestion(Model):
    questionText = CharField()
    answer1 = CharField()
    answer2 = CharField()
    yesOrNo = BooleanField()

    class Meta:
        database = DB


class Teacher(Model):
    username = CharField()
    email = CharField()
    password = CharField()

    class Meta:
        database = DB


class teacherClassRelationship(Model):
    teacher = ForeignKeyField(Teacher)
    clazz = ForeignKeyField(Class)

    class Meta:
        database = DB


if __name__ == '__main__':
    DB.connect()
    DB.create_tables([simpleQuestion, Class, Student, Teacher, teacherClassRelationship], safe=True)
    DB.close()

