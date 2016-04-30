#!/usr/bin/python
##!/usr/local/bin/python
# from an excel spreedsheat automate creating a bunch of default user accounts for various systems
#    used for a demo for a virtualized environment
# Read excel; generate each users needed account info
# -> output to text file
# nearly all needed user credentials were finished

import xlrd
import sys
import paramiko
import StringIO
import os

# dependencies 
# sudo pip install xlrd paramiko

LOAD=3
IPSTART=149
KEYSIZE=2048
WORDLIMIT=4
IPBLOCK="192.168.1."
MACHINEBLOCK="DEMO_0"
LINUXWORDLIST="/usr/share/dict/american-english"

xl_book =xlrd.open_workbook("spreadsheet.xlsx")
first_sheet = xl_book.sheet_by_index(0)

machineOffset=0
machineLoad=0

for row_idx in range(10):
	
	exportText="=== Login ===\n"
	LOGINNAME=first_sheet.cell(row_idx,0).value+"."+ first_sheet.cell(row_idx,1).value
	exportText+=LOGINNAME
	

	exportText+="\n=== Client Password ===\n"
	stCLP=""
	for word in range(0,WORDLIMIT):
		n = 0
		fiCLP = open(LINUXWORDLIST,"r");
		r = int(os.urandom(4).encode("hex"),16)%99154
	
		for line in fiCLP:
			if n >= r:
				if len(line) > 4:
					if len(line) < 9:
						stCLP+=line
						break
					else:
						r=(r+1)%99154
						n=n%99154
						if r >= 99154:
							fiCLP.seek(0)
			n=n+1
		fiCLP.seek(0)

	fiCLP.close()
	nstCLP=stCLP.replace("\n","")
	nnstCLP=nstCLP.replace("\'","")
	exportText+=nnstCLP+"\n"
	exportText+="=== VPN Password ===\n"
	stVNP=""
	for word in range(0,WORDLIMIT):
		n = 0
		fiVNP = open(LINUXWORDLIST,"r");
		r = int(os.urandom(4).encode("hex"),16)%99154
	
		for line in fiVNP:
			if n >= r:
				if len(line) > 4:
					if len(line) < 9:
						stVNP+=line
						break
					else:
						r=(r+1)%99154
						n=n%99154
						if r>=99154:
							fiVNP.seek(0)
			n=n+1
		fiVNP.seek(0)

	fiVNP.close()
	nstVNP=stVNP.replace("\n","")
	nnstVNP=nstVNP.replace("\'","")
	exportText+=nnstVNP+"\n"
	exportText+="=== IP ===\n"

	machineLoad = machineLoad % LOAD
	
	if machineLoad==0:
		machineOffset+=1
		
	machineLoad+=1
	exportText+=IPBLOCK+str(IPSTART+machineOffset)
	MACHINENAME=MACHINEBLOCK+str(machineOffset)
	exportText+="\n=== Machine Name ===\n"
	exportText+=MACHINENAME

	exportText+="\n=== Public SSH Key ===\n"
	exportText+="ssh-rsa "	
	k = paramiko.RSAKey.generate(KEYSIZE)
	pub_key = k.get_base64()
	out = StringIO.StringIO()
	k.write_private_key(out)
	exportText+=pub_key
	exportText+=" "+LOGINNAME+"@"+MACHINENAME
	exportText+="\n=== Private SSH Key ===\n"
	exportText+= out.getvalue()

	exportText+="\n=== x2go config file==="
	exportText+="\nWIP\n\n"

	fo = open(first_sheet.cell(row_idx,0).value+"."+ first_sheet.cell(row_idx,1).value+".txt","w")
	fo.write(exportText)
	fo.close()
