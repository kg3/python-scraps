#!/usr/bin/env python
'''
Modify tckeyfilecrack.py for keyfile directory and no keyfile directory
Cycle through password list
Only making script because Truecrypt doesn't work with cascade crypto
Using Truecrypt to Crack itself, so do don't have to configure specialized crypto code.
!!! MUST RUN AS SUDO !!!
'''
import subprocess,os
from sys import argv,exit

'''
if len(argv) < 5 :
    print "Must Run With SUDO!"
    print "Usage: %s truecrypt.volume passlist.txt keyfiledir/ mountpoint/ [options]" % argv[0]
    print "options: k [keyfiles only] p [passwords only] c [combination both keyfiles & passwords]"
    print "while cycling through: aes | serpent | twofish"
    exit(0)
truevol  = argv[1]
passfile = argv[2]
keyfile_foder = argv[3]
mount_point = argv[4]
options = argv[5]
'''

# Development
keyfiledirs = ['/home/user/keyfiles/one.mp3',
               '/home/user/keyfiles/two.flv',
               ]

truevol  = '/true/file' #'truetest.volume'    
passfile = '/true/forgottenpass.txt' #'truepass.txt'    
mount_point = '/media/truecrypt1/'    # Mount point if TrueCrypt is able to decrypt the file
# keyfile_folder = ''    # Location of keyfiles, you must copy all possible keyfiles in that folder

# Check files & directories #
if (os.path.isfile(truevol) == 0):
  print "%s file does not exist" % (truevol)
  exit(1)

if (os.path.isdir(mount_point) == 0):
  print "Mount point, %s does not exist" % (mount_point)
  exit(1)
  
if (os.path.ismount(mount_point) == 1):
  print "Mount point, %s already mounted" % (mount_point)
  exit(1)

#  # Best Assume OKAY For Now
# for folder in keyfiledirs :
#     if (os.path.isdir(folder) == 0):
#       print "Keyfile folder, %s does not exist or is empty" % (keyfile_folder)
#       exit(1)
# 

fp = open(passfile,"r")
data = fp.readlines()
fp.close()

passwords = []
for line in data :
    word = line.strip()
    passwords.append(word)


# try only keyfile directories/files
for keyfiles in keyfiledirs :
        print "Trying keyfolder/keyfile: %s" % (keyfiles)
        child = subprocess.Popen(['truecrypt', '-t', '--non-interactive','-k', keyfiles, truevol, mount_point], \
            stderr=open(os.devnull, 'w'), stdout=open(os.devnull, 'w'))
        child_output = child.communicate()[0]  
        child_rc =  child.returncode
        
        if (child_rc == 0):
            print "Successfully opened TrueCrypt keyfile(dir): %s" % (keyfiles)
            exit(0)

# try passwords with keyfile dir & without keyfile dir
for password in passwords :
    # TrueCrypt #
    '''
    print "Trying %s without keyfiles" % password
    child = subprocess.Popen(['truecrypt', '-t', '--non-interactive', '-p', password, truevol, mount_point], \
        stderr=open(os.devnull, 'w'), stdout=open(os.devnull, 'w'))
    child_output = child.communicate()[0]  
    child_rc =  child.returncode
  
    if (child_rc == 0):
        print "Successfully opened TrueCrypt pass: %s NO keyfiles" % password
        exit(0)
    '''
    
    # Try passwords with Keyfile Directories
    for keyfiles in keyfiledirs :
        print "Trying %s with keyfolder: %s" % (password,keyfiles)
        child = subprocess.Popen(['truecrypt', '-t', '--non-interactive', '-p', password, '-k', keyfiles, truevol, mount_point], \
            stderr=open(os.devnull, 'w'), stdout=open(os.devnull, 'w'))
        child_output = child.communicate()[0]  
        child_rc =  child.returncode
        
        if (child_rc == 0):
            print "Successfully opened TrueCrypt pass: %s keyfiledir: %s" % (password,keyfiles)
            exit(0)


# if we are here, then the return value from truecrypt was never 0 and therefore not successful
if (child_rc != 0): 
    print "Failed to open TrueCrypt file"
    exit(1)

