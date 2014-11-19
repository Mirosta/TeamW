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

    #TODO: Do some division on the amount of debt to add
    def addDebt(self, debt):
        for user in self.users:
            user.addDebt(debt)

    #TODO: Implement methods
    def getDebtAmount(self):
        return super(Group, self).getDebtAmount()

    def getNetAmounts(self):
        return super(Group, self).getNetAmounts()

    def getNetCreditAmount(self):
        return super(Group, self).getNetCreditAmount()

    def getCredits(self):
        return super(Group, self).getCredits()

    def getDebtsAmounts(self):
        return super(Group, self).getDebtsAmounts()

    def getCreditsAmount(self):
        return super(Group, self).getCreditsAmount()

    def getDebts(self):
        super(Group, self).getDebts()

    def getNetAmount(self):
        return super(Group, self).getNetAmount()


