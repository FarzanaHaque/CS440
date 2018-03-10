def alpha_beta(self,level_0_node):
	lev_0_max=float('-inf')
	for level_1_node in level_0_node['children']:
		lev_1_min=float('inf')
		for level_2_node in level_1_node['children']:
			lev_3_max=float('-inf')
			valid=1
			for level_3_node in level_2_node['children']:
				ret = eval_function[level_3_node['initial_board']]
				if ret > lev_1_min:
					valid=0
					break
				if ret > lev_3_max:
					lev_3_max=ret
					
			if valid:
				level_2_node['value']=lev_3_max   
			else:
				level_2_node['value']=float('inf')
			if level_2_node['value'] < lev_1_min:
				lev_1_min = level_2_node['value']
				
		level_1_node['value']=lev_1_min
		if level_1_node['value']>lev_0_max:
			lev_0_max=level_1_node['value']
			
	level_0_node['value']=lev_0_max