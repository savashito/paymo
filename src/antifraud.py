#!/usr/bin/python
######
# Author: Rodrigo Savage
# Desc: Program that detects suspicious transactions
# 		fraud detection algorithm
######



#####
import sys
# from scipy.sparse import coo_matrix,csr_matrix
# from scipy.sparse.csgraph import floyd_warshall,csgraph_to_masked
# import numpy as np
# def test():
# 	row  = np.array([1,2,3,2,4,5,5])
# 	col  = np.array([0,0,0,1,1,4,3])
# 	data = np.ones(len(row))
# 	graph = csr_matrix((data, (row, col)), shape=(6,6))
# 	# graph = csgraph_to_masked(graph)
# 	# print .toarray().T
# 	distMat = floyd_warshall(graph,directed=False, unweighted=True)
# 	print distMat

verifyText = {True:"trusted\n",False:"unverified\n"}

class Buyeres:
	def __init__(self):
		self.buyersTable = {}
	def bought(self,buyerId,sellerId):
		# the buyer trust the seller
		try:
			self.buyersTable[buyerId].append(sellerId)
		except KeyError, e:
			self.buyersTable[buyerId] = [sellerId];
		# The seller now trusts the buyer
		try:
			self.buyersTable[sellerId].append(buyerId)
		except KeyError, e:
			self.buyersTable[sellerId] = [buyerId];
	def isFriend(self,buyerId,sellerId):
		try:
			sellers = self.buyersTable[buyerId]
			return sellerId in sellers
		except KeyError, e:
			return False

	def isFriendOfFriend (self,buyerId,sellerIdToFind):
		return self.degreeFriend(2,buyerId,sellerIdToFind)

	def getSellersAndUpdateDepth(self,buyerId,depth):
		sellers = []
		try:
			sellers = []+self.buyersTable[buyerId]
			# print "getSellersAndUpdateDepth",buyerId,sellers
		except KeyError, e:
			sellers = []
		for sellerId in sellers:
			try:
				oldDepth = depth[sellerId]
			except KeyError, e:
				oldDepth = sys.maxint
			depth[sellerId] = min (oldDepth,depth[buyerId]+1)
		return sellers
	def degreeFriend(self,degree,buyerId,sellerIdToFind):
		# print self.buyersTable
		# print "finding ",sellerIdToFind
		visited = {buyerId:True}
		depth = {buyerId:0}
		stack = self.getSellersAndUpdateDepth(buyerId,depth)
			# stack = stack + self.getSellersAndUpdateDepth(buyerId,depth)
		# print stack
		while len(stack)>0:
			sellerId = stack.pop()
			try:
				if(visited[sellerId]):
					continue
			except KeyError, e:
				pass
			visited[sellerId]=True
			if(depth[sellerId]>degree):
				continue
			if(sellerId==sellerIdToFind):
				return True
			else:
				tStack = self.getSellersAndUpdateDepth(sellerId,depth)
				stack = tStack+stack
				# print "newStack",tStack

		return False
		# try:
		# 	sellers = self.buyersTable[nodeId]
		# 	for key,sellerId in sellers
				
		# 	return sellerId in sellers
		# except KeyError, e:
		# 	return False
	# def is4thDegreeFriend(self):

	def __str__(self):
		s = ""
		for key, value in self.buyersTable.iteritems():
			s+= str(key) +": "+str(value)+"\n"
		return s


def main(argv):
	# print 'Number of arguments:', len(argv), 'arguments.'
	# print 'Argument List:', str(argv)

	print "Fraud detection running"

	fname = argv[0]
	fnameStream = argv[1]
	fout1 = open(argv[2],'w')
	fout2 = open(argv[3],'w')
	fout3 = open(argv[4],'w')
	print "Reading batch input "+fname
	print "Results in %s, %s and %s"%(fout1,fout2,fout3)
	# Build friends graph
	buyers = Buyeres()
	with open(fname) as f:
		linesRead = 0
		for line in f:
			linesRead += 1
			# skip the header
			if(linesRead==1):
				continue
			words = line.split(', ')
			id1 = int(words[1])
			id2 = int(words[2])
			# print line
			# print words,id1,id2
			buyers.bought(id1,id2)

			if linesRead>8:
				break
	# print buyers.buyersTable
	# build transaction lists
	# transactionsList = []

	# print buyers.isFriendOfFriend(1,5)
	# return
	with open(fnameStream) as f:
		linesRead = 0
		for line in f:
			linesRead += 1
			# skip the header
			if(linesRead==1):
				continue
			words = line.split(', ')
			buyerId = int(words[1])
			sellerId = int(words[2])
			fout1.write( verifyText[buyers.isFriend(buyerId,sellerId)])
			fout2.write( verifyText[buyers.degreeFriend(2,buyerId,sellerId)])
			fout3.write( verifyText[buyers.degreeFriend(3,buyerId,sellerId)])
			# perform the transaction regarless as in the documentation
			buyers.bought(buyerId,sellerId)
			# print buyers.degreeFriend(3,6,7)
			# print line
			# print words,id1,id2
			# buyers.bought(id1,id2)

		for line in f:
			linesRead += 1

	# print buyers.isFriend(1,2)
	# print buyers.isFriendOfFriend(1,5)
	# print buyers.isFriend(1,3)
	# print buyers.isFriendOfFriend(1,5)
	# # print buyers.isFriendOfFriend(1,7)
	# print buyers.isFriendOfFriend(6,1)
	# print buyers.degreeFriend(3,6,7)
	# print buyers.degreeFriend(3,1,7)
	# print buyers.degreeFriend(2,1,7)



	# print buyers.isFriend(47055,6044)
	# print buyers.isFriend(47055,5817)
		# content = f.readlines()
	# fout1.write('unverified\n')
	# fout2.write('trusted\n')
	# fout3.write('trusted\n')
	fout1.close()
	fout2.close()
	fout3.close()

if __name__ == "__main__":
	main(sys.argv[1:])
	# test()