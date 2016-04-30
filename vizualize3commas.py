#!/usr/bin/env python
'''
Play with a Billion Dollars 1$$$$$$$$
By: Kurt Gibbons
Psuedo:
 X  Read Money from file into dictionary
 X   Input name and cost
 X   Subtract Logically from dictionary (in parts)
 X   Write "Spent" dictionary to text file
 X   Write Billion$ to text file
 X   Benjamin$ Flow Show
 X   Remove or sell purchases
     Add option to print cash in different denominations
     Try enlarging wall and or columns
'''

import pprint       # for development
import sys, os      # for printing correctly

from sys import platform as _platform       # Correct Clear Screen Command
if _platform == "linux" or _platform == "linux2":
    # Linux
    Clear = 'clear'
elif _platform == "darwin":
    # OS X
    Clear = 'clear'
elif _platform == "win32":
    # Windows
    Clear = 'cls'

#$#$#$# Functions #$#$#$#$#
def Pprint( datatoprint ) :
    #  Input: list or dictionary
    # Return: Nothing
    #Purpose: quick code for development (debug) using pPrint
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(datatoprint)

def PrintAll( dictionary ) :
    #  Input: dictionary
    # Return: Nothing
    #Purpose: Print Dictionary for development debug
    for key in dictionary.keys() :
        print "%s" % (key)
        for l in range( len(dictionary[key]) ) :
            print "   %s" % (dictionary[key][l])

def billionOut( filename,mode,currency,moneyint ) :
    #  Input: "filename" "mode" $currency Integer
    # Output: Noting
    #Purpose: Populate text file with Billion$$$
    # formatted specifically to GenerateFunds function
    # hard-coded each line to 10 numbers (mandatory)
    # hard-coded each break to 10 lines (mandatory) 
    rows = 10
    # one billion in one million
    bwrite = open(filename,mode)
    
    title = "%s $1,000,000,000 in %s %s\n" % ("="*3,currency,"="*3)
    bwrite.write(title)
    
    for k in range(billion/(moneyint*(rows*rows))) :
        i = 1
        while i <= rows :
            string = "%s " % (currency)*10
            bwrite.write(string)
            bwrite.write("\n")
            i += 1
        bwrite.write("---\n")
    
    closetitle = "%s END %s\n" % ("="*3,"="*3)
    bwrite.write(closetitle)
    
    bwrite.close()
    
def GenerateFunds( filename ) :
    #  Input: filename
    # Return: dictionary
    #Purpose: Retrieve saved game file
    # specifically formatted for hundred thousand denomination
    file = open(filename,"r")
    data = file.readlines()
    file.close()
    
    dictionary = { }
    thekey = 1      # keys are numbers
    for line in data :
        token = line.strip()
        if '=' not in token[0]  :
            token = token.split(' ')
            if thekey not in dictionary.keys() :
                
                dictionary[thekey] = [token]
            elif '-' in token[0] :
                thekey += 1
            else :
                dictionary[thekey].append(token)
    return dictionary

def RecoverSpent( filename ) :
    #  Input: filename
    # Return: dictionary
    #Purpose: Retrieve saved game 'Spent' file
    # specifically formatted for spent file
    file = open(filename,"r")
    data = file.readlines()
    file.close()
    
    dictionary = { }
    
    for line in data :
        token = line.strip().split(',')
        money = token[1].split(':')
        money.remove('')    # delete extra space
        dictionary[token[0]] = money
        
    return dictionary

def SaveSpent( savedfile,dictionary ) :
    #  Input: Save File, Dictionary
    # Return: Nothing
    #Purpose: Save data to file (opened on start)
    # only used for spending dictionary
    save = open(savedfile,"w")
    for key in dictionary.keys() :
        string = "%s," % (key)
        save.write(string)
        i = 0
        for i in dictionary[key] :
            string = "%s:" % (i)
            save.write(string)

        string = "\n"
        save.write(string)
    save.close()

def SaveBank( savefile,dictionary ) :
    #  Input: save file, dictionary
    # Return: Nothing
    #Purpose: Save moneydata to file (opened on start)
    # only used for billion dollar dictionary in hundred thousands
    save = open(savefile,"w")
    keys = dictionary.keys()
    keys.sort()
    save.write("===\n")
    for key in keys :
        for l in dictionary[key] :
            for i in l :
                string = "%s " % (str(i))
                save.write(string)
            save.write("\n")
        save.write("---\n")
    save.write("===")
    save.close()

def ListSum( dictionary, key, l ) :
    #  Input: dictionary key list
    # Return: sum of list
    #Purpose: generate sum of list in key
    # inner inner innner loop
    listsum = 0
    for i in range(len(dictionary[key][l])) :
        listsum += int(dictionary[key][l][i])
    return listsum

def KeySum( dictionary,key ) :
    #  Input: dictionary key
    # Return: sum of key
    #Purpose: generate sum of key(s)
    # inner inner loop
    keysum = 0
    for l in range(len(dictionary[key])) :
        keysum += ListSum(dictionary,key,l)
    return keysum

def TotalSum(dictionary) :
    #  Input: dictionary
    # Return: TotalSum of Keys
    #Purpose: Generate total sum of all keys
    # inner loop
    totalsum = 0
    for key in dictionary.keys() :
        totalsum += KeySum(dictionary,key)
    return totalsum

def VisualCash(Dictionary) :
    #  Input: Dictionary
    # Return: Nothing
    #Purpose: Print Visual Money Wall
    # separated from main loop for ease of reading
    rows = 20
    cols = 5
    cash = 5
    key = 1
    r = 0 
    sys.stdout.write("{}")
    print "="*(rows - 8) ,
    sys.stdout.write(":. $%10d .:" % TotalSum(Dictionary)) ,
    print "="*(rows - 8) ,
    sys.stdout.write("{}"),
    print
    while r < rows :
        c = 0
        sys.stdout.write(' |') # Beginning of line
        while c < cols :
            # Bars
            sys.stdout.write(' |')
            ca = 0 
            list = 0
            while ca < cash :
                # Dollar$
                tmpsum = 0
                while list < len(Dictionary[key]) :
                    if (list+1) < len(Dictionary[key]) :
                        tmpsum = ListSum(Dictionary,key,list) + ListSum(Dictionary,key,list+1)
                        list += 1
                    if tmpsum == (billion/(cash*cols*rows)) :      # $2,000,000
                        sys.stdout.write('$')
                    elif tmpsum >= (billion/(cash*cols*rows)/2)  :  # $1,000,000
                        sys.stdout.write('S')
                    elif (billion/(cash*cols*rows)/2) > tmpsum and tmpsum != 0 :
                        sys.stdout.write('.')
                    elif tmpsum == 0 :
                        sys.stdout.write(' ')
                    list += 1
                ca += 1
            # Bars
            sys.stdout.write('|')
            key += 1
            c += 1
        sys.stdout.write(' |\n')  # End of line
        r += 1
    sys.stdout.write("{}")
    print "="*(10)      ,
    sys.stdout.write(":. $ is $%s .:"%(format((billion/(cash*cols*rows)),",d"))) ,
    print "="*(10)    ,
    sys.stdout.write("{}")       ,
    print

def Menu(Dict1,Dict2) :
    #  Input: MoneyDict SpentDict
    # Return: Nothing
    #Purpose: Main Loop of program (function for easier development)
    # raw_input doesn't allow arrow keys to be used by default
    Input = ' '
    delim = '$'
    while '!' not in Input[0] :
        VisualCash(Dict1)   # Print the visual wall
        # Menu #
        print ":{------ http://youtu.be/xwgRDW05-ZY ------}:"
        print ":}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{:"
        print ".:  (H)$100,000 : (B)$100 (VERY VERY LONG) :."
        print ".: (T)otal $$$ : (A)ccount Total$ : (S)ave :."
        print ".: (E)very Account : (P)urchases : (!)Exit :."
        print ":}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{:"
        print " Example Input >> House $500000  (no commas)"
        Input = raw_input(">> ")
        
        if 'billion' in Input :     # secret option
            # re-make billion in file and reinsert into dictionary
            try :
                billionOut( bfile,"w",100000,100000)
                Dict1 = GenerateFunds(bfile)
                print "Resetting $Billion fund"
            except :
                print "Couldn't write into file"
            
        elif 'reload' in Input :      # secret option
            # re-purchase spent file. used with 'billion' 
            try :         
                Dict2 = RecoverSpent( sfile )
                print "Reloading purchases into program"
            except :
                print "Couldn't read the file or it doesn't exist"
            
            mysum = 0
            for key in Dict2.keys() :
                for i in Dict2[key] :
                    mysum += int(i)
                    print key, i
            
            if mysum != 0 :
                for key in Dict2.keys() :
                    for l in range( len(Dict2[key]) ) :
                        Subtract(int(Dict2[key][l]),Dict1)
            else :
                print "Purchases are empty"
                    
        elif len(Input) <= 1 :      # User accessing menu options
            if 'T' in Input or 't' in Input :
                # Print Total
                print "$%s" % format(TotalSum(Dict1),",d")
                
            elif 'A' in Input or 'a' in Input :
                # Print sections of accounts
                # SectionPrint(10,Dict1)      # Evenly divisible by 100
                section = 10
                tmpsum = 0
                count, space= 1,2 
                for account in Dict1.keys() :
                    if account % section != 0 :
                        tmpsum += KeySum(Dict1,account)
                    else :
                        tmpsum += KeySum(Dict1,account)
                        print "%3d <-> %3d: $%12s" % (account-(section-1),account, format(tmpsum,",d")) ,
                        if count % space == 0 :
                            print 
                        tmpsum = 0
                        count += 1
                print
                
            elif 'S' in Input or 's' in Input :
                # Save Progress
                print "Saving Spending..."
                # Save Spent
                try :
                    SaveSpent( sfile,spentdict )
                except :
                    print "Couldn't save %s for some reason" % (sfile)
                # Save Bank
                print "Saving Accounts..."
                try :
                    SaveBank( bfile,moneydata )
                except :
                    print "Couldn't save %s for some unknown reason" % (bfile)
                    
            elif 'E' in Input or 'e' in Input :
                # Print All Accounts
                space = 5
                count = 0 
                for account in Dict1.keys() :
                    print "#%3d: $%10s" % (account, format(KeySum(Dict1,account),",d"))   ,
                    count += 1
                    if count % space == 0 :
                        print
                        
            elif 'P' in Input or 'p' in Input :
                # Print Purchases
                keys = Dict2.keys()
                keys.sort()
                for key in keys :
                    tmpsum = 0
                    count = 0
                    print "%s" % (key)  ,
                    for i in Dict2[key] :
                        tmpsum += int(i)
                        count += 1
                    if count > 1 :
                        print " : %3d Total -> $%s" % (count,format(tmpsum,",d"))
                    for i in Dict2[key] :
                        print "   $%s" % (format(int(i),",d"))
                        
            elif 'B' in Input or 'b' in Input :
                # Print Billion in Hundreds
                print "Benjamins!"
                Benjamins( Dict1 )
                
            elif 'H' in Input or 'h' in Input :
                # Print Billion in Hundred Thousands
                print " %s in Hundred Thousands! " % (format(TotalSum(Dict1),",d"))
                HundredThousand( Dict1 )
                
            elif '!' in Input :
                # Exit
                print "exiting..."
                Input = '!'
                
            else :
                # error in input
                print "error in input"
                Input = ' '
    
        else :          # user entering other than menu option
            if delim not in Input :     # forgot delimeter 
                print "Forgot to enter a ""%s"" " % (delim)
            else :      # everything entered correctly and continue altering dictionary
                purchase = Input.strip().split(delim)
                balance = TotalSum(Dict1)
                spent = int(purchase[1])
                # Check if enough funds before altering dictionary
                if spent > balance :
                    print " ! Account OVERDRAWN ! "
                    nbalance = spent - balance
                    print "You have $%s available" % (format(balance,",d"))
                    print "You are short $%s of $%s for %s" % (format(nbalance,",d"),format(spent,",d"),purchase[0])
                # funds are plentiful
                else :
                    # Add to Spending Dictionary
                    if purchase[0] not in Dict2.keys() :
                        Dict2.setdefault(purchase[0], [spent])
                    else :
                        Dict2[purchase[0]].append(spent)
                    print "%s costs $%s" % (purchase[0],format(spent,',d'))
                    # Algorithm to subtract from Money Dictionary
                    Subtract(spent,Dict1)
                
        if '!' not in Input :   # gives display a pause before clearing
            waitInput = raw_input("press [enter] to continue...")
        os.system(Clear)

def Subtract( spent, bankdict ) :
    #  Input: int(purchase[1]), bankdict
    # Return: Nothing
    #Purpose: Remove purchase from bank dictionary
    # check for funds in account before using this function
    key = 1   
    while key <= 100 :
        l = 0
        while l < len(bankdict[key]) :
            i = 0
            while i < len(bankdict[key][l]) :
                n = int(bankdict[key][l][i])
                if n > 0 :
                    # print "n=%s :" % (n)
                    if l == 9 and i == 9 and key != 100:
                        # cleaning out whole key. adding that value to next key
                        bankdict[key+1][0][0] = n + int(bankdict[key+1][0][0])
                        bankdict[key][l][i] = 0
                        key + 1
                    
                    elif i == 9 and l != 9:
                        # cleaning out whole list. adding that value to next list
                        bankdict[key][l+1][0] = n + int(bankdict[key][l+1][0])
                        bankdict[key][l][i] = 0
                        l + 1
                    
                    elif n < spent :    # collection still not enough
                        # add left over to next index and set == 0
                        currI = int(bankdict[key][l][i])
                        if i+1 != 10 :
                            nextI = int(bankdict[key][l][i+1])
                            bankdict[key][l][i+1] = nextI + currI
                            bankdict[key][l][i] = 0
                        else :
                            bankdict[key][l][i] = currI
                    elif n >= spent:    # collection more or equal to spent
                        # from here subtract from index then exit loop
                        # development
                        # foundkey,foundlist,foundindex = key,l,i
                        # print "found moneydict[%s][%s][%s] = %s" % (foundkey,foundlist,foundindex,
                        #                                bankdict[foundkey][foundlist][foundindex])
                        prevI = int(bankdict[key][l][i-1])
                        currI = int(bankdict[key][l][i])
                        bankdict[key][l][i] = prevI + currI
                        bankdict[key][l][i] = currI - spent
                        # development
                        # print
                        # print "found moneydict[%s][%s][%s] = %s" % (foundkey,foundlist,foundindex,
                        #                                bankdict[foundkey][foundlist][foundindex])
                        i = 11   # Exit Loop
                i += 1
            if n > spent :  # collected enough funds
                l = 11      # Exit Loop
            l += 1
        if key == 100 :     # exhausted all other keys
            print "Coming down to the last pennies. $%s left" % (format(KeySum(bankdict,key),",d"))
        if n > spent :  # collected enough funds
            key = 101   # Exit Loop
        key += 1 

def Benjamins( Dictionary ) :
    #  Input: Money Dictionary
    # Return: Nothing
    #Purpose: Print $100 denominations from money dictionary
    div = 20        # evenly divisible into 100
    keys = Dictionary.keys()
    keys.sort()
    counter = 1
    mysum = 0
    for key in keys :
        for l in Dictionary[key] :
            for i in l :
                money = int(i)
                if money % 100 == 0 :
                    out = money / 100
                    count = 1
                    while count <= out :
                        print " $100" * div ,
                        if counter % 10 == 0 :   # printing separating line
                            print
                            print " "   ,
                            print "-"*( div*5 - 3)  , counter/10 ,
                            print "stacks of $%s" % format(mysum,",d")
                            mysum = 0
                        else :      # print next line
                            print
                        mysum += (100*div)
                        count += div
                        counter += 1
                #else :
   
def HundredThousand( Dictionary ) :
    #  Input: Money Dictionary
    # Return: Nothing
    #Purpose: print out money in $100,000 denominations
    keys = Dictionary.keys()
    keys.sort()
    for key in keys :
        for l in Dictionary[key] :
            for i in l :
                m = int(i)
                if m != 0 and m % 100000 == 0 :
                    sys.stdout.write(" $%s" % (format(m,",d"))) ,
            if m != 0 : 
                print
        print " "   ,
        print "-"*((10*9) - 3) # len($100,000) * # of occurances
    print "\t $%s in $100,000 " % (format(TotalSum(Dictionary),",d"))

#~#~#~#~ MAIN ~#~#~#~#
billion = 1000000000        # using python's global variable ability
bfile = "b-save.txt"        # bank file
sfile = "p-save.txt"        # spending file

# Get Saved Bank
try :       # About 22 different errors can occur when opening a file
    moneydata = GenerateFunds(bfile)
except :
    print "Could not open %s, starting with new data" % (bfile)
    try :
        billionOut( bfile,"w",100000,100000)
        moneydata = GenerateFunds(bfile)
    except :
        print "Could not create %s for some reason" % (bfile)

# Get Saved Spending or create empty dictionary
try :
    spentdict = RecoverSpent( sfile )
except :
    print "%s couldn't be opened, using empty file" % (sfile)
    spentdict = { }

# Menu (main loop)
os.system(Clear)
Menu(moneydata,spentdict)   # hash out for development

# development spot

# Save Spent
try :
    SaveSpent( sfile,spentdict )
except :
    print "Couldn't save %s for some reason" % (sfile)

# Save Bank
try :
    SaveBank( bfile,moneydata )
except :
    print "Couldn't save %s for some unknown reason" % (bfile)

