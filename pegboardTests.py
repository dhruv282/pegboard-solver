#!/usr/bin/python3
import sys
import time
import subprocess

CUTOFF_TIME = 900 #15 mins
ATTEMPTS = 3
algorithms = ['BFS', 'DFS', 'Greedy', 'AStar']
board = [4, 5, 6, 7, 8, 9, 10]

for boardItem in board:
	for algo in algorithms:
		counter = 0
		solved = False
		while counter < ATTEMPTS:
			counter += 1
			print("\n\nBoard: " + str(boardItem) + " x " + str(boardItem))
			print("Algorithm: " + str(algo))
			print("Attempt #: " + str(counter))
			try:
				start = time.time()
				p = subprocess.run(['./pegboard.py',
									str(boardItem),
									str(boardItem),
									algo], timeout=CUTOFF_TIME)
				if(p.returncode == 0):
					print("Solution Generated before cut off\n")
					solved = True
			except:
				print("Execution terminated due to cut off\n")
				if counter == ATTEMPTS:
					print("Last attempt, writing to file\n")
					end = time.time()
					duration = end - start
					with open('results.txt', 'a') as file:
						file.write("****************************************************")
						file.write("\nBoard: " + str(boardItem) + " x " + str(boardItem))
						file.write("\nStrategy used: " + algo)
						file.write("\nTime: " + str(duration) + " seconds")
						file.write("\nExecution ended after " + str(CUTOFF_TIME/60) + " minutes")
						file.write("\nResult: No Solution Found :(")
						file.write("\n****************************************************\n")
			if solved == True:
				break
