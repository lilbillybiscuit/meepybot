user = "<@&898018723292667955>"

print(user[3:-1])

from persist_pq import Persist_PQ

pq = Persist_PQ("meepy1.pq")

pq.put((5,4))
pq.put((6.3))
pq.put((5,4))

while (not pq.empty()):
    hi = pq.get()
    print(hi)