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
            self.disease_duration = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self,new_position)

    def infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if(len(cellmates) > 1):
            for inhabitant in cellmates:
                if inhabitant.infected == False:
                    if(random.uniform(0,1)<self.transmissibility):
                        inhabitant.infected = True
                        inhabitant.disease_duration = int(round(random.expovariate(1.0/self.mean_length_of_disease),0))
    
    def step(self):
        if(random.uniform(0,1)<self.level_of_movement):
            self.move()
        if(self.infected == True):
            self.infect()
            self.disease_duration -= 1
        if(self.disease_duration <= 0):
            self.infected = False

class Disease_Model(Model):
    def __init__(self, N,width,height,initial_infection,transmissibility,level_of_movement,mean_length_of_disease) -> None:
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width,height,True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = Person_Agent(i,self,initial_infection,transmissibility,level_of_movement,mean_length_of_disease)
            self.schedule.add(a)

            try:
                start_cell = self.grid.find_empty()
                self.grid.place_agent(a,start_cell)
            except:
                    x = random.randrange(self.grid.width)
                    y = random.randrange(self.grid.height)
                    self.grid.place_agent(a,(x,y))
    
    def step(self):
        self.schedule.step()