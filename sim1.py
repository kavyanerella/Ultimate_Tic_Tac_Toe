import sys
import random
import signal
import python_tree
import copy


class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    raise TimedOutExc()

def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

def update_lists(game_board, block_stat, move_ret, fl):
	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3
	id1 = block_no/3
	id2 = block_no%3
	mg = 0
	mflg = 0
	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
			mflg=1
		
                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl


        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' 
        
        return


class Manual_player:
	
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		global old_node
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		new_board = copy.deepcopy(temp_board)
		mvp = mvp.split()
		x = int(mvp[0])
		y = int(mvp[1])
		new_board[x][y] = flag
		temporary_block = copy.deepcopy(temp_block)
		update_lists(new_board, temporary_block, (x, y), flag)
		new_node = python_tree.Node(new_board, temporary_block, [], old_node, (x, y))
		old_node = new_node
		return (x, y)
		

def heuristic(temp_board, block_stat, flag):
	h_values = []
	h_values.append(heuristic_mini([temp_board[0][0], temp_board[0][1], temp_board[0][2],temp_board[1][0], temp_board[1][1], temp_board[1][2], temp_board[2][0], temp_board[2][1], temp_board[2][2] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[0][3], temp_board[0][4], temp_board[0][5],temp_board[1][3], temp_board[1][4], temp_board[1][5], temp_board[2][3], temp_board[2][4], temp_board[2][5] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[0][6], temp_board[0][7], temp_board[0][8],temp_board[1][6], temp_board[1][7], temp_board[1][8], temp_board[2][6], temp_board[2][7], temp_board[2][8] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[3][0], temp_board[3][1], temp_board[3][2],temp_board[4][0], temp_board[4][1], temp_board[4][2], temp_board[5][0], temp_board[5][1], temp_board[5][2] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[3][3], temp_board[3][4], temp_board[3][5],temp_board[4][3], temp_board[4][4], temp_board[4][5], temp_board[5][3], temp_board[5][4], temp_board[5][5] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[3][6], temp_board[3][7], temp_board[3][8],temp_board[4][6], temp_board[4][7], temp_board[4][8], temp_board[5][6], temp_board[5][7], temp_board[5][8] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[6][0], temp_board[6][1], temp_board[6][2],temp_board[7][0], temp_board[7][1], temp_board[7][2], temp_board[8][0], temp_board[8][1], temp_board[8][2] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[6][3], temp_board[6][4], temp_board[6][5],temp_board[7][3], temp_board[7][4], temp_board[7][5], temp_board[8][3], temp_board[8][4], temp_board[8][5] ], flag, 0))
	h_values.append(heuristic_mini([temp_board[6][6], temp_board[6][7], temp_board[6][8],temp_board[7][6], temp_board[7][7], temp_board[7][8], temp_board[8][6], temp_board[8][7], temp_board[8][8] ], flag, 0))
	h_small = 0
	for i in h_values:
		h_small += i
	h_big = heuristic_mini(block_stat, flag, 1)
	return h_small + h_big

def heuristic_mini(mini_board, flag, decide):
	h_sum = 0
	lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 7], [2, 4, 8]]
	if flag == 'x':
		flag1 = 'o'
	else:
		flag1 = 'x'

	if decide == 0:
		for line in lines:
			if mini_board[line[0]] == flag and mini_board[line[1]] == flag and mini_board[line[2]] == flag:
				h_sum = h_sum + 10

			elif mini_board[line[0]] == flag and mini_board[line[1]] == flag and mini_board[line[2]] == '-':
				h_sum = h_sum + 5

			elif mini_board[line[0]] == flag and mini_board[line[2]] == flag and mini_board[line[1]] == '-':
				h_sum = h_sum + 5

			elif (mini_board[line[1]] == flag and mini_board[line[2]] == flag and mini_board[line[0]] == '-'):
				h_sum = h_sum + 5
			
			elif (mini_board[line[0]] == flag and mini_board[line[1]] == '-' and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag and mini_board[line[2]] == '-' and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag and mini_board[line[2]] == '-' and mini_board[line[0]] == '-'):
				h_sum = h_sum + 1
			
			elif mini_board[line[0]] == flag1 and mini_board[line[1]] == flag1 and mini_board[line[2]] == flag1:
				h_sum = h_sum - 10
			
			elif (mini_board[line[0]] == flag1 and mini_board[line[1]] == flag1 and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag1 and mini_board[line[2]] == flag1 and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag1 and mini_board[line[2]] == flag1 and mini_board[line[0]] == '-'):
				h_sum = h_sum - 5
			
			elif (mini_board[line[0]] == flag1 and mini_board[line[1]] == '-' and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag1 and mini_board[line[2]] == '-' and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag1 and mini_board[line[2]] == '-' and mini_board[line[0]] == '-'):
				h_sum = h_sum - 1
			
			else:
				pass
	else:
		for line in lines:
			if mini_board[line[0]] == flag and mini_board[line[1]] == flag and mini_board[line[2]] == flag:
				h_sum = h_sum + 1000

			elif mini_board[line[0]] == flag and mini_board[line[1]] == flag and mini_board[line[2]] == '-':
				h_sum = h_sum + 500

			elif mini_board[line[0]] == flag and mini_board[line[2]] == flag and mini_board[line[1]] == '-':
				h_sum = h_sum + 500

			elif (mini_board[line[1]] == flag and mini_board[line[2]] == flag and mini_board[line[0]] == '-'):
				h_sum = h_sum + 500
			
			elif (mini_board[line[0]] == flag and mini_board[line[1]] == '-' and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag and mini_board[line[2]] == '-' and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag and mini_board[line[2]] == '-' and mini_board[line[0]] == '-'):
				h_sum = h_sum + 100
			
			elif mini_board[line[0]] == flag1 and mini_board[line[1]] == flag1 and mini_board[line[2]] == flag1:
				h_sum = h_sum - 1000
			
			elif (mini_board[line[0]] == flag1 and mini_board[line[1]] == flag1 and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag1 and mini_board[line[2]] == flag1 and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag1 and mini_board[line[2]] == flag1 and mini_board[line[0]] == '-'):
				h_sum = h_sum - 500
			
			elif (mini_board[line[0]] == flag1 and mini_board[line[1]] == '-' and mini_board[line[2]] == '-') or (mini_board[line[0]] == flag1 and mini_board[line[2]] == '-' and mini_board[line[1]] == '-') or (mini_board[line[1]] == flag1 and mini_board[line[2]] == '-' and mini_board[line[0]] == '-'):
				h_sum = h_sum - 100
			
			else:
				pass
	return h_sum

count = 0

def print_tree(pres):
	global count
	print pres.current_move
	count += 1
	print count
	if len(pres.child_array) == 0:
		return
	for child in pres.child_array:
		print_tree(child)
	print "######"

dummy_board, dummy_block = get_init_board_and_blockstatus()
tree = python_tree.Tree()
old_node = python_tree.Node(dummy_board, dummy_block, [], None, (-1, -1))

class Player1:
	
	
	def __init__(self):
		pass

	def alpha_beta_new(self, branch, depth, alpha, beta, flag):
		if len(branch.child_array) == 0:
			if(depth % 2 == 1):
				branch.beta = heuristic(branch.board, branch.block, flag)
				#print depth, "branch_beta=", branch.beta 
			else:
				branch.alpha = heuristic(branch.board, branch.block, flag)
				#print depth, "branch_alpha=", branch.alpha 
		for child_object in branch.child_array:
			self.alpha_beta_new(child_object, depth + 1, branch.alpha, branch.beta, flag)
			# Pruning 
			if(depth%2 ==1):
				if(branch.beta < alpha ):
					break
			else:
				if(branch.alpha > beta):
					break
			if(depth % 2 ==1):
				branch.beta = child_object.alpha if branch.beta > child_object.alpha else branch.beta
				#print depth, "beta", branch.beta			
			else:
				branch.alpha = child_object.beta if branch.alpha < child_object.beta else branch.alpha
				#print depth, "alpha", branch.alpha			
		return

	def move(self, temp_board, temp_block, old_move, flag):
		global old_node
		global tree
		new_board = copy.deepcopy(temp_board)
		temporary_block = copy.deepcopy(temp_block)
		update_lists(new_board, temporary_block, old_move, flag)
		new_node = python_tree.Node(new_board, temporary_block, [], old_node, old_move)
		old_node = new_node
		tree.build_tree(old_node, 3, flag)
		self.alpha_beta_new(old_node, 0, -10000, 10000, flag)
		temp1 = old_node.alpha
		for child in old_node.child_array:
			for child in old_node.child_array:
				if temp1 == child.beta:
					old_node = child
					return child.current_move
				else:
					pass

class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
		global old_node
		for_corner = [0,2,3,5,6,8]
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				blocks_allowed = [0, 1, 3]
			
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				blocks_allowed = [1, 2, 5]
			
			elif old_move[0] in [2, 5, 8] and old_move[1] % 3 == 0:
				blocks_allowed  = [3, 6, 7]
			
			elif old_move[0] in [2, 5,8] and old_move[1] in [2,5,8]:
				blocks_allowed = [5, 7, 8]
			
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				blocks_allowed = [5]
			
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

		for i in reversed(blocks_allowed):
			if temp_block[i] != '-':
				blocks_allowed.remove(i)
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		x, y = cells[random.randrange(len(cells))]
		#new_board = copy.deepcopy(temp_board)
		#temporary_block = copy.deepcopy(temp_block)
		#update_lists(new_board, temporary_block, (x, y), flag)
		#new_node = python_tree.Node(new_board, temporary_block, [], old_node, (x, y))
		#old_node = new_node
		return (x, y)


def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

def get_empty_out_of(gameb, blal,block_stat):
	cells = []  
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	if cells == []:
		for i in range(9):
			for j in range(9):
				no = (i/3)*3
				no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
def check_valid_move(game_board,block_stat, current_move, old_move):

	print current_move, old_move
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [0,1,3]
		
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			blocks_allowed = [1,2,5]
		
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
			blocks_allowed  = [3,6,7]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
			blocks_allowed = [5,7,8]

		else:
			print "SOMETHING REALLY WEIRD HAPPENED!"
			sys.exit(1)

	else:
		if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
			blocks_allowed = [1]
	
		elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
			blocks_allowed = [3]
		
		elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
			blocks_allowed = [7]

		elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
			blocks_allowed = [5]

		elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
			blocks_allowed = [4]

	for i in reversed(blocks_allowed):
	#	print block_stat
		if block_stat[i] != '-':
			blocks_allowed.remove(i)

	cells = get_empty_out_of(game_board, blocks_allowed,block_stat)
	print "allowed blocks are ", blocks_allowed
	print cells

	if current_move in cells:
		return True
	else:
		return False


def terminal_state_reached(game_board, block_stat):

	bs = block_stat
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		print block_stat
		return True, 'W'

	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		print block_stat
		return True, 'W'

	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		print block_stat
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			point1 = 0
			point2 = 0
			for i in block_stat:
				if i == 'x':
					point1+=1
				elif i=='o':
					point2+=1
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				point1 = 0
				point2 = 0
				for i in range(len(game_board)):
					for j in range(len(game_board[i])):
						if i%3!=1 and j%3!=1:
							if game_board[i][j] == 'x':
								point1+=1
							elif game_board[i][j]=='o':
								point2+=1

				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
				else:
					return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) 

	WINNER = ''
	MESSAGE = ''

	TIMEALLOWED = 6

	print_lists(game_board, block_stat)
	
	while(1):
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
			print ret_move_pl1

		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		if not check_valid_move(game_board, block_stat, ret_move_pl1, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L', 'MADE AN INVALID MOVE')
			break

		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

		update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat) 
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
		
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)

		try:
			ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break

		if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
		update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			break

		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER + " won!"
	print MESSAGE

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = Player2()

	elif option == '2':
		obj1 = Player1()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()
        

	num = random.uniform(0,1)
#	if num > 0.5:
#		simulate(obj2, obj1)
#	else:
#		simulate(obj1, obj2)
	simulate(obj2, obj1)
