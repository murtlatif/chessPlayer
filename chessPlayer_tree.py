# Create a queue class to assist with getLevelOrder
class treeQueue:
	
	# Initialize an empty storage
	def __init__(self):
		self.store = []
		
	# Add items to storage
	def push(self, item):
		self.store += [item]
		return True
	
	# Remove first item in the queue
	def pop(self):
		if (len(self.store) > 0):
			item = self.store[0]
			self.store = self.store[1: len(self.store)]
			return item
		return False
		
# Create a tree class 
class tree:
	
	# Initialize a storage value that contains the player value, the initial/final positions and a list of nodes
	def __init__(self, move):
		self.store = [move, False, []]
		self.nextBest = None
		
	# Adds a successor node ot the list of nodes
	def addSuccessor(self, successor):
		# Add a successor to the children
		self.store[2] += [successor]
		return True
		
	# Display the depth first order of the tree
	def printDepthFirst(self, tabs):
		printNextBest = self.nextBest
		if self.nextBest:
			printNextBest = self.nextBest.getMove()
		print [self.store[0], self.store[1], printNextBest]
		# Loop through all children
		for node in self.store[2]:
			if node != None:
				for tab in range(0, tabs + 1):
					print '\t',
				node.printDepthFirst(tabs + 1)
		return True
		
	# Gets the level order of the tree
	def getLevelOrder(self):
		# Setup
		treeQ = treeQueue() # Initialize a treeQueue
		levels = []			# Initialize a list of levels
		treeQ.push(self)	# Add the current tree to the tree
		self.getLevels(treeQ, levels)
		return levels
	
	# Get the levels of the tree
	def getLevels(self, treeQ, levels):
		node = treeQ.pop()
		if (not node):
			return True
			
		levels.append(node.store[0])
		for treeNode in node.store[2]:
			treeQ.push(treeNode)
		for treeNode in treeQ.store:
			treeNode.getLevels(treeQ, levels)
		return True
	
	# Get the evaluation value of the tree
	def getEvaluation(self):
		return self.store[1]
		
	# Sets the evaluation score of the tree
	def setEvaluation(self, value):
		self.store[1] = value
		return True
	
	# Set the value for the next best move
	def setNextBest(self, child):
		self.nextBest = child
		return True
	
	# Set the value for the next best move
	def getNextBest(self):
		return self.nextBest
	
	# Get the 2-list move = [initialPos, finalPos]
	def setMove(self, move):
		self.store[0] = move
		return True
	
	# Get the 2-list move = [initialPos, finalPos]
	def getMove(self):
		return self.store[0]
	
	# Get all the children of the tree
	def getChildren(self):
		children = []
		for child in self.store[2]:
			children.append(child)
		return children

	# Get the store value of the tree
	def getStore(self):
		return self.store

class treeStore:
	
	def __init__(self):
		self.store = []