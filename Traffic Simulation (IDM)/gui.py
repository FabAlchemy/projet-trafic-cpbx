import tkinter as tk
from math import cos, sin

W, H = 500, 300
marge = 5000

class Map(tk.Canvas):
    def __init__(self, master, width, height, background):
        # Initialize a canvas
        tk.Canvas.__init__(self, master=master, width=width, height=height, background=background)
        self.configure(scrollregion=(-marge, -marge, marge, marge))
        self.create_rectangle(-50,-50,W-1, H-1, tags="container")

        # Enable scrolling with the mouse:
        self.bind("<ButtonPress-1>", self.scroll_start)
        self.bind("<B1-Motion>", self.scroll_move)

        # Keep track of the current scale to make correct operations when zoomed in or out
        self.current_scale = 1
        self.configure(xscrollincrement=1)
        self.configure(yscrollincrement=1)

    def scroll_start(self, event):
        # Save the current position of the map
        self.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        # Move the map accordingly to the new event position
        self.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        # Zoom in if the user scrolls up, zoom out otherwise
        factor = 2 if event.delta > 0 else .5

        # Scale every object on the canvas by (factor)
        self.scale("all", 0,0 , factor, factor)
        self.current_scale *= factor
        marge = self.current_scale * 5000

        # Reconfiguration for the scrollbars
        self.configure(scrollregion=(-marge, -marge, marge, marge))
        x,y = self.canvasx(event.x), self.canvasy(event.y)

        self.xview_scroll(int(x*(factor-1)), "units")
        self.yview_scroll(int(y*(factor-1)), "units")

    def draw_cross(self, cross):
        (x,y) = cross.coords
        self.create_oval(x-2.5, y-2.5, x+2.5, y+2.5, fill="grey26", outline = "grey26", tag="cross")

    def draw_road(self, road):
        (l, w) = (road.length, road.width)
        ang = road.angle
        (x,y) = road.cross1.coords
        dx = sin(ang)*w/2
        dy = cos(ang)*w/2
        dxb = l*cos(ang)
        dyb = l*sin(ang)
        a = self.create_polygon(x+dx, y+dy, x-dx, y-dy, x+dxb-dx, y-dyb-dy, x+dxb+dx, y-dyb+dy, fill="grey26", tag="road")
        # a = map.canvas.create_polygon(x+dx, y+dy, x-dx, y-dy, x-dxb-dx, y+dyb-dy, x-dxb+dx, y+dyb+dy, fill="black", tag="road")

    def draw_vehicle(self, vehicle):
        if vehicle.origin_cross == vehicle.road.cross1:
            angle = vehicle.road.angle
            x = vehicle.road.cross1.coords[0] + vehicle.x * cos(angle)
            y = vehicle.road.cross1.coords[1] + vehicle.x * sin(angle)
        else:
            angle = - vehicle.road.angle
            x = vehicle.road.cross2.coords[0] + vehicle.x * cos(angle)
            y = vehicle.road.cross2.coords[1] + vehicle.x * sin(angle)

        (l, w) = (vehicle.length, vehicle.width)
        e = self.current_scale
        x = x*e
        y = y*e
        dx = sin(angle)*w/2 *e
        dy = cos(angle)*w/2 *e
        dxb = l*cos(angle) *e
        dyb = l*sin(angle) *e

        if vehicle.rep == None :
            vehicle.rep = self.create_polygon(x+dx, y+dy, x-dx, y-dy, x-dxb-dx, y+dyb-dy, x-dxb+dx, y+dyb+dy, fill="red", tag="car")
        else:
            self.coords(vehicle.rep, x+dx, y+dy, x-dx, y-dy, x-dxb-dx, y+dyb-dy, x-dxb+dx, y+dyb+dy)

class Container(tk.Frame):
    def __init__(self, root):
        # Initialize a Frame
        tk.Frame.__init__(self, root)
        # Initialize the canvas representating the map
        self.map = Map(self, W, H, "SeaGreen2")
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
        #
        # # Allows the canvas to expand as much as it can
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class Controls(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.time_mgmt = tk.LabelFrame(self, text="Time managment", padx=10, pady= 10)
        self.time_mgmt.pack()

        self.speed = tk.Scale(self.time_mgmt, label="Simulation speed", from_=0, to=10, resolution=0.01, orient=tk.HORIZONTAL, length=200)
        self.speed.set(1)
        self.speed.pack(fill="both", expand="yes")
        self.play = tk.BooleanVar()
        self.play.set(True)
        self.play_b = tk.Radiobutton(self.time_mgmt, text="Play", variable=self.play, value=True)
        self.pause_b = tk.Radiobutton(self.time_mgmt, text="Pause", variable=self.play, value=False)
        self.play_b.pack(side=tk.LEFT)
        self.pause_b.pack(side=tk.LEFT)


def clavier(event):

    if event.char == " ":
        controls.play.set(False) if controls.play.get() == True else controls.play.set(True)




# Create a window
root = tk.Tk()
container = Container(root)
container.grid(row=0, column=0, sticky="nsew")
map = container.map
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

controls = Controls(root)
controls.grid(row=0, column=1, sticky="ne")

# Event-listeners
map.bind("<MouseWheel>", map.zoom)
root.bind("<KeyPress>", clavier)


def start():
    root.mainloop()
