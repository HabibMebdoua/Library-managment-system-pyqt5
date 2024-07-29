from peewee import *
import datetime


db = SqliteDatabase('library.db')

class Catigory(Model):
    name = CharField(unique=True,default=('None'))
    parent_category = IntegerField(null=True)
    class Meta:
        database = db

class Publisher(Model):
    name = CharField()
    location = CharField(null=True)
    code = CharField()
    class Meta:
        database = db
    
class Authors(Model):
    name = CharField(default='None')
    email = CharField(null=True)
    class Meta:
        database = db


class Branch(Model):
    name = CharField(default='None')
    code = CharField(unique=True)
    location = CharField()
    class Meta:
        database = db

BOOK_STATUS = [
    ('New','New'),
    ('Used','Used'),
    ('Damaged','Damaged'),
]
class Books(Model):
    title = CharField(max_length=255 , unique=True)
    desc = TextField()
    catigory = ForeignKeyField(Catigory , backref='book_catigory',null=True)
    barcode = CharField()
    partorder = IntegerField(null=True)
    price = DecimalField(default=0)
    publisher = ForeignKeyField(Publisher,backref='book_bulisher')
    author = ForeignKeyField(Authors ,backref='book_author')
    img = CharField(null=True)
    status = CharField(choices=BOOK_STATUS)
    date = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

class Clients(Model):
    name  = CharField()
    email = CharField(null=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(unique=True)
   
    class Meta:
        database = db

class Employees(Model):
    name  = CharField(unique=True)
    email = CharField(null=True,unique=True)
    phone = CharField(null=True)
    date = DateTimeField(null=True)
    national_id = IntegerField(null=True,unique=True)
    preority = IntegerField(null=True)
    password = CharField()
    branch = IntegerField()
    class Meta:
        database = db

class EmployeePermissions(Model):
    employee_name = CharField()
    books_tab = BooleanField(default=False)
    clients_tab = BooleanField(default=False)
    dashboard_tab = BooleanField(default=False)
    history_tab = BooleanField(default=False)
    reports_tab = BooleanField(default=False)
    settings_tab = BooleanField(default=False)
    add_book = BooleanField(default=False)
    edit_book = BooleanField(default=False)
    delete_book = BooleanField(default=False)
    import_book = BooleanField(default=False)
    export_book = BooleanField(default=False)
    add_client = BooleanField(default=False)
    edit_client = BooleanField(default=False)
    delete_client = BooleanField(default=False)
    import_client = BooleanField(default=False)
    export_client = BooleanField(default=False)
    add_branch = BooleanField(default=False)
    add_publisher = BooleanField(default=False)
    add_author = BooleanField(default=False)
    add_catigory =BooleanField(default=False)
    add_employee = BooleanField(default=False)
   
    
    class Meta:
        database = db


PROCESS_TYPE = [
    ('Rent','Rent'),
    ('Retrive','Retrive'),
]
class DailyMovements(Model):
    #book = ForeignKeyField(Books , backref='d_book')
    book_barcode = IntegerField()
    #client = ForeignKeyField(Clients , backref='d_client')
    client_national_id = IntegerField()
    type = CharField(choices = PROCESS_TYPE) 
    date = DateField(null=True,default=datetime.datetime.now)
    branch = ForeignKeyField(Branch , backref='d_branch')
    book_from = DateField(null=True) 
    book_to = DateField(null=True) 
    employee = ForeignKeyField(Employees , backref='d_employee',null=True)
    class Meta:
        database = db

ACTIONS = [
    (1,'Login'),
    (2,'Update'),
    (3,'Create'),
    (4,'Delete'),
]

TABLE_CHOICES = [
    (1,'Books'),
    (2,'Clients'),
    (3,'Employee'),
    (4,'Catigory'),
    (5,'Branch'),
    (6,'Publisher'),
    (7,'Author'),
    (8,'Daily movements'),
]
class History(Model):
    #employee = ForeignKeyField(Employees , backref='hisoty_employee')
    employee = IntegerField()
    action = IntegerField
    db_table = IntegerField()
    date = DateTimeField()
    # branch = ForeignKeyField(Branch , backref='history_branch')
    branch = IntegerField()
    class Meta:
        database = db




db.connect()
db.create_tables([EmployeePermissions,Catigory,Publisher,Authors,Branch,Books,Clients,Employees,DailyMovements,History])