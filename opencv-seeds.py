import numpy as np
import cv2
import sys

NBR_ITERATIONS = 10
WAITING  = "-\\|//"

if __name__ == '__main__':

	if len(sys.argv) < 3:
		print("[!] %s <file path> <number of clusters>" % sys.argv[0])
		print("example: %s dog.png 400" % sys.argv[0])
		sys.exit(1)

	filePath = sys.argv[1]
	nbr_superpixels = int(sys.argv[2])

	seeds = None
	display_mode = 0
	prior = 2
	nbr_levels = 4
	nbr_histogram_bins = 5

	img = cv2.imread(filePath, 1)

	converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	height, width, channels = converted_img.shape
	nbr_superpixels = 400

	seeds = cv2.ximgproc.createSuperpixelSEEDS(width, height, channels, nbr_superpixels, nbr_levels, prior, nbr_histogram_bins)
	color_img = np.zeros((height, width, 3), np.uint8)
	color_img[:] = (0, 0, 255)

	for n in range(NBR_ITERATIONS):
		print("\r[%s] iteration %d (%d %%)..." % (WAITING[n % 4], n, (100*n/NBR_ITERATIONS))),
		sys.stdout.flush()
		seeds.iterate(converted_img, NBR_ITERATIONS)
	print("done!")

	mask = seeds.getLabelContourMask(False)

	# stitch foreground & background together
	mask_inv = cv2.bitwise_not(mask)
	result_bg = cv2.bitwise_and(img, img, mask=mask_inv)
	result_fg = cv2.bitwise_and(color_img, color_img, mask=mask)
	
	result = cv2.add(result_bg, result_fg)

	pointIndex = filePath.rfind('.')
	filePath = filePath[:pointIndex] + "-seeds-" + str(nbr_superpixels) + filePath[pointIndex:]
	print("[-] saving result in file %s" % filePath)
	cv2.imwrite(filePath, result)
