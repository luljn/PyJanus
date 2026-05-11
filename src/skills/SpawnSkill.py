from abc import abstractmethod

from skills.Skill import Skill


class SpawnSkill(Skill):

    def __init__(self):
        super().__init__()

    def spawn(self, agent_type):
        print(f"Spawn agent type {agent_type}")

    def spawn_in_context(self, agent_type):
        print(f"Spawn in current context : {agent_type}")

    def spawn_with_id(self, agent_type, agent_id):
        print(f"Spawn agent {agent_type} with id {agent_id}")

    @abstractmethod
    def execute(self):
        print("SpawnSkill executed")