import numpy as np 

from matrx.actions.action import Action, ActionResult
from matrx.actions.object_actions import GrabObject, DropObject
from matrx.utils import get_distance


class CarryObjectTogether(GrabObject):
    def __init__(self, duration_in_ticks=1):
        super().__init__(duration_in_ticks)

    def is_possible(self, grid_world, agent_id, world_state, **kwargs):
        grab_range = np.inf if 'grab_range' not in kwargs else kwargs['grab_range']
        other_agent = world_state[{"name": "Robot"}]
        obj_to_grab = world_state[kwargs["object_id"]]

        # check if the collaborating agent is close enough to the object as well 
        if get_distance(other_agent['location'], obj_to_grab['location']) > grab_range:
            return CarryTogetherResult(CarryTogetherResult.OTHER_TOO_FAR, False)
        
        # do the checks for grabbing a regular object as well
        return super().is_possible(grid_world, agent_id, world_state, **kwargs)
        
        

    def mutate(self, grid_world, agent_id, world_state, **kwargs):
        other_agent_id = world_state[{"name": "Robot"}]['obj_id']

        # if we want to change objects, we need to change the grid_world object 
        other_agent = grid_world.registered_agents[other_agent_id]
        agent = grid_world.registered_agents[agent_id]

        # make the other agent invisible 
        other_agent.change_property("visualize_opacity", 0)

        # change our image 
        agent.change_property("img_name", "carry_together.png")

        # pickup the object 
        return super().mutate(grid_world, agent_id, world_state, **kwargs)


class DropObjectTogether(DropObject):
    def __init__(self, duration_in_ticks=0):
        super().__init__(duration_in_ticks)

    def mutate(self, grid_world, agent_id, world_state, **kwargs):
        other_agent_id = world_state[{"name": "Robot"}]['obj_id']

        # if we want to change objects, we need to change the grid_world object 
        other_agent = grid_world.registered_agents[other_agent_id]
        agent = grid_world.registered_agents[agent_id]

        # teleport the other agent to our current position 
        other_agent.change_property("location", agent.properties['location'])

        # make the other agent visible again 
        other_agent.change_property("visualize_opacity", 1)

        # change the agent image back to default 
        agent.change_property("img_name", "human.png")

        # drop the actual object like we would do with a normal drop action 
        return super().mutate(grid_world, agent_id, world_state, **kwargs)


class CarryTogetherResult(ActionResult):
    PICKUP_SUCCESS = 'Successfully grabbed object together'
    OTHER_TOO_FAR = 'Failed to grab object. The other agent is too far from the object'
