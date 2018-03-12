from chessPlayer_tree import *

def getPiece(name):
	# Retrieve piece values from name
	if name == 'pawn':
		return 0
	elif name == 'knight':
		return 1
	elif name == 'bishop':
		return 2
	elif name == 'rook':
		return 3
	elif name == 'queen':
		return 4
	elif name == 'king':
		return 5
	else:
		return False

def getNameOfPiece(value):
	if value == 0:
		return 'pawn'
	elif value == 1:
		return 'knight'
	elif value == 2:
		return 'bishop'
	elif value == 3:
		return 'rook'
	elif value == 4:
		return 'queen'
	elif value == 5:
		return 'king'
	else:
		return False

def genBoard():
	# Initializes a chess board with starting pieces in place on an 8x8 board.
	board = [13, 11, 12, 15, 14, 12, 11, 13,
			10, 10, 10, 10, 10, 10, 10, 10,
			0,	0,	0,	0,	0,	0,	0,	0,
			0,	0,	0,	0,	0,	0,	0,	0,
			0,	0,	0,	0,	0,	0,	0,	0,
			0,	0,	0,	0,	0,	0,	0,	0,
			20, 20, 20, 20, 20, 20, 20, 20,
			23, 21, 22, 25, 24, 22, 21, 23]
	
	return board

def getSymbol(inputValue):
	symbolListWhite = ['WP', 'WK', 'WB', 'WR', 'WQ', 'WK+']
	symbolListBlack = ['BP', 'BK', 'BB', 'BR', 'BQ', 'BK+']
	
	# Return empty space for 0 value
	if inputValue == 0:
		return ''
	
	# Checking if input value is valid.
	# Valid range of inputs is: [0, 10-15, 20-25]
	if ((inputValue < 10) or (inputValue > 25)):
		return False
	
	# For white piece input
	if inputValue < 20:
		return symbolListWhite[inputValue % 10]
	# For black piece input
	elif inputValue >= 20:
		return symbolListBlack[inputValue % 10]
		
def gamePrintBoard(board, showValues):
	
	# Prints out a readable format of the chess board
	
	# If the input is not a len = 64 then 
	if len(board) != 64:
		print('Error! Board is not a list of 64 elements.')
		return -1
	
	# Create a string to be able to manipulate it before printing it
	# boardprint setup
	boardprint = ''
	for row in range(7, -1, -1):
		# Prints horizontal line every row
		boardprint = boardprint + ('-' * 49) + '\n' 
		
		# DEBUG PRINT
		# if showValues:
		# 	# Printing first line of contents: position value of the board
		# 	for column in range(7, -1, -1):
		# 		currentVal = '{0:^3}'.format(board[(row * 8) + column])	# Set the value inside the square
		# 		boardprint = boardprint + "| " + currentVal + ' '
		# 	# Appending necessary string values
		# 	boardprint = boardprint + '|\n'
		
		# Printing second line of contents: symbol character of value on the board
		for column in range(7, -1, -1):
			symbolVal = '{0:^3}'.format(getSymbol(board[(row * 8) + column]))
			boardprint = boardprint + "| " + symbolVal + ' '
		# Appending necessary string values
		boardprint = boardprint + '|\n'
		
		if showValues:
			# Printing third line of contents: position index on the board
			for column in range(7, -1, -1):
				currentPos = '{0:^3}'.format((row * 8) + column) # Set the position of each square
				boardprint = boardprint + "| " + currentPos + ' '
			# Appending necessary string values
			boardprint = boardprint + '|\n'
	
	# Add bottom frame to the last line of the string
	boardprint = boardprint + ('-' * 49)
	
	print boardprint
	return True
	
def printBoard(board):
	gamePrintBoard(board, False)
	return True

# Move a piece
def testMove(board, move):
	# Cannot move to a position with a piece of the same team, and cannot perform a null movement
	if ((board[move[1]] // 10 == board[move[0]] // 10) or (move[1] == move[0])):
		return False

	board[move[1]] = board[move[0]]
	board[move[0]] = 0
	return True

def GetPlayerPositions(board, player):
	# Returns a list of positions on the board for all of a player's pieces
	# Player definitions
	white = 10
	black = 20
	
	# If input was not a player value
	if (player != white) and (player != black):
		return []
	else:
		# Creates a list of 2-list 
		boardValues = zip(board, range(0, 64))

		# Filter out all values that do not contain the player's position
		# filter(func, list) removes all values that do not match with the function
		filteredBoardValues = filter(lambda values : ((values[0] - player) <= 5) and ((values[0] - player) >= 0), boardValues)
		
		# Return the position values only
		return map(lambda x:x[1],filteredBoardValues)

# Find the player value of the targeted piece
def getPlayer(board, position):
	if board[position] in range(10, 16):
		return 10
	elif board[position] in range(20, 26):
		return 20
	return False

# Get the opponent's colour value
def getOpponent(player):
	white = 10
	black = 20
	if player == white:
		return black
	elif player == black:
		return white
	else:
		return False

# Gets the position of the player's king
def getKingPosition(board, player):
	# Gets all player positions
	playerPositions = GetPlayerPositions(board, player)
	# Search through the board and find the index of the player's king
	king = board.index(player + 5)
	return king

# Checking if position is on the board
def isOnBoard(position):
	if ((position > 63) or (position < 0)):
		return False
	return True

# Checking if position is empty
def isPosEmpty(board, position):
	if board[position] == 0:
		return True
	else:
		return False

# Checking if a certain position's value is equal to a piece
def isPiece(board, position, piece):
	checkingPiece = board[position]
	
	# Checking if input values are valid.
	# Valid range of inputs is: [0, 10-15, 20-25]
	if ((checkingPiece < 10) or (checkingPiece > 25)):
		return False
	# If the requested piece is a valid option
	if (getPiece(piece) is False):
		return False
	# If the piece matches requested piece
	if checkingPiece % 10 == getPiece(piece):
		return True

# Check if that many horizontal movements go off the board
def checkHorizontal(position, steps):
	# Cannot divide or modulo by zero so deal with this seperately
	if steps == 0:
		return True
	currentRow = position // 8
	if (((position + steps) // 8) != currentRow):
		return False
	else:
		return True

# Check if that many vertical movements go off the board
def checkVertical(position, steps):
	# Cannot divide or modulo by zero so deal with this seperately
	if steps == 0:
		return True
	newRow = (position + steps) // 8
	if newRow in range(0, 7):
		return True
	else:
		return False
	
# Finding all legal moves for a pawn
def getPawnMoves(board, position):
	# Defining setup variables
	white = 10
	black = 20
	direction = 0
	forwardMovement = 8
	pawn = board[position]
	legalMoves = []
	
	# Setting direction based on player colour
	if pawn == white:
		direction = +1
	elif pawn == black:
		direction = -1
		
	# Moving forward
	forwardPos = position + (direction * forwardMovement)
	if isOnBoard(forwardPos) and isPosEmpty(board, forwardPos):
		legalMoves.append(forwardPos)
	
	# Capturing enemies diagonally
	forwardLeft = forwardPos + direction
	forwardRight = forwardPos - direction
	diagonals = [1, -1] # 1 for a left turn, -1 for a right turn
	for diagonal in diagonals:
		forwardDiagonal = forwardPos + (diagonal * direction)
		# Check if the horizontal position does not move off board
		if checkHorizontal(forwardPos, (diagonal * direction)):
			
			# Check if the diagonal position is <on the board> and <has an opponent>
			if (isOnBoard(forwardDiagonal) and ((getPlayer(board, position) != getPlayer(board, forwardDiagonal)) and not isPosEmpty(board, forwardDiagonal))):
				legalMoves.append(forwardDiagonal)
				
	return legalMoves

# Finding all legal moves for a knight
def getKnightMoves(board, position):
	# Defining setup variables
	knight = board[position]
	knightColour = getPlayer(board, position)
	legalMoves = []
	
	# Check 2 x <vertical movement> and 1 x <horizontal movement>
	for vertical in [-16, 16]:
		for horizontal in [-1, 1]:
			# Check if the horizontal and vertical movement get player off the board
			if checkHorizontal(position, horizontal) and checkVertical(position, vertical):
				# Check if the new position has an opponent piece or is empty
				newPosition = position + vertical + horizontal
				if getPlayer(board, newPosition) != knightColour:
					legalMoves.append(newPosition)
	
	# Check 1 x <vertical movement> and 2 x <horizontal movement>
	for vertical in [-8, 8]:
		for horizontal in [-2, 2]:
			# Check if the horizontal and vertical movement get player off the board
			if checkHorizontal(position, horizontal) and checkVertical(position, vertical):
				# Check if the new position has an opponent piece or is empty
				newPosition = position + vertical + horizontal
				if getPlayer(board, newPosition) != knightColour:
					legalMoves.append(newPosition)
					
	return legalMoves

# Finding all legal moves for a bishop
def getBishopMoves(board, position):
	# Defining setup variables
	bishop = board[position]
	bishopColour = getPlayer(board, position)
	legalMoves = []
	
	# Movement values for a bishop
	plusDiag = 8 - 1 # <Up 1, right 1>; -plusDiag is <Down 1, left 1>
	minusDiag = 8 + 1 # <Up 1, left 1>; -plusDiag is <Down 1, right 1>
	
	# Finding the maximum amount of up/down/right/left movements
	maxRight = position % 8
	maxLeft = 7 - (position % 8)
	maxUp = 7 - (position // 8)
	maxDown = position // 8
	
	# Create a list to be able to iterate through all directions
	vdirections = [maxUp, maxDown]
	hdirections = [maxRight, maxLeft]
	
	# Loop through all vertical directions
	for vdirection in vdirections:
		# Loop through horizontal directions for each vertical direction
		for hdirection in hdirections:
			# Maximum travel distance is the minimum max travel distances vertically and horizontally
			possibleDistance = min(vdirection, hdirection)
			for i in range(possibleDistance):
				# Setting whether to use plusDiag or minusDiag
				diagMovement = 0
				if vdirections.index(vdirection) == hdirections.index(hdirection):
					diagMovement = plusDiag
				else:
					diagMovement = minusDiag
				# If moving down, diagMovement is negative
				if (vdirections.index(vdirection) == 1):
					diagMovement = -diagMovement
				# Evaluate newPosition
				newPosition = position + (diagMovement * (i + 1))
				if isPosEmpty(board, newPosition):
					legalMoves.append(newPosition)
				else:
					if getPlayer(board, newPosition) != bishopColour:
						legalMoves.append(newPosition)
					break

	return legalMoves

# Finding all legal moves for a rook
def getRookMoves(board, position):
	# Defining setup variables
	rook = board[position]
	rookColour = getPlayer(board, position)
	legalMoves = []
	
	# Finding the maximum amount of up/down/right/left movements
	maxRight = position % 8
	maxLeft = 7 - (position % 8)
	maxUp = 7 - (position // 8)
	maxDown = position // 8
	
	# Create a list to be able to iterate through all directions
	directions = [maxUp, maxDown, maxLeft, maxRight]
	# Loop through all directions
	for i in range(len(directions)):
		direction = directions[i]
		# Maximum travel distance is the minimum max travel distances vertically and horizontally
		possibleDistance = direction
		for distance in range(possibleDistance):
			# Setting which movement value to use
			movement = 0
			if i < 2:
				# Set movement to 8 if direction is vertical
				movement = 8
			else:
				# Set movement to 1 if direction is horizontal
				movement = 1
			# Set the signage of movement (right and down are negative)
			if i % 2 == 1:
				movement = -movement
			# Evaluate newPosition
			newPosition = position + (movement * (distance + 1))
			if isPosEmpty(board, newPosition):
				legalMoves.append(newPosition)
			else:
				if getPlayer(board, newPosition) != rookColour:
					legalMoves.append(newPosition)
				break
			
	return legalMoves

# Finding all legal moves for a queen
def getQueenMoves(board, position):
	legalMoves = []
	
	# A queen's set of moves is the set of rook moves and bishop moves combined
	legalMoves += getRookMoves(board, position) + getBishopMoves(board, position)
	
	return legalMoves

# Finding all legal moves for a king
def getKingMoves(board, position):
	king = board[position]
	kingColour = getPlayer(board, position)
	legalMoves = []
	
	# A king can move in all directions for one unit
	# Check 2 x <vertical movement> and 1 x <horizontal movement>
	for vertical in [-8, 0, 8]:
		for horizontal in [-1, 0, 1]:
			if (not (vertical == 0 and horizontal == 0)):
				# Check if the horizontal and vertical movement get player off the board
				if checkHorizontal(position, horizontal) and checkVertical(position, vertical):
					# Check if the new position has an opponent piece or is empty
					newPosition = position + vertical + horizontal
					if getPlayer(board, newPosition) != kingColour:
						legalMoves.append(newPosition)
		
	return legalMoves
	
def GetPieceRawLegalMoves(board, position):
	# If position is not on board
	if (position < 0) or (position > 63):
		return False
	
	# If position does not contain a piece
	if (board[position] % 10) not in range(0,6):
		return False
		
	# Setup variables
	legalMoves = []
	
	# Check piece and return legal moves of that piece
	if isPiece(board, position, 'pawn'):
		legalMoves += getPawnMoves(board, position)
		 
	if isPiece(board, position, 'knight'):
		legalMoves += getKnightMoves(board, position)
	
	if isPiece(board, position, 'bishop'):
		legalMoves += getBishopMoves(board, position)
	
	if isPiece(board, position, 'rook'):
		legalMoves += getRookMoves(board, position)
		
	if isPiece(board, position, 'queen'):
		legalMoves += getQueenMoves(board, position)
	
	if isPiece(board, position, 'king'):
		legalMoves += getKingMoves(board, position)
	
	return legalMoves

# Getting the legal moves of a piece, filtering moves that put the king in check
def GetPieceLegalMoves(board, position):
	# If position is not on board
	if (position < 0) or (position > 63):
		return False
	
	# If position does not contain a piece
	if (board[position] % 10) not in range(0,6):
		return False
	
	# If position is empty	
	if isPosEmpty(board, position):
		return []
	
	# Setup variables
	pieceColour = getPlayer(board, position)
	kingPosition = getKingPosition(board, pieceColour)
	legalMoves = GetPieceRawLegalMoves(board, position)
	dummyLegalMoves = list(legalMoves)
	
	# Use a dummy list because .remove() skips the next index if looping while calling it
	for legalMove in dummyLegalMoves:
		if WillPositionBeUnderThreat(board, kingPosition, pieceColour, [position, legalMove]):
			legalMoves.remove(legalMove)
			
	return legalMoves

# Checking if a piece can be taken next round
def IsPositionUnderThreat(board, position, player):
	white = 10
	black = 20
	threatened = False
	opponentLegalMoves = []
	# Trivial cases where position cannot be under threat: invalid position, piece at position is not caller's player
	if ((not isOnBoard(position)) or getPlayer(board, position) != player):
		return False
	
	# If a possible move of an opponent is equal to piece's current position then position is under threat
	# Get the opponent's player value
	opponent = getOpponent(player)
	
	# Get all the possible positions that the all opponent pieces can move to
	opponentPiecePositions = GetPlayerPositions(board, opponent)
	for opponentPiecePosition in opponentPiecePositions:
		opponentLegalMoves += GetPieceRawLegalMoves(board, opponentPiecePosition)
	
	# Create a list of unique positions
	opponentLegalMoves = list(set(opponentLegalMoves))
	
	# The piece at <position> is in check if one of the opponent's legal moves is to that position
	if position in opponentLegalMoves:
		threatened = True
	
	return threatened

# Checks whether a certain piece will be threatened after a piece makes a move
def WillPositionBeUnderThreat(board, position, player, move):
	# position is the piece under consideration
	# initialPos and finalPos are positions for the move that will be made
	# Setup variables
	white = 10
	black = 20
	threatened = False
	opponentLegalMoves = []
	
	# Create a test board
	testBoard = list(board)
	
	# Perform the requested move and evaluate the board at that state
	if (not testMove(testBoard, move)):
		return False
	
	# Trivial cases where position cannot be under threat: invalid position, piece at position is not caller's player
	if ((not isOnBoard(position)) or getPlayer(testBoard, move[1]) != player):
		return False
	
	# If the piece that is moving is the king
	if (position == move[0]):
		position = move[1]
	
	# If a possible move of an opponent is equal to piece's current position then position is under threat
	# Get the opponent's player value
	opponent = getOpponent(player)
	
	# Get all the possible positions that the all opponent pieces can move to
	opponentPiecePositions = GetPlayerPositions(testBoard, opponent)
	for opponentPiecePosition in opponentPiecePositions:
		opponentLegalMoves += GetPieceRawLegalMoves(testBoard, opponentPiecePosition)
	
	# Create a list of unique positions
	opponentLegalMoves = list(set(opponentLegalMoves))
	# The piece at <position> is in check if one of the opponent's legal moves is to that position
	if position in opponentLegalMoves:
		threatened = True
	
	return threatened

# Get an evaluation for the state of the board relative to the player
def evaluateBoard(board, player):
	# Setup variables
	score = 0.0
	opponent = getOpponent(player)
	# Create a list of values for each piece
	# In the order of [pawn, knight, bishop, rook, queen, king]
	pieceValues = [10.0, 35.0, 35.0, 52.5, 150.0, 10000000.0]
	
	# The relative rankings for each piece having higher mobility
	mobilityRatings = [1.125, 1, 1, 1, 1, 1]
	
	# Add score for the player's pieces
	for piecePos in GetPlayerPositions(board, player):
		piece = board[piecePos] % 10
		
		# Make sure that the piece is a valid number
		if ((piece < 0) or (piece > 5)):
			return False
		
		# If the player has more mobility than the player has more score.
		mobilityScore = len(GetPieceRawLegalMoves(board, piecePos)) * mobilityRatings[piece]
		score += mobilityScore
		
		# The player earns score for having more (and higher value) pieces
		score += pieceValues[piece]
		
		#if IsPositionUnderThreat(board, piecePos, player):
		#	score -= pieceValues[piece] * 0.80
			#print 'You are threatened!', piecePos
	
	# Remove score for the opponent having pieces
	for opponentPiecePos in GetPlayerPositions(board, opponent):
		opponentPiece = board[opponentPiecePos] % 10
		
		# Make sure that the piece is a valid number
		if ((opponentPiece < 0) or (opponentPiece > 5)):
			return False
			
		#If the opponent has more mobility than the player has less score.
		mobilityScore = len(GetPieceRawLegalMoves(board, opponentPiecePos)) * mobilityRatings[opponentPiece]
		score -= mobilityScore
		
		# The player earns score for the opponent having less (and lower value) pieces
		score -= pieceValues[opponentPiece]
	
		#if IsPositionUnderThreat(board, opponentPiecePos, opponent):
		#	score += pieceValues[piece] * 0.70
			#print 'Opponent threatened!', opponentPiecePos
	
	return score
	
# Uses evaluateBoard for a test movement, (does not actually perform the move)
def evaluateBoardAt(board, player, move):
	evaluation = 0.0
	
	# Make sure the positions are valid
	if (not(isOnBoard(move[0]) and isOnBoard(move[1]))):
		return False
	
	# Create a test board
	testBoard = list(board)
	
	# Perform the requested move and evaluate the board at that state
	if (testMove(testBoard, move)):
		evaluation = evaluateBoard(testBoard, player)
	else:
		return False
	
	return evaluation

# Gets a list of all possible moves
def getAllMoves(board, player):
	# Initialize a list to store all possible moves
	allMoves = []
	# Iterate through all pieces
	for piecePos in GetPlayerPositions(board, player):
		# Iterate through all legal moves of that piece
		for legalMove in GetPieceLegalMoves(board, piecePos):
			allMoves.append([piecePos, legalMove])
	return allMoves

# Returns the maximum value for even depths, minimum value for odd depths
def determineNextMove(board, move, player, depth, bestMax, bestMin):
	# Get the opponent player
	opponent = getOpponent(player)
	
	currentTree = tree(move)
	
	# Terminate the traversal when hitting the base case
	if depth == 0:
		currentTreeEvaluation = evaluateBoard(board, player)
		currentTree.setEvaluation(currentTreeEvaluation)
		return currentTree
	
	# Determine whether function is maximizing or minimizing
	# Function is maximizing when at even depths (0, 2, ...) and minimizing at odd depths
	maximizing = (depth % 2 == 0)
	
	# Loop through all possible moves
	for possibleMove in getAllMoves(board, player):
		# Re-initialize testBoard
		testBoard = list(board)
		
		# Make the move on the testBoard
		testMove(testBoard, possibleMove)
		
		# Determine the value of the next move
		possibleMoveNode = determineNextMove(testBoard, possibleMove, opponent, depth - 1, bestMax, bestMin)
		
		if (not possibleMoveNode):
			continue
		
		possibleMoveValue = possibleMoveNode.getEvaluation()
		
		# Add the possible move node as a child of the current node
		currentTree.addSuccessor(possibleMoveNode)
		
		# Perform maximizing functions
		if maximizing:
		
			# The bestMax will be the maximum between the 
			# current bestMax and the value of the next move.
			if possibleMoveValue > bestMax:
				bestMax = possibleMoveValue
				# Set the next best move of the current node to this possible move
				currentTree.setNextBest(possibleMoveNode)
				
			# Essentially, we can perform this function:
			# bestMax = max(bestMax, possibleMoveValue)
			# If the best move was not recorded
			
			# Set the evaluation of the current node to the best maximum value
			currentTree.setEvaluation(bestMax)
			
		# Perform minimizing function (maximizing for the opponent)
		else:
			
			# The bestMin will be the minimum between the
			# current bestMin and the value of the next move.
			if possibleMoveValue < bestMin:
				bestMin = possibleMoveValue
				# Set the next best move of the current node to this possible move
				currentTree.setNextBest(possibleMoveNode)
				
			# Essentially, we can perform this function:
			# bestMin = min(bestMin, possibleMoveValue)
			# If the best move was not recorded
			
			# Set the evaluation of the current node to the best minimum value
			currentTree.setEvaluation(bestMin)
			
		# If the best possible value is greater than the opponent's best possible value
		if bestMax >= bestMin:
			# Ignore the rest of the moves, because opponent will not allow it
			break
	
	return currentTree

# Retrieves the best possible move 
def chessPlayer(board, player):
	# Return variables
	status = True
	move = []
	candidateMoves = []
	evalTree = None
	
	# Setting up variables
	opponent = getOpponent(player)
	bestMoveTree = None
	bestMove = []
	alpha = -99999
	beta = 99999
	
	#Iterate through all player moves and find the move that provides
	#the lowest enemy score (the player's highest score)
	playerMoves = getAllMoves(board, player)
	for playerMove in playerMoves:
		nextMoveTree = determineNextMove(board, playerMove, opponent, 2, alpha, beta)
		# If the determineNextMove doesn't return a tree skip to the next move
		if (not nextMoveTree):
			continue
		
		# Getting the score of the move
		nextMoveScore = nextMoveTree.getEvaluation()
		# Checking whether the current enemy score is less than the current highest enemy score
		
		#print nextMoveTree.getStore()
		if -nextMoveScore > alpha:
			bestMoveTree = nextMoveTree
			bestMove = nextMoveTree.getMove()
			alpha = -nextMoveScore
			#print 'Yes! score:', nextMoveScore, 'move:', bestMove
		# Add the move to the list of candidate moves
		candidateMoves += [nextMoveTree.getMove(), nextMoveTree.getEvaluation()]
	
	move = bestMove
	evalTree = bestMoveTree
	
	evalTree.printDepthFirst(0)
	# If the function fails to retrieve the following information, the function fails and returns False
	if ((move == []) or (candidateMoves == []) or (evalTree == None)):
		status = False
	
	return [status, move, candidateMoves, evalTree]

# Initiates a game of chess
def play():
	# Setup variables
	white = 10
	black = 20
	option = '0'
	turn = white
	nextTurn = black
	turnText = ''
	yourturn = True
	# Initialize a game board
	board = genBoard()
	# Loops until the user exits with 'exit'
	while (option != 'exit'):
		
		# Set the turn-based variables
		if turn == white:
			turnText = 'WHITE'
		else:
			turnText = 'BLACK'
		nextTurn = getOpponent(turn)
		
		# Prompting user for input.
		option = raw_input("Type 'exit' to stop playing. Press enter to continue.\n")
		
		# Stop playing if 'exit' is submitted
		if option.lower() == 'exit':
			break
		
		# Display game board
		print ('=' * 17), turnText + '\'s TURN', ('=' * 17)
		gamePrintBoard(board, True)
		
		# Prompt user until their turn ends.
		while yourturn:
			# Continuously loop as long as their inputted position is invalid
			validPosition = False
			while (not validPosition):
				option = raw_input("Input the position of the piece you'd like to move.\n")
				# Check if input is a number -- not priority. might add later.
				# Check if piece at inputted position belongs to player
				if (int(option) in GetPlayerPositions(board, turn)):
					break
				# Check if the position is on the board
				elif (not (isOnBoard(int(option)))):
					print("Please select a number from 0 to 63.")
				# Check if the position is empty
				elif (isPosEmpty(board, int(option))):
					print("That position is empty.")
				# Check if the position is an opponent
				elif (int(option) in GetPlayerPositions(board, nextTurn)):
					print("That is the opponent's piece!")
			
			# Selection variables
			selectedPosition = int(option)	
			selectedPiece = board[selectedPosition]
			selectedPieceName = getNameOfPiece(selectedPiece % 10) 
			legalMoves = GetPieceLegalMoves(board, selectedPosition)
			
			# Feedback
			print "You've selected a", selectedPieceName + '.'
			
			while (not validPosition):
				# Prompt user for their final position
				option = raw_input("Type 'back' if you want to go back.\n")
				print("Input the position you'd like to move the " + str(selectedPieceName) + " to.")
				# Restart loop if user wants to go back
				if option.lower() == 'back':
					break
				# Check if selected position is a legal move
				if (int(option)) in legalMoves:
					validPosition = True
				else:
					validPosition = False
					print("That's not a legal move.")
				
			# If the user did not select 'back' as their option.
			if (option.lower() != 'back'):
				selectedFinalPosition = int(option)
				testMove(board, [selectedPosition, selectedFinalPosition])
				print "Moving", selectedPieceName, "to", str(selectedFinalPosition) + "."
				# Swap turns
				turn = getOpponent(turn)
				yourturn = False
			
		if (not yourturn):
			# AI moves
			print 'AI is thinking...'
			# Find the best possible move using the tree
			bestInformation = chessPlayer(board, turn)
			# Get the best move in a 2-list [initialPos, finalPos]
			bestMove = bestInformation[1]
			if bestInformation[1] == []:
				print 'Checkmate!'
				break
			# Gather data from the selected positions
			selectedPosition = bestMove[0]
			selectedPiece = board[selectedPosition]
			selectedPieceName = getNameOfPiece(selectedPiece % 10) 
			
			selectedFinalPosition = bestMove[1]
			print "AI is moving", selectedPieceName, "from ", selectedPosition, "to", str(selectedFinalPosition) + "."
			testMove(board, [selectedPosition, selectedFinalPosition])
			turn = getOpponent(turn)
		
		# AI's turn is complete, now your turn
		yourturn = True

# AI playing against itself
def automaticPlay():
	white = 10
	black = 20
	board = genBoard()
	
	while True:
		
		printBoard(board)
		
		print 'Damyon-a-tron is thinking...'
		# Find the best possible move using the tree
		bestInformation = chessPlayer(board, white)
		# Get the best move in a 2-list [initialPos, finalPos]
		bestMove = bestInformation[1]
		if bestInformation[1] == []:
			print 'Checkmate!'
			break
		# Gather data from the selected positions
		selectedPosition = bestMove[0]
		selectedPiece = board[selectedPosition]
		selectedPieceName = getNameOfPiece(selectedPiece % 10) 
		
		selectedFinalPosition = bestMove[1]
		print "Damyon-a-tron moved", selectedPieceName, "from ", selectedPosition, "to", str(selectedFinalPosition) + "."
		testMove(board, [selectedPosition, selectedFinalPosition])
		
		printBoard(board)
		
		print 'Suhay-Bot is thinking...'
		# Find the best possible move using the tree
		bestInformation = chessPlayer(board, black)
		# Get the best move in a 2-list [initialPos, finalPos]
		bestMove = bestInformation[1]
		# Gather data from the selected positions
		if bestInformation[1] == []:
			print 'Checkmate!'
			break
		selectedPosition = bestMove[0]
		selectedPiece = board[selectedPosition]
		selectedPieceName = getNameOfPiece(selectedPiece % 10) 
		
		selectedFinalPosition = bestMove[1]
		print "Suhay-Bot moved", selectedPieceName, "from ", selectedPosition, "to", str(selectedFinalPosition) + "."
		testMove(board, [selectedPosition, selectedFinalPosition])

board = genBoard()
play()