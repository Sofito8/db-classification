import mysql.connector
from api.models import Column, InformationType, Table
from mysql.connector import Error


def connect(database):
    """
    It connects to the database and returns a tuple of
    (connected, connection, error)

    The first element of the tuple is a boolean that
    indicates whether the connection was successful or not

    :param database: The database object that contains the
    connection information
    :return: A tuple of 3 values.
    """
    try:
        connection = mysql.connector.connect(
            host=database.host,
            port=database.port,
            user=database.username,
            passwd=database.password,
        )
        print("MySQL Database connection successful")
        if connection.is_connected():
            connected = True
            return connected, connection, None
    except Error as err:
        print(f"Error: '{err}'")
        connected = False
        return connected, None, err


def scanner(connection, database):
    """
    Gets all the tables and columns from de database to scan,
    and then creates the tables and columns in the database system_db

    :param connection: The connection object that you created in
    the previous section
    :param database: The name of the database you want to connect to
    """
    cursor = connection.cursor()
    cursor.execute("SELECT database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    for db in databases:
        if ('information_schema' in db or 'mysql' in db or
            'performance_schema' in db or 'sys' in db):
            continue
        else:
            cursor.execute("USE " + db[0])
            break
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    created_tables = Table.objects.filter(database=database)
    for table in tables:
        try:
            table_new = Table.objects.get(name=table[0], database=database)
        except Table.DoesNotExist:
            table_new = Table(name=table[0], database=database)
            table_new.save()
        cursor.execute("DESCRIBE " + table[0])
        columns = cursor.fetchall()
        for column in columns:
            try:
                column_new = Column.objects.get(name=column[0],
                                                table=table_new)
            except Column.DoesNotExist:
                column_new = Column(name=column[0], table=table_new)
            types = InformationType.objects.exclude(name='N/A')
            for type in types:
                if type.subString.lower() in column[0].lower():
                    column_new.informationType = type
                    break
            if column_new.informationType is None:
                column_new.informationType = InformationType.objects.get(name='N/A')
            column_new.save()

    """
    Search for the tables that are not in the database anymore
    and delete them
    """
    for created_table in created_tables:
        for table in tables:
            if created_table.name == table[0]:
                no_drop = True
                break
            else:
                no_drop = False
        if no_drop:
            continue
        else:
            columns_of_table = Column.objects.filter(table=created_table)
            for column in columns_of_table:
                column.delete()
            created_table.delete()

    cursor.close()
    connection.close()
    print("MySQL connection is closed")
