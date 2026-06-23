import bcrypt
import sqlite3 

#hashing using bcrypt
def hash_generation(password):
    salt = bcrypt.gensalt()
    byte_psw = password.encode('utf-8')
    hashed_psw = bcrypt.hashpw(byte_psw, salt)

    return hashed_psw.decode('utf-8')

#Hash validation against the password
def is_hash_valid(password, hash):
    hash_ = hash.encode('utf-8')
    byte_psw = password.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid

#User registration
def register_user():
    name = input("Please enter your name: > ")
    password = input("Please enter your password: > ")
    hash = hash_generation(password)
    with open("DATA/user_data.txt", "a") as f:
        f.write(f"{name},{hash}\n")
    print("User Successfully registered")


#user log in
def login_user():
    name = input("Please enter your username: >  ")
    password = input("Please enter your password: > ")
    with open("DATA/user_data.txt", "r") as f:
        users  = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(",")
        if name == user_name and is_hash_valid(password, user_hash):
            print("Logged in successfully")
        else:
            print("Incorrect username or password! Please try again.")
            return True
    return False

#Main menu
def main():
    while True:
        print("Welcome to the User Authentication System")
        print("Please select an option: ")
        print("1. Register New User")
        print("2. Login Existing User")
        print("3. Exit")

        choice = input(": > ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Exiting User Authentication System. Goodbye!")
            break
        else:
            print("Option not recognised. Please try again.")

#user table
def create_user_table(conn):
    cur = conn.cursor()
    sql = ('''
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
    conn.execute(sql)
    conn.commit() 

#add user
def add_user(conn, name, hash):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    param = (name, hash)
    conn.execute(sql, param)
    conn.commit()

#user migration
def migration_user(conn):
    with open ('DATA/user_data.txt', "r") as f:
        users = f.readlines()

    for user in users:
        name, hash =user.strip().split(",")
        add_user(conn,name, hash)
                

#if __name__ == "__main__":
#    main()

#Connecting to a DATABASE
conn = sqlite3.connect('DATA/project_data.db')


conn.close()




