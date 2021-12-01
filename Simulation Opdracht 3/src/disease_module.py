"""
========== SERVER FILE ==========
This file contains the modules (Agent and Enviroment) of the MESA simulation.
=================================
"""

# =============== IMPORTS =============== #
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random


# =============== CLASSES =============== #
class Person(Agent):
    def __init__(self, id, model, IF, transmis, LOM, MLOD):
        """
        Here the properties of the Person object are defined.
        @param id: int
        @param model: Model Object
        @param IF: float
        @param transmis: float
        @param LOM: float
        @param MLOD: float
        @return: void
        """
        super().__init__(id, model)
        self.transmis = transmis
        self.LOM = LOM
        self.MLOD = MLOD

        if random.uniform(0, 1) > IF:
            self.infected = True
            self.disease_duration = int(round(random.expovariate(1.0 / self.MLOD), 0))
        else:
            self.infected = False

    def move(self):
        """
        This function checks the neighbouring places the agent can move.
        It then chooses a random new place and moves to it.
        @return: void
        """
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect(self):
        """
        This function determines if non-infected Person(s) in the immediate
        area will be infected by the Person. If so, then they are infected.
        @return: void
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            for p in cellmates:
                if not p.infected:
                    if random.uniform(0, 1) < self.transmis:
                        p.infected = True
                        p.disease_duration = int(round(random.expovariate(1.0 / self.MLOD), 0))

    def step(self):
        """
        This function manages what the Person (Agent) does each step or what is changed
        about the person. The person can move but that is not a given. If the person is
        infected then the infection will try to infect nearby Person(s) using the
        'self.infect' function and determine their disease_duration. The disease_duration
        of the Person itself becomes lower each step until it reaches zero. Then the
        Person becomes cured and non-infected.
        @return: void
        """
        if random.uniform(0, 1) < self.LOM:
            self.move()
        if self.infected:
            self.infect()
            self.disease_duration -= 1
            if self.disease_duration <= 0:
                self.infected = False


class Enviroment(Model):
    def __init__(self, N, width, height, initial_infection, transmissibility, level_of_movement, mean_length_of_disease):
        """
        Here the properties of the Model object are defined.
        The Agents are also created here and put on their start positions of
        the grid. They are scheduled and will be used when the model has started.
        @param N: int
        @param width: int
        @param height: int
        @param initial_infection: float
        @param transmissibility: float
        @param level_of_movement: float
        @param mean_length_of_disease: float
        @return: void
        """
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = Person(i, self, initial_infection, transmissibility, level_of_movement, mean_length_of_disease)
            self.schedule.add(a)
            try:
                start_cell = self.grid.find_empty()
                self.grid.place.agent(a, start_cell)
            except:
                X = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                self.grid.place_agent(a, (X, y))

    def step(self):
        """
        This function makes the simulation move one step in time.
        @return: void
        """
        self.schedule.step()
