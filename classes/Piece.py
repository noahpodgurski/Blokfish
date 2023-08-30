import numpy as np
from .Coords import Coords
from python.id import id
import copy

class Dims:
	def __init__(self, w, h):
		self.w = w
		self.h = h

	def __repr__(self):
		return f"Dims({self.w}, {self.h})"
	
def findOffsets(w, h, corners):
	offsets = []
	
	for y in range(h):
		for x in range(w):
			for corner in corners:
				if corner.x+1 == x and corner.y+1 == y:
				# if tileArray[y][x] == 1:
					offsets.append(Coords(x, y))
					break
	return offsets

class Piece:
	def __init__(self, w, h, color, tileArray, isUselessToFlip=False, maxRotations=4):
		self.id = id()
		self.w = w
		self.h = h
		self.tileArray = np.array(tileArray) # [[0, 0], [0, 1]] ##
		self.color = color
		self.coords = None
		self.placed = False
		self.placedRotationIndex = None
		self.isUselessToFlip = isUselessToFlip
		self.maxRotations = maxRotations
		self.isUselessToRotate = maxRotations == 1

		# get # of tiles
		self.numTiles = 0
		for y in range(self.h):
			for x in range(self.w):
				if self.tileArray[y][x] == self.color:
					self.numTiles += 1
		
		self.rotationTileArray = [copy.deepcopy(self.tileArray)]
		self.rotationDims:list[Dims] = [Dims(self.w, self.h)]
		# self.rotationOffsets = [findOffsets(self.w, self.h, self.getCorners(0))]
		
		#add all rotation possibilities to arrays
		if not self.isUselessToRotate:
			for i in range(self.maxRotations-1):
				# print('adding???')
				# print('here')
				# print(self)
				# print(self.isUselessToRotate)
				tmp = self.h
				self.h = self.w
				self.w = tmp
				tileArray = copy.deepcopy(self.rotationTileArray[-1])
				tileArray = self.rotate(tileArray, i)
				self.rotationDims.append(Dims(self.rotationDims[-1].h, self.rotationDims[-1].w))
				self.rotationTileArray.append(tileArray)
		

		if not self.isUselessToFlip:
			tileArray = copy.deepcopy(self.rotationTileArray[0])
			self.rotationDims.append(copy.deepcopy(self.rotationDims[0]))
			tileArray = self.flip(tileArray, 0)
			self.rotationTileArray.append(tileArray)
			for i in range(self.maxRotations-1):
				#flipped
				tmp = self.h
				self.h = self.w
				self.w = tmp
				tileArray = copy.deepcopy(self.rotationTileArray[-1])
				tileArray = self.rotate(tileArray, i+self.maxRotations)
				self.rotationDims.append(Dims(self.rotationDims[-1].h, self.rotationDims[-1].w))
				self.rotationTileArray.append(tileArray)

			
			
			# find offsets
			# self.rotationOffsets.append(findOffsets(self.rotationDims[-1].w, self.rotationDims[-1].h, self.getCorners(i+1)))
		
		# self.flip()
		# self.rotationTile


	def rotate(self, tileArray, rotationIndex):
		#transpose
		tileArray = np.transpose(tileArray)
		
		#reverse columns
		selfW = self.rotationDims[rotationIndex].h
		selfH = self.rotationDims[rotationIndex].w
		for x in range(selfW):
			for y in range(selfH):
				if y >= selfH / 2:
					break
				# print(f"swapping {tileArray[y][x]} with {tileArray[selfH-1-y][x]}")
				# print(f"{selfH-1-y}")
				tmp = tileArray[y][x]
				tileArray[y][x] = tileArray[selfH-1-y][x]
				tileArray[selfH-1-y][x] = tmp
		return tileArray

	# ???
	def flip(self, tileArray, rotationIndex):
		for y in range(self.rotationDims[rotationIndex].h):
			tileArray[y] = tileArray[y][::-1]
		return tileArray

	def getCorners(self, rotationIndex):
		# [-1, -1] (top left)
		corners:list[Coords] = []
		for y in range(self.rotationDims[rotationIndex].h):
			for x in range(self.rotationDims[rotationIndex].w):
				# print(self.rotationTileArray[rotationIndex])
				tile = self.rotationTileArray[rotationIndex][y][x]
				# print(f"{tile=}")
				if tile != 1:
					continue
				
				top = y-1 >= 0 and self.rotationTileArray[rotationIndex][y-1][x]
				left = x-1 >= 0 and self.rotationTileArray[rotationIndex][y][x-1]
				bot = y+1 <= self.rotationDims[rotationIndex].h-1 and self.rotationTileArray[rotationIndex][y+1][x]
				right = x+1 <= self.rotationDims[rotationIndex].w-1 and self.rotationTileArray[rotationIndex][y][x+1]
				# print(f"{top=}")
				# print(f"{left=}")
				# print(f"{bot=}")
				# print(f"{right=}")

				if top != 1 and left != 1:
					# if x-1 < 0 or y-1 < 0:
					# 	continue
					# print(f"1. appending: ${Coords(x-1, y-1)}")
					corners.append(Coords(x-1, y-1))
				if top != 1 and right != 1:
					# if x+1 > self.w or y-1 < 0:
					# 	continue
					# print(f"2. appending: ${Coords(x+1, y-1)}")
					corners.append(Coords(x+1, y-1))
				if bot != 1 and left != 1:
					# if x-1 < 0 or y+1 > self.h:
					# 	continue
					# print(f"3. appending: ${Coords(x-1, y+1)}")
					corners.append(Coords(x-1, y+1))
				if bot != 1 and right != 1:
					# if x+1 > self.w or y+1 > self.h:
					# 	continue
					# print(f"4. appending: ${Coords(x+1, y+1)}")
					corners.append(Coords(x+1, y+1))


		return corners
	
	def getAttachingCorners(self, rotationIndex):
		attachingCorners:list[Coords] = []
		corners = self.getCorners(rotationIndex)
		
		# [(0, -1), (3, -1), (3, 1), (-1, 1), (-1, 3), (2, 3)]
		#get min x for each row
		for i in range(-1, self.rotationDims[rotationIndex].h):
			minX = 999999
			tmpCorner = None
			for corner in corners:
				if corner.y == i and corner.x < minX:
					minX = corner.x
					tmpCorner = corner
			if tmpCorner:
				self.rotationOffsets[rotationIndex] = tmpCorner
				# attachingCorners.append(tmpCorner)

		print(f"{self.rotationOffsets=}")
		return attachingCorners

	def __repr__(self):
		msg = ""
		for y in range(len(self.tileArray)):
			for x in range(len(self.tileArray[0])):
				if self.tileArray[y][x] == 1:
					msg += "#"
				else:
					msg += '.'
				if x == self.w-1:
					msg += '\n'
		return msg[:-1]
	