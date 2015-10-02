import sys
import copy
import random


def copy_update_lists(game_board, block_stat, move_ret, fl):
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



class Node:
	def __init__(self, board, block, child_array, parent, current_move):
		self.board = board
		self.block = block
		self.current_move = current_move
		self.child_array = child_array
		self.parent = parent
		self.heuristic = 0
		self.alpha = -sys.maxint -1
		self.beta = sys.maxint
		return

class Tree:
	def __init__(self):
		self.root_node = None
		return


	def blocks_allowed(self, old_move, temp_block):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			
			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				blocks_allowed = [0, 1, 3]

			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				blocks_allowed = [1,2,5]

			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				blocks_allowed  = [3,6,7]

			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
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
		
		return blocks_allowed

	def check_win_state(self, board, move, flag):
		row_num = move[0]
		col_num = move[1]
		row_var = row_num /3 * 3
		col_var = col_num /3 * 3
		rows = [row_var, row_var + 1, row_var + 2]
		cols = [col_var, col_var + 1, col_var + 2]
		if flag == 'x':
			flag1 = 'o'
		else:
			flag1 = 'x'
		if board[rows[0]][cols[0]] == flag and board[rows[0]][cols[1]] == flag and board[rows[0]][cols[2]] == flag:
			return True
		elif board[rows[1]][cols[0]] == flag and board[rows[1]][cols[1]] == flag and board[rows[1]][cols[2]] == flag:
			return True
		elif board[rows[2]][cols[0]] == flag and board[rows[2]][cols[1]] == flag and board[rows[2]][cols[2]] == flag:
			return True
		elif board[rows[0]][cols[0]] == flag and board[rows[1]][cols[0]] == flag and board[rows[2]][cols[0]] == flag:
			return True
		elif board[rows[0]][cols[1]] == flag and board[rows[1]][cols[1]] == flag and board[rows[2]][cols[1]] == flag:
			return True
		elif board[rows[0]][cols[2]] == flag and board[rows[1]][cols[2]] == flag and board[rows[2]][cols[2]] == flag:
			return True
		elif board[rows[0]][cols[0]] == flag and board[rows[1]][cols[1]] == flag and board[rows[2]][cols[2]] == flag:
			return True
		elif board[rows[0]][cols[2]] == flag and board[rows[1]][cols[1]] == flag and board[rows[2]][cols[0]] == flag:
			return True # from here
		elif board[rows[0]][cols[0]] == flag1 and board[rows[0]][cols[1]] == flag1 and board[rows[0]][cols[2]] == flag1:
			return True
		elif board[rows[1]][cols[0]] == flag1 and board[rows[1]][cols[1]] == flag1 and board[rows[1]][cols[2]] == flag1:
			return True
		elif board[rows[2]][cols[0]] == flag1 and board[rows[2]][cols[1]] == flag1 and board[rows[2]][cols[2]] == flag1:
			return True
		elif board[rows[0]][cols[0]] == flag1 and board[rows[1]][cols[0]] == flag1 and board[rows[2]][cols[0]] == flag1:
			return True
		elif board[rows[0]][cols[1]] == flag1 and board[rows[1]][cols[1]] == flag1 and board[rows[2]][cols[1]] == flag1:
			return True
		elif board[rows[0]][cols[2]] == flag1 and board[rows[1]][cols[2]] == flag1 and board[rows[2]][cols[2]] == flag1:
			return True
		elif board[rows[0]][cols[0]] == flag1 and board[rows[1]][cols[1]] == flag1 and board[rows[2]][cols[2]] == flag1:
			return True
		elif board[rows[0]][cols[2]] == flag1 and board[rows[1]][cols[1]] == flag1 and board[rows[2]][cols[0]] == flag1:
			return True
		else:
			return False 

	def check_win_state_new(self, block,move):
		no = (move[0]/3)*3
		no += (move[1]/3)
		if block[no] != '-':
			return False
		else:
			return True

	def get_empty(self, gameb, gameblock, blal, flag):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
					if gameb[i][j] == '-' and self.check_win_state_new(gameblock, (i,j)) == True:
						cells.append((i,j))
		#print "Block shizz", gameblock	
		#print "This is the shizz", cells
		return cells
	
	def generate_moves(self, node, flag):
		blocks = self.blocks_allowed(node.current_move, node.block)
		#print "Just pure Shiz ", node.block
		child_states = self.get_empty(node.board, node.block, blocks, flag)
		temp_board = node.board
		l = []
		for child in child_states:
			new_board = copy.deepcopy(temp_board)
			new_board[child[0]][child[1]] = flag
			temporary_block = copy.deepcopy(node.block)
			copy_update_lists(new_board, temporary_block, child, flag)
			child_node = Node(new_board, temporary_block, [], node, child) 
			l.append(child_node)
		return l

	def build_tree(self, root_node, depth, flag):
		child_states = []
		if self.root_node == None and root_node.current_move[0] == -1 and root_node.current_move[1] == -1:
			new_board = copy.deepcopy(root_node.board)
			temporary_block = copy.deepcopy(root_node.block)
			blocks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
			states = self.get_empty(new_board, temporary_block, blocks, flag)
			x, y = states[random.randrange(len(states))]
			new_board[x][y] = flag
			#temporary_block = copy.deepcopy(root_node.block)
			copy_update_lists(new_board, temporary_block, (x, y), flag)
			dummy = Node(new_board, temporary_block, [], root_node,(x, y))
			child_states.append(dummy)
			self.root_node = root_node    ## Have to send a legal node for the first time. i.e, parent set to none, child set to none etc.		
		
		if child_states == []:		#child states here are child nodes
			child_states = self.generate_moves(root_node, flag) ## generate_moves has to set child_states parent
		root_node.child_array = child_states
		parent = root_node
		layer_nodes = child_states
		
		while depth - 1:
			new_layer_nodes = []
			for node in layer_nodes:
				if node.child_array == []:
					if flag == 'x' : 
						flag = 'o'             
					else:
						flag = 'x'
					new_child_states = self.generate_moves(node, flag)
					node.child_array = new_child_states
					new_layer_nodes += new_child_states
				else:
					for child in node.child_array:
						child.heuristic = 0
						child.alpha = -sys.maxint - 1
						child.beta = sys.maxint 
			depth -= 1
			layer_nodes = new_layer_nodes
			
		return
