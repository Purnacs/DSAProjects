#Reference has been taken from the follwing sources:
# https://homes.cs.washington.edu/~jrl/teaching/cse525wi15/lectures/lecture1.pdf
# https://www.cs.cmu.edu/afs/cs/academic/class/15451-f14/www/lectures/lec6/karp-rabin-09-15-14.pdf
# http://www.cs.toronto.edu/~anikolov/CSC473W18/Lectures/karp-rabin.pdf

import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
    N = findN(eps,len(p))
    print(N)
    q = randPrime(N)
    return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
    k = (2*m*math.log2(26))/eps
    N = k**(162/125)
    return int(N)

#REASONING: 
# With reference to the above mentioned papers,
# The error bound eps, is less than or equal to the No of primes dividing d/ No of primes less than or equal to N
# The error bound eps, is less than or equal to the log d/ pi(N)
# Here d is the d-bit representation used for the string
# In our case, we use a 26-bit representation, thus d = 26
# pi(N) is the no of primes less than or equal to N
# Thus, by rearranging terms, the inequality now becomes N/logN >= (2*m*log26)/eps
# Thus we need to find N, satisfying this bound
# Since the equality is not homogenously solvable, an approximation for LogN is considered
# The tightest bound for Log N would be N^37/162.i.e, N^37/162 > Log N
# Thus N/N^(37/162) = N^(125/162) is the tight bound for with the equality would be solved
# Thus N^(125/162) = 2*m*log(26))/eps
# N = (2*m*log(26))/eps)^(162/125)




#Constant Time
# c*26 bits of storage (constant) for storing the dictionary
#hashindex is a dictionary function which stores the 26-bit based index for each alphabet
def hashindex(alpha):
    
    bitrepdict = {'A':0, 'B':1, 'C': 2, 'D': 3, 'E':4, 'F':5, 'G':6, 'H':7, 'I': 8, 'J': 9, 'K':10, 'L':11, 'M':12, 'N':13, 'O': 14, 'P': 15, 'Q':16, 'R':17,
    'S':18, 'T':19, 'U': 20, 'V': 21, 'W':22, 'X':23, 'Y': 24, 'Z': 25, '\n':0, ' ': 0}
    return(bitrepdict[alpha])

# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
    m = len(p) 
    n = len(x)
    patternhash = (hashindex(p[m-1]))%q #storing the hashindex of last char of pattern mod q
    texthash = (hashindex(x[m-1]))%q #storing the hashindex of last char of text mod q
    i = 0 #i is initialised to 0
    mod = 1 #mod is initialised to 1, which would store the (powers of 26) mod q
    occurance = [] #occurance list to store the matched indexes
    
    j = m-2 #j is initialised to m-2

    #preprocessing of the pattern, thus obtaining the hash function of the pattern
    #preprocessing of the first m chars of the text, thus obtaining the hash function of the first m chars of the text
    while(j>=0):
        iterhash = ((((26%q)*(mod))%q)*(hashindex(p[j]))%q)%q #iterhash stores the value of (26^(m-j-1))*hashkey of the alphabet mod q
        patternhash = (patternhash%q+iterhash)%q #patternhash iteratively adds each value of iterhash and computes modq of the final patternhash value

        iterhashtext = ((((26%q)*(mod))%q)*(hashindex(x[j]))%q)%q #iterhashtext stores the value of (26^(m-j-1))*hashkey of the alphabet mod q
        texthash = (texthash%q+iterhashtext)%q #texthash iteratively adds each value of iterhashtext and computes modq of the final texthash value


        mod = ((26%q)*(mod))%q #mod is multiplied with 26%q and its mod with q is computed. Thus, is re-assigned the value iteratively
        
        j = j-1

    subhash = texthash #subhash initially takes the value of texthash, i.e., the hashfn value of first m characters of the text
    while(i<=n-m):
        if(subhash == patternhash): #if subhash is equal to pattern hash
            occurance.append(i) #index is appended
        if(i==n-m):
            break #if i+m is equal to n, the loop is broken
        else:

            #since in the preprocessing step, mod is already assigned a value of (26^m-1)%q through m iterations.
            #For efficient space management, the same value,i.e., mod is used
            power = mod%q 
            hashmod = hashindex(x[i])%q
            hashindmod = hashindex(x[i+m])%q
            mul = (power*hashmod)%q

            #for the next iterations, the hashfunction of the next m characters is being computed
            #for i+1th iteration, we subtract the hashfunction of the first character of the ith iteration hashfunction
            #since all the characters are now shifted by one in the next iteration, we multiplied the obtained hashfunction with 26
            #for the i+1th iteration, the next character is the new addition and thus its hash function is added to the previously obtained value
            #All the above mentioned calculations are done w.r.t taking mod q, for efficient usage of space
            subhash = (((26%q)*((subhash-mul)%q))%q + hashindmod)%q
        i = i+1
    return occurance #list of matches is returned





# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):
    m = len(p)
    n = len(x)
    if(p[m-1] == '?'): #if the last character is "?"
        patternhash = 0 #patternhash is initialised to 0
    else:
        patternhash = (hashindex(p[m-1]))%q #storing the hashindex of last char of pattern mod q

    texthash = (hashindex(x[m-1]))%q #storing the hashindex of last char of text mod q
    i = 0 #i is initialised to 0
    mod = 1 #mod is initialised to 1, which would store the (powers of 26) mod q
    indexqn = -1 #indexqn is the variable which stores the index of the wildcard char '?'. It is initialised to -1
    occurance = [] #occurance list to store the matched indexes
    
    j = m-2 #j is initialised to m-2

    #preprocessing of the pattern, thus obtaining the hash function of the pattern excluding the wildcard character
    #preprocessing of the first m chars of the text, thus obtaining the hash function of the first m chars of the text
    while(j>=0):
        if(p[j] == '?'): #if the wildcard character is encountered, its index is stored and we move to the next iteration
            indexqn = j
        else: #else, the rest of the hash function is computed
            iterhash = ((((26%q)*(mod))%q)*(hashindex(p[j]))%q)%q #iterhash stores the value of (26^(m-j-1))*hashkey of the alphabet mod q
            patternhash = (patternhash%q+iterhash)%q #patternhash iteratively adds each value of iterhash and computes modq of the final patternhash value

        iterhashtext = ((((26%q)*(mod))%q)*(hashindex(x[j]))%q)%q #iterhashtext stores the value of (26^(m-j-1))*hashkey of the alphabet mod q
        texthash = (texthash%q+iterhashtext)%q #texthash iteratively adds each value of iterhashtext and computes modq of the final texthash value


        mod = ((26%q)*(mod))%q #mod is multiplied with 26%q and its mod with q is computed. Thus, is re-assigned the value iteratively
        
        j = j-1
    subhash = texthash #subhash initially takes the value of texthash, i.e., the hashfn value of first m characters of the text
    powerwildcard = (26**(m-indexqn-1))%q #26th power of the index corresponding to the wildcard char is computed

    while(i<=n-m):
        hashindwildcard = hashindex(x[i+indexqn])%q  #hashindex of the wildcard char is computed
        mulwildcard = (powerwildcard*hashindwildcard)%q #it is then multiplied to the corresponding 26th power

        #the hashfn value of the wildcard indexed character is subtracted from the total hashfunction computed 
        #This value is assigned to subhashwildcard
        subhashwildcard = (subhash-mulwildcard)%q

        if(subhashwildcard == patternhash):#if subhashwildcard is equal to pattern hash
            occurance.append(i) #index is appended
        if(i==n-m):
            break #if i+m is equal to n, the loop is broken
        else:

             #since in the preprocessing step, mod is already assigned a value of (26^m-1)%q through m iterations.
            #For efficient space management, the same value,i.e., mod is used
            power = mod%q
            hashmod = hashindex(x[i])%q
            hashindmod = hashindex(x[i+m])%q
            mul = (power*hashmod)%q

            #for the next iterations, the hashfunction of the next m characters is being computed
            #for i+1th iteration, we subtract the hashfunction of the first character of the ith iteration hashfunction
            #since all the characters are now shifted by one in the next iteration, we multiplied the obtained hashfunction with 26
            #for the i+1th iteration, the next character is the new addition and thus its hash function is added to the previously obtained value
            #All the above mentioned calculations are done w.r.t taking mod q, for efficient usage of space
            subhash = (((26%q)*((subhash-mul)%q))%q + hashindmod)%q
        i = i+1
    return occurance #list of matches is returned

