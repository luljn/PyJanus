from skills.Skill import Skill


class EventSkill(Skill):

    def __init__(self):
        super().__init__()

    def emit(self, event):
        print(f"Emit event : {event}")

    def receive(self, event):
        print(f"Receive event : {event}")

    def wake(self):
        print("Wake up behavior")

    def execute(self):
        print("EventSkill executed")