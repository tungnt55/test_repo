import sys
import subprocess


def densecap_from_file(file_name):
	pro = subprocess.Popen(['th','run_model_captions.lua','-input_image',file_name],shell=False,stdout=subprocess.PIPE)
	#pro = subprocess.Popen('th run_model_captions.lua -input_image imgs/theta/theta-pic-01.jpg',shell=True,stdout=subprocess.PIPE)
	pro.wait()	
	print("\nfinish captioning image with DenseCap.")
	print("----------------------------------------")
	return

def main(args):
	# remove shell=False in the line below to print output 
	#pro = subprocess.Popen(['th','run_model_captions.lua','-input_image','imgs/theta/theta-pic-01.jpg'],shell=False,stdout=subprocess.PIPE)
	pro = subprocess.Popen(['th','run_model_captions.lua','-input_dir','imgs/theta/'],shell=False,stdout=subprocess.PIPE)
	#pro = subprocess.Popen('th run_model_captions.lua -input_image imgs/theta/theta-pic-01.jpg',shell=True,stdout=subprocess.PIPE)
	pro.wait()	

	print("finish captioning image with DenseCap.")
	return

if __name__ == '__main__':
	main(sys.argv)
