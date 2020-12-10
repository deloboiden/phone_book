import sys
from PyQt4.QtGui import QApplication
import mysql.connector
from EnterWindow import EnterWindow
import argparse

def Connect(database, host, port, user, password):
    try:
        connection = mysql.connector.connect(database=database, host=host, port=port,
                                             user=user, password=password)
        if connection.is_connected():
            print('Connected to MariaDB database')
    except Exception as e:
        print("Error connecting to MariaDB Platform:", e)
        sys.exit(1)
    try:
        cursor = connection.cursor()
        cursor.execute("""CREATE Table IF NOT EXISTS logins (id serial primary key,
                                                             login varchar(100) not null,
                                                             password_hash varchar(100) not null,
                                                             birth_date date not null,
                                                             remembered bit not null default FALSE)""")
        cursor.execute("""CREATE Table IF NOT EXISTS records (id serial primary key,
                                                              login_id integer not null,
                                                              name varchar(100) not null,
                                                              telephone_number varchar(100) not null,
                                                              birth_date date not null)""")
        cursor.close()
        connection.commit()
    except Exception as e:
        print("Error while execute query:", e)
        sys.exit(1)
    return connection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='creds to database')
    parser.add_argument('database', type=str, help='Name of MariaDB batabase')
    parser.add_argument('host', type=str, help='Host of MariaDB batabase')
    parser.add_argument('port', type=int, help='Portt of MariaDB batabase')
    parser.add_argument('user', type=str, help='Username of MariaDB batabase')
    parser.add_argument('password', type=str, help='Password for username')
    args = parser.parse_args()
    connection = Connect(args.database, args.host, args.port, args.user, args.password)
    app = QApplication(sys.argv)
    ex = EnterWindow(connection)
    sys.exit(app.exec_())
