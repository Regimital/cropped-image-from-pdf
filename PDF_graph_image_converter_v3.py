import fitz
import os
from pdf2image import convert_from_path
from PIL import Image


for f in os.listdir('.'):
	if f.endswith('.pdf'): #use just PDF files
		fn, fext =  os.path.splitext(f) #split the filename into name and extensions for JPEG naming
		doc = fitz.open(f)
		control_score = True #add control score to break out of loop after meeting criterion
		page_number = 0 #keep track of page number
		for page in doc:
			areas = page.searchFor("UV Detector: 254 Nm", hit_max = 1) #look for this specific phrase
			for element in areas:
				x0, y0, x1, y1 = element.x0, element.y0, element.x1, element.y1 #assign the coordinates
				control_score = False
			if control_score == False:
				break #break out of the loop when phrase found
			page_number += 1 #increase the page number in case phrase not found

		image_name = str(fn) + '.jpg'
		pages = convert_from_path(f, dpi=500,first_page=page_number,last_page=page_number+1) #convert the PDF to JPEG by pdf2image
		selected_page = pages[page_number]
		selected_page.save(image_name,'JPEG')

		im = Image.open(image_name)
		dimensions = (x0*(4250/612), y0*(5500/792), x1*(4250/612)+3000, y1*(5500/792)+950)
		cropped = im.crop(dimensions)
		cropped.save(image_name)

		print(f"{image_name} has been generated.") #Just to check the file chosen
		print(f"The graph was found on page {page_number} and the dimensions are: {x0,y0,x1,y1}.\n") #check the dimensions

