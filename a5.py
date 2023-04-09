class MaxHeap:
    class Node:
        def __init__(self,value,parent,left,right):
            self.value = value
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        self.root  = None
        self.parent = None
        self._list = []
    
    def isempty(self):
        if(self.root == None):
            return True
        return False
    
    # A modified version of create node
    # Apart from creating a node in the heap
    # It also links the node corresponding to the index i of the tuple
    def createnode(self,key,dict):
        if(self.root == None):
            new = self.Node(key,None,None,None)
            self.root = new
            dict[key[0].key] = new
            self._list.append(new)
        else:
            j = len(self._list)
            parent = self._list[(j-1)//2]
            new = self.Node(key,parent,None,None)
            if((j-1)%2 == 0):
                self._list[(j-1)//2].left = new
            else:
                self._list[(j-1)//2].right = new
            self._list.append(new)
            dict[key[0].key] = new
            Heapup(new,dict)

    #deletes the last node of the Heap
    def lastdelete(self,node):
        parent = node.parent
        if(node==None):
            raise ValueError
        else:
            if(parent == None):
                self.root = None
            elif(parent.left == node):
                parent.left = None
            elif(parent.right == node):
                parent.right = None
            self._list.pop()

    # A modified version of extract min
    # Apart from extracting the min node of the heap
    # It also de-links the node corresponding to the index i of the tuple
    def extractmax(self,dict):
        if(self.root == None):
            raise ValueError
        else:
            value = self.root.value
            dict[value[0].key] = None
            lastnode = self._list[len(self._list)-1]
            self.root.value = lastnode.value
            self.lastdelete(lastnode)
            if(self.root!=None):
                Heapdown(self.root,dict) 
        return value

    # Modifies the value of the node linked to the index i of the tuple 
    def modify(self,i,keynew,dict):
        dict[i.key].value = keynew
        Heapup(dict[i.key],dict)
        Heapdown(dict[i.key],dict)

    
    # A modified version of fast build heap
    # Apart from creating the heap using the values in the list given as input
    # It also links the node corresponding to the index i of the tuple
    def fastbuildheap(self,l,dict):
        for i in range (0,len(l)):
            key = l[i]
            if(self.root == None):
                new = self.Node(key,None,None,None)
                self.root = new
                dict[key[0].key] = new
                self._list.append(new)
            else:
                j = len(self._list)
                parent = self._list[(j-1)//2]
                new = self.Node(key,parent,None,None)
                if((j-1)%2 == 0):
                    self._list[(j-1)//2].left = new
                else:
                    self._list[(j-1)//2].right = new
                self._list.append(new)
                dict[key[0].key] = new

        for i in range (len(self._list)-1,-1,-1):
            if(self._list[i].left != None or self._list[i].right!=None):
                Heapdown(self._list[i],dict) 

# A modified version of Heapup
# Apart from the traditional heapup operation
# It also Heaps up w.r.t to the index i
# It also modifies the node corresponding to the index i of the tuple
def Heapup(node,dict):
    v = node
    while(v.parent!=None and v.value[1] > v.parent.value[1]):
        (i1,t1) = v.value
        (i2,t2) = v.parent.value
        dict[i1.key] = v.parent
        dict[i2.key] = v

        prev = v.parent.value
        v.parent.value = v.value
        v.value = prev
        v = v.parent

# A modified version of Heapdown
# Apart from the traditional heapdown operation
# It also Heaps down w.r.t to the index i
# It also modifies the node corresponding to the index i of the tuple
def Heapdown(node,dict):
    v = node
    while(v.left!=None):
        u = v.left
        if(v.right!=None and v.right.value[1] > v.left.value[1]):
            u = v.right

        if(u.value[1]>v.value[1]):

            (i1,t1) = v.value
            (i2,t2) = u.value
            dict[i1.key] = u
            dict[i2.key] = v

            prev = u.value
            u.value = v.value
            v.value = prev
            v = u
        else:
            break


class Graph:
    class Vertex:
        def __init__(self,key):
            self.key = key
            self.adjlist = []
    
    class AdjNode:
        def __init__(self,key,edge):
            self.key = key
            self.edge = edge

    def __init__(self,L):
        self.n = L[0]
        self.vertexlist = [None]*self.n
        inlist = L[1]

        for i in range (0,self.n):
            vertex = self.Vertex(i)
            self.vertexlist[i] = vertex
        for i in range (0,len(inlist)):
            source = inlist[i][0]
            dest = inlist[i][1]
            data = inlist[i][2]
            adjsource = self.AdjNode(dest,data)
            adjdest = self.AdjNode(source,data)
            self.vertexlist[source].adjlist.append(adjsource)
            self.vertexlist[dest].adjlist.append(adjdest)
    def sizevertex(self):
        return self.n

def min (a,b):
    if(a<=b):
        return a
    else:
        return b 

def findMaxCapacity(n,L,source,dest):
    Capacity = Graph([n,L])
    nodedict = dict([])
    visited = [0]*n
    Heap = MaxHeap()
    prev = [None]*n
    cap = [0]*n
    cap[source] = float("inf")
    heaplist = []
    finaldict = dict([])
    path = [dest]
    finalpath = []

    for v in Capacity.vertexlist:
        heaplist.append((v,cap[v.key]))
    Heap.fastbuildheap(heaplist,nodedict)
    
    while Heap.root!=None:
        (maxnode,maxcap) = Heap.extractmax(nodedict)
        finaldict[maxnode.key] = maxcap
        if(maxnode.key == dest):
            maxcapacity = maxcap
            break
        for v in maxnode.adjlist:
            if(visited[v.key] == 0):
                HeapNode = nodedict[v.key]
                if(HeapNode !=None):
                    (node,capadj) = HeapNode.value
                    capnew = min(maxcap,v.edge)
                    if(capnew > capadj): 
                        Heap.modify(node,(node,capnew),nodedict)
                        prev [v.key] = maxnode.key

        visited[maxnode.key] = 1 

    while v!=source:
        u = prev[dest]
        if(u == None):
            break
        path.append(u)
        dest = u

    for i in range (0,len(path)):
        finalpath.append(path[len(path)-i-1])
    
    return (maxcapacity,finalpath)