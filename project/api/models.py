from django.db import models

# Create your models here.


class Database(models.Model):
    idDatabase = models.AutoField(primary_key=True)
    host = models.CharField(max_length=15)
    port = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)


class Record(models.Model):
    idRecord = models.AutoField(primary_key=True)
    database = models.ForeignKey(Database, on_delete=models.DO_NOTHING)
    status = models.BooleanField(null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)


class Table(models.Model):
    idTable = models.AutoField(primary_key=True)
    database = models.ForeignKey(Database, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)


class Column(models.Model):
    idColumn = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    informationType = models.ForeignKey('InformationType',
                                        on_delete=models.DO_NOTHING, null=True)


class InformationType(models.Model):
    idInformationType = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    subString = models.CharField(max_length=50, null=True)
