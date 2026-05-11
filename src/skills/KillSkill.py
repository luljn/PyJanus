from skills.Skill import Skill


class KillSkill(Skill):

    def __init__(self):
        super().__init__()

    def kill_me(self):
        print("Current agent killed")

    def execute(self):
        print("KillSkill executed")