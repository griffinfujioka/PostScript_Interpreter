# Griffin Fujioka
# 11044124
# Fall 2011
# CptS 355 - Professor Carl Hauser 

#!/usr/bin/env python
import sys, re

# A regular expression that matches postscript each different kind of postscript token
pattern = '/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]+|%.*|[^\t\n ]'

# This is the global operand stack
opstack = []

# and this the global dictionary stack
dictStack = [{}]          # used exclusively by dynamic scoping?

# Static chain is a stack of tuples
    # each tuple contains an int and a dictionary
    # int = static links (indexes in a list) 
staticChain = []        # used exclusively by static scoping

# index to keep track of static links 
indx = 0

# Test cases
testx = '''/x 4 def'''
testg = '''/g {x} def'''
testf = '''/f { /x 7 def g } def'''

# Arithmetic ops: each take two numbers and return a number
def plus(x,y):
    return x+y

def minus(x,y):
    return x-y

def times(x,y):
    return x*y

def divide(x,y):
    return x/y

# Comparisons take two numbers and return a boolean
def eq(x,y):
    return x==y

def lt(x,y):
    return x<y

def gt(x,y):
    return x>y

def le(x,y):
    return x<=y

def ge(x,y):
    return x>=y

# Boolean operators (and, or, not)
def andd(x,y):
    return(x and y)

def orr(x,y):
    if (x or y):
        opstack.append(True)
    else:
        opstack.append(False)

def nott():
    op1 = opstack.pop()
    print(' ')
    print('*****************')
    if(not op1):
        opstack.append(False)
    else:
        opstack.append(True)

        
# Check sys.argv to see what rules to use
# Return true if dynamic, false if static 
def SDChecker():
    if '-s' in sys.argv:
        return False
    else:
        return True

# Look for a dictionary in the static chain
# determine if name x is in a dictionary that's stored in staticChain
# helper function. could be called SCDefined()
def SCDictFinder(x):
    SClength = len(staticChain)
    i=0
    while(i<SClength):                      # Iterate through static chain looking for name x in each tuple
        (link,tempDict)=staticChain[i]      
        if(x in tempDict.keys()):           # look for name x in tempDict
            return True
        else:
            i +=1
    return False

# Look for dict with key==x in staticChain and return it's index
def SCLinkReturner(x):
    SClength = len(staticChain)
    i=0
    while(i<SClength):              # Iterate through static chain looking for name x 
        (link,tempDict)=staticChain[i]      
        if(x in tempDict.keys()):           # look for name x in tempDict
            return link                     # return index 
        else:
            i +=1
    return None                             # or None


# Print stack
def printStack():
    print("Operand stack:")
    print ("---Top---")
    for elt in reversed(opstack):
        print (elt)
    print ("---Bottom---")
    print("Dictionary stack:")
    print ("---Top---")
    for elt in reversed(dictStack):
        print(elt)
    print("---Bottom---")       
        
# Map the postscript operator names to the above functions
# using a dictionary
binops={
    "add": plus,
    "sub": minus,
    "mul": times,
    "div": divide,
    "eq": eq,
    "lt": lt,
    "gt": gt,
    "le": le,
    "ge": ge,
    "and": andd,
    "or": orr,
    "not": nott,
    }

# We need to recognize postscript names, which start with
# slash and a letter, followed by other characters
name = re.compile('/[a-zA-Z?].*')


# For dynamic scoping:
    # Look at top dictionary, and keep moving down stack until the definitions is found
# For static scoping:
    # Look at the top dictionary and if it isn't there then go to the next index and look for it
    
# Check to see if name t is defined
# Returns True if t is defined, else false 
# Note the assumption that the warmest end of dictStack is at 
# position 0.
def defined(t):
    checker = SDChecker()           # determine scoping rules 
    if(checker==True):              # dynamic case 
        # look from warmest entry 
        for d in dictStack:
            if t in d.keys():
                return True
    elif(checker==False):                           # static case 
        if(len(staticChain)>0):                     # if staticChain is not empty   
            (link, tempDict) = staticChain[0]           # use SCDictFinder helper function
            finder = SCDictFinder(t);               # look for a name t in staticChain 
            return finder
    else:
        return False 

# check if name t is defined, returning either
# its defined value or None if not found
def definition(t):
    SD = SDChecker()
    if(SD==True):                       # dynamic case 
        for d in dictStack:             # look through dictStack and return definition if found    
            if t in d.keys():
                return d[t]
    elif(SD==False):                    # static case 
        if(len(staticChain)>0):
            link=SCLinkReturner(t)      # get the static link to the name t 
            if(link != None):           # link == None if the name t wasn't found 
                (linkIndex, linkDict) = staticChain[link]       # otherwise, return it's definition 
                return linkDict[t]
            else:
                return None
    else:
        return None

# Having seen a { read input to the
# matching }, returning the code between the braces
# and the position following the }
def readCode(tokens, p):
    code = []                   # A temporary stack 
    braceCount = 1
    # invariant: p points at the next tokent to be read
    while True:
        t = tokens[p]
        p += 1
        if t=='}':
            braceCount = braceCount - 1
            if braceCount==0: 
                break
            elif t=='{':
                braceCount = braceCount + 1

                
        code.append(t)
    # invariant tells us this is the correct value of  p to return
    return code, p
    
# The main guts of the interpreter
def evalLoop(tokens):
    # stack and dictStack are declared globally because they are updated within
    # evalLoop. If they were not made global then local variables with the
    # same name would be created 
    global opstack, dictStack
    global indx
    p = 0
    # invariant: p points one position past the last
    # token processed, whether that is the token after t
    # or after a code array beginning at t
    
    SD = SDChecker()        # check for command line rules 
    while p < len(tokens):
        t = tokens[p]
        p += 1
        
        # handle the binary operators
        if t in binops.keys():          # if the token is a binary op
            op = binops[t]              # use binops to access the function definition
            if len(opstack)>1:
                dictStack.append({})
                print("dictStack is now: ", dictStack)
                opstack[-3:] = [op(opstack[-2],opstack[-1])]
                dictStack.pop()
                print("dictStack is now: ", dictStack)
            else:
                print ("not enough operands for"), t

        # handle an opening brace - read to the 
 	# matching brace and push the resulting code array
        # on the operand stack
        elif t=='{':
            code, p = readCode(tokens, p)       # get all of the code
            opstack.append(code)                  # push all of the code onto the stack 

        # the stack operations exch, pop, clear are easy
        # should add error checking
        elif t=='exch':
            opstack[-2:] = [opstack[-1],opstack[-2]]
        elif t=='pop':
            opstack.pop()
        elif t=='clear':
            opstack = []
        elif t=='stack':
            printStack()
        elif t=='true':
            opstack.append(True)
        elif t=='false':
            opstack.append(False)
            
        # handle def 
        elif t=='def':
            if len(opstack)>1 and type(opstack[-2])==type('') and (SD == True):
                # dynamic definition rules
                dictStack[0][opstack[-2]] = opstack[-1]         # add new dictionary to dictStack
                opstack[-2:] = []                             # remove name and definition from stack
            elif len(opstack)>1 and type(opstack[-2])==type('') and (SD == False):
                # static definition rules
                tempDict = {opstack[-2]:opstack[-1]}        # create dictionary with {name=stack[-2]:value=stack[-1]}
                opstack[-2:] = []                         # remove name and definition from stack
                staticChain.append((indx,tempDict))     # add this dictionary to staticChain
                indx +=1                                # can't forget to increment indx
                print("staticChain now = ", staticChain)
            else: print ("invalid operands for", t)

        # handle if
        elif t=='if':
            if len(opstack)>1 and type(opstack[-1])==type(True) and type(opstack[-2])==type([]):
                code = opstack.pop()
                cond = opstack.pop()
                if cond:
                    # recursively process the true branch code
                    evalLoop(code)
            else: print ("invalid operands for" , t)

        # handle ifelse  
        elif t=='ifelse':
	    # ifelse is similar but takes two code arrays as args
            if (len(opstack)>1 and type(opstack[-3])==type(True)
                             and type(opstack[-2])==type([])
                             and type(opstack[-1])==type([])):
                elsecode = opstack.pop()
                ifcode = opstack.pop()
                cond = opstack.pop()
                if cond:
                    code = ifcode
                else:
                    code = elsecode
                evalLoop(code)
            else: print ("invalid operands for" , t)

        # Use regular expression match to see if the token
        # t is a name constant, e.g. /abc123; if so push it
        elif name.match(t):
            opstack.append(t[1:])

        # Is it a name defined in a postscript dictionary?
        elif defined(t):
            defn = definition(t)
            if(type(defn)==type([])):
                evalLoop(defn)               
            else:
	        # otherwise, just push the value on the op stack
                opstack.append(defn)
        else:
	# if nothing else works try to interpret it as a number
            try:
                 # if it is a number push it
                 opstack.append(float(t))
            except:
	         # otherwise, it's an error
                 print (t,  " is not a valid token")
    return

def parse(s):
    tokens = re.findall(pattern, s)
    evalLoop(tokens)
    
printStack()
