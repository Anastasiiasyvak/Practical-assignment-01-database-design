import mysql.connector
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Connection settings
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')
DATABASE = os.getenv('database')


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


def read_uncommited_demo():
    """
    Shows how READ UNCOMMITED isolation level works.
    Shows dirty read.
    :return: void
    """
    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1: Read Uncommitted
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor1.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")

        # Transaction 2: Read Uncommitted
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ UNCOMMITTED')
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_dirty_read = cursor2.fetchone()[0]

        print(f"Dirty Read (READ UNCOMMITTED): Alice's balance = {balance_dirty_read}")

        print(f"Transaction 1 rollback(): {datetime.now()}")
        connection1.rollback()
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        rollback_read = cursor1.fetchone()[0]
        print(f"Balance after rollback: {rollback_read}")

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_after_commit = cursor2.fetchone()[0]
        print(f"Balance after commit: {balance_after_commit}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


def read_committed_demo():

    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1: Read Committed
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")

        # Transaction 2: Read Committed
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_committed_read = cursor2.fetchone()[0]

        print(f"Read Committed (READ COMMITTED): Alice's balance = {balance_committed_read}")

        print(f"Transaction 1 rollback(): {datetime.now()}")
        connection1.rollback()
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        rollback_read = cursor1.fetchone()[0]
        print(f"Balance after rollback: {rollback_read}")

        print(f"Transaction 2 commit(): {datetime.now()}")
        connection2.commit()
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_after_commit = cursor2.fetchone()[0]
        print(f"Balance after commit: {balance_after_commit}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


def repeatable_read_demo():

    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1:
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='REPEATABLE READ')
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance = cursor1.fetchone()[0]
        print(f"Transaction 1 reads Alice's balance = {balance}")

        # Transaction 2:
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='REPEATABLE READ')
        cursor2.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")
        connection2.commit()

        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_after = cursor1.fetchone()[0]
        print(f"Transaction 1 reads Alice's balance after Transaction 2 commits = {balance_after}")

        print(f"Transaction 1 commit(): {datetime.now()}")
        connection1.commit()
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_after_commit = cursor1.fetchone()[0]
        print(f"Balance after commit: {balance_after_commit}")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


def non_repeatable_read_demo():

    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1:
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='READ COMMITTED')
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_before = cursor1.fetchone()[0]
        print(f"Transaction 1 reads Alice's balance = {balance_before}")

        # Transaction 2:
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='READ COMMITTED')
        cursor2.execute("UPDATE accounts SET balance = 9999 WHERE name = 'Alice'")
        connection2.commit()

        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice'")
        balance_after = cursor1.fetchone()[0]
        print(f"Transaction 1 reads Alice's balance after Transaction 2 commits = {balance_after}")

        print(f"Transaction 1 commit(): {datetime.now()}")
        connection1.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


def deadlock_demo():

    connection1 = create_connection()
    connection2 = create_connection()

    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        # Transaction 1:
        print(f"Transaction 1 started: {datetime.now()}")
        connection1.start_transaction(isolation_level='REPEATABLE READ')
        cursor1.execute("SELECT balance FROM accounts WHERE name = 'Alice' FOR UPDATE")

        # Transaction 2:
        print(f"Transaction 2 started: {datetime.now()}")
        connection2.start_transaction(isolation_level='REPEATABLE READ')
        cursor2.execute("SELECT balance FROM accounts WHERE name = 'Bob' FOR UPDATE")

        cursor1.execute("UPDATE accounts SET balance = 4000 WHERE name = 'Alice'")
        connection1.commit()

        cursor2.execute("UPDATE accounts SET balance = 4000 WHERE name = 'Bob'")
        connection2.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if connection1 and connection1.is_connected():
            connection1.close()
        if cursor2:
            cursor2.close()
        if connection2 and connection2.is_connected():
            connection2.close()


if __name__ == "__main__":
    # print("----read_uncommited_demo----")
    # read_uncommited_demo()
    # print("-read_commited_demo-")
    # read_committed_demo()
    # print("-repeatable_read_demo-")
    # repeatable_read_demo()
    # print("-non_repeatable_read_demo-")
    # non_repeatable_read_demo()
    print("-deadlock_demo-")
    deadlock_demo()


