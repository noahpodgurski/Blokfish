import pygame
from pygame.locals import *
import os
from classes.Board import Board
from classes.Player import Player
from classes.Piece import Coords
import asyncio

WIDTH = 1200
HEIGHT = 1200
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
ORANGE = (255, 153, 51)
BLUE = (87,155,252)
GREY = (100, 100, 100)
TAN = (229, 156, 91)

BEER_SIZE = 12

PLAYER_COLOR_MAP = {
	"Red": RED,
	"Blue": BLUE,
	"Green": GREEN,
	"Yellow": YELLOW
}

#flipped building colors
PLAYER_BUILDING_RETIRED_COLOR_MAP = {
	"Red": (84, 0, 0),
	"Blue": (0, 0, 84),
	"Green": (4, 84, 0),
	"Yellow": (85, 72, 0)
}

PLAYER_COLORS = [
	(84, 0, 0),
	(0, 0, 84),
	(4, 84, 0),
	(85, 72, 0)
]

MARGIN = 50


class Render:
	def __init__(self, players: list[Player], board:Board=None, callback=None, x=0, y=0):
		pygame.init()
		pygame.font.init()
		# local_dir = os.path.dirname(__file__)
		# font = pygame.font.Font(None, 24)
		self.bigFont = pygame.font.Font(None, 48)
		self.players = players
		self.board = board
		self.callback = callback
		self.win = pygame.display.set_mode((WIDTH, HEIGHT))
		self.x = x
		self.y = y
		self.frame = Rect(MARGIN/2, MARGIN/2, WIDTH-MARGIN, HEIGHT-MARGIN)
		self.running = True
		self.tileWidth = WIDTH//self.board.n
		self.tileHeight = HEIGHT//self.board.n

		self.draw()

	def createGame(self, numPlayers, p1Name="Noah", p2Name="Tyler", p3Name="Sam", p4Name="Mr. McDonald"):
		self.board = Board()
		
	def drawTile(self, coords:Coords, color):
		rect = Rect(coords.x, coords.y, self.tileWidth, self.tileHeight)
		pygame.draw.rect(self.win, PLAYER_COLORS[color-1], rect)
	
	def drawWinner(self):
		# find winner
		winner = min(self.players, key=lambda player: player.getRemainingSquares())

		img = self.bigFont.render(f"{winner} wins with {winner.getRemainingSquares()} left", True, WHITE)
		self.win.blit(img, (WIDTH//2, HEIGHT//2))

	async def drawWindow(self):
		while self.running:
			await asyncio.sleep(0.00001)
			self.win.fill(GREY)
			self.win.blit(self.win, (self.x, self.y))
			
			for y in range(self.board.n):
				for x in range(self.board.n):
					if self.board.tiles[y][x] != 0:
						self.drawTile(Coords(x*self.tileWidth, y*self.tileHeight), self.board.tiles[y][x])

			if self.board.gameOver:
				self.drawWinner()

			pygame.display.update()

	async def handleEvents(self):
		while self.running:
			await asyncio.sleep(0.00001)
			# event = pygame.event.wait()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					print(pygame.mouse.get_pos())

				# Did the user hit a key?
				if event.type == KEYDOWN:
					# Was it the Escape key? If so, stop the loop.
					if event.key == K_ESCAPE:
						self.running = False

				# Did the user click the window close button? If so, stop the loop.
				elif event.type == QUIT:
					self.running = False



	def draw(self):
		# animation_task = asyncio.ensure_future(self.drawWindow())
		# event_task = asyncio.ensure_future(self.handleEvents())
		# pygame_task = self.loop.run_in_executor(None, self.pygame_event_loop, self.loop, self.event_queue)
		# animation_task = self.loop.create_task(self.drawWindow())
		# event_task = self.loop.create_task(self.handleEvents())
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		coros = [self.drawWindow(), self.handleEvents()]
		if self.callback:
			coros.append(self.callback())
		loop.run_until_complete(asyncio.gather(*coros))
		# asyncio.run_coroutine_threadsafe(self.drawWindow(), loop)
		# asyncio.run_coroutine_threadsafe(self.handleEvents(), loop)
		loop.close()

		pygame.quit()
			
	async def main(self, loop):
		loop.create_task(self.drawWindow())
		loop.create_task(self.handleEvents())

def render(players, board:Board, callback=None):
	Render(players, board, callback)