#!/usr/local/bin/python

"""
fibonacci is the worst example for programming recursion

"""

def fibLoop( k ) :
    p = 0
    c = 1
    if k == 0 :
        return p
    if k == 1 :
        return c

    i = 2
    while i <= k :
        n = p + c
        p = c
        c = n
        i += 1
        
    return n


def fibRec( k ) :
    if k == 0 :
        return 0
    if k == 1 :
        return 1

    return fibRec(k - 1) + fibRec(k - 2)
    
#####   main   #####
print fibLoop( 0 )
print fibLoop( 1 )
print fibLoop( 2 )
print fibLoop( 8 )
print fibLoop( 20 )
print fibLoop( 40 )

print
print fibRec( 0 )
print fibRec( 1 )
print fibRec( 2 )
print fibRec( 8 )
print fibRec( 20 )
print fibRec( 40 )
