from queue import PriorityQueue
import pickle
import os

class Persist_PQ:
    def __init__(self, filename):
        self.filename=filename
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.pq=pickle.load(f)
        else:
            self.pq = PriorityQueue() 
            with open(self.filename, 'wb') as f:
                pickle.dump(self.pq, f)

    def put(self,element):
        self.pq.put(element)
        with open(self.filename, 'wb') as f:
            pickle.dump(self.pq, f)
        return
    def get(self):
        ret = self.pq.get()
        with open(self.filename, 'wb') as f:
            pickle.dump(self.pq, f)
        return ret
    def qsize(self):
        return self.pq.qsize()
    def empty(self):
        return self.pq.empty()
    def full(self)
        return self.pq.full()
        