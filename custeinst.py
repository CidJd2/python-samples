
from __future__ import print_function
from ortools.constraint_solver import pywrapcp

def main():
	solver = pywrapcp.Solver("einsteins riddle")
	
	#number_of_houses
	
	n = 5
	
	house_0 = 0
	house_1 = 1
	house_2 = 2
	house_3 = 3
	house_4 = 4
	
	#all different
	color = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	nationality = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	drink = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	smoke = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	pet = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	position = [solver.IntVar(0, n-1, "x%i" % i) for i in range(n)]
	
	#nationality_brit = 0
	brit = 0
	swede = 1
	norvegian = 2
	german = 3
	dane = 4
	
	#color_red = 0 etc...
	red = 0
	green = 1
	white = 2
	yellow = 3
	blue = 4
	
	coffe = 0
	milk = 1
	beer = 2
	water = 3
	tea = 4
	
	pall_mall = 0
	dunhill = 1
	blend = 2
	blue_master = 3
	prince = 4
	
	dog = 0
	bird = 1
	cat = 2
	horse = 3
	fish = 4
	
	position_0 = 0
	position_1 = 1
	position_2 = 2
	position_3 = 3
	position_4 = 4
	
	# labels
	nationalities = ["Brit", "Swede", "Norvegian", "German", "Dane"]
	colors = ["red","green","white","yellow", "blue"]
	drinks = ["coffe", "milk", "beer", "water", "tea"]
	smokes = ["pall mall","dunhill", "blend", "blue master", "prince"]
	pets = ["dog","bird","cat","horse","fish"]
	positions = [0,1,2,3,4]
	
	# constraints
	# all different
	
	solver.Add(solver.AllDifferent(color))
	solver.Add(solver.AllDifferent(nationality))
	solver.Add(solver.AllDifferent(drink))
	solver.Add(solver.AllDifferent(smoke))
	solver.Add(solver.AllDifferent(pet))
	solver.Add(solver.AllDifferent(position))
	
	# contrainst according to the problem
	
	for i in range(n-1):
		solver.Add((position[i]) < (position[i+1]))
	
	for i in range(n):
		# brit in red house
		solver.Add((color[i] == red) == (nationality[i] == brit))
		
		# swedes has dogs
		solver.Add((nationality[i] == swede) == (pet[i] == dog))
		
		# dane drinks tea
		solver.Add((nationality[i] == dane) == (drink[i] == tea))
		
		# green house left of white house
		if(i != n-1):
			solver.Add((color[i] == green) == (color[i+1] == white))
		solver.Add(color[n-1] != green)
		
		# green house drinks coffe
		solver.Add((color[i] == green) == (drink[i] == coffe))
		
		# smoke pall mall with birds
		solver.Add((smoke[i] == pall_mall) == (pet[i] == bird))
		
		# yellow house smokes dunhill
		solver.Add((color[i] == yellow) == (smoke[i] == dunhill))
		
		# center house drinks milk
		solver.Add((position[i] == position_2) == (drink[i] == milk))
		
		# norvegian in the first house
		solver.Add((position[i] == position_0) == (nationality[i] == norvegian))
		
		# smokes blue master and drinks beer
		solver.Add((smoke[i] == blue_master) == (drink[i] == beer))
		
		# german smokes prince
		solver.Add((nationality[i] == german) == (smoke[i] == prince))
		
		# smoke blends and live next to the cat owner
		if(i != 0 and i != n-1):
			solver.Add((smoke[i] == blend) <= (solver.Sum([(pet[i-1] == cat),(pet[i+1] == cat)]) == 1))
			solver.Add((pet[i] == cat) <= (solver.Sum([(smoke[i-1] == blend),(smoke[i+1] == blend)]) == 1))
		
		# have horses and lives next to the dunhill smoker
		if(i != 0 and i != n-1):
			solver.Add((pet[i] == horse) <= (solver.Sum([(smoke[i-1] == dunhill),(smoke[i+1] == dunhill)]) == 1))
			solver.Add((smoke[i] == dunhill) <= (solver.Sum([(pet[i-1] == horse),(pet[i+1] == horse)]) == 1))
		
		# norvegian next to blue house
		if(i != 0 and i != n-1):
			solver.Add((nationality[i] == norvegian) <= (solver.Sum([(color[i-1] == blue),(color[i+1] == blue)]) == 1))
			solver.Add((color[i] == blue) <= (solver.Sum([(nationality[i-1] == norvegian),(nationality[i+1] == norvegian)]) == 1))
		
		# smokes blend has a neighbour drinking water
		if(i != 0 and i != n-1):
			solver.Add((smoke[i] == blend) <= (solver.Sum([(drink[i-1] == water),(drink[i+1] == water)]) == 1))
			solver.Add((drink[i] == water) <= (solver.Sum([(smoke[i-1] == blend),(smoke[i+1] == blend)]) == 1))
			
	solver.Add(color[1] == blue)
		
	solver.Add((smoke[0] == blend) == (pet[1] == cat))
	solver.Add((smoke[n-1] == blend) == (pet[n-2] == cat))
	solver.Add((smoke[1] == blend) == (pet[0] == cat))
	solver.Add((smoke[n-2] == blend) == (pet[n-1] == cat))
	
	solver.Add((pet[0] == horse) == (smoke[1] == dunhill))
	solver.Add((pet[n-1] == horse) == (smoke[n-2] == dunhill))
	solver.Add((pet[1] == horse) == (smoke[0] == dunhill))
	solver.Add((pet[n-2] == horse) == (smoke[n-1] == dunhill))
	
	solver.Add((nationality[0] == norvegian) == (color[1] == blue))
	solver.Add((nationality[n-1] == norvegian) == (color[n-2] == blue))
	solver.Add((nationality[1] == norvegian) == (color[0] == blue))
	solver.Add((nationality[n-2] == norvegian) == (color[n-1] == blue))
	
	solver.Add((smoke[0] == blend) == (drink[1] == water))
	solver.Add((smoke[n-1] == blend) == (drink[n-2] == water))
	solver.Add((smoke[1] == blend) == (drink[0] == water))
	solver.Add((smoke[n-2] == blend) == (drink[n-1] == water))
		
	# assignment
	solution = solver.Assignment()
		
	solution.Add([color[i] for i in range(n)])
	solution.Add([nationality[i] for i in range(n)])
	solution.Add([drink[i] for i in range(n)])
	solution.Add([smoke[i] for i in range(n)])
	solution.Add([pet[i] for i in range(n)])
	solution.Add([position[i] for i in range(n)])
		
	collector = solver.AllSolutionCollector(solution)
		
	solver.Solve(solver.Phase([color[i] for i in range(n)]+[nationality[i] for i in range(n)]+[drink[i] for i in range(n)]+[smoke[i] for i in range(n)]+[pet[i] for i in range(n)]+[position[i] for i in range(n)], solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE), [collector])
		
	num_solutions = collector.SolutionCount()
		
	print("num_solutions: ", num_solutions)
	if num_solutions > 0:
		for s in range(num_solutions):
			#color_colution
			colsol = [collector.Value(s, color[i]) for i in range(n)]
			natsol = [collector.Value(s, nationality[i]) for i in range(n)]
			drisol = [collector.Value(s, drink[i]) for i in range(n)]
			smosol = [collector.Value(s, smoke[i]) for i in range(n)]
			petsol = [collector.Value(s, pet[i]) for i in range(n)]
			possol = [collector.Value(s, position[i]) for i in range(n)]
			print("colors :", colsol)
			print("nation :", natsol)
			print("drinks :", drisol)
			print("smokes :", smosol)
			print("pets   :", petsol)
			print("positi :", possol)
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
