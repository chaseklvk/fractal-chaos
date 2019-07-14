import tkinter as tk
import random

REFRESH_RATE = 10

class ChaosApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Set up window
        self.parent.title("Chaos Application")
        self.parent.geometry("800x800")

        # Set up canvas
        self.canvas = tk.Canvas(self.parent, height=800, width=800)
        self.canvas.pack()

        # Generate random points
        self.generate_endpoints()

        # Begin chaos
        self.parent.after(REFRESH_RATE, self.take_step)
    
    def generate_endpoints(self):
        first = self.center_to_coordinates(self.random_coordinate(x_limit=(200, 200), y_limit=(0, 700)))
        second = self.center_to_coordinates(self.random_coordinate(x_limit=(100, 600), y_limit=(600, 100)))
        third = self.center_to_coordinates(self.random_coordinate(x_limit=(600, 100), y_limit=(600, 100)))

        current = self.center_to_coordinates(self.random_coordinate(), radius=3)

        self.canvas.create_oval(first[0], first[1], first[2], first[3], fill="green")
        self.canvas.create_oval(second[0], second[1], second[2], second[3], fill="green")
        self.canvas.create_oval(third[0], third[1], third[2], third[3], fill="green")
        self.canvas.create_oval(current[0], current[1], current[2], current[3], fill="red")

        self.endpoints = (first, second, third)
        self.current_point = current

    def random_coordinate(self, x_limit=(0, 0), y_limit=(0, 0)):
        x = random.randint(5 + x_limit[0], 795 - x_limit[1])
        y = random.randint(5 + y_limit[0], 795 - y_limit[1])

        return (x, y)

    def center_to_coordinates(self, center, radius=5):
        x1 = center[0] - radius
        y1 = center[1] - radius
        x2 = center[0] + radius
        y2 = center[1] + radius

        return (x1, y1, x2, y2)

    def take_step(self):
        # Select an endpoint
        point = random.randint(1, 3)

        end_coords = self.endpoints[point - 1]
        start_coords = self.current_point

        mid_x = (start_coords[0] + end_coords[0]) / 2
        mid_y = (start_coords[1] + end_coords[1]) / 2

        middle_coordinates = (mid_x, mid_y)
        self.current_point = middle_coordinates

        next_point = self.center_to_coordinates(middle_coordinates, radius=1)

        self.canvas.create_oval(next_point[0], next_point[1], next_point[2], next_point[3], fill="black")
        self.parent.after(REFRESH_RATE, self.take_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChaosApplication(root)
    app.pack(side="top", fill="both", expand=True)
    root.mainloop()