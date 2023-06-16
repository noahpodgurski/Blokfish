import copy
from .Board import Board
from .Piece import Piece
from .Coords import Coords
from .Move import Move
from consts import PIECES, PLAYER_COLOR_NAMES
import uuid

class Player:
	def __init__(self, color: int, startCorner: Coords, board: Board):
		self.id = str(uuid.uuid4())
		self.color = color # 1 2 3 4
		self.name = PLAYER_COLOR_NAMES[color-1]
		self.pieces:list[Piece] = copy.deepcopy(PIECES) #generate pieces
		
		self.moveNumber = 0
		self.startCorner = startCorner #0 top left, 1 top right, 2 bot right, 3 bot left
		self.board = board

	def getRemainingSquares(self):
		squares = 0
		for piece in self.pieces:
			if not piece.placed:
				squares += len(piece.tileArray)
		return squares

	def place(self, move: Move):
		#if rotated, find and replace piece in self.pieces with same id
		id = move.piece.id
		for i in range(len(self.pieces)):
			if self.pieces[i].id == id:
				self.pieces[i] = move.piece

		move.piece.coords = move.coords
		move.piece.placed = True
		move.piece.placedRotationIndex = move.rotationIndex
		self.moveNumber += 1

		for y in range(move.coords.y, move.coords.y+move.dims.h):
			for x in range(move.coords.x, move.coords.x+move.dims.w):
				if x < self.board.n and y < self.board.n and \
				move.tileArray[y-move.coords.y][x-move.coords.x] == 1:
					self.board.tiles[y][x] = self.color
					
	#is placed correctly (not on top of other moves)
	def isValidMove(self, move: Move):
		if self.moveNumber == 0:
			if move.coords.x != self.startCorner.x and move.coords.y != self.startCorner.y:
				return False
		
		for y in range(move.dims.h):
			for x in range(move.dims.w):
				# Y = move.coords.y+y+move.offset.y
				# X = move.coords.x+x+move.offset.x
				Y = move.coords.y+y
				X = move.coords.x+x

				if Y < self.board.n and X < self.board.n and Y >= 0 and X >= 0:
					if self.board.tiles[Y][X] != 0:
						return False
					
		# if move.piece.id == 999:
		# 	print(move.offset.x, move.offset.y)
		# 	print('move.offset')
		return True
				
	# RETURNS ALL MOVE POSSIBILITIES (NOT ONES THAT COVER TILES)
	def getPossibleMoves(self, piece: Piece, rotationIndex: int):
		moves:list[Move] = []
		if self.moveNumber == 0:
			# no pieces placed yet
			for y in range(self.board.n):
				for x in range(self.board.n):
					move = Move(piece, rotationIndex, Coords(x, y))
					if self.isValidMove(move) and self.isLegalMove(move):
						moves.append(move)
			return moves
			

		for _piece in self.pieces:
			if _piece.placed:
				#go from top left of placed piece to very bottom right of placing piece and check all
				hDiff = _piece.rotationDims[_piece.placedRotationIndex].h + piece.rotationDims[rotationIndex].h
				wDiff = _piece.rotationDims[_piece.placedRotationIndex].w + piece.rotationDims[rotationIndex].w

				for y in range(-hDiff, hDiff):
					for x in range(-wDiff, wDiff):
						move = Move(piece, rotationIndex, Coords(_piece.coords.x+x, _piece.coords.y+y))
						if self.isValidMove(move) and self.isLegalMove(move):
							moves.append(move)
				
		return moves

	# IS LEGAL (NOT ADJACENT TO SAME, OPPOSITE TO SAME)
	def isLegalMove(self, move: Move):		
		touching = False
		for y in range(move.dims.h):
			for x in range(move.dims.w):

				Y = move.coords.y+y
				X = move.coords.x+x

				if self.moveNumber == 0:
					if X >= 0 and Y >= 0 and X < self.board.n and Y < self.board.n and move.tileArray[y][x] == 1 and X == self.startCorner.x and Y == self.startCorner.y:
						return True
				
				
				#goes outside bounds
				if (X < 0 or Y < 0 or X >= self.board.n or Y >= self.board.n) and move.tileArray[y][x] == 1:
					return False
				
				if X >= 0 and Y >= 0 and X < self.board.n and Y < self.board.n and move.tileArray[y][x] == 1:
					if self.board.tiles[Y][X] == 0:
						#piece tile, ensure its not adjacent to color
						top = Y-1 >= 0 and self.board.tiles[Y-1][X] == self.color
						left = X-1 >= 0 and self.board.tiles[Y][X-1] == self.color
						bot = Y+1 < self.board.n and self.board.tiles[Y+1][X] == self.color
						right = X+1 < self.board.n and self.board.tiles[Y][X+1] == self.color

						topLeft = Y-1 >= 0 and X-1 >= 0 and self.board.tiles[Y-1][X-1] == self.color
						topRight = Y-1 >= 0 and X+1 < self.board.n and self.board.tiles[Y-1][X+1] == self.color
						botLeft = Y+1 < self.board.n and X-1 >= 0 and self.board.tiles[Y+1][X-1] == self.color
						botRight = Y+1 < self.board.n and X+1 < self.board.n and self.board.tiles[Y+1][X+1] == self.color


						#todo color
						if top or left or bot or right:
							return False
						
						#not touching any on the corners :(
						if topLeft or topRight or botLeft or botRight:
							touching = True
		return touching
	
	def getLegalMoves(self):
		legalMoves:list[Move] = []
		for piece in self.pieces:
			if not piece.placed:
				for i in range(len(piece.rotationTileArray)):
				# for i in range(len(piece.rotationTileArray)):
					legalMoves += self.getPossibleMoves(piece, i)
					
		# print(legalMoves)
		return legalMoves
				
	def __repr__(self):
		return self.name