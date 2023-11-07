from dataclasses import dataclass
from SaladDraw import SaladCreator
from typing import List

Mapping = {
	"Size": {
		"Large": "LRG",
		"Regular": "REG",
		"Mini": "MINI"
		},
	"Protein": {
		"Chicken": "CHICKEN",
		"Halloumi": "HALLOUMI",
		"Tempeh": "TEMPEH",
		"Goat Ch.": ['GOAT' , 'CH.'],
		"Avocado": "AVOCADO",
		"Kimchi": "KIMCHI",
		"Sashimi": "SASHIMI",
		},
	"Dressing": {
		"Teriyaki Mayo": ['TERIYAKI' , 'MAYO'],
		"Smoked Chilli": ['SMOKED' , 'CHILLI'],
		"Lemon Pesto": ['LEMON' , 'PESTO' ],
		"Balsamic": "BALSAMIC",
		"Lemon Must.": ['LEMON' , 'MUST.'],
		"Siracha Mayo": ['SRIRACHA' , 'MAYO'],
		"Honey & Must.": "HONEY&MUST.",
		"Ponzu": "PONZU",
		},
	"Sprinkles": {
		"Croutons" : "CROUTONS",
		"Seeds" : "SEEDS",
		"Crispy Onion" : ['CRISPY' , 'ONION'],
		"Chilli Flakes" : ['CHILLI' , 'FLAKES'],

		}
	}







class Dots:
	HALF_SIZE = 436
	WHOLE_SIZE = 492
	DOUBLE_SIZE = 545

	Protein_YCoords = {
		"Chicken": 100 ,
		"Halloumi": 175 ,
		"Tempeh": 245 ,
		"Goat Ch.": 325 ,
		"Avocado": 400 ,
		"Kimchi": 475 ,
		"Sashimi": 545 ,
		}

	DOT_Locations = {
		"Dressing": {
			"Teriyaki Mayo": (680 , 85) ,
			"Smoked Chilli": (680 , 125) ,
			"Lemon Pesto": (680 , 168) ,
			"Balsamic": (680 , 210) ,
			"Lemon Must.": (680 , 252) ,
			"Siracha Mayo": (680 , 292) ,
			"Honey & Must.": (680 , 335) ,
			"Ponzu": (680 , 377) ,
			} ,
		"Sprinkles": {
			"Croutons": (680 , 439) ,
			"Seeds": (680 , 468) ,
			"Crispy Onion": (680 , 500) ,
			"Chilli Flakes": (680 , 532) ,
			}
		}

	@staticmethod
	def getProteinSize(Size):
		if Size == "1/2":
			return Dots.HALF_SIZE
		elif Size == "1":
			return Dots.WHOLE_SIZE
		elif Size == "2":
			return Dots.DOUBLE_SIZE
	@staticmethod
	def getProteinType(Name):
		return Dots.Protein_YCoords.get(Name)

	@staticmethod
	def getDressingDot(Name):
		return Dots.DOT_Locations.get("Dressing").get(Name)
	@staticmethod
	def getSprinklesDot(Name):
		return Dots.DOT_Locations.get("Sprinkles").get(Name)


protein_sizes = ["1/2" , "1" , "2" ]

@dataclass
class Protein:
	Name : str
	Size : str # ["1/2" , "1" , "2" ]

	def __repr__(self):
		return f"{self.Size} {self.Name}"

@dataclass
class Salad:
	Size: str
	Proteins: List[Protein]
	Dressings: List[str]
	Sprinkles: List[str]

	Quantity : int = 1

	def getSize (self):
		return Mapping.get("Size" , { }).get(self.Size)

	def getProteinDot(self):
		return [( Dots.getProteinSize(Protein.Size) , Dots.getProteinType(Protein.Name)) for Protein in self.Proteins]

	def getDressingDot(self):
		return [Dots.getDressingDot(Name) for Name in self.Dressings ]
	def getSprinklesDot(self):
		return [Dots.getSprinklesDot(Name) for Name in self.Sprinkles ]

	def getDressingsNames(self):
		return self.Dressings

	def getSprinklesNames(self):
		return self.Dressings

if  __name__ == "__main__":
	Salad_Example = Salad(
		Size = "Large" ,
		Proteins = [
			Protein(Name = "Chicken" , Size = "1/2") ,
			Protein(Name = "Halloumi" , Size = "1/2") ,
			Protein(Name = "Avocado" , Size = "2") ,

			] ,
		Dressings = [ "Ponzu" ,
		              "Smoked Chilli" ,
		              "Lemon Pesto" ,
		              "Siracha Mayo" ,
		              "Honey & Must." ,

		              ] ,
		Sprinkles = [ "Croutons" ]
		)

	Salad_Example_2 = Salad(
		Size = "Mini" ,
		Proteins = [
			Protein(Name = "Goat Ch." , Size = "2") ,
			Protein(Name = "Tempeh" , Size = "2")
			] ,
		Dressings = [ "Honey & Must." , "Balsamic" ] ,
		Sprinkles = [ "Seeds" ] ,
		)

	Salad_Example_3 = Salad(
		Size = "Regular" ,
		Proteins = [
			Protein(Name = "Kimchi" , Size = "1") ,
			Protein(Name = "Chicken" , Size = "2") ,

			] ,
		Dressings = [ "Ponzu" ] ,
		Sprinkles = [
			"Chilli Flakes" ,
			"Seeds" ,
			"Crispy Onion"
			]
		)

	pdfInstance = SaladCreator(Salad = Salad_Example)
	pdfInstance.run()
	# pdfInstance.image # This is the PIL Image
	pdfInstance.save("annotated_image.jpg")
