
from __future__ import print_function
from ortools.constraint_solver import pywrapcp

def main():
	# Create the solver.
	solver = pywrapcp.Solver("nqueens")
	
	grid_size = 4
	
	queenx = [solver.IntVar(0, grid_size - 1, "x%i" % i) for i in range(grid_size)]
	queeny = [solver.IntVar(0, grid_size - 1, "x%i" % i) for i in range(grid_size)]
	
	#queen_flat = [(queenx[i],queeny[i]) for i in range(grid_size)]
	
	solver.Add(solver.AllDifferent(queenx))
	solver.Add(solver.AllDifferent(queeny))
	
	for i in range(grid_size-1):
		solver.Add(queenx[i] <= queenx[i+1])
	
	for i in range(grid_size):
		for j in range(i):
			if i != j:
				solver.Add(queeny[i] != queeny[j])
				solver.Add(queeny[i] + queenx[i] != queeny[j] + queenx[j])
				solver.Add(queeny[i] - queenx[i] != queeny[j] - queenx[j])
	
	solution = solver.Assignment()
	solution.Add([queenx[i] for i in range(grid_size)])
	solution.Add([queeny[j] for j in range(grid_size)])
	
	collector = solver.AllSolutionCollector(solution)
	
	solver.Solve(solver.Phase([queenx[i] for i in range(grid_size)] + [queeny[i] for i in range(grid_size)], solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE), [collector])
	
                   
	num_solutions = collector.SolutionCount()
    
	print("num_solutions: ", num_solutions)
	if num_solutions > 0:
		for s in range(num_solutions):
			qxval = [collector.Value(s, queenx[i]) for i in range(grid_size)]
			qyval = [collector.Value(s, queeny[i]) for i in range(grid_size)]
			print("qx:", qxval)
			print("qy:", qyval)
			for i in range(grid_size):
				for j in range(grid_size):
					if qxval[i] == i and qyval[i] == j:
						print("Q", end=" ")
					else:
						print("_", end=" ")
				print()
			print()
			
		print()
		print("num_solutions:", num_solutions)
		print("failures:", solver.Failures())
		print("branches:", solver.Branches())
		print("WallTime:", solver.WallTime())
		
	else:
		print("No solutions found")

if __name__ == "__main__":
  main()
