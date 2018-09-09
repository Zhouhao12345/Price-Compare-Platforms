import settings
import json
import gitadapters

class DeserializeHook(object):

    def __init__(self):
        self.support_agents = {}
        for git_agent in settings.support_agents:
            self.support_agents[git_agent.get("agent_name")] = \
                git_agent.get("agent_func")


    @classmethod
    def deserialize(cls, **kwargs):
        agent = kwargs.get("agent", settings.support_agents[0])
        payload_str = kwargs.get("payload", "")
        payload_json = json.loads(payload_str)
        ser = cls()
        if agent not in ser.support_agents:
            raise Exception("Not support git agent!!")
        return getattr(gitadapters, ser.support_agents[agent])(payload_json)
