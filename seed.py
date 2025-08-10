import sqlite3
import faker
from random import randint, choice

NUM_OF_USERS = 10
NUM_OF_TASKS = 50

def generate_fake_data(user_count, task_count):
    fake_users = []
    fake_emails = []
    fake_tasks = []
    fake_descriptions = []

    fake = faker.Faker(locale='uk_UA')

    for _ in range(user_count):
        fake_users.append(fake.name())
        fake_emails.append(fake.email())

    for _ in range(task_count):
        fake_tasks.append(fake.sentence())
        fake_descriptions.append(fake.paragraph())

    return fake_users, fake_emails, fake_tasks, fake_descriptions


def prepare_data(users, emails, tasks, descriptions):
    for_users = []
    for_tasks = []

    for user in users:
        email = choice(emails)
        for_users.append((user, email, ))
        emails.remove(email)

    for task, description in zip(tasks, descriptions):
        for_tasks.append((task, description, randint(1, 3), randint(1, NUM_OF_USERS), ))

    return for_users, for_tasks

def insert_data(users, tasks):
    status = [('new',), ('in progress',), ('completed',)]
    sql_to_users = '''INSERT INTO users (fullname, email) VALUES (?, ?)'''
    sql_to_tasks = '''INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)'''
    sql_to_status = '''INSERT INTO status (name) VALUES (?)'''

    with sqlite3.connect('hw_db.db') as conn:
        cur = conn.cursor()
        cur.executemany(sql_to_status, status)
        cur.executemany(sql_to_users, users)
        cur.executemany(sql_to_tasks, tasks)

        conn.commit()

if __name__ == '__main__':
    users, tasks = prepare_data(*generate_fake_data(NUM_OF_USERS, NUM_OF_TASKS))
    insert_data(users, tasks)
