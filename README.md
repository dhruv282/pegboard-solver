# Pegboard Game Solver

This solver uses the Breadth First Search, Depth First Search, Greedy, and A* algorithms to solve a given board.

[Python 3](https://www.python.org/downloads/) along with the [random](https://docs.python.org/3/library/random.html) and [copy](https://docs.python.org/3/library/copy.html) packages are required to run this solver.

## Running the solver:
The solver requires exactly 3 arguments;

- `m`: number of rows
- `n`: number of columns
- `algorithm`: algorithm to solve the puzzle. Algorithm options include:
	- `BFS`: Breadth First Search
	- `DFS`: Depth First Search
	- `Greedy`: Greedy Algorithm
	- `AStar`: A* Algorithm

```shell
$ python3 pegboard.py m n algorithm
```
### Example:
```shell
$ python3 pegboard.py 3 4 AStar
```