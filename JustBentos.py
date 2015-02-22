import requests 
from bs4 import BeautifulSoup

page_number = 0
#There is a total of 4 pages
for i in range(4):
	url = "http://justbento.com/recipes?page={}".format(page_number)

	try:
		r = requests.get(url)
	except:
		"Exceed page limit:"
		print page_number, " is max"

	soup = BeautifulSoup(r.content)

	g_data = soup.find_all("td", {"class": "view-field view-field-node-title"})

	for item in g_data:
		with open("Bento_Log.txt", "a") as f:

			recipe_name = item.text
			recipe_url = item.find("a").get("href")
			r_ingredients = requests.get("http://justbento.com" + recipe_url)
			soup_ingredients =  BeautifulSoup(r_ingredients.content)

			#writes title and url
			try:
				f.write("Recipe Name: " + recipe_name + "\n" + "Recipe URL: http://justbento.com" + recipe_url + "\n\n")
			except:
				"Unable to write Title, Url"

			lists_on_page = soup_ingredients.find_all("li")

			for item in lists_on_page:
				try:
					#Needed exception on "1 egg" because it is in side bar and will appaer almost everytime
					if item.text[0].isdigit() and item.text != "1 egg tamagoyaki (Japanese omelette)":
						f.write(item.text + "\n")
				except:
					pass
		

			for line in soup_ingredients.find_all("span", {"rel": "v:ingredient"}):
				ingredient = line.text.strip()
				try:
					f.write(ingredient + "\n")
				except:
					pass
				

			f.write("\n" + "-" * 72 + "\n")

	page_number += 1	
