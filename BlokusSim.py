"""BLACKJACK SIM"""

from render import render
from classes.Board import Board
from classes.Piece import Piece
from classes.Coords import Coords
from classes.Move import Move
from classes.Player import Player
import asyncio
import random
import copy

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
	
	def render(self, cb=None):
		return render(self.players, self.board, cb)

# if __name__ == "__main__":
	# 			await asyncio.sleep(.1)
	# 	print(moves)
	# 	print('here')
	# 	board.gameOver = True

	# async def playGame():
	# 	LOSE_ARRAY = [0] * len(players)
	# 	moves = [1] * len(players)
	# 	while moves != LOSE_ARRAY:
	# 		for i, player in enumerate(players):
	# 			legalMoves = player.getLegalMoves()
	# 			moves[i] = len(legalMoves)
	# 			print(moves)

	# 			if len(legalMoves) > 0:
	# 				player.place(random.choice(legalMoves))

	# 			await asyncio.sleep(.1)
	# 	print(moves)
	# 	print('here')
	# 	board.gameOver = True

	# render(players, board, playGame)