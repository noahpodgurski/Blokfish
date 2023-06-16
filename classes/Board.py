class Board:
	def __init__(self):
		self.n = 20 #square side of board
		self.tiles = [[0 for _ in range(self.n)] for _ in range(self.n)]
		self.gameOver = False

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
