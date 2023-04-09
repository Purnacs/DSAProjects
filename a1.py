# Defining stack data structure using linked lists
class stack:
    class Node:
        def __init__(self,element,next):
            self.element = element
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def isempty(self):
        if(self.size == 0):
            return True
        return False
    
    def push(self,v):
        next = self.head
        self.head = self.Node(v,next)
        self.size = self.size+1
    
    def pop(self):
        if(self.isempty()):
            raise ValueError ("Stack is empty")
        else:
            self.head = self.head.next
            self.size = self.size - 1

    def top(self):
        if(self.isempty()):
            raise ValueError("Stack is empty")
        else:
            return self.head.element

# Helper function which gives the coordinates based on the type and length of the stack
# when stack is x_stack gives the x co-ordinate, y_stack gives the y coordinate and z_stack gives the z coordinate
def get_coord(stack):
    if(stack.isempty()):
        return 0
    elif(stack.top() == '-X' or stack.top() == '-Y' or stack.top() == '-Z'):
        return -1*len(stack)
    else:
        return len(stack)
#Time Complexity: Assuming all the elementary and mathematical operations take constant time
#                 Accessing elements from stacks and lists take constant time
#Time Complexity = T(k) = O(1)

# Function to multiply an integer to all the elements in the list which represents co-ordinates
# Since the co-ordinates list contains only four elements, each element is accessed and modified seperately
# The modified elements are returned as a list
def const_mul_coord(k,l):
    new_xcoord = k*l[0]
    new_ycoord = k*l[1]
    new_zcoord = k*l[2]
    new_dist = k*l[3]

    new_coord = [new_xcoord,new_ycoord,new_zcoord,new_dist]
    return new_coord
#Time Complexity: Assuming all the elementary and mathematical operations take constant time
#                 Accessing elements from stacks and lists take constant time
#Time Complexity = T(k) = O(1)

# Function to add co-ordinates of two lists by adding elements in the list which represents co-ordinates
# Since the co-ordinates lists contains only four elements, each element is accessed and modified (added) seperately
# The modified elements are returned as a list
def sum_coord(l,p):
    new_xcoord = l[0]+p[0]
    new_ycoord = l[1]+p[1]
    new_zcoord = l[2]+p[2]
    new_dist = l[3]+p[3]

    new_coord = [new_xcoord,new_ycoord,new_zcoord,new_dist]
    return new_coord
#Time Complexity: Assuming all the elementary and mathematical operations take constant time
#                 Accessing elements from stacks and lists take constant time
#Time Complexity = T(k) = O(1)

#function which computes the final position and distance transversed
def findPositionandDistance(s):

    #declaring result list and initialising it to origin i.e., [0,0,0,0]
    result = [0,0,0,0]
    x_stack = stack() #stack to store all the x variables
    y_stack = stack() #stack to store all the y variables
    z_stack = stack() #stack to store all the z variables
    factor = stack()  #stack to store the respective factors pertaining to an expression
    factor.push(1) #assuming the initial factor to be 1 and pushing it into the factor stack

    digit = "" #digit variable which adds the digit characters. It is initialised to empty string
    dist = 0 #dist variable to keep track of the distance transversed
    for i in range (0,len(s)):
        
        if(s[i] == "+" or s[i] == "-"): #if the ith element of string s is a sign
            operator = s[i:i+2] #the string is sliced such that the sign and axis (X,Y,Z) are obtained at once. This is stored by operatior variable
            dist = dist+1 #distance is incremented by one

            #if x co-ordinate related operations are given
            #if the operator is +X
            if(operator == '+X'): 
                #if stack is empty, push it into stack
                if (x_stack.isempty()):
                    x_stack.push(operator)
                    #if the top element is +X, then push it into stack
                elif (x_stack.top() == '+X'):
                    x_stack.push(operator)
                    #if the top element is -X, pop the top element of the stack
                elif(x_stack.top() == '-X'):
                    x_stack.pop()

            #if the operator is +X
            if(operator == '-X'): 
                #if stack is empty, push it into stack
                if (x_stack.isempty()):
                    x_stack.push(operator)
                    #if the top element is -X, then push it into stack
                elif (x_stack.top() == '-X'):
                    x_stack.push(operator)
                    #if the top element is +X, pop the top element of the stack
                elif(x_stack.top() == '+X'):
                    x_stack.pop()

            #if the operator is +Y
            if(operator == '+Y'): 
                #if stack is empty, push it into stack
                if (y_stack.isempty()):
                    y_stack.push(operator)
                    #if the top element is +Y, then push it into stack
                elif (y_stack.top() == '+Y'):
                    y_stack.push(operator)
                    #if the top element is -Y, pop the top element of the stack
                elif(y_stack.top() == '-Y'):
                    y_stack.pop()

            #if the operator is -Y
            if(operator == '-Y'): 
                #if stack is empty, push it into stack
                if (y_stack.isempty()):
                    y_stack.push(operator)
                    #if the top element is -Y, then push it into stack
                elif (y_stack.top() == '-Y'):
                    y_stack.push(operator)
                    #if the top element is +Y, pop the top element of the stack
                elif(y_stack.top() == '+Y'):
                    y_stack.pop()
            
            #if the operator is +Z
            if(operator == '+Z'): 
                #if stack is empty, push it into stack
                if (z_stack.isempty()):
                    z_stack.push(operator)
                    #if the top element is +Z, then push it into stack
                elif (z_stack.top() == '+Z'):
                    z_stack.push(operator)
                    #if the top element is -Z, pop the top element of the stack
                elif(z_stack.top() == '-Z'):
                    z_stack.pop()

            #if the operator is -Z
            if(operator == '-Z'): 
                #if stack is empty, push it into stack
                if (z_stack.isempty()):
                    z_stack.push(operator)
                    #if the top element is -Z, then push it into stack
                elif (z_stack.top() == '-Z'):
                    z_stack.push(operator)
                    #if the top element is +Z, pop the top element of the stack
                elif(z_stack.top() == '+Z'):
                    z_stack.pop()
            continue #loop continues to the next iteration
        
        #if ith element is a digit 
        if(s[i] in "0123456789"):
            digit = digit+s[i] #ith element is added to the digit string

            #if any of the stacks containing x,y,z coordinates or the distance variable are not empty
            if(len(x_stack)!=0 or len(y_stack)!=0 or len(z_stack)!=0 or dist!=0):
                x = get_coord(x_stack) #x coordinate is obtained from x_stack
                y = get_coord(y_stack) #y coordinate is obtained from y_stack
                z = get_coord(z_stack) #z coordinate is obtained from z_stack
                sol = [x,y,z,dist] #sol is a list containing x,y,z coordinates and distance
                dist = 0 #dist variable is re-initialised to 0
                fact = factor.top() #top element of the factor is accessed and is stored in fact variable
                fact_sol = const_mul_coord(fact,sol) #const_mul_coord function is called to multiply the factor with the solution list
                result = sum_coord(result,fact_sol) # using sum_coord function, result and fact_sol lists are added to each other. The obtained result is re-stored in result variable
                while(not x_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    x_stack.pop()
                while(not y_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    y_stack.pop()
                while(not z_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    z_stack.pop()

        #if the ith element is not a digit and digit string is not empty
        elif(not (s[i] in "0123456789") and digit != ""): 
            top = factor.top() #top element of factor stack is accessed and top variable takes its value
            elem = top*int(digit) #the string digit is converted to digit. It is multiplied with the top element of factor stack
            factor.push(elem) #the obtained result is pushed into the factor stack
            digit = "" #digit string is reinitialised to an empty string

       #if the ith element is closed bracket '(' or i == len(s)-1,i.e., index of the last element
        elif(s[i] == ')' or i == len(s)-1):

           #if any of the stacks containing x,y,z coordinates or the distance variable are not empty
            if(len(x_stack)!=0 or len(y_stack)!=0 or len(z_stack)!=0 or dist!=0):
                x = get_coord(x_stack) #x coordinate is obtained from x_stack
                y = get_coord(y_stack) #y coordinate is obtained from y_stack
                z = get_coord(z_stack) #z coordinate is obtained from z_stack
                sol = [x,y,z,dist] #sol is a list containing x,y,z coordinates and distance
                dist = 0 #dist variable is re-initialised to 0
                fact = factor.top() #top element of the factor is accessed and is stored in fact variable
                fact_sol = const_mul_coord(fact,sol) #const_mul_coord function is called to multiply the factor with the solution list
                result = sum_coord(result,fact_sol) # using sum_coord function, result and fact_sol lists are added to each other. The obtained result is re-stored in result variable
                while(not x_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    x_stack.pop()
                while(not y_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    y_stack.pop()
                while(not z_stack.isempty()): #all the elements of x_stack are popped and x_stack is made empty
                    z_stack.pop()

            factor.pop() #top element of the factor stack is popped from the stack
    return(result) #result, in the form of list containing 4 elements is returned

#Time Complexity: Assuming all the elementary and mathematical operations take constant time
#                 Accessing elements from stacks and lists take constant time
#                 All the helper functions take O(1) time
#                 Only in certain iterations, the stacks are popped which take O(n) time in the worst case
#                 Thus the total time taken for n iterations is O(n) + k*(O(n))  [k*(O(n)) is time taken for popping the stacks]

#Time Complexity = O(n+k*n) = O(n)