from entity import Entity
#Group is made by passing a list of users. When addDebt is called, it will add 'debt' passed to every user in the group.

class Group (Entity):

    def __init__(self, name, users):
        self.groupName = name
        self.users = users

    def addUser(self, user):
        self.users.append(user)

    def renameGroup(self, name):
        self.groupName = name

    def addDebt(self, debt):
        for user in self.users:
            user.addDebt(debt)


