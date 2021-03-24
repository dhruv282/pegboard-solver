#!/usr/bin/python3
import sys
from random import randrange
import copy
import time

'''
Data structure to store information about each individual cell on the board
'''
class cell:

	def __init__(self, num, jump_dict):
		self.num = num
		self.jump_dict = jump_dict
		self.peg = True

	# Checks if cell has a peg and returns the result
	def has_peg(self):
		return self.peg

	# Adds a peg to the cell
	def add_peg(self):
		self.peg = True

	# Removes the peg in the cell
	def remove_peg(self):
		self.peg = False

	# Displays information about the cell
	def display(self):
		print(str(self.num)+" "+str(self.has_peg())+" "+str(self.jump_dict))

	# Returns possible jumps from given cell depending on the pegs on the board
	def possible_jump(self, board):
		assert self.has_peg()
		possible_jump_dict = {}
		for jump_over in self.jump_dict:
			jump_to = self.jump_dict[jump_over]
			if board[jump_over].has_peg() and not board[jump_to].has_peg():
				possible_jump_dict[jump_over] = jump_to
		return possible_jump_dict

'''
Creates m x n board
'''
def createBoard(m, n):
	board = []
	for i in range(0, m*n):
		# Generating moves that can be made from each cell
		validMoves = {}
		moveRight = i+2
		moveLeft = i-2
		moveDown = i+(2*n)
		moveUp = i-(2*n)

		if moveRight >= 0 and moveRight % n != 0 and (moveRight-1) % n != 0:
			validMoves[moveRight-1] = moveRight
		if moveLeft >= 0 and i % n != 0 and (i-1) % n != 0:
			validMoves[i-1] = moveLeft
		if moveDown >= 0 and moveDown <= ((m*n)-1):
			validMoves[i+n] = moveDown
		if moveUp >= 0:
			validMoves[i-n] = moveUp

		board.append(cell(i, validMoves))
	
	randomPegRemove = randrange(m*n)
	board[randomPegRemove].remove_peg()
	return board, randomPegRemove

'''
Prints information about all slots in the given board
'''
def printSlotInfo(board):
	for i in range(0, len(board)):
		board[i].display()

'''
Prints the given board in a m x n format
* 0 shows that the cell has no peg
* 1 shows that the cell has a peg
'''
def printBoard(board, n):
	for i in range(0, len(board)):
		if board[i].num % n == 0:
			print("\n", end="")
		if board[i].has_peg():
			print("1 ", end="")
		else:
			print("0 ", end="")
	print("\n")

'''
Checks if there is only one peg left in the board
'''
def goal(board):
	pegCounter = 0
	for i in range(0, len(board)):
		if board[i].has_peg():
			pegCounter = pegCounter + 1
		if pegCounter > 1:
			return False
	return True

'''
Adjusts pegs in the given board for a specified move
* Returns True if move was successful
* Returns False if move is invalid
'''
def makeMove(board, cur, jumpOver, jumpTo):
	if board[cur].has_peg() and board[jumpOver].has_peg() and not board[jumpTo].has_peg():
		board[cur].remove_peg()
		board[jumpOver].remove_peg()
		board[jumpTo].add_peg()
		return True
	else:
		return False

'''
Returns the number of empty slots in the given board
'''
def getEmptySlots(board):
	emptySlots = []
	for slot in board:
		if not slot.has_peg():
			emptySlots.append(slot.num)
	return emptySlots

'''
Solves the given board using the DFS algorithm
* Fringe used is a stack
* Returns a closed list that holds all the expanded nodes
* Returns type of algorithm used in this function 
'''
def DepthFirstSearchSolver(board, n):
	fringe = []
	closedList = []
	solved = False
	fringe.append(board)
	while len(fringe) > 0:
		state = fringe.pop()
		closedList.append(state)
		#printBoard(state, n)
		if goal(state):
			solved = True
			print("Solution found!")
			break
		possibleStates = successor(state, n)
		for someState in possibleStates:
			fringe.append(someState)
	if not solved:
		print("No solution found :(")
	return closedList, "Depth First Search (DFS)"

'''
Solves the given board using the BFS algorithm
* Fringe used is a queue
* Returns a closed list that holds all the expanded nodes
* Returns type of algorithm used in this function 
'''
def BreadthFirstSearchSolver(board, n):
	fringe = []
	closedList = []
	solved = False
	fringe.append(board)
	while len(fringe) > 0:
		state = fringe.pop(0)
		closedList.append(state)
		#printBoard(state, n)
		if goal(state):
			solved = True
			print("Solution found!")
			break
		possibleStates = successor(state, n)
		for someState in possibleStates:
			fringe.append(someState)
	if not solved:
		print("No solution found :(")
	return closedList, "Breadth First Search (BFS)"

'''
Solves the given board using the Greedy algorithm
* Fringe used is a priority queue
* Fringe is sorted based on the hueristic value of states at the end of the loop
* Returns a closed list that holds all the expanded nodes
* Returns type of algorithm used in this function 
'''
def greedySolver(board, m, n):
	fringe = []
	closedList = []
	solved = False
	fringe.append((board, 0))
	while len(fringe) > 0:
		popped = fringe.pop(0)
		state = popped[0]
		heuristicVal = popped[1]
		closedList.append(state)
		#printBoard(state, n)
		if goal(state):
			solved = True
			print("Solution found!")
			break
		possibleStates = successor(state, n)
		for someState in possibleStates:
			fringe.append((someState, heuristic(someState, m, n)))
		fringe = sorted(fringe, key=lambda x:x[1])
	if not solved:
		print("No solution found :(")
	return closedList, "Greedy"

'''
Solves the given board using the A* algorithm
* Fringe used is a priority queue
* Fringe is sorted based on the sum of hueristic and path cost of states at the end of the loop
* Returns a closed list that holds all the expanded nodes
* Returns type of algorithm used in this function 
'''
def AStar(board, m, n):
	fringe = []
	closedList = []
	solved = False
	fringe.append((board, 0))
	while len(fringe) > 0:
		popped = fringe.pop(0)
		state = popped[0]
		val = popped[1]
		closedList.append(state)
		#printBoard(state, n)
		if goal(state):
			solved = True
			print("Solution found!")
			break
		possibleStates = successor(state, n)
		for someState in possibleStates:
			val += heuristic(someState, m, n) + 2
			fringe.append((someState, val))
		fringe = sorted(fringe, key=lambda x:x[1])
	if not solved:
		print("No solution found :(")
	return closedList, "AStar"

'''
Generates all possible states from the given board and returns them
'''
def successor(board, n):
	emptySlots = getEmptySlots(board)
	possibleStates = []
	for slot in emptySlots:
		state = copy.deepcopy(board)
		possibleJumps = list(state[slot].jump_dict.keys())
		for jump in possibleJumps:
			tempState = copy.deepcopy(state)
			cur = tempState[slot].jump_dict[jump]
			if makeMove(tempState, cur, jump, slot):
				possibleStates.append(tempState)
				#printBoard(tempState, n)
	return possibleStates

'''
Heuristic function uses the Manhattan Distance strategy which is the sum of deltaX and deltaY.
The function begins by getting the centers of the given board wich is done by calling the getCenters() function.
Next each slot in the board is iterated through and if the slot has a peg, the Manhattan distance is evaluated from that peg to each center.
The heuristic values evaluated for the next slots is added on to the previous values and the total is returned.
'''
def heuristic(board, m, n):
	centers = getCenters(board, m, n)
	heuristicVal = 0
	for slot in board:
		if slot.has_peg():
			for center in centers:
				centerMod = center % n
				slotMod = slot.num % n
				colDiff = abs(centerMod - slotMod)

				centerDiv = center//m
				slotDiv = slot.num//m
				rowDiff = abs(centerDiv - slotDiv)

				heuristicVal += colDiff + rowDiff
	return heuristicVal

'''
Finds the centers of the given m x n board
* Some boards may have multiple center values
'''
def getCenters(board, m, n):
	centers = []
	val = ((m//2) * n) + (n//2)
	centers.append(val)
	if (m <= n or (m > n and m % 2 == 0)) and n % 2 == 0:
		centers.append(val - 1)
	if (m >= n or (m < n and m % 2 == 0)) and m % 2 == 0:
		centers.append(val - n)
	if n % 2 == 0 and m % 2 == 0:
		centers.append(val-(n+1))
	return centers

'''
Prints the closed list obtained from the different algorithms
* Writes the final result to a file named result.txt
* Prints the status of each state in the closed list
* Prints the duration it took to run the solver
'''
def printResult(res, m, n, strategy, duration):
	for board in res:
		if board == res[len(res) - 1]:
			if goal(board):
				print("****************************************************")
				print("****************************************************")
				print("Board: " + str(m) + " x " + str(n))
				print("Strategy used: " + strategy)
				print("Time: " + str(duration) + " seconds")
				print("Result: Solution Found!")
				print("# States: " + str(len(res)))
				print("Final State: ")
				printBoard(board, n)
				print("****************************************************")
				print("****************************************************")

				with open("results.txt", 'a') as file:
					file.write("****************************************************")
					file.write("\nBoard: " + str(m) + " x " + str(n))
					file.write("\nStrategy used: " + strategy)
					file.write("\nTime: " + str(duration) + " seconds")
					file.write("\nResult: Solution Found!")
					file.write("\n# States: " + str(len(res)))
					file.write("\nFinal State: ")
					#printBoard(board, n)
					for i in range(0, len(board)):
						if board[i].num % n == 0:
							file.write("\n")
						if board[i].has_peg():
							file.write("1 ")
						else:
							file.write("0 ")
					file.write("\n")
					file.write("****************************************************\n")
				break
			else:
				print("****************************************************")
				print("****************************************************")
				print("Board: " + str(m) + " x " + str(n))
				print("Strategy used: " + strategy)
				print("Time: " + str(duration) + " seconds")
				print("Result: No Solution Found :(")
				print("# States: " + str(len(res)))
				print("Final State: ")
				printBoard(board, n)
				print("****************************************************")
				print("****************************************************")

				with open("results.txt", 'a') as file:
					file.write("****************************************************")
					file.write("\nBoard: " + str(m) + " x " + str(n))
					file.write("\nStrategy used: " + strategy)
					file.write("\nTime: " + str(duration) + " seconds")
					file.write("\nResult: No Solution Found :(")
					file.write("\n# States: " + str(len(res)))
					file.write("\nFinal State: ")
					#printBoard(board, n)
					for i in range(0, len(board)):
						if board[i].num % n == 0:
							file.write("\n")
						if board[i].has_peg():
							file.write("1 ")
						else:
							file.write("0 ")
					file.write("\n")
					file.write("****************************************************\n")
				break

		else:
			possibleStates = successor(board, n)
			if len(possibleStates) == 0:
				print("****************************************************")
				print("Unable to make moves")
				print("****************************************************")
				printBoard(board, n)
			else:
				print("****************************************************")
				print("Able to make moves")
				print("****************************************************")
				printBoard(board, n)

def main():
	if len(sys.argv) != 4:
		print("Usage: ./pegboard.py m n algorithm")
		print("algorithm options:")
		print("- BFS")
		print("- DFS")
		print("- Greedy")
		print("- AStar")
		sys.exit()
	
	m = int(sys.argv[1])
	n = int(sys.argv[2])
	algorithm = sys.argv[3]

	print("Welcome to the Pegboard Game Solver\n")
	board, firstEmptySlot = createBoard(m, n)
	#printBoard(board, n)

	if algorithm == 'BFS':
		start = time.time()
		res, strategy = BreadthFirstSearchSolver(board, n)
		end = time.time()
	elif algorithm == 'DFS':
		start = time.time()
		res, strategy = DepthFirstSearchSolver(board, n)
		end = time.time()
	elif algorithm == 'Greedy':
		start = time.time()
		res, strategy = greedySolver(board, m, n)
		end = time.time()
	elif algorithm == 'AStar':
		start = time.time()
		res, strategy = AStar(board, m, n)
		end = time.time()
	else:
		print("Usage: ./pegboard.py m n algorithm")
		print("algorithm options:")
		print("- BFS")
		print("- DFS")
		print("- Greedy")
		print("- AStar")
		sys.exit()

	duration = end - start
	printResult(res, m, n, strategy, duration)

if __name__ == "__main__":
	main()