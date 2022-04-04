from matrx.agents.agent_utils.navigator import Navigator
from matrx.agents.agent_utils.state_tracker import StateTracker
from matrx.agents import AgentBrain
from matrx.messages import Message


class CustomAgent(AgentBrain):
    """ An artificial agent whose behaviour can be programmed to be, for example, (semi-)autonomous.
    
    For more extensive documentation on the functions below, see: 
    http://docs.matrx-software.com/en/master/sections/_generated_autodoc/matrx.agents.agent_brain.AgentBrain.html#matrx.agents.agent_brain.AgentBrain
    """


    def __init__(self, **kwargs):
        """ Creates an agent brain to move along a set of waypoints.
        """
        super().__init__(**kwargs)
        

    def filter_observations(self, state):
        """ Filters the world state before deciding on an action. """
        return state


    def decide_on_action(self, state):
        """ Contains the decision logic of the agent. """
        action = None
        action_kwargs = {"action_duration": 1}

        return action, action_kwargs

    
    def _set_messages(self, messages=None):
        # make sure we save the entire message and not only the content
        for mssg in messages:
            received_message = mssg
            self.received_messages.append(received_message)
