from PIL import Image, ImageDraw, ImageFont

# Open an image file




# Choose a font and size

class Add_Notes:
	name_shortener = {
		"Crunch Box": "Crunch".upper(),
		"Leaf Box" : "Leaf".upper(),
		"Poké bowl": "Poké".upper()
		}

	def __init__(self, salad):
		self.Salad = salad
		self.image = None
		self.run()

	def run(self):
		self.image = Notes(
			file_input = self.Salad.image_path,
		      GLUTEN_FREE = self.Salad.Gluten_Free,
		      Box_Name = self.name_shortener.get(self.Salad.Name)
		      ).image





class Notes:
	font_path = 'fonts/TwCenMTStd.otf'  # or .otf
	font_size = 55

	def __init__(self,
	             file_input = '../Sticker PNG.png',
	             GLUTEN_FREE = True,
	             Box_Name = "",
	             ):
		self.gluten_free = GLUTEN_FREE
		self.Box_Name = Box_Name

		self.image = Image.open(file_input)
		self.font = ImageFont.truetype(self.font_path , self.font_size)
		self.text_color = (0 , 0 , 0)  # or any RGB tuple
		self.setup_coordinates()
		self.run()
		#self.save()

	def save(self):
		# Save the edited image
		print(f"Saving!")
		self.image.save('o.jpg')

	def setup_coordinates(self):
		if self.gluten_free:
			if self.Box_Name == "Crunch".upper():
				self.name_coord = (960 , 270 + 30)
			if self.Box_Name == "Leaf".upper():
				self.name_coord = (1010 , 270 + 30)
			if self.Box_Name == "Poké".upper():
				self.name_coord = (1000 , 280 + 30)
		else:
			if self.Box_Name == "Crunch".upper():
				self.name_coord = (960 , 160)
			if self.Box_Name == "Leaf".upper():
				self.name_coord = (1000 , 160)
			if self.Box_Name == "Poké".upper():
				self.name_coord = (990 , 165)






		# bottom_left_coord_line_3 = (890, 50)
		# bottom_left_coord_line_3 = (468, 50)

	def run(self):
		# Initialize ImageDraw
		self.draw = ImageDraw.Draw(self.image)
		if self.gluten_free: self.add_gluten_free()
		self.add_name()

	def add_gluten_free(self):
		# Text to draw
		text = "Gluten Free".upper()
		# Text to add
		text_line_1 , text_line_2 = text.split()

		# Bottom-left coordinates for text
		bottom_left_coord_line_1 = (968, 173)
		bottom_left_coord_line_2 = (1011, 218)

		# Calculate the position and draw the first line of text
		text_bbox_line_1 = self.draw.textbbox((0 , 0) , text_line_1 , font = self.font)
		text_height_line_1 = text_bbox_line_1[ 3 ] - text_bbox_line_1[ 1 ]
		text_position_line_1 = (bottom_left_coord_line_1[ 0 ] , bottom_left_coord_line_1[ 1 ] - text_height_line_1)
		self.draw.text(text_position_line_1 , text_line_1 , font = self.font , fill = self.text_color)

		# Calculate the position and draw the second line of text
		text_bbox_line_2 = self.draw.textbbox((0 , 0) , text_line_2 , font = self.font)
		text_height_line_2 = text_bbox_line_2[ 3 ] - text_bbox_line_2[ 1 ]
		text_position_line_2 = (bottom_left_coord_line_2[ 0 ] , bottom_left_coord_line_2[ 1 ] - text_height_line_2)
		self.draw.text(text_position_line_2 , text_line_2 , font = self.font , fill = self.text_color)


	def add_name(self):
		# Calculate the position and draw the third line of text
		text_bbox_line_3 = self.draw.textbbox((0 , 0) , self.Box_Name , font = self.font)
		text_height_line_3 = text_bbox_line_3[ 3 ] - text_bbox_line_3[ 1 ]
		text_position_line_3 = (self.name_coord[ 0 ] , self.name_coord[ 1 ] - text_height_line_3)
		self.draw.text(text_position_line_3 , self.Box_Name , font = self.font , fill = self.text_color)












Box_Types = [ "Crunch", "Leaf", "Poké" ]
Box_Types = [ ea.upper() for ea in Box_Types ]
if __name__ == "__main__":
	Notes(
		Box_Name = Box_Types[2],
		GLUTEN_FREE = False,
		file_input = "../Sticker 2.png"

		)


