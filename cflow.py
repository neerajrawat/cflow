import sys
import telnetlib
import pexpect
import time
import os
import getopt

#from clearline import clearline,switch_exec


			


def commandExecute(ip,port,platform_dir,image_name,tftp_server_ip,tftp_server_path,file_name):

	try:
		
		print "PESPECT"
		print 'telnet ' +ip+' '+port
		child= pexpect.spawn('telnet ' +ip+' '+port)	
		
		
		child.expect('Escape.*')
		child.sendcontrol('m')
		child.expect('>')	
		
		print "here"
			
		print "d"
		
		child.sendline('en')
		child.expect('#')
			
		print "Select a mode (\"exec\" OR \"enable\")"
		
		fout=open('tempLog.txt','w')					
		child.logfile=fout
		child.sendline('dir '+file_name)
		child.expect('#')
		
		
		
		
		child.logfile=sys.stdout
		

		fin=open('tempLog.txt','r')
		count=0
		flag=0
		for r in fin.readlines():
			count+=1
			rr=r.split(' ')
			print rr
			if '%Error' in rr:
				flag=1

		if count < 5 and flag==1:
			child.sendline('cflow copy '+file_name)
			child.expect('Destination.*')
			child.sendcontrol('m')
			child.expect('Write.*')
			child.sendcontrol('m')
			child.expect('#')
		
			
		child.sendline('copy flash:' + file_name + ' tftp://'+tftp_server_ip+'/'+tftp_server_path+'/'+file_name)
		child.expect('Address*')
		child.sendcontrol('m')
		child.expect('Destination*')
		child.sendcontrol('m')
		child.expect('#')
		#child.expect('.....*')
		#child.expect('File*')
		
			
		child.close()
		
## switch over		
		print 'cp /' + tftp_server_path + '/' + file_name + ' .'		
		os.system('cp /' + tftp_server_path + '/' + file_name + ' .')
		print '/auto/ses/repository/sesut_bleeding/cflow/cflowProcessing -f '+file_name+' -p ' + platform_dir + ' -i ' + image_name + ' -c .'
		os.system('/auto/ses/repository/sesut_bleeding/cflow/cflowProcessing -f '+file_name+' -p ' + platform_dir + ' -i ' + image_name + ' -c .')
		print 'cd da_files'
		os.system('cd da_files')
		print 'Run ls command and check for cflow.report file'
		
		
	except:
		print "Exception error"
		sys.exit(2)	
		

		

		
				
			

def arg_parser(args):
	ip=''
	port=0
	platform_dir=''
	image_name=''
	tftp_server_ip=''
	tftp_server_path=''
	file_name=''
	print "hello",args
	try:
		print "TRY"
		opts, argss = getopt.getopt(args,"hI:P:d:i:t:p:f:",["IP=","PORT=","platform_dir=","image_name=","tftp_server_ip=","tftp_server_path=","file_name="])
	except:
		print "ERROR"
		print 'Usage : python cflow.py -I <IP address of device> -P <Port number of device> -d <platform direcroty path (absolute path)> -i <image name> -t <IP of tftp server> -p <path in tftp server> -f <file name>'
		sys.exit(2)
	
	print args
	for opt, arg in opts:
		print opt,arg
		if opt == '-h':
			print 'Usage : python cflow.py -I <IP address of device> -P <Port number of device> -d <platform direcroty path (absolute path)> -i <image name> -t <IP of tftp server> -p <path in tftp server> -f <file name>'
			sys.exit()
		elif opt in ("-I", "--IP"):
			ip = arg
		elif opt in ("-P", "--PORT"):
			port = arg
		elif opt in ("-d", "--platform_dir"):
			platform_dir = arg
		elif opt in ("-i", "--image_name"):
			image_name = arg
		elif opt in ("-t", "--tftp_server_ip"):
			tftp_server_ip = arg
		elif opt in ("-p", "--tftp_server_path"):
			tftp_server_path = arg
		elif opt in ("-f", "--file_name"):
			file_name = arg	
			
	print ip,port,platform_dir,image_name,tftp_server_ip,tftp_server_path,file_name		
	commandExecute(ip,port,platform_dir,image_name,tftp_server_ip,tftp_server_path,file_name)
			

if __name__ == "__main__":
	try:
		#print sys.argv[1:]
		arg_parser(sys.argv[1:])
		#print sys.argv[1:]
				
	except:
		print "ERROR HERE"
		print 'Usage : python cflow.py -I <IP address of device> -P <Port number of device> -d <platform direcroty path (absolute path)> -i <image name> -t <IP of tftp server> -p <path in tftp server> -f <file name>'
		sys.exit()



