class User(object):
    username = ""
    password = ""
    fullName = ""

    def __init__(self, username, password, fullName):
        self.username = username
        self.password = password
        self.fullName = fullName

    def to_string(self):
        return "Username: "+self.username + " Password: "+self.password+" FullName: "+self.fullName
