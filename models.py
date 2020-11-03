from peewee import *


class Class(Model):
    name = CharField()


class Student(Model):
    username = CharField()
    email = CharField()
    password = CharField()
    Class = ForeignKeyField(Class, backref="students")


class Teacher(Model):
    username = CharField()
    email = CharField()
    password = CharField()


class teacherClassRelationship(Model):
    teacher = ForeignKeyField(Teacher)
    clazz = ForeignKeyField(Class)

