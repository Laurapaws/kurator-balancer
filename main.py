import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

class Weapon:
    instances = []
    def __init__(self, name, colour, optimal, falloff_mod, DPS, line_object=None, plot_type='line'):
        self.name = name
        self.colour = colour
        self.optimal = optimal
        self.falloff_mod = falloff_mod
        self.DPS = DPS
        self.plot_type = plot_type
        self.result = []
        self.line_object = line_object
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

# class SlideController:
#     def __init__(self, slider=None, axis=None):
#         self.slider = slider
#         self.axis = self.slider.axis
        
        
def init_data_dict(min_range, max_range, steps):
    
    interval = (max_range - min_range) / steps
    range_series = np.arange(min_range, max_range, interval).tolist() 
    data_dict = {'ranges':range_series}
    
    return data_dict, range_series

def plot_data(data_dict, weapon_list):
    
    fig, ax = plt.subplots()
      
    for weapon in weapon_list:
        weapon.line_object, = plt.plot(data_dict["ranges"], data_dict[weapon.name], label = weapon.name)
        
    plt.title('Kurator')
    
    return fig, ax

def setup_data_dict(data_dict, range_series):
        for weapon in Weapon.instances:
            data_dict[weapon.name] = []
            weapon.result = []
            data_dict[weapon.name] = weapon.calc_damage(range_series)
        return data_dict

def update_values():
    setup_data_dict(data_dict, range_series)
    for weapon in Weapon.instances:
        weapon.line_object.set_ydata(data_dict[weapon.name])    
    fig.canvas.draw_idle()

def update_falloff_intensity(val):
    sim.falloff_intensity = val
    update_values()
    
# def set_slider(name, pos_tuple, axis, valmin, valmax, valinit):
#     ax_control = plt.axes(pos_tuple)
#     falloff_slider = Slider(ax_control, name, valmin, valmax, valinit=valinit)
    
    
    

if __name__ == "__main__":
    
    sim = SimulationProperties(5, 15000, 500, 0.8)
    data_dict, range_series = init_data_dict(sim.min_range, sim.max_range, sim.steps)

    autocannon = Weapon('Autocannon', 'red', 2000, 3, 30)
    burst_laser = Weapon('Burst_Laser', 'black', 6000, 0.2, 22.9)
    
    # slide_controllers = []
    
    #set_slider('Falloff Intensity:', [0.2, 0.05, 0.6, 0.03], ax_control, 0, 1, sim.falloff_intensity)
    ax_control = plt.axes([0.2, 0.05, 0.6, 0.03])
    falloff_slider = Slider(ax_control, 'Falloff Intensity:', 0, 1, valinit=sim.falloff_intensity)
    
    # slide_controllers.append(SlideController(
    #     Slider(ax_control, 'Falloff Intensity:', 0, 1, valinit=sim.falloff_intensity), 
    #     plt.axes([0.2, 0.05, 0.6, 0.03]) 
    #     ))
    
    fig, ax = plot_data(setup_data_dict(data_dict, range_series), Weapon.instances)
    
    falloff_slider.on_changed(update_falloff_intensity)
    
    plt.show()
    