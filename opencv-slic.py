import numpy as np
import cv2
import sys

NBR_ITERATIONS = 10
WAITING  = "-\\|//"

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("[!] %s <file path> [region_size]" % sys.argv[0])
		print("example: %s dog.png 20" % sys.argv[0])
		sys.exit(1)

	region_size = 20
	filePath = sys.argv[1]
	if (len(sys.argv) >= 2):
		region_size = int(sys.argv[2])

	slic = None
	ruler = 40

	img = cv2.imread(filePath, 1)

	converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

	slic = cv2.ximgproc.createSuperpixelSLIC(converted_img, cv2.ximgproc.SLIC, region_size, ruler)
	color_img = np.zeros(img.shape, np.uint8)
	color_img[:] = (0, 0, 0)

	for n in range(NBR_ITERATIONS):
		print("\r[%s] iteration %d (%d %%)..." % (WAITING[n % 4], n, (100*n/NBR_ITERATIONS))),
		sys.stdout.flush()
		slic.iterate(NBR_ITERATIONS)
	print("done!")

	print("[*] %d superpixels have been generated" % slic.getNumberOfSuperpixels())

	slic.enforceLabelConnectivity()
	mask = slic.getLabelContourMask(False)

	# stitch foreground & background together
	mask_inv = cv2.bitwise_not(mask)
	result_bg = cv2.bitwise_and(img, img, mask=mask_inv)
	result_fg = cv2.bitwise_and(color_img, color_img, mask=mask)
	
	result = cv2.add(result_bg, result_fg)

	pointIndex = filePath.rfind('.')
	filePath = filePath[:pointIndex] + "-slic-" + str(region_size) + filePath[pointIndex:]
	print("[-] saving result in file %s" % filePath)
	cv2.imwrite(filePath, result)
