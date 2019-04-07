
from __future__ import print_function
from ortools.constraint_solver import pywrapcp

def main():
	solver = pywrapcp.Solver("agatha")
	
	#number of people
	n = 3
	
	agatha = 0
	butler = 1
	charles = 2
	
	agatha_hate = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	butler_hate = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	charles_hate = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	
	agatha_richer = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	butler_richer = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	charles_richer = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	
	assassins = [solver.IntVar(0, 1, "x%i" % i) for i in range(n)]
	victim = 0
	
	#no one is richer than him/herself
	solver.Add(agatha_richer[agatha] == 0)
	solver.Add(butler_richer[butler] == 0)
	solver.Add(charles_richer[charles] == 0)
	
	#specificity of richer relation
	solver.Add((agatha_richer[butler] == 1) == (butler_richer[agatha] == 0))
	solver.Add((agatha_richer[charles] == 1) == (charles_richer[agatha] == 0))
	
	solver.Add((butler_richer[agatha] == 1) == (agatha_richer[butler] == 0))
	solver.Add((butler_richer[charles] == 1) == (charles_richer[agatha] == 0))
	
	solver.Add((charles_richer[agatha] == 1) == (agatha_richer[charles] == 0))
	solver.Add((charles_richer[butler] == 1) == (butler_richer[charles] == 0))
	
	#Chales hates none that Agatha hates
	for i in range(n):
		solver.Add((agatha_hate[i] == 1) <= (charles_hate[i] == 0))
		
	#Agatha hates everybody except the butler
	for i in range(n):
		if i != butler:
			solver.Add(agatha_hate[i] == 1)
		else:
			solver.Add(agatha_hate[i] == 0)
	
	#The butler hates everyone whom Agatha hates
	for i in range(n):
		solver.Add((agatha_hate[i] == 1) <= (butler_hate[i] == 1))
	
	#The butler hates everyone not richer than Agatha
	#for i in range(n):
	#	solver.Add((agatha_richer[i] == 1) <= (butler_hate[i] == 1))
		
	#alternative of above
	solver.Add((agatha_richer[agatha] == 0) <= (butler_hate[agatha] == 1))
	solver.Add((butler_richer[agatha] == 0) <= (butler_hate[butler] == 1))
	solver.Add((charles_richer[agatha] == 0) <= (butler_hate[charles] == 1))
	
	#None hates everyone
	solver.Add(solver.Sum(agatha_hate[i] for i in range(n)) <= 2)
	solver.Add(solver.Sum(butler_hate[i] for i in range(n)) <= 2)
	solver.Add(solver.Sum(charles_hate[i] for i in range(n)) <= 2)
	
	solver.Add((assassins[agatha] == 1) == (solver.Sum([(agatha_hate[victim] == 1), (agatha_richer[victim] == 0)]) == 2))
	solver.Add((assassins[butler] == 1) == (solver.Sum([(butler_hate[victim] == 1), (butler_richer[victim] == 0)]) == 2))
	solver.Add((assassins[charles] == 1) == (solver.Sum([(charles_hate[victim] == 1), (charles_richer[victim] == 0)]) == 2))
	
	solution = solver.Assignment()
	
	solution.Add([agatha_hate[i] for i in range(n)])
	solution.Add([butler_hate[i] for i in range(n)])
	solution.Add([charles_hate[i] for i in range(n)])
	
	solution.Add([agatha_richer[i] for i in range(n)])
	solution.Add([butler_richer[i] for i in range(n)])
	solution.Add([charles_richer[i] for i in range(n)])

	solution.Add([assassins[i] for i in range(n)])
	
	
	collector = solver.AllSolutionCollector(solution)
	
	solver.Solve(solver.Phase([agatha_hate[i] for i in range(n)]+[butler_hate[i] for i in range(n)]+[charles_hate[i] for i in range(n)]+[agatha_richer[i] for i in range(n)]+[butler_richer[i] for i in range(n)]+[charles_richer[i] for i in range(n)]+[assassins[i] for i in range(n)], solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE), [collector])
	
	
	num_solutions = collector.SolutionCount()
    
	print("num_solutions: ", num_solutions)
	if num_solutions > 0:
		for s in range(num_solutions):
			killval = [collector.Value(s, assassins[i]) for i in range(n)]
			agathah = [collector.Value(s, agatha_hate[i]) for i in range(n)]
			butlerh = [collector.Value(s, butler_hate[i]) for i in range(n)]
			charlesh = [collector.Value(s, charles_hate[i]) for i in range(n)]
			agathar = [collector.Value(s, agatha_richer[i]) for i in range(n)]
			butlerr = [collector.Value(s, butler_richer[i]) for i in range(n)]
			charlesr = [collector.Value(s, charles_richer[i]) for i in range(n)]
			print("killers:", killval)
			print("agatha hates ", agathah)
			print("butler hates", butlerh)
			print("charles hates", charlesh)
			print("agatha is richer than ", agathar)
			print("butler is richer than ", butlerr)
			print("charles is richer than ", charlesr)
		
		print()
		print("num_solutions:", num_solutions)
		print("failures:", solver.Failures())
		print("branches:", solver.Branches())
		print("WallTime:", solver.WallTime())
		
	else:
		print("No solutions found")

if __name__ == "__main__":
  main()
