from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
	solver = pywraplp.Solver('CoinsGridCBC',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
	
	#number of nodes
	nn = 11
	nodes = [1,2,3,4,5,6,7,8,9,10,11]
	
	#number of links
	nl = 20
	links = [[0,1],[0,3],[0,6],[0,8],[1,2],[1,5],[1,7],[2,4],[2,6],[2,9],[3,4],[3,5],[3,9],[4,7],[4,8],[5,10],[6,10],[7,10],[8,10],[9,10]]
	
	#number of colors
	nc = 4
	colors = [i for i in range(nc)]
	
	#variables
	x = {}
	for i in range(nn):
		for j in range(nc):
			x[i,j] = solver.IntVar(0,1,'x[%i,%i]' % (i,j))
	
	y = [solver.IntVar(0, 1, "y[%i]" % i) for i in range(nc)]
	
	z = solver.Sum(y)
	
	#constraints
	'''for i in range(nn):
		for j in range(nc):
			solver.Add(solver.Sum([(solver.Sum([x[i,j] == 1,y[j]]) == 0),(solver.Sum([x[i,j] == 1,y[j]]) == 2)]) == 1)'''
			
	for i in range(nn):
		solver.Add(solver.Sum([x[i,j] for j in range(nc)]) == 1)
		
	for i,j in links:
		for k in range(nc):
			solver.Add(solver.Sum([x[i,k],x[j,k]]) <= 1)
			
	#objective
	objective = solver.Minimize(z)
	
	#
	# solution and search
	#
	solver.Solve()
	
	print()
	print('z: ', int(solver.Objective().Value()))
	
	print('y: ', [int(y[i].SolutionValue()) for i in range(nc)])
	
	for i in range(nn):
		print("color for :",nodes[i])
		print([int(x[i,j].SolutionValue()) for j in range(nc)])
	
	print()
	print('walltime  :', solver.WallTime(), 'ms')
	print('iterations:', solver.Iterations())

if __name__ == "__main__":
  main()
