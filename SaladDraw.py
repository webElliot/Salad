from PIL import Image , ImageDraw
from Classes.fonts import Add_Notes

class Size:
	@staticmethod
	def getMini(): # first param for rectangle
		# Coordinates and size
		top_left = (55 , 163)
		width , height = 49 , 105
		bottom_right = (top_left[ 0 ] + width , top_left[ 1 ] + height)
		return [top_left, bottom_right]

	@staticmethod
	def getReg(): # first param for rectangle
		# Coordinates and size
		top_left = (51 , 279)
		width , height = 56 , 95
		bottom_right = (top_left[ 0 ] + width , top_left[ 1 ] + height)
		return [top_left, bottom_right]

	@staticmethod
	def getLrg(): # first param for rectangle
		# Coordinates and size
		top_left = (56 , 387)
		width , height = 47 , 92
		bottom_right = (top_left[ 0 ] + width , top_left[ 1 ] + height)
		return [top_left, bottom_right]


class SaladCreator:
	MARGIN = 8

	def __init__(self, Salad):
		self.Salad = Salad
		#self.image = Image.open(self.Salad.image_path)
		self.image = Add_Notes(self.Salad).image
		self.colour = "black" # Colour for all Circles / Rectangles

	def run(self):
		# Draw Rectangle around MINI/REG/LRG
		self.drawSize()

		# Draw Circles around Protein sizes.
		for Location in self.Salad.getProteinDot():
			print(Location)
			self.drawCircle(coord = Location)

		# Fill in dots for Dressings
		for Location in self.Salad.getDressingDot():
			self.drawDot(coord = Location)

		# Fill in dots for Sprinkles
		for Location in self.Salad.getSprinklesDot():
			self.drawDot(coord = Location)

	def drawDot(self,coord):
		draw = ImageDraw.Draw(self.image)
		dot_radius = 10

		x , y = coord[0],coord[1]
		left_up_point = (x - dot_radius , y - dot_radius)
		right_down_point = (x + dot_radius , y + dot_radius)
		draw.ellipse([ left_up_point , right_down_point ] , fill = self.colour)

	def drawCircle (self , coord , circle_radius = 25):
		draw = ImageDraw.Draw(self.image)

		x , y = coord[ 0 ] , coord[ 1 ]
		left_up_point = (x - circle_radius , y - circle_radius)
		right_down_point = (x + circle_radius , y + circle_radius)
		draw.ellipse([ left_up_point , right_down_point ] , outline = self.colour,width=3 )

	def drawSize(self):
		draw = ImageDraw.Draw(self.image)
		if self.Salad.getSize() == "MINI":
			draw.rectangle(Size.getMini() , outline = "black" , width = 3)
		elif self.Salad.getSize() == "REG":
			draw.rectangle(Size.getReg() , outline = "black" , width = 3)
		elif self.Salad.getSize() == "LRG":
			draw.rectangle(Size.getLrg() , outline = "black" , width = 3)

	def save (self , filename):
		self.image.save(filename)