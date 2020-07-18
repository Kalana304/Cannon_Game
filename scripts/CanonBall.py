# ####################################################################################################################
## Author: Kalana Abeywardene
## Created on: 23/04/2020
#######################################################################################################################

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import math

class Basis:                                        # Class with gravity - without air-resistance
    def __init__(self, tyng):
        self.tyng = tyng                            # tyng = gravitaional acceleration
    
    # Function for gravity class. tidspunkt = time, tilstandsvektor = vector (used as parameter)
    def evaluate(self, tidspunkt, tilstandsvektor):
        x_pos = 0                           # x acceleration
        y_pos = self.tyng                   # y acceleration
        x_fart = tilstandsvektor[2]         # x_fart = x_velocity
        y_fart = tilstandsvektor[3]         # y_fart = y_velocity
        endring = np.array([x_fart, y_fart, x_pos, y_pos])*tidspunkt        # endring = change
        return endring                                                      # returning [new_x, new_y, new_xDot, new_yDot] vector


class Luft:                                  # Class where drag is applied. Luft = Air (with air resistance)

    def __init__(self, tyng, luftm):                         # luftm = drag (parameter - air resistance)
        self.tyng = tyng
        self.luftm = luftm

    def evaluate(self, tidspunkt, tilstandsvektor):             #   function for drag
        x_fart = tilstandsvektor[2]                             #   same as in the previous class function
        y_fart = tilstandsvektor[3]
        F = math.sqrt(x_fart**2 + y_fart**2)                    #  F = V for velocity
        x_pos = -(self.luftm * x_fart * F)                      # x position
        y_pos = self.tyng - (self.luftm * y_fart * F)           # y posistion
        endring = np.array([x_fart, y_fart, x_pos, y_pos]) * tidspunkt      # change
        return endring

# Class integrator

class Integrator:

    def __init__(self, delta_time, time_end):

        self.delta_time = delta_time
        self.time_end = time_end
        self.time = 0
        self.initial_condition_vector = []
        self.k = 0


    def integrate(self, function:(Basis, Luft), initial_condition_vector):

        self.initial_condition_vector = np.array(initial_condition_vector.copy())
        while self.time <= self.time_end:
            frs = function.evaluate(self.delta_time, self.initial_condition_vector)
            self.initial_condition_vector = self.initial_condition_vector + frs
            yield self.initial_condition_vector
            self.time += self.delta_time
        return 

def canon_balls(x, y, r, canvasName, color='#000000'):                                             # Function to draw the canon balls on canvas
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color, outline=color)

def make_screen(root, v):            # Function to make the GUI screen widgets (inputs - root session, var paramter)
    inputs = {}

    min_force = 0                    # Setting min and max values for STRENGTH Slider
    max_force = 200

    min_angle = 0                    # Settint min and max values for ANGLE Slider
    max_angle = 90

    # Creating a checkbox to choose whether the air resistance is taken into calculations
    air_res = tk.Checkbutton(root, text="With Air Resistance", variable = v, justify = tk.CENTER, onvalue='With', offvalue='Without')
    air_res.deselect()
    air_res.place(x=800, y = 680, width = 280, height = 40)
    
    # Creating the slider for STRENGTH parameter
    slider1 = tk.Scale(root, from_=min_force, to=max_force, orient=tk.HORIZONTAL)
    slider1.place(x=0, y=640, width = 400, height = 40)

    slLabel1 = tk.Label(root, text="STRENGTH", justify = tk.CENTER)
    slLabel1.place(x=0, y=690, width = 400, height = 40)

    # Creating the slider for ANGLE parameter
    slider2 = tk.Scale(root, from_=min_angle, to=max_angle, orient=tk.HORIZONTAL)
    slider2.place(x=400, y=640, width = 400, height = 40)

    slLabel2 = tk.Label(root, text="ANGLE", justify = tk.CENTER)
    slLabel2.place(x=400, y=690, width = 400, height = 40)

    # Set each widget instances into a dictionary to be passed into trajectory calculations 
    inputs['Air_Res'] = v
    inputs['Force'] = slider1
    inputs['Angle'] = slider2

    return inputs

def trajectory(elements, init_x, init_y):           # Function for trajectory calculation and draw on canvas

    Force = elements['Force'].get()                         # Get the Total velocity from GUI
    Angle = elements['Angle'].get() * math.pi/180           # Get the angle value from the GUI and convert to radians
    Air_Res = elements['Air_Res'].get()                     # Status as to whether the air resistance is used or not from GUI 

    sleepTime = 25                          # set sleep time for canvas before updating it
    
    init_xDot, init_yDot = Force*math.cos(Angle), Force*math.sin(Angle)     # Initial (x_dot, y_dot) - velocities
    init_conditions = [init_x, init_y, init_xDot, init_yDot]                # Initial condition vector

    tyng = -9.81                                    # Gravitational pull = 9.81 acceleration
    time = 20                                       # Example of start time. Can be changed
    delta_t = 1                                     # Time increment set to be 1s. Can be changed

    canvas.create_line(init_x, init_y, init_x+canon_pipe*math.cos(Angle), init_y-canon_pipe*math.sin(Angle), width=5) 
        
    tidssteg = Integrator(delta_t, time)            # Create the Integrator instance 

    if Air_Res == 'With':                           # Checking whether we use air resistance or not
        print('Calculating with air resistance')
        luftm = 0.001
        traj_class = Luft(tyng, luftm)              # If using, use Luft Class
        color = 'red'
    else:
        print('Calculating with-out air resistance')
        traj_class = Basis(tyng)                    # If not, use Basis Class
        color = '#000000'
    # Create the generator which gives the [new_x, new_y, new_xDot, new_yDot] vector
    vector_generator = tidssteg.integrate(traj_class, init_conditions) 

    canon_balls(init_x+canon_pipe*math.cos(Angle), init_y-canon_pipe*math.sin(Angle), 5, canvas, color)     # Draw the Canon Ball at the starting point

    iter = 0
    while iter < time/delta_t:                                  
        new_vect = next(vector_generator)                       # use next() to generate the next vector from generator
        x_new, y_new = new_vect[0], 2*init_y - new_vect[1]      # adjust for drawing on canvas
        canon_balls(x_new, y_new, 5, canvas, color)                    # draw on canvas
        canvas.after(sleepTime)
        canvas.update()                                         # update the canvas after the drawing 
        iter += 1
    

if __name__=='__main__':
    res_x, res_y = 1080, 720                                    # para used for resolution

    root = tk.Tk()                                              # setting the main session of GUI
    root.geometry(f'{res_x}x{res_y}+5+5')
    root.title('Lets Play CanonBall!!!')

    v = tk.StringVar()
    elements = make_screen(root, v)                             # Getting the dict of widgets added on GUI
        
    init_x, init_y = 29,632                                     # Initial values to place the cannon sphere

    canva_x, canva_y = 2,2                              # parameters for canvas placement
    canva_h, canva_w = 630, 1068

    piller_h, piller_w = 200, 10                        # parameters for the obstacle piller
    piller_x, piller_y = 525, 632

    target_x, target_y = 900, 632                       # parameters for target 
    target_w, target_h = 12,20

    canon_x, canon_y = 4, 607               # Canon placment coord
    canon_r = 25                            # Canon radius 
    canon_pipe = 50                         # Canon tube length set to 50. Can be changed ( >25)

    canvas = tk.Canvas(root, width=1080, height=630, bg="grey")
    canvas.place(x=0,y=0)

    canvas = tk.Canvas(root, width=canva_w, height=canva_h, bg="white", bd=2)
    canvas.place(x=canva_x,y=canva_y)

    canvas.create_arc(canon_x, canon_y, canon_x+2*canon_r, canon_y+2*canon_r, extent=180, outline="#000000", fill="#000000", width=1)
    
    canvas.create_rectangle(piller_x, piller_y, piller_x+piller_w, piller_y-piller_h, fill='#000000', outline='#000000')
    canvas.create_rectangle(target_x, target_y, target_x+target_w, target_y-target_h, fill='red', outline='#000000')

    # Creating the button FIRE!!
    button = tk.Button(root, text='FIRE!!!!', command=(lambda e=elements: trajectory(e, init_x, init_y)) ) # invoke function trajectory when you press the button
    button.place(x=800, y = 640, width = 280, height = 40)
    
    root.mainloop() # main session loop