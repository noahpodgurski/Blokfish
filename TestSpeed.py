"""BLACKJACK SIM"""

from classes.Board import Board
from classes.Piece import Piece
from classes.Coords import Coords
from classes.Move import Move
from classes.Player import Player
import asyncio
from render import Render
import random
import copy
import time
import numpy as np

printing = False

# board = Board()
# players = [Player(1, Coords(0, 0), board), Player(2, Coords(19, 0), board)]
NUM_PLAYERS = 4
LOSE_ARRAY = [0] * NUM_PLAYERS


class Blokus:
	def __init__(self):
		self.wins = [0] * NUM_PLAYERS
		self.createGame()
	
	def reset(self):
		self.createGame()

	def createGame(self):
		self.board = Board()	
		self.players = [Player(1, Coords(0, 0), self.board), Player(2, Coords(19, 0), self.board), Player(3, Coords(19, 19), self.board), Player(4, Coords(0, 19), self.board)]
		self.moves = [1] * NUM_PLAYERS
		self.turn = 0 # 0 1 2 3 -> 0 1 2 3

	def rotateBoard(self):
		self.board.rotate()

		#update all piece coordinates
		for player in self.players:
			for piece in player.pieces:
				if piece.placed:
					# do this? not sure if necessary
					tmp = piece.w
					piece.w = piece.h
					piece.h = tmp

					piece.placedRotationIndex = (piece.placedRotationIndex + 1) % 4
					#update piece coords
					piece.coords.rotate()
					piece.coords.y -= piece.rotationDims[piece.placedRotationIndex].h

		
		# update player's starting coords
		tmp = self.players[0].startCorner
		self.players[0].startCorner = self.players[3].startCorner
		self.players[3].startCorner = self.players[2].startCorner
		self.players[2].startCorner = self.players[1].startCorner
		self.players[1].startCorner = tmp

	def update(self):
		if self.moves == LOSE_ARRAY:
			self.board.gameOver = True

	def playMove(self, playerIndex: int, move: Move):
		assert self.turn == playerIndex
		self.players[playerIndex].place(move)
		self.turn = (self.turn + 1) % NUM_PLAYERS

	def Pass(self, playerIndex: int):
		assert self.turn == playerIndex
		self.turn = (self.turn + 1) % NUM_PLAYERS

	def isTie(self):
		min = 9999
		for player in self.players:
			x = player.getRemainingSquares()
			if x < min:
				min = x
			elif x == min:
				print("TIE")
				return True
		return False		

	def getWinner(self):
		winner = min(self.players, key=lambda player: player.getRemainingSquares())
		for i, player in enumerate(self.players):
			if player.id == winner.id:
				self.wins[i] += 1
		# print(self.wins)
		return winner
	
	# def render(self, cb=None):
	# 	return render(self.players, self.board, cb)

	async def playGame(self):
		LOSE_ARRAY = [0] * len(self.players)
		moves = [1] * len(self.players)
		while moves != LOSE_ARRAY:
			for i, player in enumerate(self.players):
				legalMoves = player.getLegalMoves()
				moves[i] = len(legalMoves)
				print(moves)

				if len(legalMoves) > 0:
					player.place(random.choice(legalMoves))

				await asyncio.sleep(.1)
		print(moves)
		print('here')
		self.board.gameOver = True

if __name__ == "__main__":
				# await asyncio.sleep(.1)
		# print(moves)
		# print('here')
		# board.gameOver = True


	game = Blokus()
	# game.playMove(0, Move(game.players[0].pieces[0], 0, Coords(0, 0)))
	# game.Pass(1)
	# game.Pass(2)
	# game.Pass(3)
	# game.playMove(0, Move(game.players[0].pieces[1], 0, Coords(1, 1)))
	# print(game.board)
	# game.rotateBoard()
	# print(game.board)

	# Render(game, game.playGame)

	t = time.time()

	piece = game.players[0].pieces[10]
	for i in range(1000000):
		index = i % piece.maxRotations
		piece.rotate(piece.rotationTileArray[index], index)

	print(f"Took {time.time()-t} seconds")

