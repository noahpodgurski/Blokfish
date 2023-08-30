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
				squares += piece.numTiles
		return squares

	def place(self, move: Move):
		assert self.isValidMove(move)
		assert self.isLegalMove(move)
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
		touchingCorner = True
		if move.coords.x < 0 or move.coords.x >= self.board.n or move.coords.y < 0 or move.coords.y >= self.board.n:
			return False

		if self.moveNumber == 0:
			touchingCorner = False
		
		# print(move)
		# print(move.dims.w)
		# print(move.dims.h)
		for y in range(move.dims.h):
			for x in range(move.dims.w):
				# Y = move.coords.y+y+move.offset.y
				# X = move.coords.x+x+move.offset.x
				Y = move.coords.y+y
				X = move.coords.x+x

				if Y < self.board.n and X < self.board.n and Y >= 0 and X >= 0:
					if self.moveNumber == 0:
						# print(move.tileArray)
						if move.tileArray[y][x] != 0 and Y == self.startCorner.y and X == self.startCorner.x:
							touchingCorner = True
					#touching another piece
					if self.board.tiles[Y][X] != 0:
						return False
				elif move.tileArray[y][x] != 0:
					return False
					
		return touchingCorner
				
	# RETURNS ALL MOVE POSSIBILITIES (NOT ONES THAT COVER TILES)
	def getPossibleMoves(self, piece: Piece, rotationIndex: int):
		moves:list[Move] = []
		if self.moveNumber == 0:
			# no pieces placed yet
			bop = Coords(min(self.board.n, max(0, self.startCorner.x-piece.rotationDims[rotationIndex].w-1)), min(self.board.n, max(0, self.startCorner.y-piece.rotationDims[rotationIndex].h-1)))
			
			for y in range(bop.y-4, bop.y+4):
				for x in range(bop.x-4, bop.x+4):
					move = Move(piece, rotationIndex, Coords(x, y))
					# print(move)
					if self.isValidMove(move) and self.isLegalMove(move):
						# if self.startCorner.x == 19 and self.startCorner.y == 19:
						# 	print(move)
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
		trigg = 0
		# if self.startCorner.x == 19 and self.startCorner.y == 19:
		# 	print(move)
		for y in range(move.dims.h):
			for x in range(move.dims.w):

				Y = move.coords.y+y
				X = move.coords.x+x

				#goes outside bounds
				if (X < 0 or Y < 0 or X >= self.board.n or Y >= self.board.n) and move.tileArray[y][x] == 1:
					return False

				trigg += 1
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
						if self.moveNumber == 0 or topLeft or topRight or botLeft or botRight:
							touching = True
		# 	print('here')
		# print(f"{trigg=}")		
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
	
	# return all legal moves for pieces passed
	def getLegalMovesExactPieces(self, pieces):
		legalMoves:list[Move] = []
		myPieceIds = [piece.id for piece in self.pieces]
		for piece in pieces:
			if not piece.placed and piece.id in myPieceIds:
				for i in range(len(piece.rotationTileArray)):
				# for i in range(len(piece.rotationTileArray)):
					legalMoves += self.getPossibleMoves(piece, i)
					
		# print(legalMoves)
		return legalMoves
				
	def __repr__(self):
		return self.name