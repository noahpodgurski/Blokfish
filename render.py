import pygame
from pygame.locals import *
import os
from classes.Board import Board
from classes.Player import Player
import BlokusSim
from classes.Piece import Coords
import asyncio

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1300
WIDTH = 1000
HEIGHT = 1000
WHITE = (255,255,255)
RED = (230, 62, 44)
GREEN = (0,192,0)
BLACK = (0,0,0)
YELLOW = (245, 195, 32)#F5C320
ORANGE = (255, 153, 51)
BLUE = (0, 115, 207)
GREY = (100, 100, 100)
TAN = (229, 156, 91)

HIGHLIGHT = (150, 150, 150)
SHADOW = (40, 40, 40)

PLAYER_COLOR_MAP = {
	"Red": RED,
	"Blue": BLUE,
	"Green": GREEN,
	"Yellow": YELLOW
}

PLAYER_COLORS = [
	BLUE,
	YELLOW,
	RED,
	GREEN
]

BOARD_POS = (100, 100)
SHADOW_P = .1
SHADOW_Q = 1-SHADOW_P

"""
	Overlays color2 onto color1 with opacity
"""
def overlayColor(color1, color2, opacity):
	return  ((1-opacity)*color1[0] + opacity*color2[0], (1-opacity)*color1[1] + opacity*color2[1], (1-opacity)*color1[2] + opacity*color2[2])

class Render:
	def __init__(self, game, callback=None, x=0, y=0):
		pygame.init()
		pygame.font.init()
		# local_dir = os.path.dirname(__file__)
		# font = pygame.font.Font(None, 24)
		self.bigFont = pygame.font.Font(None, 48)
		self.game = game
		self.callback = callback
		self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.x = x
		self.y = y
		self.frame = Rect(BOARD_POS[0], BOARD_POS[1], WIDTH, HEIGHT)
		self.running = True
		self.tileWidth = WIDTH//self.game.board.n
		self.tileHeight = HEIGHT//self.game.board.n

		self.draw()

	def createGame(self, numPlayers, p1Name="Noah", p2Name="Tyler", p3Name="Sam", p4Name="Mr. McDonald"):
		self.game.board = Board()

	def drawGrid(self):
		for x in range(0, 20):
			#draw cols shadows
			col = Rect(BOARD_POS[0]+(x*(WIDTH)/20), BOARD_POS[0], 2, HEIGHT)
			pygame.draw.rect(self.win, HIGHLIGHT, col)
			col = Rect(BOARD_POS[0]+(x*(WIDTH)/20), BOARD_POS[0], 1, HEIGHT)
			pygame.draw.rect(self.win, SHADOW, col)
			#draw cols highlights
		#draw rows
		for y in range(0, 20):
			row = Rect(BOARD_POS[0], BOARD_POS[0]+(y*(WIDTH)/20), WIDTH, 2)
			pygame.draw.rect(self.win, HIGHLIGHT, row)
			row = Rect(BOARD_POS[0], BOARD_POS[0]+(y*(WIDTH)/20), WIDTH, 1)
			pygame.draw.rect(self.win, SHADOW, row)
		
	def drawTile(self, coords:Coords, color):
		#todo make dynamic based off height/width - why 8?? idk
		col = (coords.x/self.tileWidth)
		row = (coords.y/self.tileWidth)

		# print(row, col)
		# print(f"{coords.x=}")
		# print(f"{xAmtPaddingFromGrid=}")
		# print(BOARD_POS[0]+coords.x)
		# print(BOARD_POS[0]+coords.x+col, BOARD_POS[0]+coords.y+row)
		rect = Rect(BOARD_POS[0]+coords.x, BOARD_POS[0]+coords.y, self.tileWidth-2, self.tileHeight-2)
		pygame.draw.rect(self.win, PLAYER_COLORS[color-1], rect)
		# draw highlights and shadows
		shadow1 = Rect(BOARD_POS[0]+coords.x, BOARD_POS[0]+coords.y+(self.tileHeight*.9), self.tileWidth, self.tileHeight*SHADOW_P)
		pygame.draw.rect(self.win, overlayColor(PLAYER_COLORS[color-1], SHADOW, .5), shadow1)
		shadow2 = Rect(BOARD_POS[0]+coords.x+(self.tileWidth*.9), BOARD_POS[0]+coords.y, self.tileWidth*SHADOW_P, self.tileHeight)
		pygame.draw.rect(self.win, overlayColor(PLAYER_COLORS[color-1], SHADOW, .5), shadow2)
		highlight1 = Rect(BOARD_POS[0]+coords.x, BOARD_POS[0]+coords.y, self.tileWidth, self.tileWidth*SHADOW_P)
		pygame.draw.rect(self.win, overlayColor(PLAYER_COLORS[color-1], HIGHLIGHT, .5), highlight1)
		highlight2 = Rect(BOARD_POS[0]+coords.x, BOARD_POS[0]+coords.y, self.tileHeight*SHADOW_P, self.tileHeight)
		pygame.draw.rect(self.win, overlayColor(PLAYER_COLORS[color-1], HIGHLIGHT, .5), highlight2)

	def drawWinner(self):
		# find winner
		winner = self.game.getWinner()
		isTie = self.game.isTie()
		if isTie:
			img = self.bigFont.render(f"TIE", True, WHITE)
		else:
			img = self.bigFont.render(f"{winner} wins with {winner.getRemainingSquares()} left", True, WHITE)

		self.win.blit(img, (WIDTH//2, HEIGHT//2))

	async def drawWindow(self):
		while self.running:
			await asyncio.sleep(0.00001)
			self.win.fill(WHITE)
			pygame.draw.rect(self.win, GREY, self.frame)
			self.win.blit(self.win, (self.x, self.y))
			
			for y in range(self.game.board.n):
				for x in range(self.game.board.n):
					if self.game.board.tiles[y][x] != 0:
						self.drawTile(Coords(x*self.tileWidth, y*self.tileHeight), self.game.board.tiles[y][x])
			self.drawGrid()

			if self.game.board.gameOver:
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

def render(game, callback=None):
	Render(game, callback)


class Button:
	def __init__(self, render: Render, text: str, coords: Coords, icon: str):
		self.render = render
		self.text = text
		self.coords = coords
		self.icon = icon
		

if __name__ == "__main__":
	game = BlokusSim.Blokus()
	for p in game.players:
		for _p in game.players:
			if p.id != _p.id:
				for piece in p.pieces:
					match = False
					for _piece in _p.pieces:
						if piece.tileArray.all() == _piece.tileArray.all():
							match = True
	# game.Pass(0)
	# game.Pass(1)
	x1 = BlokusSim.Move(game.players[0].pieces[1], 0, Coords(0, 0))
	x2 = BlokusSim.Move(game.players[1].pieces[0], 0, Coords(19, 0))
	x3 = BlokusSim.Move(game.players[2].pieces[0], 0, Coords(19, 19))
	x4 = BlokusSim.Move(game.players[3].pieces[0], 0, Coords(0, 19))
	game.playMove(0, x1)
	game.playMove(1, x2)
	game.playMove(2, x3)
	game.playMove(3, x4)
	game.players[2]
	Render(game)