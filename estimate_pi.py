import tkinter as tk
import random
import numpy as np

REFRESH_RATE = 10

SQUARE_SIDE = 600
SQUARE_BUFFER = 100

CIRCLE_SIDE = 600
CIRCLE_BUFFER = 100

class EstimatePi(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# Set up window
		self.parent.title("Estimate Pi")
		self.parent.geometry("800x800")

		# Approximation
		self.pi_approximation = 0
		self.total_points = 0
		self.total_in_circle = 0
		self.error = 0

		# Set up canvas
		self.canvas = tk.Canvas(self.parent, height=800, width=800)
		self.canvas.pack()

		# Generate random points
		self.setup_shapes()

		# Begin chaos
		self.parent.after(REFRESH_RATE, self.take_step)

	def setup_shapes(self):
		self.canvas.create_rectangle(
			SQUARE_BUFFER, 
			SQUARE_BUFFER, 
			SQUARE_BUFFER + SQUARE_SIDE, 
			SQUARE_BUFFER + SQUARE_SIDE, 
			fill="white"
		)

		self.canvas.create_oval(
			CIRCLE_BUFFER, 
			CIRCLE_BUFFER, 
			CIRCLE_BUFFER + CIRCLE_SIDE, 
			CIRCLE_BUFFER + CIRCLE_SIDE, 
			fill="green"
		)

		self.pi_text = self.canvas.create_text(
			CIRCLE_BUFFER, 
			CIRCLE_BUFFER / 2, 
			text="Pi is unknown", 
			fill="yellow", 
			font=('Helvetica 15 bold'), 
			justify=tk.LEFT
		)

		self.error_text = self.canvas.create_text(
			CIRCLE_BUFFER, 
			(CIRCLE_BUFFER / 2) + 20, 
			text="Error is unknown", 
			fill="yellow", 
			font=('Helvetica 15 bold'), 
			justify=tk.LEFT
		)

	def coordinate_to_plot(self, random_value, isX):	
		shift = (CIRCLE_SIDE / 2) + CIRCLE_BUFFER

		if isX: 
			return shift + ((CIRCLE_SIDE / 2) * random_value)

		return ((CIRCLE_SIDE / 2) * random_value) + CIRCLE_BUFFER
	
	def vector_magnitude(self, point):
		# point -> (x, y)
		return np.sqrt(point[0] ** 2 + point[1] ** 2)

	def update_approximation(self, vector):
		magnitude = self.vector_magnitude(vector)

		self.total_points += 1
		if magnitude <= 1:
			self.total_in_circle += 1
		
		self.pi_approximation = 4 * (self.total_in_circle / self.total_points)
		self.error = abs(((self.pi_approximation - np.pi) / np.pi)) * 100
		
	def take_step(self):
		x_coord = random.uniform(0, 1)
		y_coord = random.uniform(0, 1)

		vector = (x_coord, y_coord)

		plot_x = self.coordinate_to_plot(vector[0], True)
		plot_y = self.coordinate_to_plot(vector[1], False)

		self.canvas.create_oval(
			plot_x - 4, 
			plot_y - 4, 
			plot_x + 4,
			plot_y + 4,
			fill="red"
		)

		# Update our estimation
		self.update_approximation(vector)

		self.canvas.itemconfigure(self.pi_text, text=f"Pi is approximately {round(self.pi_approximation, 6)}")
		self.canvas.itemconfigure(self.error_text, text=f"Error is {round(self.error, 6)}")

		self.parent.after(REFRESH_RATE, self.take_step)

if __name__ == "__main__":
	root = tk.Tk()
	app = EstimatePi(root)
	app.pack(side="top", fill="both", expand=True)
	root.mainloop()