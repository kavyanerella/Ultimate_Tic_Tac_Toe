import python_tree
import copy


dummy_board, dummy_block = get_init_board_and_blockstatus()
tree = python_tree.Tree()
old_node = python_tree.Node(dummy_board, dummy_block, [], None, (-1, -1))

class Player87:
	
	
	def __init__(self):
		pass

	def heuristic(self, temp_board, block_stat, flag):
		h_values = []
		h_values.append(self.heuristic_mini([temp_board[0][0], temp_board[0][1], temp_board[0][2],temp_board[1][0], temp_board[1][1], temp_board[1][2], temp_board[2][0], temp_board[2][1], temp_board[2][2] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[0][3], temp_board[0][4], temp_board[0][5],temp_board[1][3], temp_board[1][4], temp_board[1][5], temp_board[2][3], temp_board[2][4], temp_board[2][5] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[0][6], temp_board[0][7], temp_board[0][8],temp_board[1][6], temp_board[1][7], temp_board[1][8], temp_board[2][6], temp_board[2][7], temp_board[2][8] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[3][0], temp_board[3][1], temp_board[3][2],temp_board[4][0], temp_board[4][1], temp_board[4][2], temp_board[5][0], temp_board[5][1], temp_board[5][2] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[3][3], temp_board[3][4], temp_board[3][5],temp_board[4][3], temp_board[4][4], temp_board[4][5], temp_board[5][3], temp_board[5][4], temp_board[5][5] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[3][6], temp_board[3][7], temp_board[3][8],temp_board[4][6], temp_board[4][7], temp_board[4][8], temp_board[5][6], temp_board[5][7], temp_board[5][8] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[6][0], temp_board[6][1], temp_board[6][2],temp_board[7][0], temp_board[7][1], temp_board[7][2], temp_board[8][0], temp_board[8][1], temp_board[8][2] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[6][3], temp_board[6][4], temp_board[6][5],temp_board[7][3], temp_board[7][4], temp_board[7][5], temp_board[8][3], temp_board[8][4], temp_board[8][5] ], flag, 0))
		h_values.append(self.heuristic_mini([temp_board[6][6], temp_board[6][7], temp_board[6][8],temp_board[7][6], temp_board[7][7], temp_board[7][8], temp_board[8][6], temp_board[8][7], temp_board[8][8] ], flag, 0))
		h_small = 0
		for i in h_values:
			h_small += i
		h_big = self.heuristic_mini(block_stat, flag, 1)
		return h_small + h_big

	def heuristic_mini(self,mini_board, flag, decide):
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


	def alpha_beta_new(self, branch, depth, alpha, beta, flag):
		if len(branch.child_array) == 0:
			if(depth % 2 == 1):
				branch.beta = self.heuristic(branch.board, branch.block, flag)
				#print depth, "branch_beta=", branch.beta 
			else:
				branch.alpha = self.heuristic(branch.board, branch.block, flag)
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


