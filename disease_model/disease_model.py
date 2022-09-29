import random

from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation


class Person_Agent(Agent):
    def __init__(self,unique_id,model,initial_infection,transmissibility,level_of_movement,mean_length_of_disease):
        super().__init__(unique_id,model)
        self.transmissibility = transmissibility
        self.level_of_movement = level_of_movement
        self.mean_length_of_disease = mean_length_of_disease


        if(random.uniform(0,1) < initial_infection):
            self.infected = True
            self.disease_duration = int(round(random.expovariate(1.0/self.mean_length_of_disease),0))
        else:
            self.infected = False
    def move(self):
        possible_steps = self.model.grid.get_neighbourhood(self.pos,moore=True,include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self,new_position)