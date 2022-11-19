import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

class Weapon:
    instances = []
    def __init__(self, name, colour, optimal, falloff_mod, DPS, plot_type='area'):
        self.name = name
        self.colour = colour
        self.optimal = optimal
        self.falloff_mod = falloff_mod
        self.DPS = DPS
        self.plot_type = plot_type
        self.result = []
        self.__class__.instances.append(self)
        
    def calc_damage(self, distance_series):
            
        for distance_to_target in distance_series:
            falloffCount = max(0, ( (distance_to_target - self.optimal) / self.optimal) * (1 / self.falloff_mod))  
            damageModifier = (sim.falloff_intensity ** (falloffCount ** 2))
            damage = self.DPS * damageModifier
            self.result.append(damage)
            
        return self.result
        
class SimulationProperties:
    def __init__(self, min_range, max_range, steps, falloff_intensity):
        self.min_range = min_range
        self.max_range = max_range
        self.steps = steps
        self.falloff_intensity = falloff_intensity
    
def calculate_single(optimal, falloff_modifier, distance_to_target):
    
    falloffCount = max(0, ( (distance_to_target - optimal) / optimal) * (1 / falloff_modifier))  
    damageModifier = (sim.falloff_intensity ** (falloffCount ** 2))
        
    return damageModifier
    
def init_data_dict(min_range, max_range, steps):
    
    interval = (max_range - min_range) / steps
    range_series = np.arange(min_range, max_range, interval).tolist() 
    data_dict = {'ranges':range_series}
    
    return data_dict, range_series

def init_plots(data_dict):    
    df = pd.DataFrame(data_dict)
    ax = plt.gca() 

def plot_data(data_dict, weapon_list):
    
    df = pd.DataFrame(data_dict)
    ax = plt.gca()
    
    for weapon in weapon_list:
        df.plot(kind = weapon.plot_type,
                x = 'ranges',
                y = weapon.name,
                color = weapon.colour,
                alpha = 0.4,
                ax = ax
                )
    
    plt.title('Kurator')
    plt.show()

def setup_data_dict(data_dict, range_series):
        for weapon in Weapon.instances:
            data_dict[weapon.name] = weapon.calc_damage(range_series)
        return data_dict
    

if __name__ == "__main__":
    
    sim = SimulationProperties(5, 15000, 500, 0.8)
    data_dict, range_series = init_data_dict(sim.min_range, sim.max_range, sim.steps)


    autocannon = Weapon('Autocannon', 'red', 2000, 3, 30, 'line')
    burst_laser = Weapon('Burst_Laser', 'black', 6000, 0.2, 22.9)
    
    print("test")
    plot_data(setup_data_dict(data_dict, range_series), Weapon.instances)