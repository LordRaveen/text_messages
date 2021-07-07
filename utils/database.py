from utils.DatabaseConnection import DatabaseConnection


def create_table():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS members(identity integer, name text, phone text primary key, '
                       'level text)')
        print('Table Created')


message = ''


def save(name, phone, position):
    global message
    create_table()
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        print(name, phone, position)
        if name != '' and phone != '':
            try:
                identity = len(member_list()) + 1
                cursor.execute('INSERT INTO members VALUES(?,?,?,?)', (identity, name, phone, position))
                message = 'Record saved successfully'
                print(message)
            except Exception:
                message = 'An Error Occurred!'
        else:
            message = 'Please Enter all fields'
            print(message)
    print(member_list())
    return message


def member_list():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM members')
        students = [[row[0], row[1], row[2], row[3]] for row in cursor.fetchall()]
        print(len(students))
    return students


def reset_fields(fields):
    for i in fields:
        i.delete(0, 1000)


def delete(identity):
    try:
        with DatabaseConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'DELETE FROM members WHERE identity = ?', (identity,))
            return True
    except Exception as ex:
        print('Could not delete', ex)


def update():
    pass


def fetch_all():
    pass


def delete_all():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor .execute('DELETE FROM members')
    print(member_list())
