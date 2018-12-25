"""
An edge-matching puzzle game solver.

Take 9 square cards. Each edge of each card has half of an image on it.
There is some valid arrangement of the 9 cards in a 3x3 grid,
such that each edge lines up with an edge with the other half of its image.

Ben Schreiber 12/25/18
"""

"""
Each card is a list of tuples, with the index of the tuple corresponding
to the following edge of the card. This is only for the purpose of
internal consistency.
/---2---\
|       |
3       1
|       |
\---0---/

Cards in the list have these positions in the 3x3 grid.
0 1 2
3 4 5
6 7 8
"""

from enum import Enum
from itertools import permutations
import copy

# Replace images with those from your puzzle (use 4 characters to pretty-print)
Image = Enum('Image', 'corn orng burr chal')
Side = Enum('Side', 'frnt back')

# Replace with your cards
# Each line is a card, each tuple is an edge
# See above comment on ordering of tuples
starting = [[(Image.burr, Side.frnt), (Image.corn, Side.back), (Image.chal, Side.back), (Image.corn, Side.frnt)],
		[(Image.chal, Side.frnt), (Image.orng, Side.back), (Image.burr, Side.back), (Image.orng, Side.frnt)],
		[(Image.chal, Side.back), (Image.orng, Side.back), (Image.corn, Side.back), (Image.burr, Side.back)],
		[(Image.chal, Side.back), (Image.burr, Side.back), (Image.corn, Side.back), (Image.orng, Side.back)],
		[(Image.burr, Side.back), (Image.orng, Side.frnt), (Image.chal, Side.frnt), (Image.corn, Side.back)],
		[(Image.burr, Side.back), (Image.corn, Side.frnt), (Image.chal, Side.frnt), (Image.orng, Side.back)],
		[(Image.chal, Side.back), (Image.burr, Side.frnt), (Image.orng, Side.back), (Image.corn, Side.frnt)],
		[(Image.orng, Side.frnt), (Image.burr, Side.frnt), (Image.corn, Side.back), (Image.chal, Side.back)],
		[(Image.burr, Side.back), (Image.corn, Side.frnt), (Image.chal, Side.frnt), (Image.orng, Side.back)]]

def validEdge(e1, e2):
	assert(len(e1) == 2)
	assert(len(e2) == 2)
	return e1[0] == e2[0] and e1[1] != e2[1]

def validGrid(cards):
	central = validEdge(cards[4][2], cards[1][0]) and \
			validEdge(cards[4][1], cards[5][3]) and \
			validEdge(cards[4][0], cards[7][2]) and \
			validEdge(cards[4][3], cards[3][1])
	if not central:
		return False
	
	top = validEdge(cards[1][3], cards[0][1]) and \
			validEdge(cards[1][1], cards[2][3])
	if not top:
		return False
	
	left = validEdge(cards[3][2], cards[0][0]) and \
			validEdge(cards[3][0], cards[6][2])
	if not left:
		return False
	
	right = validEdge(cards[5][2], cards[2][0]) and \
			validEdge(cards[5][0], cards[8][2])
	if not right:
		return False
	
	bottom = validEdge(cards[7][3], cards[6][1]) and \
			validEdge(cards[7][1], cards[8][3])
	return bottom

# Solver takes a brute-force approach
# Checks each arrangement of cards in grid
# For each arrangement, tries rotating all cards
def searchArrangements(cards):
	for n, arrangement in enumerate(permutations(range(len(cards)))):
		if n % 1000 == 0:
			print("{} searched".format(n))
		cards = copy.deepcopy(cards)
		shuffle = [cards[i] for i in arrangement]
		searchOrientations(shuffle)

def searchOrientations(cards):
	orientHelper(cards, len(cards) - 1)

def orientHelper(cards, n):
	if n < 0:
		return

	for _ in range(4):
		if validGrid(cards):
			print("~~~~~ NEW VALID GRID FOUND ~~~~~")
			prettyPrint(cards)
		cards[n] = cards[n][1:] + cards[n][:1]
		orientHelper(cards, n-1)

def name(tup):
	return tup[0].name + ' ' + tup[1].name

def prettyPrint(cards):
	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[0][2]), name(cards[1][2]), name(cards[2][2])))
	print("|{}      {}| |{}      {}| |{}      {}|".format(name(cards[0][3]), name(cards[0][1]), name(cards[1][3]), name(cards[1][1]), name(cards[2][3]), name(cards[2][1])))
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[0][0]), name(cards[1][0]), name(cards[2][0])))
	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")

	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[3][2]), name(cards[4][2]), name(cards[5][2])))
	print("|{}      {}| |{}      {}| |{}      {}|".format(name(cards[3][3]), name(cards[3][1]), name(cards[4][3]), name(cards[4][1]), name(cards[5][3]), name(cards[5][1])))
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[3][0]), name(cards[4][0]), name(cards[5][0])))
	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")

	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[6][2]), name(cards[7][2]), name(cards[8][2])))
	print("|{}      {}| |{}      {}| |{}      {}|".format(name(cards[6][3]), name(cards[6][1]), name(cards[7][3]), name(cards[7][1]), name(cards[8][3]), name(cards[8][1])))
	print("|       {}        | |       {}        | |       {}        |".format(name(cards[6][0]), name(cards[7][0]), name(cards[8][0])))
	print("+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+" + " " + "+" + "-"*24 + "+")

if __name__ == "__main__":
	searchArrangements(starting)

