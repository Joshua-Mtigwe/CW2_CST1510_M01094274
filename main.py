import bcrypt

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
    with open("user_data.txt", "a") as f:
        f.write(f"{name},{hash}\n")
    print("User Successfully registered")


#user log in
def login_user():
    name = input("Please enter your username: >  ")
    password = input("Please enter your password: > ")
    with open("user_data.txt", "r") as f:
        users  = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(",")
        if name == user_name and is_hash_valid(password, user_hash):
            print("Logged in successfully")
            return True
    return False

print(register_user())
print(login_user())

