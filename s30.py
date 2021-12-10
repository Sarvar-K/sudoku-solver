from copy import deepcopy
import sys
import time
import gc

start_time = time.process_time()

print('Input elements divided by space. Horizontally, from left to right. For empty square write 0')
print()
submain = [[],[],[],[],[],[],[],[],[]]
n = 0
while n < len(submain):
	submain[n] = list(map(int, (i for i in input())))
	n += 1
print()
print('---------------------------------------')

for i in submain:
	print('||',' | '.join(map(str, i)),'||')
	print('---------------------------------------')

#sys.stdout = open("results.txt", "w")

diagonal = [[],[]]

n =0
while n < 9:
	diagonal[0].append(submain[n][n])
	diagonal[1].append(submain[8-n][n])
	n+=1

def out_print(vals_to_plot):

	res = deepcopy(submain)
	for i in vals_to_plot:
		res[i[0]][i[1]] = i[2]

	print('---------------------------------------')
	for i in res:
		print('||',' | '.join(map(str, i)),'||')
		print('---------------------------------------')

def vert_construct(y):
	x = 0
	lst = []
	while x < 9:
		lst.append(submain[x][y])
		x += 1
	return lst

def box_construct(x,y): #for any point given in the inerior of a box, returs a list of all points in this box.
#Left to right, Top to bottom
	x = int(x/3)
	y = int(y/3)
	xmax = x + 3 + x*2
	ymax = y + 3 + y*2
	xmin = x*3
	ymin = y*3
	box = []
	while xmin < xmax:
		while ymin < ymax:
			box.append(submain[xmin][ymin])
			ymin += 1
		ymin = y*3
		xmin += 1

	return box

def coord_box_construct(x,y): #for any point given in the inerior of a box, returs a list of all coords of all points in this box.
#Left to right, Top to bottom
	x = int(x/3)
	y = int(y/3)
	xmax = x + 3 + x*2
	ymax = y + 3 + y*2
	xmin = x*3
	ymin = y*3
	box = []
	while xmin < xmax:
		while ymin < ymax:
			box.append([xmin,ymin])
			ymin += 1
		ymin = y*3
		xmin += 1

	return box

def secondary_update(arrs0, answer):
	x = answer[0]
	y = answer[1]
	p = answer[2]

	count = 0
	limit = len(arrs0)
	while count < limit:

		if arrs0[count][0] == [x, y]:
			del arrs0[count]
			limit -= 1
			count -=1
		if arrs0 == []:
			break
		if arrs0[count][0][0] == x and p not in arrs0[count][1]:
			arrs0[count][1].append(p)

		if arrs0[count][0][1] == y and p not in arrs0[count][1]:
			arrs0[count][1].append(p)

		if x + y == 8:
			if arrs0[count][0][0] + arrs0[count][0][1] == 8 and p not in arrs0[count][1]:
				arrs0[count][1].append(p)

		if x == y:
			if arrs0[count][0][0] == arrs0[count][0][1] and p not in arrs0[count][1]:
				arrs0[count][1].append(p)

		if arrs0[count][0] in coord_box_construct(x, y) and p not in arrs0[count][1]:
			arrs0[count][1].append(p)

		count += 1

	return arrs0

#-----------------------------------------------------------------------------------------------------------------------------------

def secondary(arr_sample, n): # OUT: answer

	arr = deepcopy(arr_sample)

	answer = None
	kolo2 = None
	main_limit = len(arr)
	count = 0

	horz = [[], [], [], [], [], [], [], [], []]
	vert = [[], [], [], [], [], [], [], [], []]
	digs = [[], []]
	boxes = [[], [], [], [], [], [], [], [], []]

	while count < main_limit:

		spot = arr[count]
		horz[spot[0]].append(spot)
		vert[spot[1]].append(spot)

		count += 1

	for i in horz:
		if len(i) == 1:
			answer = i[0].copy()
			#print('horz')
		else:
			pass

	if answer == None:
		for i in vert:
			if len(i) == 1:
				answer = i[0].copy()
				#print('vert')
			else:
				pass
	if answer == None:
		for i in arr:
			if i[0] == i[1]:
				digs[0].append(i)
			if i[0] + i[1] == 8:
				digs[1].append(i)
		for i in digs:
			if len(i) == 1:
				answer = i[0].copy()
				#print('digs')
			else:
				pass
	if answer == None:
		for i in arr:
			x = i[0]
			y = i[1]
			if x >= 0 and x < 3 and y >= 0 and y < 3:
				boxes[0].append(i)
			elif x >= 0 and x < 3 and y >= 3 and y < 6:
				boxes[1].append(i)
			elif i[0] >= 0 and i[1] > 5 and i[0] <= 2 and i[1] <= 8:
				boxes[2].append(i)
			elif i[0] > 2 and i[1] >= 0 and i[0] <= 5 and i[1] <= 2:
				boxes[3].append(i)
			elif i[0] > 2 and i[1] > 2 and i[0] <= 5 and i[1] <= 5:
				boxes[4].append(i)
			elif i[0] > 2 and i[1] >= 5 and i[0] <= 5 and i[1] <= 8:
				boxes[5].append(i)
			elif i[0] > 5 and i[1] >= 0 and i[0] <= 8 and i[1] <= 2:
				boxes[6].append(i)
			elif i[0] > 5 and i[1] > 2 and i[0] <= 8 and i[1] <= 5:
				boxes[7].append(i)
			else:
				boxes[8].append(i)
		for i in boxes:
			if len(i) == 1:
				answer = i[0].copy()
				#print('boxes')
			else:
				pass

	if answer != None:
		answer.append(n)

	else:

		# FROM BOXES

		boxes0 = []
		control = []

		for i in [*horz, *vert, *digs]:
			if i != []:
				control.append(i)

		for i in boxes:
			if i != []:
				boxes0.append(i)

		control_limit = len(control)
		count = 0

		while count < control_limit:
			for i in boxes:
				if control[count] == i:
					del control[count]
					control_limit -= 1
					break
			count += 1

		spotter_list = []

		for i in control:
			for j in boxes0:
				count = 0
				spotter_temp = []
				for z in i:
					if z in j and count < len(j):
						count += 1
					elif z not in j:
						spotter_temp.append(z)
				if spotter_temp != [] and count >= len(j):
					spotter_list.append(spotter_temp)

		answers = []

		for i in boxes0:
			for j in spotter_list:
				count = 0
				spotter_temp = []
				for z in i:
					if z in j and count < len(j):
						count += 1
					elif z not in j:
						spotter_temp.append(z)
				if len(spotter_temp) == 1 and count >= len(j):
					answers.append(spotter_temp)

		if len(answers) == 1:
			answer = answers[0][0]
			answer.append(n)

		if answer == None:

			for i in horz:
				if len(i) == 2:
					kolo2 = i
					break
			if kolo2 == None:
				for i in vert:
					if len(i) == 2:
						kolo2 = i
						break
			if kolo2 == None:
				for i in digs:
					if len(i) == 2:
						kolo2 = i
						break
			if kolo2 == None:
				for i in boxes:
					if len(i) == 2:
						kolo2 = i
						break
			if kolo2 != None:
				kolo2.append(n)

	
	#print(kolo2)
	return answer, kolo2

#-----------------------------------------------------------------------------------------------------------------------------------

def pc_ref(sub_arr): #OUT - all points associated with each coordinate
# IN - SUBMAIN
	main = []
	x = 0
	y = 0
	
	count = -1
	while x < 9:
		while y < 9:
			if sub_arr[x][y] == 0:
				main.append([[x,y],[vert_construct(y), sub_arr[x], box_construct(x,y)]])
				count += 1
				
				if x == y:
					main[count][1].append(diagonal[0])
				
				if x + y == 8:
					main[count][1].append(diagonal[1])
			
			
	
			y += 1
		y = 0
		x += 1
	
	flat_list = []
	for i in main:
		for j in i[1]:
			for k in j:
				flat_list.append(k)
		i.append(list(set(flat_list)))
		flat_list = []
		
	for i in main:
		del i[1]

	return main

#-------------------------------------------------------------------------------------------------------------------

def plotter(arr): # IN - MAIN (pc_ref return). OUT - arr, vals to plot, kolo 2

	answer = None
	pos = 0
	end = len(arr)
	kolo2 = None

	while pos < end:
		lst_of_points = list(set(arr[pos][1])) # list of associated (exclusion) points
		if len(lst_of_points) == 9:     
			for value in range(1,10):
				if value not in lst_of_points:
					answer = [arr[pos][0][0], arr[pos][0][1], value]
					break
			break
					
		elif len(lst_of_points) == 8:
			pair = [] # two possible values for a point
			for value in range(1,10):
				if value not in lst_of_points:
					pair.append(value)
			kolo2 = [[arr[pos][0][0], arr[pos][0][1]], pair] # New value replaces the old

		pos += 1

	return answer, kolo2

def reconstruct(turns):
	vals_to_plot = []
	num = 0
	temp = deepcopy(pc_ref(submain))
	#arrs = plotter(temp)
	n = 0
	right = 1
	nn = 0
	count = 0
	limit = len(turns)

	while nn < limit:
		if temp == []:
			break

		arrs = plotter(temp)

		if arrs[0] == None:
			if type(turns[count]) == list:
				if len(turns[count]) == 2:
					answer = turns[count][1]
					temp = secondary_update(deepcopy(temp), deepcopy(answer))
					vals_to_plot.append(deepcopy(answer))
					num += 1
					nn += 1
					count += 1
				else:
					answer = turns[count]
					temp = secondary_update(deepcopy(temp), deepcopy(answer))
					vals_to_plot.append(deepcopy(answer))
					num += 1
					nn += 1
					count += 1
			else:
				x = deepcopy(arrs[1])
				answer = x[0]
				answer.append(x[1][turns[count]])
				vals_to_plot.append(answer)
				temp = secondary_update(deepcopy(temp), answer)
				nn += 1
				num += 1
				count += 1
					
		else:
			temp = secondary_update(deepcopy(temp), deepcopy(arrs[0]))
			vals_to_plot.append(deepcopy(arrs[0]))
			num += 1
	return temp, num, vals_to_plot

#-------------------------------------------------------------------------------------------------------------------

# Assignments:

vals_to_plot = []
num = 0

temp = pc_ref(submain)

kolo2_ref = []
n = 0
turns = []
loop = 0

limit = len(temp)
print("\n", limit, "\n")

while num < limit:

	arrs = plotter(temp)

	if arrs[0] == None:

		nmb = 1
		arr_sample = []
		ref_arr = deepcopy(temp)

		while nmb < 10:

			for i in ref_arr:
				if nmb not in i[1]:
					arr_sample.append(i[0])

			#print(arr_sample)
			answer = deepcopy(secondary(arr_sample, nmb))
			'''print(nmb)
			print(answer)
			print(n)
			print(arrs[1])'''
			if answer[0] == None:
				nmb += 1
				if nmb == 10:
					#



					x = arrs[1]
					y = answer[1]
				
					if x != None and n == 0: # LEFT 1 recursion step 1
						result = x[0].copy()
						result.append(x[1][n]) # 0
						temp = secondary_update(deepcopy(temp), deepcopy(result))
						vals_to_plot.append(result)
						num += 1
						turns.append(0)
						print('LEFT     ', result)
						print('\nturns', turns,'\n')

					elif x == None and y != None and n == 0: # LEFT 2
						result = y[n].copy()
						result.append(y[2])
						temp = secondary_update(deepcopy(temp), deepcopy(result))
						vals_to_plot.append(result)
						num += 1
						turns.append([0, result])
						print('LEFT2    ', result)
						print('\nturns', turns,'\n')
						
					elif x == None and y == None: # RETURN recursion step 2  n = 0

						while type(turns[-1]) == list:
							if len(turns[-1]) == 3 or turns[-1][0] == 1:
								del turns[-1]
							else:
								break

						if turns[-1] == 0:
							del turns[-1]
						elif type(turns[-1]) == list and len(turns[-1]) == 2 and turns[-1][0] == 0:
							del turns[-1]
						else:
							while turns[-1] == 1:
								del turns[-1]
								while type(turns[-1]) == list:
									if len(turns[-1]) == 2 and turns[-1][0] == 0:
										break
									else:
										del turns[-1]
							del turns[-1]

						print('RETURN')
						print('\nturns', turns,'\n')
						retrieve = list(reconstruct(turns))
						temp = deepcopy(retrieve[0])
						num = retrieve[1]
						vals_to_plot = deepcopy(retrieve[2])
						n = 1

						if loop > 10:
							gc.collect()
							loop = 0
						loop += 1

					elif x != None and n == 1: # RIGHT 1 recursion step 3
						result = x[0].copy()
						result.append(x[1][n]) # 1
						temp = secondary_update(deepcopy(temp), deepcopy(result))
						vals_to_plot.append(result)
						n = 0
						num += 1
						turns.append(1)
						print('RIGHT     ', result)
						print('\nturns', turns,'\n')
						
					elif x == None and y != None and n == 1: # RIGHT 2
						result = y[n].copy()
						result.append(y[2])
						temp = secondary_update(deepcopy(temp), deepcopy(result))
						vals_to_plot.append(result)
						n = 0
						num += 1
						turns.append([1,result])
						print('RIGHT2    ', result)
						print('\nturns', turns,'\n')


					#

				arr_sample = []

			else:
				turns.append(answer[0])
				print('SECONDARY', answer[0])
				print('\nturns', turns,'\n')
				vals_to_plot.append(answer[0])
				temp = deepcopy(secondary_update(ref_arr, answer[0]))
				num += 1
				break

	else:
		print('PRIMARY  ',arrs[0])
		temp = deepcopy(secondary_update(temp, arrs[0]))
		vals_to_plot.append(deepcopy(arrs[0]))
		num += 1
	print(num)

	

#print("\n\n\n")
#print(turns)

#sys.stdout.close()


#-------------------------------------------------------------------------------------------------------------------
# DICTIONARY:

# submain - List of rows in a sudoku grid

# pc_red(submain) - Output: A list of [Coordinates of an empty square in a grid, List of values associated with that square that cannot be put in it]

# plotter(pc_ref(submain)) - # Output[0]: An updated list of [Coordinates of an empty square in a grid, List of values associated with that square that cannot be plotted]

							 # Output[1]: A list of [X coordinate, Y coordinate, Value to be plotted in the square at those coordinates]

							 # Output[2]: # 1) In case if there were unique solutions in the grid - None
							 			  # 2) In case if there were NO inique solutions in the grid - The next best option
							 			  # [[Coordinates], [Two potential values]]

#-------------------------------------------------------------------------------------------------------------------

print("\n\n\n")
print(out_print(vals_to_plot))
print("--- %s seconds ---" % (time.process_time() - start_time))
print("Number of plotted spots is", len(vals_to_plot))

#------------------------------------------------------------------------------------------------------------------
# GENERAL REMARKS:

# After the job is done, it makes sense to introduce list of answers instead of answer variable. For example: answer = [[2,4,2], [3,3,4]]
# Then, vals_to_plot and arr[0] update should be dealt accordingly
