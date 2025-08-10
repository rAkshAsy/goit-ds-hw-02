import email
import sqlite3
from random import randint
from faker import Faker
from colorama import init, Fore, Back

init(autoreset=True)

# SERVICE FUNCTIONS

def make_query_and_print(query, return_rows = True) -> None:
    with sqlite3.connect("hw_db.db") as conn:
        cur = conn.cursor()
        print(Fore.YELLOW + query)
        cur.execute(query)
        if return_rows:
            columns = [desc[0] for desc in cur.description]
            column_width = 30
            header = ''
            for col in columns:
                header += f'|{col:^{column_width}}|'
            line = '-' * len(header)
            print(line, header, line, sep='\n')
            for row in cur.fetchall():
                res_row = ''
                for i in range (len(row)):
                    if len(str(row[i])) > column_width:
                        abbr_str = row[i][:column_width-3] + '...'
                        res_row += f'|{abbr_str}|'
                    else:
                        cell = row[i] if row[i] else 'EMPTY'
                        res_row += f'|{cell:^{column_width}}|'
                print(res_row)
            print(line, '\n')
        else:
            print(f'Records changed or deleted: {cur.rowcount}', '\n')


# QUERY FUNCTIONS


def get_all_tasks_by_user(user_id):
    query = f'SELECT title, status_id, user_id FROM tasks WHERE user_id = {user_id}'
    print(Back.CYAN + Fore.BLACK + 'First QUERY')
    make_query_and_print(query)


def get_tasks_by_status(status_id):
    query = f'SELECT title, status_id, user_id FROM tasks WHERE status_id = {status_id}'
    print(Back.CYAN + Fore.BLACK + 'Second QUERY')
    make_query_and_print(query)


def update_task_status(task_id, status_id):
    query = f'UPDATE tasks SET status_id = {status_id} WHERE id = {task_id}'
    print(Back.CYAN + Fore.BLACK + 'Third QUERY')
    make_query_and_print(query, False)


def get_users_without_task():
    query = """SELECT id, fullname FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)"""
    print(Back.CYAN + Fore.BLACK + 'Fourth QUERY')
    make_query_and_print(query)


def insert_task_for_user(user_id):
    task_title = "Some new task"
    task_description = "Some description for new task"
    task_status_id = 1
    query = f'INSERT INTO tasks (title, description, status_id, user_id) VALUES ("{task_title}", "{task_description}", {task_status_id}, {user_id})'
    print(Back.CYAN + Fore.BLACK + 'Fifth QUERY')
    make_query_and_print(query, False)


def get_all_not_finished_tasks():
    query = """SELECT title, status_id, user_id FROM tasks WHERE status_id != 3"""
    print(Back.CYAN + Fore.BLACK + 'Sixth QUERY')
    make_query_and_print(query)


def delete_added_tasks():
    query = 'DELETE FROM tasks WHERE id IN (SELECT id FROM tasks WHERE title = "Some new task")'
    print(Back.CYAN + Fore.BLACK + 'Seventh QUERY')
    make_query_and_print(query, False)


def get_user_by_email():
    some_email = 'taras44@example.net'
    query = f'SELECT fullname, email FROM users WHERE email = "{some_email}"'
    print(Back.CYAN + Fore.BLACK + 'Eighth QUERY')
    make_query_and_print(query)


def change_name_by_id(user_id, new_name):
    query = f'UPDATE users SET fullname = "{new_name}" WHERE id = {user_id}'
    print(Back.CYAN + Fore.BLACK + 'Ninth QUERY')
    make_query_and_print(query, False)


def get_task_count_by_status():
    query = """SELECT s.name, COUNT(t.status_id) AS tasks_count
FROM tasks t 
LEFT JOIN status s ON s.id = t.status_id
GROUP BY s.name"""
    print(Back.CYAN + Fore.BLACK + 'Tenth QUERY')
    make_query_and_print(query)


def all_tasks_by_email_domain():
    query = """SELECT t.title, t.user_id, u.email AS email
FROM tasks t 
JOIN users u
WHERE u.email LIKE '%@example.com'"""
    print(Back.CYAN + Fore.BLACK + 'Eleventh QUERY')
    make_query_and_print(query)


def get_tasks_without_desc():
    query = """SELECT * FROM tasks WHERE description is NULL"""
    print(Back.CYAN + Fore.BLACK + 'Twelfth QUERY')
    make_query_and_print(query)


def get_users_and_tasks_by_status():
    query = """SELECT 
	u.fullname AS user,
	t.title AS task,
	s.name
FROM tasks t
INNER JOIN users u
ON u.id = t.user_id
JOIN status s
ON s.id = t.status_id 
WHERE s.name = 'in progress'"""
    print(Back.CYAN + Fore.BLACK + 'Thirteenth QUERY')
    make_query_and_print(query)


def get_count_tasks_by_user():
    query = """SELECT
	u.fullname AS user,
	COUNT(t.id)
FROM tasks t
LEFT JOIN users u
ON u.id = t.user_id
GROUP BY u.fullname"""
    print(Back.CYAN + Fore.BLACK + 'Fourteenth QUERY')
    make_query_and_print(query)


if __name__ == '__main__':
    # First QUERY
    user_id = randint(1, 10)
    get_all_tasks_by_user(user_id)

    # Second QUERY
    status_id = randint(1, 3)
    get_tasks_by_status(status_id)


    # Third QUERY
    task_id = randint(1, 50)
    status_id = randint(1, 3)
    update_task_status(task_id, status_id)

    # Fourth QUERY
    get_users_without_task()

    # Fifth QUERY
    user_id = randint(1, 9)
    insert_task_for_user(user_id)

    # Sixth QUERY
    get_all_not_finished_tasks()

    # Seventh QUERY
    delete_added_tasks()

    # Eighth QUERY
    get_user_by_email()

    # Ninth QUERY
    fake_data = Faker(locale='uk_UA')
    fake_name = fake_data.name()
    rand_id = randint(1, 10)
    change_name_by_id(rand_id, fake_name)

    # Tenth QUERY
    get_task_count_by_status()

    # Eleventh QUERY
    all_tasks_by_email_domain()

    # Twelfth QUERY
    get_tasks_without_desc()

    # Thirteenth QUERY
    get_users_and_tasks_by_status()

    # Fourteenth QUERY
    get_count_tasks_by_user()