from api.models import Column, Database, InformationType, Record, Table
from rest_framework import serializers


class DatabaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Database
        fields = ['idDatabase', 'host', 'port', 'username', 'password']


class RecordSerializer(serializers.ModelSerializer):
    database = DatabaseSerializer()

    class Meta:
        model = Record
        fields = ['idRecord', 'database', 'status', 'date']


class TableSerializer(serializers.ModelSerializer):
    database = DatabaseSerializer()

    class Meta:
        model = Table
        fields = ['idTable', 'database', 'name']


class InformationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationType
        fields = ['idInformationType', 'name', 'subString']


class ColumnSerializer(serializers.ModelSerializer):
    table = TableSerializer()
    informationType = InformationTypeSerializer()

    class Meta:
        model = Column
        fields = ['idColumn', 'table', 'name', 'informationType']
