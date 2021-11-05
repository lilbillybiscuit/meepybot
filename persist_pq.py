from queue import PriorityQueue
import pickle
import os

class Persistent_PQ:
    def __init__(self, filename, initial_size=50):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.H, self.size = pickle.load(f)
        else:
            self.H=[0]*(initial_size*2)
            self.size=-1
            with open(filename, 'wb') as f:
                pickle.dump((self.H, self.size), f)

    # Priority Queue using Binary Heap
    def parent(i):
        return (i-1)//2
    
    def left(i) :
        return ((2 * i) + 1)
    
    def right(i) :
        return ((2 * i) + 2)

    def shiftup(self, i) :
        while (i > 0 and self.H[self.parent(i)] < self.H[i]) :
            self.swap(self.parent(i), i)
            i = self.parent(i)
            
    def shiftdown(self, i) :
        maxIndex = i
        l = self.left(i)
        if (l <= self.size and self.H[l] > self.H[maxIndex]) :
            maxIndex = l
        r = self.right(i)
        if (r <= self.size and self.H[r] > self.H[maxIndex]) :
            maxIndex = r
        if (i != maxIndex) :
            self.swap(i, maxIndex)
            self.shiftdown(maxIndex)

    def insert(self, p) :
        self.size = self.size + 1
        self.H[self.size] = p
        self.shiftup(self.size)

    def extractMax(self) :
        result = self.H[0]
        self.H[0] = self.H[self.size]
        self.size = self.size - 1
        self.shiftdown(0)
        return result
    
    def changePriority(self,i,p) :
        oldp = self.H[i]
        self.H[i] = p
        if (p > oldp) :
            self.shiftup(i)
        else :
            self.shiftdown(i)
    
    def getMax(self) :
        return self.H[0]
    
    def Remove(self, i) :
        self.H[i] = self.getMax() + 1
        self.shiftup(i)
        self.extractMax()
    
    def swap(self, i, j) :
        temp = self.H[i]
        self.H[i] = self.H[j]
        self.H[j] = temp
        