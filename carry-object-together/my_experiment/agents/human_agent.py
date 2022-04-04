from matrx.agents import HumanAgentBrain

from my_experiment.actions.custom_actions import CarryObjectTogether, DropObjectTogether

class CustomHumanAgent(HumanAgentBrain):
    """ Creates an Human Agent which is an agent that can be controlled by a human.

    For more extensive documentation on the functions below, see: 
    http://docs.matrx-software.com/en/master/sections/_generated_autodoc/matrx.agents.agent_types.human_agent.HumanAgentBrain.html
    """

    def __init__(self, memorize_for_ticks=None, max_carry_objects=3,
            grab_range=1, drop_range=1, door_range=1):
        """ Creates an Human Agent which is an agent that can be controlled by
        a human.

        """
        super().__init__(memorize_for_ticks=memorize_for_ticks)
        self.__max_carry_objects = max_carry_objects
        self.__grab_range = grab_range


    def filter_observations(self, state):
        """ Filters the world state before deciding on an action. """

        return state


    def decide_on_action(self, state, user_input):
        """ Contains the decision logic of the agent. """
        action = None
        action_kwargs = {"action_duration": 1}

        # if no keys were pressed, do nothing
        if user_input is None or user_input == []:
            return None, {}

        # take the latest pressed key and fetch the action
        # associated with that key
        pressed_keys = user_input[-1]
        action = self.key_action_map[pressed_keys]

        # if the user chose a grab action, choose an object within grab_range
        if action == CarryObjectTogether.__name__:
            # Set grab range
            action_kwargs['grab_range'] = self.__grab_range
            # Set max amount of objects
            action_kwargs['max_objects'] = self.__max_carry_objects

            # grab the closest victim
            obj = state.get_closest_with_property(props={"name": "Victim"})
            obj_id = obj[0]['obj_id'] if obj is not None else None
            action_kwargs['object_id'] = obj_id

        # If the user chose to drop an object in its inventory
        elif action == DropObjectTogether.__name__:
            pass 


        return action, action_kwargs

    
    def _set_messages(self, messages=None):
        # make sure we save the entire message and not only the content
        for mssg in messages:
            received_message = mssg
            self.received_messages.append(received_message)
