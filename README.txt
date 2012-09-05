I ran my interpretter using Python 3.2 on a Windows 64-bit system and the Python IDLE GUI. 

I used a function called "parse" to parse all of the tokens according to PostScript rules. 
To use my interpreter, pass a string of tokens to parse. Parse will separate all of the tokens and call my evalLoop function, which is the main guts. 

I used a couple of helper functions, namely SCDictFinder() and SCLinkReturner()
SCDictFinder(x) could be re-named SCDefined(x), as it only checks for the existence of a name x anywhere in the staticChain 
SCLinkReturner(x) returns the static link to the tuple which has name x in it's dictionary 

I altered my defined() and definition() functions using these helper functions for static scoping. 
Those definitions stayed the same for dynamic scoping as in the SPS, but for static scoping they were different. 
In the defined(x) function for static scoping I look through the entire staticChain, looking at each tuple. 
	For each tuple, I check if the dictionary contains the name x 
In the definition(x) function for static scoping I simply look get the static link index of the name x and return it's definition

Examples: 

parse('1 2 add')
parse('2 3 mul') 
parse('/x {1 2 add} def')
parse('x')



So, to invoke the stack method for displaying output you input: 

parse('stack')



To clear the operand stack: 

parse('clear')


I ran interpreter against the code given in the assignment and got correct outputs. Here are my test outputs: 



>>> ================================ RESTART ================================
>>> 
Operand stack:
---Top---
---Bottom---
Dictionary stack:
---Top---
{}
---Bottom---
>>> parse(testx)					# testx, testg, testf are some test strings defined in my program
>>> parse(testg)
>>> parse(testf)
>>> parse('f')						# since f is a defined function, it's code will be called 
>>> parse('stack')					# this runs dynamic scoping by default 
Operand stack:
---Top---
7.0							# the right answer! 
---Bottom---
Dictionary stack:
---Top---
{'x': 7.0, 'g': ['x'], 'f': ['/x', '7', 'def', 'g']}
---Bottom---
>>> parse('clear')					# to clear the stack
>>> sys.argv.append('-s')				# this will indicate static scoping 
>>> parse(testx)
staticChain now =  [(0, {'x': 4.0})]
>>> parse(testg)
staticChain now =  [(0, {'x': 4.0}), (1, {'g': ['x']})]
>>> parse(testf)
staticChain now =  [(0, {'x': 4.0}), (1, {'g': ['x']}), (2, {'f': ['/x', '7', 'def', 'g']})]
>>> parse('f')
staticChain now =  [(0, {'x': 4.0}), (1, {'g': ['x']}), (2, {'f': ['/x', '7', 'def', 'g']}), (3, {'x': 7.0})]
>>> parse('stack')
Operand stack:
---Top---
4.0							# the right answer! 
---Bottom---
Dictionary stack:
---Top---
{'x': 7.0, 'g': ['x'], 'f': ['/x', '7', 'def', 'g']}
---Bottom---
>>> 