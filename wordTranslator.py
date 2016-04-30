#!/usr/bin/env python3

# Word translate list: 
#	Input: Word List, Origin Language, Language To Translate To, Output File
#
#		For Word in wordList :
#			commandline(googleTranslate -Word -OriginLanguage -TranslateTo >> OutputFile)
# LaTeX output for automatic flash card print

### Check For Dependencies ###
# Translate Shell #
# Directly
#	gawk "$(curl -Ls git.io/translate)" -I
# Linux
# 	http://www.soimort.org/translate-shell/
# 	sudo apt-get install gawk wget
# 	cd /tmp
# 	wget https://github.com/soimort/google-translate-cli/archive/master.tar.gz
# 	tar -xvf master.tar.gz
# 	cd google-translate-cli-master/
# 	sudo make install
# OR
#	wget git.io/trans
#	chmod +x ./trans
# MacOS
#	brew install http://www.soimort.org/translate-shell/translate-shell.rb
# SET LOCALE TO UTF-8
#
# UNICODE HELP
#		Unicode Sandwhich: bytes< unicode >bytes
#	http://nedbatchelder.com/text/unipain/unipain.html#35
#	http://nedbatchelder.com/text/unipain.html


import sys,pprint,subprocess,traceback

##### FUNCTS #####

def Pprint( datatoprint ) :
	#  Input: list or dictionary or anything
	# Return: Nothing
	#Purpose: quick code for development (debug) using pPrint
	pp = pprint.PrettyPrinter(indent=1)
	pp.pprint( datatoprint )

	#END Pprint #

def PrintStackTrace(_sysInfo, _limit):
	#	Input: sys.exc_info()
	#  Return: Nothing
	# Purpose: Quick Debug line, print stack trace from # of last executions
	exc_type, exc_value, exc_traceback = _sysInfo
	traceback.print_exception(exc_type, exc_value, exc_traceback, limit=_limit, file=sys.stdout)
	
	#END PrintStackTrace #

def Usage( debug ):
	#	Input: Boolean
	#  Return: Nothing
	# Putpose: Check for correct arguments and print usage statement
	if len(sys.argv) < 4 :
		print("")
		print("Usage: %s [word-list] [Origin Language] [translate Language] [output file] " % sys.argv[0])
		print("Example: ") 
		print("Translate a list of words from Greek to Urdu: ")
		print("%s translateThese.txt el ur memorizeThese.txt" % sys.argv[0])
		print("")
		print(languages)

		if debug != True :		
			sys.exit(0)

	#END Usage #


def ReadFile( filename ):
	#	Input: filename
	#  Return: every line from file
	# Purpose: Try to pen a file with read permissions
	
	# open file, get data, close file
	try :
		#file = open(filename,"r", encoding = CODE)
		file = open(filename,"rb")
		data = file.readlines()
		file.close()
	except :
		print("Couldn't Open or Read %s \n" % filename)
		PrintStackTrace(sys.exc_info(),4)
		sys.exit(1)
	
	return data

	#END ReadFile #


def MakeDictionary( data ):
	#	Input: data (lines) from file
	#  Return: dictionary
	# Purpose: Generate PY Dictionary of list of words from file

	dictionary = {}
	thekey = 1 		# numbered words

	# For UNICODE; binary sandwhich: |B| U |B|
	for line in data :
		token = line.strip(b'\n')
		dictionary[thekey] = [token]
		thekey += 1

	return dictionary

	#END MakeDictionary #


def WordList( filename ) :
	#	Input: filename
	#  Return: dictionary
	# Purpose: In one line; open file, send to MakeDictionary return dictionary
	words = ReadFile(wordListFile)
	if(DEBUG == True):
		print("SUCCEDED WordList: words = ReadFile(wordListFile)")
	return MakeDictionary( words )

	#END WordList #


def Translation( _dictionary, _origin, _destination, r2l, _verbose, _debug ):
	#	Input: Dictionary to append new words to; Origin Language; Destined Language; right-to-left, verbose, debug
	#  Return: Nothing
	# Purpose: Popen Translate Shell, get word, append to dictionary in right spot: dict[key][0][1]
	# List[0] = origin language
	# List[1] = translated language

	# based on usage for trans
	# default is english but this method opens dynamic abilities
	translation = _origin + ":" + _destination

	for key in list(_dictionary.keys()) :
		# print "Translating %s " % _dictionary[key]
		originalWord = _dictionary[key][0]
		trans = "/usr/local/bin/trans"
		transExecute = [trans, "-b", translation, originalWord ]
		
		output = runSystemCommand(transExecute)
		tokens = output.split(b'\n')
		
		#'''
		#Listing words and finding indecies to insert into dictionary is necessary
		#for right-left Languages.  But also backwards compatible for left-right
		#'''

		jibberish = tokens[0].rstrip(b' \t\r\n\0').split(b' ')
		index = len( jibberish ) - 1
		# saving as bytes
		translatedWord = jibberish[index]

		if _verbose:
			print( originalWord.decode(CODE) + "\t = \t" + translatedWord.decode(CODE))

		if r2l:
			_dictionary[key].append( reverseWord(translatedWord) )

		if _debug:
			print(translatedWord.decode(CODE) + reverseWord(translatedWord).decode(CODE) )

		else:
			_dictionary[key].append(translatedWord)

	#END Translation #

def reverseWord(_word):
	#	Input: String (binary w/ UTF-8)
	#  Return: reversed string
	# Purpose: for right-to-left languages the little-endian architecture
	#		   seems to wite the UTF-8 code in reverse. This is a small patch

	# http://stackoverflow.com/questions/5864271/reverse-a-string-in-python-two-characters-at-a-time-network-byte-order
	# elliot42 had fastest method
	# UTF-8 is 3 bytes long for each letter. Reverse every 3 bytes #wrong#charactershaveSize1-8bytes
    # !!!!!
    # !!!!! Unicode characters are between 1 & 6 bytes, must make 3, unicode.character.size of word[i]
    #len(b'\xd7\x90'.decode('utf-8'))
	newWord = b"".join([_word[x:x+3] for x in range(0,len(_word),3)][::-1])
	#newWord = b"".join( [_word[x:x+len(_word[x].decode(CODE))] for x in range(0, len(_word), len(_word[x].decode(CODE)) )][::-1] )


	return newWord
	#END reverseWord #

def Save( _outfile, _dictionary, printType, _debug ):
	#	Input: filename to save, dictionary of words, printing Type; tex or list, right to left, debug
	#  Return: Nothing
	# Putpose: Save translated words to file, if right to left language reverse order

	header = r"""
\documentclass[avery5371,grid,frame]{flashcards}

\usepackage[utf8]{inputenc}
\usepackage{etex}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}
\usepackage{polyglossia}

\setromanfont{Times New Roman}
\setsansfont{Courier New}

\cardfrontstyle[\large\slshape]{headings}
\cardbackstyle{empty}

\begin{document}
""".encode(CODE)
	
	footer = r"""
\end{document}
""".encode(CODE)

	flashBegin = r"""
\begin{flashcard}{\Huge """.encode(CODE)

	flashMiddle = r"""}
\bigskip
\bigskip
\begin{center}
{\sffamily\Huge\vspace*{\fill}
""".encode(CODE)

	flashEnd = r"""
\vspace*{\fill}}
\end{center}
\end{flashcard}
""".encode(CODE)
	
	# Open/Create File in Binary for Unicode handeling
	if _debug:
		print("Output type: %s" % printType)
	try : 
		file = open(_outfile, 'w',encoding=CODE)
		if(_debug == True):
			print(file)

		# Write to File
		try:
			#HEADER
			if printType == "tex":	
				file.write( header.decode(CODE) )
				if(_debug == True):
					print(header.decode(CODE))

			#LOOP
			for key in _dictionary:
				#List
				if printType == "list":
					if(_debug == True ):
						print("\n%30s   \t\t\t\t %s " % ( _dictionary[key][0],_dictionary[key][1] ))

					file.write("\n%30s   \t\t\t\t %s " % ( _dictionary[key][0],_dictionary[key][1] ))

				#LaTeX
				elif printType == "tex":		
					if(_debug == True ):
						Pprint( _dictionary[key] )

					# BEGIN FLASH CARD
					frontWord = _dictionary[key][0]
					backWord  = _dictionary[key][1]

					file.write( flashBegin.decode(CODE)	)
					file.write( frontWord.decode(CODE)	)
					file.write( flashMiddle.decode(CODE)	)
					file.write( backWord.decode(CODE)	)
					file.write( flashEnd.decode(CODE)	)
					# END FLASH CARD

			#END LOOP
			if printType == "list":
				file.write("\n\n")

			elif printType == "tex":
				file.write( footer.decode(CODE))
		#Error Writing
		except:
			print("%s Error writing output to %s !" % (printType,_outfile) )
			PrintStackTrace( sys.exc_info(), 4)

		# Close File
		try:
			file.close()
			print("Saved: %s" % _outfile)
		#Error Closing
		except:
			print("Could Not Close the file %s !" % _outfile)
			PrintStackTrace( sys.exc_info(), 4)
	#Error opening
	except :
		print("Cannot create/open %s !" % _outfile)
		PrintStackTrace( sys.exc_info(), 4)

	
	#END Save #

def runSystemCommand(_command):
	#	Input: Array of shell command with args
	#  Return: process.stdout.readline()
	# Purpose: Execute one system command, stdout=PIPE, return readline()

	#command = [transCommand, "-b", translation, originalWord ]
	try:
		process = subprocess.Popen(_command, stdout=subprocess.PIPE)
	except:
		print("Trying: %s : FAILED!" % _command)
		PrintStackTrace(sys.exc_info(),4)

	output = process.stdout.readline()

	return output
	#END runSystemCommand


##### MAIN #####
# wordlist = translateme.txt
# output   = memorizeme.txt
# DEPENDENCIES: xelatex, pdflatex, trans
#
##### MAIN #####

#GLOBALS
DEBUG = True
CODE = 'UTF-8'

languages = '''
┌───────────────────────────────┬───────────────────────┬──────────────────┐
│ Afrikaans           \- af     │ Hausa          \- ha  │ Persian    \- fa │
│ Albanian            \- sq     │ Hebrew         \- he  │ Polish     \- pl │
│ Arabic              \- ar     │ Hindi          \- hi  │ Portuguese \- pt │
│ Armenian            \- hy     │ Hmong          \- hmn │ Punjabi    \- pa │
│ Azerbaijani         \- az     │ Hungarian      \- hu  │ Romanian   \- ro │
│ Basque              \- eu     │ Icelandic      \- is  │ Russian    \- ru │
│ Belarusian          \- be     │ Igbo           \- ig  │ Serbian    \- sr │
│ Bengali             \- bn     │ Indonesian     \- id  │ Sesotho    \- st │
│ Bosnian             \- bs     │ Irish          \- ga  │ Sinhala    \- si │
│ Bulgarian           \- bg     │ Italian        \- it  │ Slovak     \- sk │
│ Catalan             \- ca     │ Japanese       \- ja  │ Slovenian  \- sl │
│ Cebuano             \- ceb    │ Javanese       \- jv  │ Somali     \- so │
│ Chichewa            \- ny     │ Kannada        \- kn  │ Spanish    \- es │
│ Chinese Simplified  \- zh\-CN │ Kazakh         \- kk  │ Sundanese  \- su │
│ Chinese Traditional \- zh\-TW │ Khmer          \- km  │ Swahili    \- sw │
│ Croatian            \- hr     │ Korean         \- ko  │ Swedish    \- sv │
│ Czech               \- cs     │ Lao            \- lo  │ Tajik      \- tg │
│ Danish              \- da     │ Latin          \- la  │ Tamil      \- ta │
│ Dutch               \- nl     │ Latvian        \- lv  │ Telugu     \- te │
│ English             \- en     │ Lithuanian     \- lt  │ Thai       \- th │
│ Esperanto           \- eo     │ Macedonian     \- mk  │ Turkish    \- tr │
│ Estonian            \- et     │ Malagasy       \- mg  │ Ukrainian  \- uk │
│ Filipino            \- tl     │ Malay          \- ms  │ Urdu       \- ur │
│ Finnish             \- fi     │ Malayalam      \- ml  │ Uzbek      \- uz │
│ French              \- fr     │ Maltese        \- mt  │ Vietnamese \- vi │
│ Galician            \- gl     │ Maori          \- mi  │ Welsh      \- cy │
│ Georgian            \- ka     │ Marathi        \- mr  │ Yiddish    \- yi │
│ German              \- de     │ Myanmar        \- my  │ Yoruba     \- yo │
│ Greek               \- el     │ Mongolian      \- mn  │ Zulu       \- zu │
│ Gujarati            \- gu     │ Nepali         \- ne  │                  │
│ Haitian Creole      \- ht     │ Norwegian      \- no  │                  │
└───────────────────────────────┴───────────────────────┴──────────────────┘
'''

# check usage
Usage(DEBUG)

# Word List file, Origin Language, Translate Language, Output File
if ( DEBUG == True ) & ( len(sys.argv) < 4 ) :
	wordListFile  = "translateme.txt"
	originLanguage = "en"
	translateLanguage = "ar"
	outputFile = "memorizeme.tex"
	print("DEBUGGING: ") 
else :
	wordListFile  = sys.argv[1]
	originLanguage = sys.argv[2]
	translateLanguage = sys.argv[3]
	outputFile = sys.argv[4]


# Collect words, insert into Dictionary[#][wordFromList]
wordDictionary = WordList( wordListFile )

# Translate each word from Dictionary, append translation Dictionary[#][wordFromList][translatedWord]
#			read Dictionary,	languange,	translate to,	right to left,  verbose, debug
Translation( wordDictionary,originLanguage,translateLanguage, True, True, DEBUG )

# Write words to file in either list: List or XeLaTeX: tex
#		file, 		dictionary,	  type,  debug
Save( outputFile, wordDictionary, "tex", False )




#### SCRAP ####

#print("%s %s %s %s %s" % ( sys.argv[0],wordListFile,originLanguage,translateLanguage,outputFile ))

# def MakeLaTeX(frontWord,backWord):
# 	#	Input: Front Word, & Back Word
# 	#  Return: String of Tex
# 	# Purpose: automate flash card making to Tex file

# 	# \begin{flashcard}{\Huge """ + frontWord.decode(CODE) + r"""}
# 	# """ + backWord.decode(CODE) + r"""
# 	flashcard = r"""
# \begin{flashcard}{\Huge """ + frontWord + r"""}
# \bigskip
# \bigskip
# \begin{center}
# \Huge
# """ + backWord + r"""
# \end{center}
# \end{flashcard}
# """.encode(CODE)
# 	#% ( frontWord.decode(CODE), backWord.decode(CODE) )

# 	return flashcard
# 	#END MakeLaTeX #


# def compileTex(_texFile):
# 	#
# 	#
# 	#
# 	xelatex = "/usr/texbin/xelatex"
# 	xelatexExecute = [xelatex, "-synctex=1", "-interaction=nonstopmode", _texFile]

# 	pdflatex = "/usr/texbin/pdflatex"
# 	pdflatexExecute = [pdflatex, "-synctex=1", "-interaction=nonstopmode", _texFile]
#	#END compileTex #
