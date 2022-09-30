from disease_model import Disease_Model
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import Slider
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    portrayal = {"Shape":"circle","Filled":"true","r":0.5}

    if agent.infected == True:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
        portrayal["Layer"] = 1
    return portrayal
    
grid = CanvasGrid(agent_portrayal,10,10,500,500)
num_of_agents_slider = Slider("No of Agents",20,2,100,1)
initial_infection_slider = Slider('Probability of Infection',0.3,0.01,1,0.01)
transmissibility_slider = Slider('Transmissibility',0.2,0.01,1,0.01)
level_of_movement_slider = Slider('Level of Movement',0.5,0.01,1,0.01)
mean_length_of_disease_slider = Slider('Mean Length of Disease in days',10,1,100,1)
total_infected_graph = ChartModule([{"Label":"Total_Infected","Color":"Red"}],data_collector_name='datacollector')

server = ModularServer(Disease_Model,[grid,total_infected_graph ],"Disease Spread Model",{"N":num_of_agents_slider,"width":10,"height":10,"initial_infection":initial_infection_slider,"transmissibility":transmissibility_slider,"level_of_movement":level_of_movement_slider,"mean_length_of_disease":mean_length_of_disease_slider})