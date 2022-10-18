# Create your views here.
from api.functions import connect, scanner
from api.models import Column, Database, InformationType, Record, Table
from api.serializer import (ColumnSerializer, DatabaseSerializer,
                            InformationTypeSerializer, RecordSerializer,
                            TableSerializer)
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):
    """
    It takes a request and returns a response

    :param request: HttpRequest object
    :return: HttpResponse
    """
    return HttpResponse("Hello, world. You're at the polls index.adasdas")


class DatabaseView(APIView):
    def get(self, request):
        """
        It gets all the databases from the database and returns them
        in a JSON format

        :param request: The request object
        :return: A list of all the databases in the database.
        """
        databases = Database.objects.all()
        if databases.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "No elements found"})
        serializer = DatabaseSerializer(databases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        If the database exists, return 409, otherwise create it and return 201

        :param request: The request object
        :return: The id of the database that was created.
        """
        try:
            database = Database.objects.get(host=request.data['host'],
                                            port=request.data['port'],
                                            username=request.data['username'],
                                            password=request.data['password'])
        except Database.DoesNotExist:
            serializer = DatabaseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data['idDatabase'],
                                status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_409_CONFLICT,
                        data={"message": "The database already exists. Id: "
                              + str(database.idDatabase)})


class InformationTypeView(APIView):
    def get(self, request):
        """
        It gets all the information types from the database and returns them
        in a serialized form
        :return: A list of all the information types in the database.
        """
        information_types = InformationType.objects.all()
        if information_types.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "No elements found"})
        serializer = InformationTypeSerializer(information_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        If the information type already exists, return a 409 error, otherwise,
        if the serializer is valid,
        save it and return the id of the information type,
        otherwise return the serializer errors

        :param request: The request object
        :return: The id of the information type created.
        """
        serializer = InformationTypeSerializer(data=request.data)
        try:
            existent = InformationType.objects.get(name=request.data['name'])
        except InformationType.DoesNotExist:
            existent = None
        if existent is not None:
            return Response(status=status.HTTP_409_CONFLICT,
                            data={"message": "Information type already exists"}
                            )
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data['idInformationType'],
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        It deletes an information type and all of its columns

        :param request: The request object
        :param id: The id of the information type to be deleted
        :return: The information type is being returned.
        """

        try:
            information_type = InformationType.objects.get(
                            idInformationType=id)
            if information_type == InformationType.objects.get(name="N/A"):
                return Response(status=status.HTTP_409_CONFLICT,
                                data={"message": "You can't delete the N/A "
                                      + "information type"})
        except InformationType.DoesNotExist:
            information_type = None
        if information_type is not None:
            columns = Column.objects.filter(informationType=information_type)
            for column in columns:
                column.informationType = InformationType.objects.get(name="N/A")
                column.save()
            information_type.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Information type not found"})


class RecordView(APIView):
    def get(self, request):
        """
        It gets all the records from the database, serializes them,
        and returns them as a response

        :param request: The request object
        :return: A list of all the records in the database.
        """
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DatabaseScanView(APIView):
    def get(self, request, id):
        """
        Get all the tables and columns from a database,
        and then pass them to the template.

        :param request: The request object
        :param id: the id of the database
        :return: The tables and columns of the database.
        """
        try:
            database = Database.objects.get(idDatabase=id)
        except Database.DoesNotExist:
            database = None
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"message": "Database not found"})
        if database is not None:
            tables = Table.objects.filter(database=database)
            tables_serializer = TableSerializer(tables, many=True)
            columns = Column.objects.filter(table__database=database)
            columns_serializer = ColumnSerializer(columns, many=True)
            return render(request, 'database_scan.html',
                          {'tables': tables_serializer.data,
                           'columns': columns_serializer.data},
                          status=status.HTTP_200_OK)

    def post(self, request, id):
        """
        It takes a database object, connects to it, and then scans it

        :param request: The request object
        :param id: The id of the database to be scanned
        :return: The response is a JSON object with a message and
        a status code.
        """
        try:
            database = Database.objects.get(idDatabase=id)
        except Database.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"No database found with that id"})

        connected, connection, err = connect(database)
        record = Record()
        record.database = database
        record.status = connected
        record.save()

        if connected is True:
            scanner(connection, database)
            return Response(status=status.HTTP_200_OK,
                            data={"message": "Successfully scanned"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "Connection to database failed. "
                                  f"Error: '{err}'"})
