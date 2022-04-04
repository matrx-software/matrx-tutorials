import itertools
from collections import OrderedDict
from itertools import product
import os

# MATRX stuff
from matrx import WorldBuilder, utils
import numpy as np
from matrx.actions import MoveNorth, OpenDoorAction, CloseDoorAction
from matrx.actions.move_actions import MoveEast, MoveSouth, MoveWest
from matrx.grid_world import GridWorld, DropObject, GrabObject, AgentBody
from matrx.objects import EnvObject, SquareBlock
from matrx.world_builder import RandomProperty
from matrx.goals import WorldGoal, CollectionGoal
from matrx_visualizer import visualization_server

# custom code
from my_experiment.agents.agent import CustomAgent
from my_experiment.agents.human_agent import CustomHumanAgent
from my_experiment.actions.custom_actions import CarryObjectTogether, DropObjectTogether

# Some general settings
tick_duration = 1 / 10  # 0.1s or lower tick duration recommended, to keep the human agent responsive
random_seed = 1
verbose = False
key_action_map = {  # Controls for the human agent
    'w': MoveNorth.__name__,
    'd': MoveEast.__name__,
    's': MoveSouth.__name__,
    'a': MoveWest.__name__,
    'q': CarryObjectTogether.__name__,
    'e': DropObjectTogether.__name__
}


def create_builder():

    # Set numpy's random generator
    np.random.seed(random_seed)

    # The world size
    world_size = [10, 10]

    # Create our world builder
    builder = WorldBuilder(shape=world_size, tick_duration=tick_duration, random_seed=random_seed, run_matrx_api=True,
                           run_matrx_visualizer=True, verbose=verbose, visualization_bg_clr="#f0f0f0",
                           visualization_bg_img="")

    # create objects 
    builder.add_object([5,5], name="Victim", is_traversable=True, is_movable=True, img_name="victim_lightlywounded.png")

    # Now we add our agents as part of the same team
    team_name = "Team Awesome"

    # Custom human agent
    brain = CustomHumanAgent(max_carry_objects=1)
    builder.add_human_agent([3, 3], brain, name="Human", key_action_map=key_action_map, is_traversable=True, img_name="human.png")

    # Custom artificial agent
    brain = CustomAgent()
    builder.add_agent([4,5], brain, name="Robot", is_traversable=True, img_name="robot.png")

    # Return the builder
    return builder

def run():
    # By creating scripts that return a builder, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    builder = create_builder()

    # we set a path pointing to our custom images 
    media_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "images")

    # startup world-overarching MATRX scripts, such as the api and/or visualizer if requested
    builder.startup(media_folder=media_folder)

    for world in builder.worlds():
        world.run(builder.api_info)

    builder.stop()
