import json
import os


class AgentManager:
    def __init__(self):
        self.agents_file = "data/agents.json"
        self.agents = {}
        self.refresh_agents()

    def get_agents(self):
        return self.agents

    def refresh_agents(self):
        with open(self.agents_file, "r") as f:
            self.agents = json.load(f)
        pass

    def add_to_agents(self, json_obj):
        self.agents.update(json_obj)
        with open(self.agents_file, "w") as f:
            json.dump(self.agents, f, indent=4)
        self.refresh_agents()
        pass

    def update_agent(self, obj):
        self.agents.update(obj)
        with open(self.agents_file, "w") as f:
            json.dump(self.agents, f, indent=4)
        self.refresh_agents()
        pass