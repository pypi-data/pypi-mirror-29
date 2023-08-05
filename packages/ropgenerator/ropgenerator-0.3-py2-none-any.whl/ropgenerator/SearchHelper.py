# ROPGenerator - SearchHelper module 
# Keeping track of gadgets to fasten the search 
# This module supports the Gadget_finder module 
# It merely stores chains of gadgets obtained by different search strategies 

import Database
import Analysis
from Gadget import GadgetType

#####################################
#	ROP Chains format
#
# A ROP Chain is a list of gadget UID
# A negative UID ( so that does not correspond to a gadget) indicates padding units 
# UID -x is the padding unit stored at PADDING_UNITS[x] 
#
#######################################



# Some overall variables 
DEFAULT_PADDING_BYTE = 0xFF # The default byte used for padding 
PADDING_UNITS = []  # List of the different padding units ( as integers )
MAX_PADDING = 40 # The maximum padding accepted for a gadget in an ROP chain 
MAX_CHAINS = 10 # The maximum number of chains we store for one operation 



def is_padding(gadget_num):
	return gadget_num < 0 

def set_padding_unit():
	global DEFAULT_PADDING_BYTE
	global PADDING_UNITS
	
	if( PADDING_UNITS == [] ):
		# Set the default padding unit  
		bytes_in_unit = Analysis.ArchInfo.bits/8
		res = 0
		for i in range(0, bytes_in_unit):
			res = res*0x100 + DEFAULT_PADDING_BYTE
		PADDING_UNITS = [res]
		return -1
	else:
		## So far we return the default padding unit
		## Later we'll implement adding new padding_units (for other strategies)
		return -1
		
def get_padding_unit(uid=-1):
	global PADDING_UNITS
	return PADDING_UNITS[-1-uid]
	


#############################################
# Chains for REGtoREG transitivity strategy #
#############################################

record_REGtoREG_reg_transitivity = dict()
built_REGtoREG_reg_transitivity = False 


def build_REGtoREG_reg_transitivity(iterations):
	"""
	Builds chains for operation REG <- REG 
	Parameters:
		iterations - (int) Number of iterations for the transitive closure algorithm  
	"""
	# Transitive closure 
	#Initialisation 
	global built_REGtoREG_reg_transitivity
	global record_REGtoREG_reg_transitivity
	global PADDING_BYTE
	global PADDING_UNIT
	global PADDING_GADGET  
	global MAX_PADDING 
	
	# Choose a padding unit 
	padding_uid = set_padding_unit()
	
	# Transitive closure 
	# During algorithm the chains are stored as triples:
	# 	( chain, used_regs, nb_instr )
	# 	where used_regs is the list of registers we already considered for the chain rY <- rX <- .... <- rZ
	#	nb_instr is the total number of instructions (in REIL) composing the gadgets of the chain 
	db = Database.gadgetLookUp[GadgetType.REGtoREG]
	for reg1 in range(0,Analysis.ssaRegCount):
		record_REGtoREG_reg_transitivity[reg1] = dict()
		for reg2 in range(0,Analysis.ssaRegCount):
			record_REGtoREG_reg_transitivity[reg1][reg2] = []
			for gadget_num in db[reg1][reg2]:
				if( Database.gadgetDB[gadget_num].isValidSpInc() and Database.gadgetDB[gadget_num].hasNormalRet()  ):
					padding_units = (Database.gadgetDB[gadget_num].spInc - Analysis.ArchInfo.bits/8)/8
					if( padding_units <= MAX_PADDING ):
						padding_chain = [padding_uid for i in range(0,padding_units)] 
						nbInstr = Database.gadgetDB[gadget_num].nbInstr
						add_REGtoREG_reg_transitivity(reg1, reg2, [gadget_num]+padding_chain, [reg2], nbInstr)
				else:
					pass
				
	modified = True
	while( modified and (iterations > 0)):
		modified = False
		iterations = iterations - 1
		for reg1 in range(0,Analysis.ssaRegCount):
			for reg2 in range(0,Analysis.ssaRegCount):
				for reg3 in range(0,Analysis.ssaRegCount):
					if( reg3 != reg1 and reg1 != reg2 and reg2 != reg3 ):
						for chain2_3 in record_REGtoREG_reg_transitivity[reg2][reg3]:
							for chain1_2 in record_REGtoREG_reg_transitivity[reg1][reg2]:
								# Check for path redundency and looping 
								if( not [reg for reg in chain2_3[1] if reg in chain1_2[1]]):
									new_chain = chain2_3[0] + chain1_2[0]
									new_regs_chain = chain2_3[1] + [reg2] + chain1_2[1]
									new_nbInstr = chain2_3[2] + chain1_2[2]
									added = add_REGtoREG_reg_transitivity(reg1, reg3, new_chain, new_regs_chain, new_nbInstr)
									modified = modified or added
									
								else:
									pass
									
									
									
	# Remove the reg paths 
	for reg1 in range(0,Analysis.ssaRegCount):
		for reg2 in range(0,Analysis.ssaRegCount):
			record_REGtoREG_reg_transitivity[reg1][reg2] = [c[0] for c in record_REGtoREG_reg_transitivity[reg1][reg2]]		
			
										
	built_REGtoREG_reg_transitivity = True
			


def add_REGtoREG_reg_transitivity(reg1, reg2, chain , regs_chain, nbInstr):
	"""
	Adds gadgets that put reg2 into reg1 
	Addition is made in increasing order ( order is number of gadgets in the chain, and if equal then the number of instructions of the chain ) to get the best chains (shorter) first 
	
	Parameters:
		chain = ROP chain ( list of gadgets, e.g [4,365,3,4] )
		regs_chain = the list of the registers appearing in the path of chain
		nbInstr = nb of REIL instructions of chain 
		reg1, reg2 = int
	
	Returns true if added the chain, or False if the chain was already present 
	"""
	# DURING SEARCH, chains or not only lists of gadgets but triples (gadget_list, list of used intermediate resigters, number of instructions) to avoid looping through the same gadgets over and over again  
	
	global record_REGtoREG_reg_transitivity
	global MAX_CHAINS
	
	#print("DEBUG I AM CALLING THIS SHIT ?") 
	if( not chain ):
		#print("DEBUG ERROE CHAIN IS EMPTY")
		return False
	if( not reg1 in record_REGtoREG_reg_transitivity ):
		record_REGtoREG_reg_transitivity[reg1] = dict()
	if( not reg2 in record_REGtoREG_reg_transitivity[reg1] ):
		record_REGtoREG_reg_transitivity[reg1][reg2] = []
	
	# Adding the chain in sorted 
	for i in range(0, len(record_REGtoREG_reg_transitivity[reg1][reg2])):
		if( i >= MAX_CHAINS ):
			return False
		nbInstr_recorded_chain = record_REGtoREG_reg_transitivity[reg1][reg2][i][2]
		if( chain == record_REGtoREG_reg_transitivity[reg1][reg2][i][0] ):
			return False
		elif( len(chain) < len(record_REGtoREG_reg_transitivity[reg1][reg2][i][0])):
			record_REGtoREG_reg_transitivity[reg1][reg2].insert(i, (chain, regs_chain, nbInstr))
			
			#print("DEBUG Inserted " + str(chain) + " into " + str(record_REGtoREG_reg_transitivity[reg1][reg2]))
			if( len(record_REGtoREG_reg_transitivity[reg1][reg2]) >= MAX_CHAINS ):
				del record_REGtoREG_reg_transitivity[reg1][reg2][-1]
			return True
		elif( len(chain) <= len(record_REGtoREG_reg_transitivity[reg1][reg2][i][0]) and nbInstr <= nbInstr_recorded_chain):
			record_REGtoREG_reg_transitivity[reg1][reg2].insert(i, (chain, regs_chain, nbInstr))
			#print("DEBUG Inserted " + str(chain) + " into " + str(record_REGtoREG_reg_transitivity[reg1][reg2]))	
			if( len(record_REGtoREG_reg_transitivity[reg1][reg2]) >= MAX_CHAINS ):
				del record_REGtoREG_reg_transitivity[reg1][reg2][-1]
			return True
	# If longer than all, add in the end 
	if( len(record_REGtoREG_reg_transitivity[reg1][reg2]) < MAX_CHAINS ):
		record_REGtoREG_reg_transitivity[reg1][reg2].append((chain, regs_chain, nbInstr))
		return True
	else:
		return False
	
def found_REGtoREG_reg_transitivity(reg1, reg2, n=1):
	"""
	Returns the n first chains found for reg1 <- reg2 
	"""
	global record_REGtoREG_reg_transitivity
	if( not reg1 in record_REGtoREG_reg_transitivity ):
		return []
	if( reg2 in record_REGtoREG_reg_transitivity[reg1] ):
		return record_REGtoREG_reg_transitivity[reg1][reg2][:n]
	else:
		return []	
