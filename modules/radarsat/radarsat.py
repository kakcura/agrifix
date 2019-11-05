#----------------------------------------------------------------------
#  radarsat.py
#
# Convert and open Radarsat-1 data.
#----------------------------------------------------------------------
import gdal
from PIL import Image
import imagehash
import os
import operator

#Original Name and     => Renamed File 
#Extension
#<original name>.nvol   =>  nul_vdf.001
#<original name>.sard   =>  dat_01.001
#<original name>.sarl   =>  lea_01.001
#<original name>.sart   =>  tra_01.001
#<original name>.vol    =>  vdf_dat.001

class radarsat:
	def __init__(self):
		self.data_directory = "modules/radarsat/data/"
		self.static_images = "static/images/radarsat1/original/"

	#----------------------------------------------------------------------
	#  Do the necessary formatting on the response.
	#----------------------------------------------------------------------
	def convert_to_png(self,sard_file):
		full_path = self.data_directory + sard_file
		dataset = gdal.Open(full_path, gdal.GA_ReadOnly)
		band = dataset.GetRasterBand(1)
		img_array = band.ReadAsArray()

		im = Image.fromarray(img_array.astype('uint8'))
		im.save(self.data_directory + "output.png")

	#def merge_images(self,sard_file):
	#	gdal_merge -o ba_25k_gdal *.jpeg

	def calculate_similarity(self):
		# Pair of similar images.
		similarity_dict = {}
		for origin in os.listdir(self.static_images):
			compare_origin = os.fsdecode(origin)
			for target in os.listdir(self.static_images):
				compare_target = os.fsdecode(target)
				if compare_origin != compare_target and target not in similarity_dict:
					hash0 = imagehash.average_hash(Image.open(self.static_images + origin)) 
					hash1 = imagehash.average_hash(Image.open(self.static_images + target)) 
					cutoff = 30

					if hash0 - hash1 < cutoff:
						#images are similar
						similarity_dict[target] = origin
		return similarity_dict


