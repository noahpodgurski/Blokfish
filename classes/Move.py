from .Piece import Piece
from .Coords import Coords

class Move:
	def __init__(self, piece:Piece, rotationIndex: int, coords:Coords):
		self.piece = piece
		self.rotationIndex = rotationIndex
		self.coords = coords
		
        #
		self.tileArray = self.piece.rotationTileArray[rotationIndex]
		self.dims = self.piece.rotationDims[rotationIndex]

	def __repr__(self):
		return f"\n===MOVE===\n{self.piece} at ({self.coords.x}, {self.coords.y})."
		# return f"\n===MOVE===\n{self.piece} at ({self.coords.x}, {self.coords.y}). Offsets: {self.offsets})"
