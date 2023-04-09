
# Defining stack data structure using linked lists
class stack:
    class Node:
        def __init__(self,value,next):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0
    
    def isempty(self):
        return self.size==0

    def push(self,value):
        new = self.Node(value,self.head)
        self.head = new
        self.size = self.size+1
    
    def pop(self):
        if(self.isempty()):
            raise ValueError
        else:
            self.head = self.head.next
            self.size = self.size-1
    
    def top(self):
        if(self.isempty()):
            raise ValueError
        else:
            return self.head.value

# Defining Heap data structure which stores nodes in an array
class Heap:
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
            dict[key[0]] = new
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
            dict[key[0]] = new
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
    def extractmin(self,dict):
        if(self.root == None):
            raise ValueError
        else:
            value = self.root.value
            dict[value[0]] = None
            lastnode = self._list[len(self._list)-1]
            self.root.value = lastnode.value
            self.lastdelete(lastnode)
            if(self.root!=None):
                Heapdown(self.root,dict) 
        return value

    # Modifies the value of the node linked to the index i of the tuple 
    def modify(self,i,key,dict):
        dict[i].value = key
        Heapup(dict[i],dict)
        Heapdown(dict[i],dict)
    
    # A modified version of fast build heap
    # Apart from creating the heap using the values in the list given as input
    # It also links the node corresponding to the index i of the tuple
    def fastbuildheap(self,l,dict):
        for i in range (0,len(l)):
            key = l[i]
            if(self.root == None):
                new = self.Node(key,None,None,None)
                self.root = new
                dict[key[0]] = new
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
                dict[key[0]] = new

        for i in range (len(self._list)-1,-1,-1):
            if(self._list[i].left != None or self._list[i].right!=None):
                Heapdown(self._list[i],dict) 

# A modified version of Heapup
# Apart from the traditional heapup operation
# It also Heaps up w.r.t to the index i
# It also modifies the node corresponding to the index i of the tuple
def Heapup(node,dict):
    v = node
    while(v.parent!=None and v.value[1] < v.parent.value[1]):
        (i1,t1) = v.value
        (i2,t2) = v.parent.value
        dict[i1] = v.parent
        dict[i2] = v

        prev = v.parent.value
        v.parent.value = v.value
        v.value = prev
        v = v.parent

    while(v.parent!=None and v.value[1] == v.parent.value[1] and v.value[0]<v.parent.value[0]):
        (i1,t1) = v.value
        (i2,t2) = v.parent.value
        dict[i1] = v.parent
        dict[i2] = v

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
        if(v.right!=None and v.right.value[1] < v.left.value[1]):
            u = v.right
        if(v.right!=None and v.right.value[1] == v.left.value[1] and v.right.value[0] < v.left.value[0]):
            u = v.right
        if(u.value[1]<v.value[1]):

            (i1,t1) = v.value
            (i2,t2) = u.value
            dict[i1] = u
            dict[i2] = v

            prev = u.value
            u.value = v.value
            v.value = prev
            v = u
        elif (u.value[1] == v.value[1] and u.value[0]<v.value[0]):
            (i1,t1) = v.value
            (i2,t2) = u.value
            dict[i1] = u
            dict[i2] = v

            prev = u.value
            u.value = v.value
            v.value = prev
            v = u
        else:
            break

def listCollisions(M,x,v,m,T):
    # index i means the ith block
    result = [] #list storing all collisions
    elapsedtime = stack() #stack which contains the time of recent collision
    elapsedtime.push(0)
    timeheap = Heap() #Heap which stores the tuple (i,collision time) of different collisions happening b/w i nd i+1
    indextime = dict() #dictionary which stores the time of recent collision that occurred for ith block
    nodeindex = dict() #dictionary which links the nodes of the heap to index i
    firstiter = [] #list containing the possible collisions in the first iteration of the function
    possiblecollisions = set([]) #set having all the possible collisions which can occur once ith block underwent collision with i+1th block
    
    #all the dictionaries are initialised to o and none respectively
    for i in range (0,len(x)): 
        indextime[i] = 0
        nodeindex[i] = None
    #if elapsed time is > T, the iteration would return the list of collisions
    if(elapsedtime.top() > T):
            return result
    else:
        s = set([]) #s is the set containing the index of collision happening in a iteration
        lastcolltime = elapsedtime.top() #the top element of the elapsed time stack which is the time of recent collision
        for i in range (0,len(x)-1): #O(n) time - to be reduced to O(logn) time 
            #can be done by extract min of heap

            #timei1 and time1 are time taken for collisions starting from the recent least collision in prev iteration
            timei1 = (lastcolltime-indextime[i+1]) 
            timei = (lastcolltime-indextime[i])
            d1 = x[i+1] + timei1*v[i+1] #position of i+1th block
            d2 = x[i] + timei*v[i] #position of the ith block
            d = abs(d1-d2) #relative displacement
            rel = v[i+1]-v[i] #relative velocity

            #conditon for collision, relative velocity<0
            if(rel < 0):
                t = abs(d/rel) #time is calculated
                firstiter.append((i,t)) #the tuple(i,t) is appended to the firstiter list

        timeheap.fastbuildheap(firstiter,nodeindex) #using the firstiter list, time heap is built
        try:
            #element having the least time is extracted from the heap
            (i,least) = timeheap.extractmin(nodeindex)
        except ValueError: #valueerror occurs if the heap is empty,i.e., root of heap = None which implies no collision occurs
            return result

        
        #final time is calculated by adding the least time in this iteration to total time elapsed till the last iteration
        finaltime = (elapsedtime.top()+least)
        elapsedtime.pop() #element is popped from the elapsed time stack
        elapsedtime.push(finaltime) #new time is pushed into the elapsed time list


        #distance of collision is calculated 
        timei1 = (lastcolltime-indextime[i+1])
        timei = (lastcolltime-indextime[i])
        d1 = x[i+1] + timei1*v[i+1]
        d2 = x[i] + timei*v[i] 
        if(v[i]>=0):
            cdist = d2+v[i]*least #distance
        else:
            cdist = d1+v[i+1]*least

        #tuple containing time of collision, index i of the block and collision distance is formed
        x_coll = round(cdist,4)
        timeres = round(finaltime,4)
        tuple = (timeres,i,x_coll)
        result.append(tuple)
        s.add(i) #ith block is added into the set s
                
    
        while (timeheap.root != None): 
            if(least == timeheap.root.value[1]): #if multiple collisions are occuring at the same time
                (i,t) = timeheap.extractmin(nodeindex) #extracting minimum of that particular collision

                #finding the collision distance of the collision
                timei1 = (lastcolltime-indextime[i+1])
                timei = (lastcolltime-indextime[i])
                d1 = x[i+1] + timei1*v[i+1]
                d2 = x[i] + timei*v[i] 
                if(v[i]>=0):
                    cdist = d2+v[i]*t
                else:
                    cdist = d1+v[i+1]*t

                #tuple containing time of collision, index i of the block and collision distance is formed
                x_coll = round(cdist,4)
                timeres = round(finaltime,4)
                tuple = (timeres,i,x_coll)
                result.append(tuple)
                s.add(i) #ith block is added into the set s         
            else:
                break
                
        #for all the set of collisions that occurred in the iteration
        for i in s:

            #collision distance is calculated
            timei1 = (lastcolltime-indextime[i+1])
            timei = (lastcolltime-indextime[i])
            d1 = x[i+1] + timei1*v[i+1]
            d2 = x[i] + timei*v[i] 
            if(v[i]>=0):
                cdist = d2+v[i]*least
            else:
                cdist = d1+v[i+1]*least
            
            #positions of i and i+1th block are updated in the x list to collision distance
            x[i] = cdist
            x[i+1] = cdist
            v1 = v[i]
            v2 = v[i+1]
            m1 = M[i]
            m2 = M[i+1]
            
            #velocities after collision are calculated and updated in the v list
            v[i] = ((m1-m2)*v1 + 2*m2*v2)/(m1+m2)
            v[i+1] = (2*m1*v1 - ((m1-m2)*v2))/(m1+m2)
            
            #time of recent collision of ith block is updated to finaltime
            indextime[i] = finaltime
            indextime[i+1] = finaltime
            
            #after a collision, the only set of new collisions that can occur are between i-1,i or i,i+1 or i+1,i+2
            #thus indexes i-1,i,i+1 are added to possiblecollisions set to iterate over them in the next iterations
            if(i-1>=0 and i-1<len(x)):
                possiblecollisions.add(i-1)
            possiblecollisions.add(i)
            if(i+1>=0 and i+1<len(x)):
                possiblecollisions.add(i+1)

    for j in range (0,m-1): 
        #if elapsed time is > T, the loop would break and return the list of collisions
        if(elapsedtime.top() > T):
            break
        else:
            s = set([]) #s is the set containing the index of collision happening in a iteration
            lastcolltime = elapsedtime.top() #the top element of the elapsed time stack which is the time of recent collision
 
            #all the indexes in the possible collisions set,i.e., i-1,i,i+1 are iterated to check for collisions
            for i in possiblecollisions: 
                
                if(i+1<len(x)):
                    #timei1 and time1 are time taken for collisions starting from the recent least collision in prev iteration
                    timei1 = (lastcolltime-indextime[i+1]) 
                    timei = (lastcolltime-indextime[i])
                    d1 = x[i+1] + timei1*v[i+1] #position of i+1th block
                    d2 = x[i] + timei*v[i] #position of the ith block
                    d = abs(d1-d2) #relative displacement
                    rel = v[i+1]-v[i] #relative velocity

                    #conditon for collision, relative velocity<0
                    if(rel < 0):
                        t = lastcolltime+abs(d/rel) #time is calculated and added to the last collision time
                        elem = (i,t) #tuple of i,t
                        if(timeheap.root == None): 
                            timeheap.createnode(elem,nodeindex)
                        if(nodeindex[i] == None):
                            timeheap.createnode(elem,nodeindex)
                        else:
                            timeheap.modify(i,elem,nodeindex)


            try:
                #element having the least time is extracted from the heap
                (i,least) = timeheap.extractmin(nodeindex)
            except ValueError: #ValueError implies Root of the Heap is None, thus it breaks the loop
                break

            
            finaltime = least #final time is the least time obtained from extract min
            elapsedtime.pop() #element is popped from elapsed time stack
            elapsedtime.push(finaltime) #new final time is pushed into the stack
            if(finaltime > T): #if the final time is >T, the loop breaks
                break

            #distance of collision is calculated 
            timei1 = (lastcolltime-indextime[i+1])
            timei = (lastcolltime-indextime[i])
            d1 = x[i+1] + timei1*v[i+1]
            d2 = x[i] + timei*v[i] 
            if(v[i]>=0):
                cdist = d2+v[i]*abs((lastcolltime-least))
            else:
                cdist = d1+v[i+1]*abs((lastcolltime-least))

            #tuple containing time of collision, index i of the block and collision distance is formed
            x_coll = round(cdist,4)
            timeres = round(finaltime,4)
            tuple = (timeres,i,x_coll)
            result.append(tuple)
            s.add(i) #i is added to the set s

            
            while (timeheap.root != None): 
                if(least == timeheap.root.value[1] and i!= timeheap.root.value[0]): #if multiple collisions are occuring at the same time
                    (i,t) = timeheap.extractmin(nodeindex)#extracting minimum of that particular collision

                    #distance of collision is calculated 
                    timei1 = (lastcolltime-indextime[i+1])
                    timei = (lastcolltime-indextime[i])
                    d1 = x[i+1] + timei1*v[i+1]
                    d2 = x[i] + timei*v[i] 
                    if(v[i]>=0):
                        cdist = d2+v[i]*abs((lastcolltime-least))
                    else:
                        cdist = d1+v[i+1]*abs((lastcolltime-least))

                    #tuple containing time of collision, index i of the block and collision distance is formed
                    x_coll = round(cdist,4)
                    timeres = round(finaltime,4)
                    tuple = (timeres,i,x_coll)
                    result.append(tuple)
                    s.add(i) #i is added to the set s
                else:
                    break

            possiblecollisions.clear() #possible collisions set is cleared for the next iteration

            #for all the set of collisions that occurred in the iteration
            for i in s:

                #collision distance is calculated
                timei1 = (lastcolltime-indextime[i+1])
                timei = (lastcolltime-indextime[i])
                d1 = x[i+1] + timei1*v[i+1]
                d2 = x[i] + timei*v[i] 
                if(v[i]>=0):
                    cdist = d2+v[i]*abs((lastcolltime-least))
                else:
                    cdist = d1+v[i+1]*abs((lastcolltime-least))

                #positions of i and i+1th block are updated in the x list to collision distance  
                x[i] = cdist
                x[i+1] = cdist
                v1 = v[i]
                v2 = v[i+1]
                m1 = M[i]
                m2 = M[i+1]
                
                #time of recent collision of ith block is updated to finaltime
                v[i] = ((m1-m2)*v1 + 2*m2*v2)/(m1+m2)
                v[i+1] = (2*m1*v1 - ((m1-m2)*v2))/(m1+m2)

                #time of recent collision of ith block is updated to finaltime
                indextime[i] = finaltime
                indextime[i+1] = finaltime
                
                #after a collision, the only set of new collisions that can occur are between i-1,i or i,i+1 or i+1,i+2
                #thus indexes i-1,i,i+1 are added to possiblecollisions set to iterate over them in the next iterations
                if(i-1>=0 and i-1<len(x)):
                    possiblecollisions.add(i-1)
                possiblecollisions.add(i)
                if(i+1>=0 and i+1<len(x)):
                    possiblecollisions.add(i+1)
    return result
print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.505))
