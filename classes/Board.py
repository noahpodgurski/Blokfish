import numpy as np

class Board:
	def __init__(self):
		self.n = 20 #square side of board
		self.tiles = [[0 for _ in range(self.n)] for _ in range(self.n)]
		self.gameOver = False
		self.boardRotation = 0 #player '0' in top left

	def rotate(self):
		#transpose
		tileArray = np.transpose(self.tiles)
		
		#reverse columns
		for x in range(self.n):
			for y in range(self.n):
				if y >= self.n / 2:
					break
				# print(f"swapping {tileArray[y][x]} with {tileArray[self.h-1-y][x]}")
				# print(f"{self.h-1-y}")
				tmp = tileArray[y][x]
				tileArray[y][x] = tileArray[self.n-1-y][x]
				tileArray[self.n-1-y][x] = tmp
		self.tiles = tileArray

	def __repr__(self):
		msg = ""
		for y in range(self.n):
			for x in range(self.n):
				if self.tiles[y][x] != 0:
					msg += str(self.tiles[y][x])
				else:
					msg += '.'
				if x == self.n-1:
					msg += '\n'
		return msg
