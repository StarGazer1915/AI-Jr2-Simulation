"""
========== SERVER FILE ==========
This file contains the server (setup) of the MESA simulation.
The creation of the sliders can be found under the variables section!
=================================
"""

# =============== IMPORTS =============== #
from disease_module import Enviroment
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# ========== REGULAR FUNCTIONS ========== #
def person_portrayal(agent):
    """
    This function determines how an agent is portrayed in the visual
    representation of the simulation. Red means infected and gray non-infected.
    It then returns the representation so it can be used in the simulation.
    @param agent: Class object
    @return: dict
    """
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if agent.infected:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
        portrayal["Layer"] = 1

    return portrayal


# ============== VARIABLES ============== #
grid = CanvasGrid(person_portrayal, 10, 10, 500, 500)
number_of_agents_slider = UserSettableParameter('slider', 'Number of Agents', 20, 2, 100, 1)
initial_infection_slider = UserSettableParameter('slider', 'Probability of Initial Infection', 0.3, 0.01, 1, 0.01)
transmissibility_slider = UserSettableParameter('slider', 'Transmissibility', 0.2, 0.01, 1, 0.01)
level_of_movement_slider = UserSettableParameter('slider', 'Level of Movement', 0.5, 0.01, 1, 0.01)
mean_length_of_disease_slider = UserSettableParameter('slider', 'Mean Length of Disease (days)', 10, 1, 100, 1)

# ============ SERVER SETUP ============= #
server = ModularServer(Enviroment, [grid], "Disease Spread Model",
                       {"N": number_of_agents_slider, "width": 10, "height": 10,
                        "initial_infection": initial_infection_slider,
                        "transmissibility": transmissibility_slider,
                        "level_of_movement": level_of_movement_slider,
                        "mean_length_of_disease": mean_length_of_disease_slider}
                       )
