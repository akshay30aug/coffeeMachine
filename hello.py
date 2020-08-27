from time import sleep
from threading import Thread
import json

class CoffeeMachine:
	def __init__(self,handles): # Initializing the coffee machine
		self.busy = 0
		self.handles = int(handles)
		self.ingredients = {}
		self.configBeverages = {}
		self.miningredients = {}

	def addIngredients(self,ingredients,quantities): # adding the ingredients into separate bins
		for i in range(len(ingredients)):
			if ingredients[i] in self.ingredients.keys():
				self.ingredients[ingredients[i]] += quantities[i]
			else:
				self.ingredients[ingredients[i]] = quantities[i]
		print("Ingredients added successfully in separate containers.")

	def addBeverage(self,beverage): # adding the beverage in the list of beverages being configured in the machine
		if beverage not in self.configBeverages.keys():
			self.configBeverages[beverage] = {}
			return False
		else:
			return True

	def configureBeverage(self,beverage,ingredients,quantities): # Ingredient configuration for different beverages
		if beverage not in self.configBeverages.keys():
			self.configBeverages[beverage] = {}
		for i in range(len(ingredients)):
			if ingredients[i] not in self.ingredients:
				print("This ingredient is not present in the machine. Make sure to add it before you try to brew it.\n")
			self.configBeverages[beverage][ingredients[i]] = quantities[i]
			if ingredients[i] in self.miningredients:
				self.miningredients[ingredients[i]] = max(self.miningredients[ingredients[i]],quantities[i])
			else:
				self.miningredients[ingredients[i]] = quantities[i]
		print("Quantities configured successfully for "+beverage)

	def brew(self,beverage): # checking the possibility and brewing the drink. each drink takes about 10 seconds to brew.
		if beverage not in self.configBeverages.keys():
			print("Beverage not configured in the machine\n")
			return True
		missing_ingredients = []
		for i in self.configBeverages[beverage]:
			if i not in self.ingredients.keys():
				print(beverage+" requires "+i+" which is not there in the machine. Please add the bin for the same before to attempt to bre it again.\n")
				return True
			if self.configBeverages[beverage][i] > self.ingredients[i]:
				missing_ingredients.append(i)
		if missing_ingredients:
			print(beverage + " can't be made as machine doesn't have enough "+", ".join(missing_ingredients)+"\n")
			return True
		if self.busy == self.handles:
			print("Machine is busy try later\n")
			return True
		self.busy +=1
		for i in self.configBeverages[beverage]:
			self.ingredients[i] -= self.configBeverages[beverage][i]
		print("One "+beverage+" coming in 10 second\n")
		sleep(10)
		self.busy -=1
		print("Congratulations! You have been served..... "+beverage+"\n")
				
				
class AkshayMachine:
	def __init__(self,input_type,data=""):
		if input_type == 'f':		# if we are taking input from file
			handles = data['machine']['outlets']['count_n']
			if not type(handles) == type(1):
				print("Maybe i wasn't clear. You have to enter in numerics.\n")
			elif int(handles) <= 0:
				print("Can't really have a machine without handles now can we? Let's Try again\n")
			else:
				self.cm = CoffeeMachine(handles)
				print("Let me check if that particular model is available.... Here it is!")
				self.options(input_type,data)
		else:						# if we want input from command line
			while 1:
				print("Welcome to Akshay's Coffee Machine. We will try to serve you good today. How many beverages you want parallely?\n")
				handles = input()
				if not handles.isdigit():
					print("Maybe i wasn't clear. You have to enter in numerics. No Harm no foul. Let's start again\n")
				elif int(handles) <= 0:
					print("Can't really have a machine without handles now can we? Let's Try again\n")
				else:
					self.cm = CoffeeMachine(handles)
					print("Let me check if that particular model is available.... Here it is!")
					break
			self.options(input_type,data)
	def options(self,input_type,data):
		if input_type == 'f':
			for i in data['machine']['total_items_quantity']:
				self.cm.addIngredients([i],[data['machine']['total_items_quantity'][i]])
			for i in data['machine']['beverages']:
				res = self.cm.addBeverage(i)
				if res:
					print("This beverage is already configured. Whatever ingredient you enter, if that is already configured, then it will change the quantity to new quantity. If you want to remove an ingredient, just enter 0 as quantity. You may add new ingredient as well\n")
				else:
					print("Configuring a new beverage!! Awesome!\n")
				for j in data['machine']['beverages'][i]:
					self.cm.configureBeverage(i,[j],[data['machine']['beverages'][i][j]])
			for i in data['machine']['brew']:
				Thread(target=self.cm.brew,args=(i,)).start()
				refills = []
				for i in self.cm.miningredients:
					if i in self.cm.ingredients.keys() and self.cm.miningredients[i]>self.cm.ingredients[i]:
						refills.append(i)
				if refills:
					refills = ", ".join(refills)
					print(refills+" are running low\n")
			if 'add_items_quantity' in data['machine'].keys():
				for i in data['machine']['add_items_quantity']:
					self.cm.addIngredients([i],[data['machine']['add_items_quantity'][i]])
			if 'brew_again' in data['machine'].keys():
				for i in data['machine']['brew_again']:
					Thread(target=self.cm.brew,args=(i,)).start()
					refills = []
					for i in self.cm.miningredients:
						if i in self.cm.ingredients and self.cm.miningredients[i]< self.cm.ingredients[i]:
							refills.append(i)
					if refills:
						refills = ", ".join(refills)
						print(refills+" are running low\n")
		else:
			while 1:
				print("Choose from the following options:\n\t1.\tAdd ingredients in different bins.\n\t2.\tConfigure a new Beverage.\n\t3.\tMake a beverage.\n\t4.\tCheck if we need any refill.\n\t5.\tExit.\n\n")
				choice = input(">")
				if not choice.isdigit():
					print("Choice not recognized. Try again\n\n")
				elif choice == "5":
					print("Bye Bye!!")
					break
				elif choice == "1":
					while 1:
						ingredient = input("Enter the ingredient name to add or e to exit: ")
						if ingredient == "e":
							break
						else:
							quantity = input("Enter the Quantity: ")
							if quantity.isdigit():
								self.cm.addIngredients([ingredient],[int(quantity)])
							else:
								print("Wrong input. Try Again\n")
				elif choice == "2":
					beverage = input("Enter the name of the beverage you want to configure: ")
					res = self.cm.addBeverage(beverage)
					if res:
						print("This beverage is already configured. Whatever ingredient you enter, if that is already configured, then it will change the quantity to new quantity. If you want to remove an ingredient, just enter 0 as quantity. You may add new ingredient as well\n")
					else:
						print("Configuring a new beverage!! Awesome!\n")
					while 1:
						ingredient = input("Enter the ingredient name to add/change or e to exit: ")
						if ingredient == "e":
							break
						else:
							quantity = input("Enter the Quantity: ")
							if quantity.isdigit():
								self.cm.configureBeverage(beverage,[ingredient],[int(quantity)])
							else:
								print("Wrong input. Try Again\n")
				elif choice == "3":
					beverage = input("Enter the name of the beverage you want to brew: ")
					Thread(target=self.cm.brew,args=(beverage,)).start()
				elif choice == "4":
					refills = []
					for i in self.cm.miningredients:
						if i in self.cm.ingredients.keys() and self.cm.miningredients[i]> self.cm.ingredients[i]:
							refills.append(i)
					if refills:
						refills = ", ".join(refills)
						print(refills+" are running low\n")
					else:
						print("Everything seems fine!\n")

				else:
					print("Wrong input. Try Again\n")


if __name__ == "__main__":
	input_type = input("Enter 'f' if you want the program to runs with test cases from files. For interactive session enter 'i': ")
	if input_type.lower() == 'f':
		# test_case.json checks the case with enough handles
		# test_case1.json checks for the case where machine is asked to be made of 0 handles
		# test_case2.json checks for the case where beverage being asked for is not configured in the machine
		# test_case3.json checks for the case where machine has less handles than the beverages asked in succession
		# test_case4.json checks for the case where ingredients are added again before asking for more beverages


		test_cases = ['test_case.json','test_case1.json','test_case2.json','test_case3.json','test_case4.json']
		for i in test_cases:
			with open(i,"r") as f:
				data = json.load(f)
			AkshayMachine(input_type='f',data=data)
			sleep(10)
	elif input_type.lower() == 'i':
		AkshayMachine(input_type='i',data="")
