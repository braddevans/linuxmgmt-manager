import json
import uuid

from flask import Flask, request

from util.AgentManager import AgentManager

agent_manager = AgentManager()
agents = agent_manager.get_agents()


def add_agent_if_not_exists(hostname, obj):
    if get_agent_by_hostname(hostname) is None:
        agent_uuid = uuid.uuid4()
        print("Adding agent: {}".format(hostname))
        parsed_obj = {
            str(agent_uuid): {
                "uuid": str(agent_uuid),
                "hostname": hostname,
                "agent_ip": obj["agent_ip"],
                "agent_port": obj["agent_port"],
                "agent_type": obj["agent_type"],
                "agent_version": obj["agent_version"],
            }
        }
        agent_manager.add_to_agents(parsed_obj)
    return None


def get_agent_by_hostname(hostname):
    for agent in agents:
        print(agent)
        if agent.hostname == hostname:
            return agent
    return None


async def flaskWorker(logger):
    prefix = "flask_sub_process"
    logger.log_message(prefix, "Flask server started at port: 32451")
    app = Flask(__name__)

    # todo: on post return a uuid for quick agent updating
    @app.route("/api/agent/add", methods=['POST'])
    def add_agent():
        data = request.data.decode('utf-8')
        js_obj = json.loads(data)
        ret = add_agent_if_not_exists(js_obj["agent_hostname"])
        if not ret:
            logger.log_message(prefix, "Agent {} already exists with uuid: {}".format(js_obj["agent_hostname"],
                                                                                      get_agent_by_hostname(js_obj["agent_hostname"])))

        logger.log_message(prefix, data)
        return "<p>Hello, World!</p>"

    @app.route("/api/agent/update", methods=['POST'])
    def update_agent():
        data = request.data.decode('utf-8')
        logger.log_message(prefix, data)
        return "<p>Hello, World!</p>"

    app.run(host='0.0.0.0', port=32451, debug=False)
