from BlokusSim import Blokus
from render import render
import random
import os
import time
import neat
import pickle

VERBOSE = False

def log(msg):
	if VERBOSE:
		print(msg)

#########AI STUFF#######
def cleanInput(tiles):
	x = []
	for row in tiles:
		for tile in row:
			x.append(tile)
	return x

gen = 0
def eval_genomes(genomes, config):
	playerIndex = 1
	"""
	runs the simulation of the current population of
	birds and sets their fitness based on the distance they
	reach in the game.
	"""
	global gen
	gen += 1

	# start by creating lists holding the genome itself, the
	# neural network associated with the genome and the
	# bird object that uses that network to play
	nets = []
	ge = []
	
	for genome_id, genome in genomes:
		genome.fitness = 0  # start with fitness level of 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		ge.append(genome)

	game = Blokus()

	initRotate = False
	while not game.board.gameOver:
		for i, player in enumerate(game.players):
			# dont rotate board on first players turn, but every turn after that
			if not initRotate:
				initRotate = True
			else:
				game.rotateBoard()
			# log(player)

			legalMoves = player.getLegalMoves()
			game.moves[i] = len(legalMoves)
			
			game.update()
			if game.board.gameOver:
				break

			moves = game.moves
			# log(len(legalMoves))
			if moves[i] == 0:
				# if i == playerIndex:
				# 	ge[i].fitness -= .05
				game.Pass(i)
				continue

			#pass legal moves into output
			if i == playerIndex:
				output = nets[i].activate([moves[i]] + cleanInput(game.board.tiles))
			else:
				output = [random.random()]
			
			log(output)
			log(f"${player} play {int(output[0] * moves[i])} out of {moves[i]}")
			game.playMove(i, legalMoves[int(output[0] * moves[i]-1)])
			

	winner = game.getWinner()
	isTie = game.isTie()
	remaining = []
	for i, player in enumerate(game.players):
		x = player.getRemainingSquares()
		remaining.append(x)
		if isTie:
			ge[i].fitness += 1
		elif winner.id == player.id and i == playerIndex:
			ge[i].fitness += 10
		ge[i].fitness -= x

		if player.getRemainingSquares() < 2:
			pickle.dump(nets[i],open("best.pickle", "wb"))
			render(game)
			

	for i, player in enumerate(game.players):
		for j, r in enumerate(remaining):
			# if i != j:
			if r > 0:
				ge[i].fitness -= r // 4
	
	# render(game)
	print(game.players)
	print(f"remaining: {[x for x in remaining]}")
	print(f"Fitness: {[x.fitness for x in ge]}")
	return #end and it will be restarted automatically?
	


def eval_multiple_genomes(genomes, config):
	"""
	runs the simulation of the current population of
	birds and sets their fitness based on the distance they
	reach in the game.
	"""

	# start by creating lists holding the genome itself, the
	# neural network associated with the genome and the
	# bird object that uses that network to play
	nets = []
	ge = []
	games = []
	for genome_id, genome in genomes:
		genome.fitness = 0  # start with fitness level of 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		games.append(Blokus())
		ge.append(genome)
	count = 0

	lastNet = False
	for i, playerTuple in enumerate(players):
		lastNet = random.choice(nets)
		# try:
		# 	lastNet = random.choice(nets)
		# except:
		# 	pass
		ge[i].fitness -= 1
		games[i].reset()

		run = True
		while run:
			for y, player in enumerate(playerTuple):
				validMoves = games[i].getValidMoves()
				if validMoves:
					if y == 0: #make player 1 train to git good
						# ge[i].fitness -= .01
						#pick move based on output
						output = nets[i].activate(games[i].getMoves())
						outputMaxIndex = output.index(max(output))
						#pick column based on index of output
						if len(validMoves) == 7:
							for move in validMoves:
								if move[0] == outputMaxIndex:
									col, row = move
									break
							
						else:
							while outputMaxIndex not in [z[0] for z in validMoves]:
								if outputMaxIndex == 0:
									outputMaxIndex = NUM_COLS
								outputMaxIndex -= 1
							for move in validMoves:
								if move[0] == outputMaxIndex:
									col, row = move
									break
					elif lastNet:
						# ge[i].fitness -= .01
						#pick move based on output
						output = lastNet.activate(games[i].getMoves())
						outputMaxIndex = output.index(max(output))
						#pick column based on index of output
						if len(validMoves) == 7:
							for move in validMoves:
								if move[0] == outputMaxIndex:
									col, row = move
									break
							
						else:
							while outputMaxIndex not in [z[0] for z in validMoves]:
								if outputMaxIndex == 0:
									outputMaxIndex = NUM_COLS
								outputMaxIndex -= 1
							for move in validMoves:
								if move[0] == outputMaxIndex:
									col, row = move
									break

					else: #make player 2 play randomly
						col, row = random.choice(validMoves)


				else: #if not validMoves:
					count += 1
					ge[i].fitness -= .1
					games[i].reset()
					run = False
				result = player.move(games[i], col, row)
				ge[i].fitness -= .05
				if result:
					if games[i].winner == player.color:
						ge[i].fitness += 2
					count += 1
					games[i].reset()
					pickle.dump(nets[0],open("best.pickle", "wb"))
					run = False

				# draw_window(WIN, gen, game, games[i])

def testNet(net, NUM_GAMES=100):
	game = Blokus()
	for i in range(NUM_GAMES):
		if i % NUM_GAMES/10 == 0:
			print(f"{i*100/NUM_GAMES}%")
		while not game.board.gameOver:
			for i, player in enumerate(game.players):
				# log(player)

				legalMoves = player.getLegalMoves()
				game.moves[i] = len(legalMoves)
				
				game.update()
				if game.board.gameOver:
					break

				moves = game.moves
				# log(len(legalMoves))
				if moves[i] == 0:
					game.Pass(i)
					continue

				#pass legal moves into output
				output = net.activate([i, moves[i]] + cleanInput(game.board.tiles))
				
				log(output)
				log(f"${player} play {int(output[0] * moves[i])} out of {moves[i]}")
				game.playMove(i, legalMoves[int(output[0] * moves[i]-1)])

		winner = game.getWinner()
		for i, player in enumerate(game.players):
			if winner.id == player.id:
				if player.getRemainingSquares() < 3:
					render(game)
					break
		game.reset()
	# print(game.wins)

def run(config_file):
	"""
	runs the NEAT algorithm to train a neural network to play Blokus.
	:param config_file: location of config file
	:return: None
	"""
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_file)

	# Create the population, which is the top-level object for a NEAT run.
	#create new
	p = neat.Population(config)

	#load
	p = neat.Checkpointer.restore_checkpoint('./checkpoints/neat-checkpoint-4181')

	# Add a stdout reporter to show progress in the terminal.
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(50))

	# Run for up to 50 generations.
	# winner = p.run(eval_multiple_genomes, 50)
	winner = p.run(eval_genomes, 100000)

	# show final stats
	print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')

	#train
	run(config_path) #trainer

	#test best net
	# testNet(pickle.load(open("best.pickle", "rb")), 10)