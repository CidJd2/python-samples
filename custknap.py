from __future__ import print_function
from ortools.constraint_solver import pywrapcp

def main():
	# Create the solver.
	solver = pywrapcp.Solver("xkcd knapsack")
	
	#
	# data
	#
	products = [
      "mixed fruit", "french fries", "side salad", "host wings",
      "mozzarella sticks", "samples place"
	]
	price = [215, 275, 335, 355, 420, 580]
	num_prices = 6
	
	total = 1505
	
	# declare variables

	# how many items of each dish
	x = [solver.IntVar(0, 10, "x%i" % i) for i in range(num_prices)]
	z = solver.IntVar(0, 1505, "z")

	#
	# constraints
	#
	solver.Add(total == solver.Sum([x[i] * price[i] for i in range(num_prices)]))
	# solver.Add(z == total)
	
	#
	# solution and search
	#
	solution = solver.Assignment()
	solution.Add([x[i] for i in range(num_prices)])
	solution.Add(z)

	#collector = solver.AllSolutionCollector(solution)
	collector = solver.FirstSolutionCollector(solution)
	
	solver.Solve(
      solver.Phase([x[i] for i in range(num_prices)], solver.INT_VAR_SIMPLE,
                   solver.ASSIGN_MIN_VALUE), [collector])
	
	num_solutions = collector.SolutionCount()
	
	print("num_solutions: ", num_solutions)
	if num_solutions > 0:
		for s in range(num_solutions):
			print("z:", collector.Value(s, z))
			xval = [collector.Value(s, x[i]) for i in range(num_prices)]
			print("x:", xval)
			for i in range(num_prices):
				if xval[i] > 0:
					print(xval[i], "of", products[i], ":", price[i] / 100.0)
			print()

	else:
		print("No solutions found")


if __name__ == "__main__":
	main()
