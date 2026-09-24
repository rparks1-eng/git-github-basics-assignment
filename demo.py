from user import User

user = User("John", "password", "john@some.com", "12/25/1999")

print(user.username)
print(user.password)
print(user)
print()
print(repr(user))
print()

user2 = User("John", "password", "john@some.com", "12/25/1999")

print(user == user2)
print(user.check_password("password"))
print(user.check_password("1234"))
print(user.get_age())
print()

user.username = "Jonathan"
print(user.username)
