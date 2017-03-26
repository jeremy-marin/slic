import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import cv2
import math
import sys


NBR_ITERATION = 10
WAITING  = "-\\|//"

m = 40



# def enforceConnectivity(img, centers):
# 	height, width, n = img.shape
# 	label = 0
# 	adjLabel = 0
# 	lims = height * width / len(centers)
# 	dx4 = [-1, 0, 1, 0]
# 	dy4 = [0, -1, 0, 1]

# 	new_centers = np.ones((height, width), dtype=np.int)
# 	new_centers = -1 * new_centers
# 	print(new_centers)

# 	elements = []
# 	for j in range(height):
# 		for i in range(width):
# 			if new_centers[j, i] == -1:
# 				elements = []
# 				elements.append((j, i))
# 				for dx, dy in zip(dx4, dy4):
# 					x = elements[0][1] + dx
# 					y = elements[0][0] + dy
# 					if x >= 0 and x < width and y >= 0 and y < height and new_centers[y, x] >= 0:
# 						adjLabel = new_centers[y, x]
# 			count = 1
# 			c = 0
# 			while c < count:
# 				for dx, dy in zip(dx4, dy4):
# 					x = elements[c][1] + dx
# 					y = elements[c][0] + dy
# 					if x >= 0 and x < width and y >= 0 and y < height:
# 						if new_centers[y, x] == -1 and centers[j, i] == centers[y ,x]:
# 							elements.append((y, x))
# 							new_centers[y, x] = label
# 							count += 1
# 				c += 1
# 			if count <= lims >> 2:
# 				for c in range(count):
# 					new_centers[elements[c]] = adjLabel
# 				label -= 1
# 			label += 1
# 	return new_centers


def d(p1, p2, S, m):
	dc_2 = (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2
	ds_2 = (p2[3] - p1[3])**2 + (p2[4] - p1[4])**2
	D    = math.sqrt( dc_2 + ds_2 * (m**2/S**2) )
	return D


def displayCenters(img, centers, color):
	print("[-] displaying %d centers" % len(centers))
	for c in centers:
		cv2.circle(img, (c[4], c[3]), 1, color, -1)
	return img


def displayContours(img, labels, color):
	print("[-] displaying contours")
	height, width = img.shape[:2]
	neighbors = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
	for y in range(height):
		for x in range(width):
			lyx = labels[y, x]
			count = 0
			for u, v in neighbors:
				if x + u >= 0 and x + u < width and y + v >= 0 and y + v < height:
					lvu = labels[y + v, x + u]
					if lyx != lvu:
						count += 1
			if count >= 2:
				img[y, x] = color
	return img

def displayMeanImage(labels, centers):
	height, width = labels.shape[:2]
	result = np.zeros((height, width, 3), dtype=np.uint8)
	for y in range(height):
		for x in range(width):
			l = labels[y, x]
			result[y, x] = [centers[l][0], centers[l][1], centers[l][2]]
	return convert_Lab_to_BGR(result)


def convert_BGR_to_Lab(img):
	print("[-] conversion to Lab color space")
	return cv2.cvtColor(img, cv2.COLOR_BGR2LAB)


def convert_Lab_to_BGR(img):
	print("[-] conversion to bgr color space")
	return cv2.cvtColor(img, cv2.COLOR_LAB2BGR)


def loadImg(path, k):
	img = cv2.imread(path, 1)
	print("[-] loading image %s [h=%d, w=%d]" % (path, img.shape[0], img.shape[1]))

	print("[*] number of clusters: k = %d" % k)
	N = img.shape[0] * img.shape[1]
	print("[*] number of pixels: N = %d" % N)
	S = int(math.sqrt(N/k) + 1)
	print("[*] grid size: S = %d" % S)
	
	return convert_BGR_to_Lab(img), N, S


def initData(img, S):
	height, width = img.shape[:2]

	# initialize labels
	labels = np.ones((height, width), dtype=np.int)
	labels = -1 * labels

	# initialize distances
	distances = np.ones((height, width), dtype=np.float)
	distances = 999999 * distances

	# initialize centers [L, a, b, y, x, count]
	centers = []
	for y in range(S/2, height, S):
		for x in range(S/2 , width, S):
			p = img[y, x]
			centers.append([int(p[0]), int(p[1]), int(p[2]), y, x, 0])
	print("[*] %d centers initialized" % len(centers))
	return distances, labels, centers


def computeSuperPixels(img, distances, labels, centers):
	height, width = img.shape[:2]
	for n in range(1, NBR_ITERATION):
		print("\r[%s] iteration %d (%d %%)..." % (WAITING[n % 4], n, (100*n/NBR_ITERATION))),
		sys.stdout.flush()
		for i in range(len(centers)):
			c = centers[i]
			ymin = max(0, c[3] - S)
			ymax = min(height, c[3] + S)
			xmin = max(0, c[4] - S)
			xmax = min(width, c[4] + S)
			for y in range(ymin, ymax):
				for x in range(xmin, xmax):
					p = img[y, x]
					v = [int(p[0]), int(p[1]), int(p[2]), y, x]
					D = d(c, v, S, m)
					if D <= distances[y, x]:
						distances[y, x] = D
						labels[y, x] = i

		for c in centers:
			c[0], c[1], c[2], c[3], c[4], c[5] = 0, 0, 0, 0, 0, 0

		for y in range(height):
			for x in range(width):
				p = img[y, x]
				label = labels[y, x]
				centers[label][0] += p[0]
				centers[label][1] += p[1]
				centers[label][2] += p[2]
				centers[label][3] += y
				centers[label][4] += x
				centers[label][5] += 1

		for i in range(len(centers)):
			c = centers[i]
			c[0] = c[0] / c[5]
			c[1] = c[1] / c[5]
			c[2] = c[2] / c[5]
			c[3] = c[3] / c[5]
			c[4] = c[4] / c[5]

	print("done!")
	return distances, labels, centers


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("[!] %s <file path> <number of clusters> [1=displayContours | 2=displayCenters | 3=displayContours&Centers]" % sys.argv[0])
		print("example: %s dog.png 400 3" % sys.argv[0])
		sys.exit(1)

	filePath = sys.argv[1]
	k = int(sys.argv[2])

	option = 0
	if len(sys.argv) >= 4:
		option = int(sys.argv[3])
		print("[*] option = %d" % option)

	LabImg, N, S = loadImg(filePath, k)
	distances, labels, centers = initData(LabImg, S)
	distances, labels, centers = computeSuperPixels(LabImg, distances, labels, centers)

	result = displayMeanImage(labels, centers)
	if option in [1, 3]:
		result = displayContours(result, labels, [0, 0, 0])
	if option in [2, 3]:
		result = displayCenters(result, centers, [0, 0, 0])

	pointIndex = filePath.rfind('.')
	filePath = filePath[:pointIndex] + "-slic-" + str(k) + "-" + str(option) + filePath[pointIndex:]
	print("[-] saving result in file %s" % filePath)
	cv2.imwrite(filePath, result)
