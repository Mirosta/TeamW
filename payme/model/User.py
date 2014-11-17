#Imports here
import entity

class User (Entity):
    'Represents a user in the system'

    def __init__(self, googleID, groups, friends):
        self.googleID = googleID
        self.groups = groups
        self.friends = friends
