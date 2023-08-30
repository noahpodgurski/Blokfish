class Coords:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def rotate(self):
		# x' = xcos(theta) - ysin(theta)
		# y' = xsin(theta) + ycos(theta)

		# cos(theta) = -0.44807361613
		# sin(theta) = 0.8939966636
		c = 0
		s = 1

		self.x -= 10
		self.y -= 10

		# print(self)

		xP = (self.y*s)
		yP = (-self.x*s)

		self.x = xP
		self.y = yP
		# print(self)

		# self.x = min(19, self.x+10)
		# self.y = min(19, self.y+10)
		self.x += 10
		self.y += 10

		# if self.x == 20:
		# 	self.x = 19
		# if self.y == 20:
		# 	self.y = 19

		# 0 0 -> 0 19
		# 5 0 -> 0 5
		# 5 5 -> 5 14
		# 10 0 -> 0 10
		# 10 10 -> 10 10

	def __repr__(self):
		return f"({self.x}, {self.y})"
	
# if __name__ == "__main__":
	# x = Coords(0, 0) # 0 19
	# x = Coords(0, 5) # 5 19
	# x = Coords(10, 10) # 1010
	# x = Coords(5, 10) # 10 14
	# x = Coords(5, 15)
	# x = Coords(19, 0)
	# x = Coords(5, 5)
	# print(x)
	# x.rotate()
	# print(x)