import tkinter as tk
from functions import get_color_from_gradient
from math import cos, sin, atan, sqrt
from constants import *

W, H = 4000, 2500
marge = 5000
dx, dy = 20, 20 # Elementary move for the canvas


class Map(tk.Canvas):
    def __init__(self, master, width, height, background):
        # Initialize a canvas
        tk.Canvas.__init__(self, master=master, width=width, height=height, background=background)
        self.configure(scrollregion=(-marge, -marge, marge, marge))
        self.configure(xscrollincrement=1)
        self.configure(yscrollincrement=1)
        self.create_rectangle(-50,-50,W-1, H-1, tags="container")

        # Keep track of the current scale to make correct operations when zoomed in or out
        self.current_scale = 1

    def scroll_start(self, event):
        # Save the current position of the map
        self.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        # Move the map accordingly to the new event position
        self.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        # Zoom in if the user scrolls up, zoom out otherwise
        factor = 0
        if event.delta > 0 or event.keysym == "Up":
            factor = 2
        elif event.delta < 0 or event.keysym == "Down":
            factor = .5

        if factor != 0:
            # Scale every object on the canvas by (factor)
            self.scale("all", 0,0 , factor, factor)
            self.current_scale *= factor
            marge = self.current_scale * 5000

            # Reconfiguration for the scrollbars
            self.configure(scrollregion=(-marge, -marge, marge, marge))
            x,y = self.canvasx(event.x), self.canvasy(event.y)

            self.xview_scroll(int(x*(factor-1)), "units")
            self.yview_scroll(int(y*(factor-1)), "units")

    def draw_cross(self, cross_list):
        for cross in cross_list:
            (x,y) = cross.coords
            cross.rep = self.create_oval(x-2.5, y-2.5, x+2.5, y+2.5, fill=ROAD_COLOR, outline=ROAD_COLOR, tag="cross")

    def draw_road(self, road_list):
        for road in road_list:
            (l, w) = (road.length, road.width)
            ang = road.angle
            (x,y) = road.cross2.coords
            dx = sin(ang)*w/2
            dy = - cos(ang)*w/2
            dxb = -l*cos(ang)
            dyb = -l*sin(ang)
            road.rep = self.create_polygon(x+dx, y+dy, x-dx, y-dy, x+dxb-dx, y+dyb-dy, x+dxb+dx, y+dyb+dy, fill=ROAD_COLOR, outline=ROAD_OUTLINE_COLOR, width = 2, tag="road")

    def draw_vehicle(self, vehicle_list):
        for veh in vehicle_list:
            angle = veh.road.angle if (veh.origin_cross==veh.road.cross1) else (veh.road.angle + 3.1415)
            e = self.current_scale
            if veh.changed_road:
                veh.changed_road = False
                (x0,y0) = veh.origin_cross.coords
                road_width = veh.road.width
                (l, w) = (veh.length, veh.width)
                x = x0 - road_width/4 *sin(angle) + (veh.x+veh.length/2)*cos(angle)
                y = y0 + road_width/4 *cos(angle) + (veh.x+veh.length/2)*sin(angle)

                x = x*e
                y = y*e
                dx = sin(angle)*w/2 *e
                dy = - cos(angle)*w/2 *e
                dxb = - l*cos(angle) *e
                dyb = - l*sin(angle) *e

                points = (x+dx, y+dy, x-dx, y-dy, x+dxb-dx, y+dyb-dy, x+dxb+dx, y+dyb+dy)
                if veh.rep == None :
                    veh.rep = self.create_polygon(points, fill=get_color_from_gradient(veh.v/veh.road.speed_limit), tag="vehicle")
                else:
                    self.coords(veh.rep, points)
            else:
                self.move(veh.rep, veh.dx*cos(angle)*e, veh.dx*sin(angle)*e)
                veh.dx = 0
                self.itemconfig(veh.rep, fill=get_color_from_gradient(veh.v/veh.road.speed_limit))



    def draw_leadership(self, vehicle_list):
        map.delete("leadership")
        for veh in vehicle_list:
            if veh.leader != None:
                leader_coords = self.coords(veh.leader.rep)
                follower_coords = self.coords(veh.rep)
                map.create_line(leader_coords[0], leader_coords[1], follower_coords[0], follower_coords[1], fill="black", width=1, tag="leadership")

class Container(tk.Frame):
    def __init__(self, root):
        # Initialize a Frame
        tk.Frame.__init__(self, root)
        # Initialize the canvas representating the map
        self.map = Map(self, W, H, BACKGROUND_COLOR)
        self.map.create_rectangle(-50,-50,W-1, H-1, tags="container")

        # Setting up scrollbars to be able to move the map in the window
        self.xsb = tk.Scrollbar(self, orient="horizontal", command=self.map.xview)
        self.ysb = tk.Scrollbar(self, orient="vertical", command=self.map.yview)
        self.map.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)

        # Place the canvas and scrollbars in their correct positions
        # Using a grid system to sustain further modifications of the layout
        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.map.grid(row=0, column=0, sticky="nsew")

        # Allows the canvas to expand as much as it can
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Controls(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.time_mgmt = tk.LabelFrame(self, text="Time managment", padx=10, pady= 10)
        self.time_mgmt.grid(row=0,column=0, sticky="new")

        self.time_str = tk.StringVar()
        self.time_str.set("Current time: 0 s.")
        tk.Label(master = self.time_mgmt, textvariable = self.time_str).pack()
        self.speed = tk.Scale(self.time_mgmt, label="Simulation speed", from_=0, to=10, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.speed.set(1)
        self.speed.pack(fill="both", expand="yes")
        self.play = tk.BooleanVar()
        self.play.set(True)
        self.play_b = tk.Radiobutton(self.time_mgmt, text="Play", variable=self.play, value=True)
        self.pause_b = tk.Radiobutton(self.time_mgmt, text="Pause", variable=self.play, value=False)
        self.play_b.pack(side=tk.LEFT)
        self.pause_b.pack(side=tk.LEFT)


        self.information = tk.LabelFrame(self, text="Information", padx=10, pady=10)
        self.information.grid(row=1,column=0, sticky="new")
        tk.Label(master = self.information, text = "Number of vehicles: ").grid(row = 0, column = 0)
        self.nb_veh = tk.IntVar()
        self.nb_veh.set(0)
        tk.Label(master = self.information, textvariable = self.nb_veh).grid(row = 0, column = 1)
        self.avg_speed = tk.StringVar()
        self.avg_speed.set("0")
        tk.Label(master = self.information, text="Average speed: ").grid(row = 1, column = 0)
        tk.Label(master = self.information, textvariable = self.avg_speed).grid(row = 1, column = 1)

        self.settings = tk.LabelFrame(self, text="Settings", padx=10, pady=10)
        self.settings.grid(row=2,column=0, sticky="new")

        tk.Label(master = self.settings, text = "Show leadership relations:").pack()
        self.leadership = tk.BooleanVar()
        self.leadership.set(True)
        self.leadership_true = tk.Radiobutton(self.settings, text="Play", variable=self.leadership, value=True)
        self.leadership_false = tk.Radiobutton(self.settings, text="Pause", variable=self.leadership, value=False)
        self.leadership_true.pack(side=tk.LEFT)
        self.leadership_false.pack(side=tk.LEFT)



def keyboard_listener(event):
    if event.char == " ":
        controls.play.set(False) if controls.play.get() else controls.play.set(True)

    elif event.keysym == "Right":
        map.scan_mark(0,0)
        map.scan_dragto(-dx,0)

    elif event.keysym == "Left":
        map.scan_mark(0,0)
        map.scan_dragto(dx,0)

    elif event.keysym == "Up":
        map.scan_mark(0,0)
        map.scan_dragto(0,dy)

    elif event.keysym == "Down":
        map.scan_mark(0,0)
        map.scan_dragto(0,-dy)

root = tk.Tk()
root.state('zoomed')
container = Container(root)
container.grid(row=0, column=0, sticky="nsew")
map = container.map
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

controls = Controls(root)
controls.grid(row=0, column=1, sticky="ne")

# Event-listeners
root.bind("<KeyPress>", keyboard_listener)
map.bind("<ButtonPress-1>", map.scroll_start)
map.bind("<B1-Motion>", map.scroll_move)
map.bind("<MouseWheel>", map.zoom)
root.bind("<Control-Key>", map.zoom)