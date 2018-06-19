#!/usr/bin/python
from __future__ import unicode_literals
from __future__ import print_function
import sys
import telnetlib
import paramiko
import datetime
import os
import csv
import random
import string
import array
import subprocess
import ipaddress
import xlwt
import xlrd
import platform
import time
import glob
import re


users_list = ['cdknoc', 'adp']
default_router_password = 'P1etHh0n!'
default_enable_password = 'iZemb3dd3D'

remarks = []
output_file_name = "Result.xls"
vrf_name = ""
login_hosts = []
incrementor_support = 0
incrementor_list = []


dict_routername=  { "ORD1-ACCESSR15" : "100.76.255.120",   "ORD1-ACCESSR16" : "100.76.255.119",
                    "ORD1-ACCESSR01" : "100.76.255.227" , "ORD1-ACCESSR02" :  "100.76.255.226",
                    "ORD1-ACCESSR03" :  "100.76.255.225",   "ORD1-ACCESSR04" : "100.76.255.224",
                     "ORD1-ACCESSR05" : "100.76.255.223",   "ORD1-ACCESSR06" : "100.76.255.222",
                     "ORD1-ACCESSR07" : "100.76.255.221",  "ORD1-ACCESSR08" : "100.76.255.220",
                   "ORD1-ACCESSR09": "100.76.255.219",
                   "LAS-ACCESSR01" : "100.80.255.227" ,   "LAS-ACCESSR02" : "100.80.255.226",
                    "LAS-ACCESSR03"  :"100.80.255.225",   "LAS-ACCESSR04" : "100.80.255.224",
                     "LAS-ACCESSR05" : "100.80.255.223",  "LAS-ACCESSR06" : "100.80.255.222" ,
                    "LAS-ACCESSR07" : "100.80.255.220" ,  "LAS-ACCESSR08" : "100.80.255.220",
		    "LAS-ACCESSR09" : "100.76.255.219"}


username = sys.argv[2]
filee = sys.argv[1]
# print(filee
# print(username)

login_username = 'admin'
pswd = 'DC21nstall'
#result_path = '/var/www/html/test_tart/failovertests/logs/'+user

#new_folder_name = "/var/www/html/failovertests/uploads/"+username+"_"+datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
#if not os.path.exists(new_folder_name):
#	os.mkdir(new_folder_name)

############################# Login process ##########################################
def auto_router_login():
        tryy = 0
	#print("auto done")
        for x in users_list:
                r1_bool = False
                time.sleep(1)
                tel_res = tel.read_until("sername: ".encode('ascii'),2)# Regular login attempt
		
		#print(tel_res)
                time.sleep(1)
                tel.write((x + '\r').encode('ascii'))
                tel.read_until('assword: '.encode('ascii'),2)
                tel.write((default_router_password + '\r' + '\n \n').encode('ascii'))
        #       time.sleep(1.2)
                tryy = tryy + 1
                login_status = tel.read_until(">".encode('ascii'),2)
		#print(login_status)
                if bool(re.search(">",login_status.decode("utf-8"))) is True:
#                        print("default login success")
			login_username = x
                        r1_bool = True
                        if enab(login_username) == True:
                        	break
			else:
				r1_bool = False
                else:
        #               print "Error Credentials on both the attempts.\n"
                        r1_bool = False
        return r1_bool

def enab(login_username):
        enab_bool = False
        #print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        #print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'),2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
	#print(enab_status)
        if bool(re.search("#",enab_status.decode("utf-8"))) is True:
                #print ("Auto ENABLE CREDENTIALS worked!")
                enab_bool = True
		if login_status == "Global":
			lic()
		elif login_status == "Local" and len(vrf_name) ==0 : # telnet from tha main router
			print("Local without VRF")
			tel.write(('telnet '+login_ip+  ' \r').encode('ascii'))
			tel.read_until("sername:".encode('ascii'))
			tel.write((login_username+'\r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_router_password+'\r').encode('ascii'))
			tel.read_until(">".encode('ascii'))
			tel.write(('en \r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_enable_password+'\r').encode('ascii'))
			tel.read_until("#".encode('ascii'))
			toc()
		elif login_status == "Local" and len(vrf_name) !=0 : # telnet from tha main router
			print("Local with VRF")
			tel.write(('telnet '+login_ip+  'vrf '+vrf_name+' \r').encode('ascii'))
			tel.read_until("sername:".encode('ascii'))
			tel.write((login_username + '\r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_router_password + '\r').encode('ascii'))
			tel.read_until(">".encode('ascii'))
			tel.write(('en \r').encode('ascii'))
			tel.read_until("assword:".encode('ascii'))
			tel.write((default_enable_password + '\r').encode('ascii'))
			tel.read_until("#".encode('ascii'))
			toc()
#		print("status",status)
	
        #elif bool(re.search("assword:",enab_status.decode("utf-8"))) is True:
		#continue
                #print ("AUTO ENABLE CREDENTIALS DID NOT WORK.")
        #       print "\nCustomer might be having CUSTOM PREVILIDGE PASSWORD. Please refer NETLIB or CRYPTO TOOL to know the password. \n Please enter the password below:\n"
                #man_enab_pwd = raw_input('Please enter the CUSTOM ENABLE password here: ')
                #tel.read_until('assword: '.encode('ascii'))
                #tel.write((man_enab_pwd + '\r').encode('ascii'))
                #if tel.read_until("#".encode('ascii'), 2):
        #                       print "Manual ENABLE CREDENTIALS worked! Previlidged access achieved\n\n"
                        #enab_bool = True
		#continue

        else:
                print ("ERROR IN CUSTOM ENABLE PASSWORD")
                enab_bool = False
		#continue
        return enab_bool


def isUp(hostname):
        response = ""
#	print(hostname)
	isUpBool = ""
	if login_status == "Global":
		
		if platform.system() == "Windows":
		 #       print ("Pinging Windows")
			response = os.system("ping "+hostname+"> /dev/null")
	 #               print ("\nPing from WINDOWS PC is successful. \nThe client " + hostname + " is LIVE!\n")
		else:
		  #      print ("Pinging Linux")
			response = os.system("ping -c 1 "+hostname+" > /dev/null")
	   #             print ("\nPing from LINUX PC is successful. \nThe client " + hostname + " is LIVE!\n")
		
		if response == 0:
			# worksheet.write(j, 17, 'success',style2)
			# workbook.save(new_folder_name + '/' + output_file_name)
			print (hostname, 'is up!')
			isUpBool = True
		else:
			# worksheet.write(j, 17, 'failed',style1)
			# workbook.save(new_folder_name + '/' + output_file_name)
			print (hostname, 'is down!')
	else:
		isUpBool = True
		
	return isUpBool
################################ Type of connectivity ########################################
def lic():
	position = index + 2
	tel.write("ter len 0 \r".encode('ascii'))
	tel.read_until("#".encode('ascii'))
	tel.write("sh ver | i ISR Software \r".encode('ascii'))
	isr_validation_output = tel.read_until("#".encode('ascii'))
	tel.write("sh ip int brief | in unnel\r".encode('ascii'))
	tunnel_validation_output = tel.read_until("#".encode('ascii'))
	print(tunnel_validation_output)
	
	
	print(isr_validation_output)
	if bool(re.search('ISR',isr_validation_output.decode("utf-8").splitlines()[1])) is True:
		worksheet.write(position, 10, 'ISR4K', style2)
		tel.write(('dir | i .lic\r').encode('ascii'))
		dir_output = tel.read_until("#".encode('ascii'))
		tel.write(('sh license | be Feature: throughput\r').encode('ascii'))
		throughput_output = tel.read_until("#".encode('ascii'))
		
		tel.write(('sh ver | i Processor board ID\r').encode('ascii'))
		serialno_output = tel.read_until("#".encode('ascii'))
		
		tel.write(('sh license udi\r').encode('ascii'))
		license_udi_output = tel.read_until("#".encode('ascii'))
		
		tel.write(('sh ver | b Technology Package License Information:\r').encode('ascii'))
		# tel.write(('sh ver | b Technology Package License Information:\r').encode('ascii'))
		version_output = tel.read_until("#".encode('ascii'))
		#print(version_output)
		
		appxk9_find = re.findall('appxk9 (.+?)\n',version_output.decode("utf-8"))
		uck9_find = re.findall('uck9 (.+?)\n',version_output.decode("utf-8"))
		securityk9_find = re.findall('securityk9 (.+?)\n',version_output.decode("utf-8"))
		ipbase_find = re.findall('ipbase (.+?)\n',version_output.decode("utf-8"))
		# print("appxk9_find",appxk9_find)
		# print("uck9_find", uck9_find)
		# print("securityk9_find", securityk9_find)
		# print("ipbase_find", ipbase_find)
		
		if appxk9_find:
			appxk9_find_split = str(appxk9_find).split()
			appxk9 = appxk9_find_split[len(appxk9_find_split)-2]
			print("appxk9", appxk9)
		if uck9_find:
			uck9_find_split = str(uck9_find).split()
			uck9 = uck9_find_split[len(uck9_find_split) - 2]
			print("uck9", uck9)
		if securityk9_find:
			securityk9_find_split = str(securityk9_find).split()
			securityk9 = securityk9_find_split[len(securityk9_find_split) - 2]
			print("securityk9", securityk9)
		if ipbase_find:
			ipbase_find_split = str(ipbase_find).split()
			ipbase = ipbase_find_split[len(ipbase_find_split) - 2]
			print("ipbase", ipbase)
			
		# print("appxk9_find_split",appxk9_find_split,type(appxk9_find_split),len(appxk9_find_split))
		
		print("dir_output",dir_output,type(dir_output),len(dir_output))
		
		
		throughput_outpu_find = re.findall('License Type: (.+?)\n', throughput_output.decode('utf-8'))
		if throughput_outpu_find:
			throughput = throughput_outpu_find[0]
			# print("throughput",throughput)
		# # throughput = str(throughput_outpu_find).replace("[","").replace("]","").replace("\\r","").replace("u'","").replace("'","")
		# appxk9 = throughput_outpu_find[0]
		# uck9 = throughput_outpu_find[1]
		# securityk9 = throughput_outpu_find[2]
		# ipbase = throughput_outpu_find[3]
		# throughput = throughput_outpu_find[7]
		# print("throughput_outpu_find", throughput_outpu_find, type(throughput_outpu_find), len(throughput_outpu_find))
		# print("appxk9", appxk9)
		# print("uck9", uck9)
		# print("securityk9", securityk9)
		# print("ipbase", ipbase)
		# print("throughput", throughput)
		
		print(serialno_output)
		
		serialno_find = re.findall('Processor board ID (.+?)\n', serialno_output.decode('utf-8'))
		if serialno_find:
			# print("serialno_find",serialno_find,type(serialno_find),len(serialno_find))
			# print(serialno_find[0])
			serial_no = serialno_find[0]
			# print("serial_no",serial_no)
		
		# print(license_udi_output)
		license_udi_output_splitlin = license_udi_output.splitlines()
		license_udi_capture = license_udi_output_splitlin[ len(license_udi_output_splitlin) - 3 ]
		if license_udi_capture:
			license_udi_split = license_udi_capture.split()
			license_udi = license_udi_split[len(license_udi_split)-2]
			
			print(license_udi,type(license_udi),len(license_udi))
		
		dir_splitline = dir_output.decode('utf-8').splitlines()[:-1]
		# print("dir_splitline",dir_splitline,type(dir_splitline),len(dir_splitline))
		if len(dir_splitline) != 1:
			last_license = dir_splitline[len(dir_splitline)-1]
			last_license_split = last_license.split()
			license_date = last_license_split[3]+" "+last_license_split[4]+" "+last_license_split[5]
			license_name = last_license_split[8]
			# print("last_license",last_license,type(last_license),len(last_license))
			# print("last_license_split", last_license_split, type(last_license_split), len(last_license_split))
			# print("date",license_date,type(license_date),len(license_date))
			# print("date", license_name, type(license_name), len(license_name))
			
			worksheet.write(position, 0, login_ip, style2)
			worksheet.write(position, 1, license_name, style2)
			worksheet.write(position, 2, license_date, style2)
			if appxk9:
				worksheet.write(position, 3, appxk9, style2)
			if uck9:
				worksheet.write(position, 4, uck9, style2)
			if securityk9:
				worksheet.write(position, 5, securityk9, style2)
			if ipbase:
				worksheet.write(position, 6, ipbase, style2)
			if throughput:
				worksheet.write(position, 7, throughput, style2)
			if serial_no:
				worksheet.write(position, 8, serial_no, style2)
			if license_udi:
				worksheet.write(position, 9, license_udi, style2)
		else:
			print("condition do not match")
			
			worksheet.write(position, 0, login_ip, style2)
			if appxk9:
				worksheet.write(position, 3, appxk9, style2)
			if uck9:
				worksheet.write(position, 4, uck9, style2)
			if securityk9:
				worksheet.write(position, 5, securityk9, style2)
			if ipbase:
				worksheet.write(position, 6, ipbase, style2)
			if throughput:
				worksheet.write(position, 7, throughput, style2)
			if serial_no:
				worksheet.write(position, 8, serial_no, style2)
			if license_udi:
				worksheet.write(position, 9, license_udi, style2)
				
		# Tunnel Validation
		
		tunnel_validation_splitline = tunnel_validation_output.splitlines()[1:][:-1]
		print(tunnel_validation_splitline,type(tunnel_validation_splitline),len(tunnel_validation_splitline))
		if bool(re.search('unnel', str(tunnel_validation_splitline))) is True:
			tunnel_available = "Yes"
			worksheet.write(position, 11, tunnel_available, style2)
		# print("Tunnel Available")
		else:
			tunnel_available = "No"
			worksheet.write(position, 11, tunnel_available, style2)
	else:
		worksheet.write(position, 0, login_ip, style2)
		worksheet.write(position, 10, 'Non-ISR4K', style2)
		print("Non ISR device")

	
	

def toc():
	sdn = []
	
	tel.write("ter len 0 \r".encode('ascii'))
        tel.read_until("#".encode('ascii'))
	tel.write(('sh vlans | i Virtual LAN ID: | IP\r').encode('ascii'))
        vlan_result = tel.read_until("#".encode('ascii'))
	tel.write(('sh ip int brief | i Vlan\r').encode('ascii'))
	sw_vlan_result = tel.read_until("#".encode('ascii'))
	tel.write("sh run | i hostname \r".encode('ascii'))
	hostname_output = tel.read_until("#".encode('ascii'))
	tel.write("sh cdp nei detail | i Interface:|Device ID:|IP address: \r".encode('ascii'))
	cdp_output = tel.read_until("#".encode('ascii'))
	tel.write("sh vlans | i vLAN Trunk Interface: \r".encode('ascii'))
	trunk_interface_output = tel.read_until("#".encode('ascii'))
	tel.write("sh ip int brief | exc administratively \r".encode('ascii'))
	interface_brief_output = tel.read_until("#".encode('ascii'))
	
	dummy_hostname_find = hostname_output.decode("utf-8").splitlines()
	#print("dummy_hostname_find", dummy_hostname_find, type(dummy_hostname_find), len(dummy_hostname_find))
	if len(dummy_hostname_find) == 3:
		dummy_hostname = dummy_hostname_find[-1]
		#print("dummy", dummy_hostname, type(dummy_hostname), len(dummy_hostname))
		tel.write("sh inv\r".encode('ascii'))
		inventory_output = tel.read_until(dummy_hostname)
		#print("inventory_output", inventory_output)
	else:
		print("command execution error")
	tel.write("sh run | be banner exec \r".encode('ascii'))
	banner_output = tel.read_until("end".encode('ascii'))
	#print(banner_output)
	# tel.write("\r".encode('ascii'))
	# print("kpppaaaa",tel.read_until("#".encode('ascii')))
	# tel.write("\r".encode('ascii'))
	# print("kpppaaaa", tel.read_until("#".encode('ascii')))
	
	#print(hostname_output)
	#
	
	
	hostname_find = re.findall('hostname (.+?)\n',hostname_output.decode("utf-8"))
	#print("hostname_find",hostname_find)
	# for hostname in hostname_find:
	# 	print(hostname,type(hostname),len(hostname) )
	#print(hostname)
	
	pid_find = re.findall('PID: (.+?),',inventory_output.decode("utf-8") )
	#print(pid_find)
	
	sn_find = re.findall('SN: (.+?)\n', inventory_output.decode("utf-8"))
	#print(sn_find)
	
	
	
	#vlan_id_find = []
	vlan_id_find = re.findall('Virtual LAN ID: (.+?) \(',vlan_result.decode("utf-8")) # Need to ignore first value
	vlan_ip_find = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', vlan_result.decode("utf-8"))
	vlan_id_find= vlan_id_find
	#print(vlan_ip_find)
	#print(vlan_id_find,len(vlan_id_find))
	
	#print('trun_interface_output', trunk_interface_output)
	
	trunk_interfaces = re.findall('vLAN Trunk Interface: (.+?)\n', trunk_interface_output.decode("utf-8"))
	trunk_interfaces = trunk_interfaces[1:]
	#print('trunk_interfaces', trunk_interfaces)
	
	router_interfaces = []
	used_interface = []
	non_used_interface = []
	no_need_interfaces = ["NVI0",'Loopback',"Interface"]
	if trunk_interfaces:
		interface_brief_output_extract = interface_brief_output.decode("utf-8").splitlines()[1:][:-1]
		for interface in interface_brief_output_extract:
			if len(interface) >2 and bool(re.search("Loopback",interface)) is not True:
				catch = interface.split()
				router_interfaces.append(catch[0])
			
		#print(router_interfaces,type(router_interfaces),len(router_interfaces))
		
		# for ints in router_interfaces:
		# 	print("ints",ints)
		# 	for inters in trunk_interfaces:
		# 		print("inters",inters)
		# 		if ints == inters:
		# 			used_interface.append(ints)
		# 		else:
		# 			non_used_interface.append(ints)
		#
		# print('used_interface',used_interface)
		# print('no used_interface', non_used_interface)
		
		# first_set = list(set(router_interfaces) - set(trunk_interfaces))
		# print('first_set',first_set)
		
		
		for ints in router_interfaces:
			if bool(re.search(ints,str(trunk_interfaces))) is not True:
				non_used_interface.append(ints)
		for inters in non_used_interface:
			# print(inters)
			# print(str(non_used_interface))
			if bool(re.search(inters, str(no_need_interfaces))) is not True:
				
				
				used_interface.append(inters)
		#print('used_interface', used_interface)
		
	sw_vlan_id = []
	unassiged_vlan = []
	assigned_vlan = []
	if not vlan_ip_find:
		#print('sw_vlan_result',sw_vlan_result)
		sw_vlan_result_extract = sw_vlan_result.splitlines()[1:][:-1]
		#print(sw_vlan_result_extract)
		for vln in sw_vlan_result_extract:
			if bool(re.search('unassigned',vln,re.I)) is True:
				unassiged_vlan.append(vln)
			else:
				assigned_vlan.append(vln)
		for vlan in str(assigned_vlan).replace(',','').split():
			if bool(re.search('Vlan',vlan,re.I)) is True:
				sw_vlan_id.append(vlan.replace('[','').replace("'",""))
		vlan_id_find = sw_vlan_id
		#vlan_id_find = vlan_id_find[1:]
			 
				
			
		sw_vlan_ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(assigned_vlan))
		vlan_ip_find = sw_vlan_ip
		#print(sw_vlan_ip,type(sw_vlan_ip),len(sw_vlan_ip))
		#print(vlan_ip_find.append(sw_vlan_ip))
		
		
		#print("vlan_id_find",vlan_id_find,type(vlan_id_find))
		
	cdp_interfaces = re.findall('Interface: (.+?),',cdp_output.decode("utf-8")) # Interface Information (Used / Available)
	cdp_device_id = re.findall('Device ID: (.+?)\n',cdp_output.decode("utf-8"))  # Uplinked to (Description)
	cdp_ip_address = re.findall('IP address: (.+?)\n',cdp_output.decode("utf-8"))  # column L
	dumm_cdp_ip_address = []
	
	for i in cdp_ip_address:
		if not i in dumm_cdp_ip_address:
			dumm_cdp_ip_address.append(i)
		
	cdp_ip_address = dumm_cdp_ip_address
	#print("cdp_interfaces",cdp_interfaces)
	#print("cdp_device_id", cdp_device_id)
	#print("cdp_ip_address", cdp_ip_address)
	for cdint in used_interface:
		cdp_interfaces.append(cdint)
	#print(cdp_interfaces)
	
	
	
	cmf_no_find = re.findall('Client CMF = (.+?)\n',banner_output.decode('utf-8'))
	site_name_find = re.findall('Client Name = (.+?)\n', banner_output.decode('utf-8'))
	
	#print(cmf_no_find,site_name_find)
	
	
	# trun_interface_output_extract = trun_interface_output.decode("utf-8").splitlines()[1:][:-1]
	# for trunk in str(trun_interface_output_extract).split():
	
	#vlan_id_find = str(vlan_id_find).replace
	excel_formating(cmf_no_find,site_name_find,vlan_id_find,vlan_ip_find,hostname_find,pid_find,sn_find,cdp_interfaces,cdp_device_id,cdp_ip_address)

################################## Excel formating #######################################
def excel_formating(cmf_no_find,site_name_find,vlan_id_find,vlan_ip_find,hostname_find,pid_find,sn_find,cdp_interfaces,cdp_device_id,cdp_ip_address):
	# variable index used here is from for index,login_ip in enumerate(login_hosts):
	print("lets format")
	print(index)
	print("row_count",row_count)
	index_value = index
	position = index_value+2
	print("pre",position)
	
	
	max_list = [len(cmf_no_find),len(site_name_find),len(vlan_id_find),len(vlan_ip_find),len(hostname_find),len(pid_find),len(sn_find),len(cdp_interfaces),len(cdp_device_id),len(cdp_ip_address)]
	print(max_list,type(max_list))
	incrementor_list.append(max(max_list))
	print("incrementor",incrementor_list,type(incrementor_list),len(incrementor_list))
	print(index_value)
	#print('incrementor_support', incrementor_support)
	
	if index == 0:
		position = index_value + 2
	else:
		incrementor = 0
		# index_incr = index + 2
		for incr in incrementor_list[:-1]:
			incrementor +=incr
		#print("j",j)
		#print("incr-2",j-2)
		i = 0
		# incrementor = incrementor_list[len(incrementor_list)-2]
		print("incrementor",incrementor )
		
		index_value = incrementor
		position = incrementor + 2
		#incrementor_support += 1
		
		
	print("post",position)
	
	print("j",j)
	# print("cmf_no_find",cmf_no_find, type(cmf_no_find), len(cmf_no_find))
	# print("site_name_find", site_name_find, type(site_name_find), len(site_name_find))
	# print("vlan_id_find", vlan_id_find, type(vlan_id_find), len(vlan_id_find))
	# print("vlan_ip_find", vlan_ip_find, type(vlan_ip_find), len(vlan_ip_find))
	# print("hostname_find", hostname_find, type(hostname_find), len(hostname_find))
	# print("pid_find", pid_find, type(pid_find), len(pid_find))
	# print("sn_find", sn_find, type(sn_find), len(sn_find))
	# print("cdp_interfaces", cdp_interfaces, type(cdp_interfaces), len(cdp_interfaces))
	# print("cdp_device_id", cdp_device_id, type(cdp_device_id), len(cdp_device_id))
	# print("cdp_ip_address",cdp_ip_address, type(cdp_ip_address), len(cdp_ip_address))
	#print("vlan_id_find", vlan_id_find, type(vlan_id_find), len(vlan_id_find))
	# print(vlan_ip_find, type(vlan_ip_find), len(vlan_ip_find))
	# print(pid_find)
	
	worksheet.write(position, 0, cmf_no_find, style2)
	worksheet.write(position, 1, site_name_find, style2)
	print("position site name and index ",position,index_value)
	for index1,vlan_ip in enumerate(vlan_ip_find):
		worksheet.write(position, 3, vlan_ip, style2)
		position +=1
		print("asjhg",index1,len(vlan_ip_find))
		if index1 == len(vlan_ip_find)-1:
			position = index_value+2
		print("position vlan_ip_find",position,index_value)
	for index1,vlan_id in enumerate(vlan_id_find):
		worksheet.write(position, 2, vlan_id, style2)
		position +=1
		if index1 == len(vlan_id_find) - 1:
			position = index_value+2
		print("position vlan_id_find", position)
	worksheet.write(position, 4, hostname_find, style2)
	#
	for index1,pid in enumerate(pid_find):
		worksheet.write(position, 5, pid, style2)
	 	position += 1
		if index1 == len(pid_find) - 1:
			position = index_value + 2
	for index1,sn in enumerate(sn_find):
		worksheet.write(position, 7,sn, style2)
		position += 1
		if index1 == len(sn_find) - 1:
			position = index_value + 2
	#worksheet.write(position, 8, used_interface, style2)
	
	for index1,interface in enumerate(cdp_interfaces) :
		worksheet.write(position, 8, interface, style2)
		position += 1
		if index1 == len(cdp_interfaces) - 1:
			position = index_value + 2
	for index1,device_id in enumerate(cdp_device_id):
		worksheet.write(position, 9, device_id, style2)
		position += 1
		if index1 == len(cdp_device_id) - 1:
			position = index_value + 2
	worksheet.write(position, 10, 'Circuit Detail', style2)
	for index1,ip_add in enumerate(cdp_ip_address):
		worksheet.write(position, 11, ip_add, style2)
		position += 1
		if index1 == len(cdp_ip_address) - 1:
			position = index_value + 2
	
	
	
	#worksheet.write(position, 13, cdp_ip_address, style2)
	workbook.save(new_folder_name + '/' + output_file_name)
	
	
################ Story begins here ####################################################
################################## Write excel #######################################
new_folder_name = "/var/www/html/test_tart/invetory/uploads/"+username
if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
        fp = os.path.join(new_folder_name) +"/log.txt"
        with open(fp, "a") as file:
                file.write("\n")
                file.close()

move_input_file = "cd /var/www/html/test_tart/invetory/uploads; mv " + filee + " " + new_folder_name + "/"
#print("ads", move_input_file)
os.system(move_input_file)
# zip = "cd  "
# new_folder_name

#print('var/www/html/test_tart/inventory/' + filee)
file_path = os.path.join(new_folder_name + '/', filee)
#print("file path", file_path)
################################## Read excel #################################
book = xlrd.open_workbook(file_path, "r")
first_sheet = book.sheet_by_index(0)
row_count = first_sheet.nrows
#print(first_sheet)
################################## Write excel #################################

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Result', cell_overwrite_ok=True)

style0 = xlwt.easyxf('alignment: horiz left; font: bold on , height 320 , color blue;  borders: left medium, top medium, bottom medium; ')# for Dealership name
style1 = xlwt.easyxf('pattern: pattern solid, fore_colour light_green; alignment: horiz centre; font: bold on , height 220')# for header
style2 = xlwt.easyxf('alignment: horiz centre; font: height 220 ')# for router output entries

# book = with open(file_path,"rb") as xlsfile


for j in range(1, row_count):
	#print(j)
	
	list_host = first_sheet.row_values(j)
	for index, value in enumerate(list_host):
		if index == 0:
			host_ip = value
			worksheet.write(j, 15, host_ip, style2)
			
			
			login_hosts.append(host_ip)
			#print(host_ip)
		# elif index == 1:
		# 	print(output_file_name)
		# 	if not output_file_name:
		# 		output_file_name = value + '.xls'
		# 		workbook.save(new_folder_name + '/' + output_file_name)
		# 	# 	worksheet.write(j, 16, core_router_name, style2)
		# 	# 	workbook.save(new_folder_name + '/Result.xls')
		# elif index == 2:
		# 	if not vrf_name:
		# 		vrf_name = value
				#print(value)
#print(login_hosts, output_file_name,vrf_name)



#print(worksheet)


#***************** creating header **************************
worksheet.write_merge(0, 0, 0, 3, 'License Validation',style0)

worksheet.write(1, 0, 'IP Address',style1)
worksheet.write(1, 1, 'Latest Licence File Name',style1)
worksheet.write(1, 2, 'Licence File Copied Date',style1)
worksheet.write(1, 3, 'appxk9',style1)
worksheet.write(1, 4, 'uck9',style1)
worksheet.write(1, 5, 'securityk9',style1)
worksheet.write(1, 6, 'ipbase',style1)
worksheet.write(1, 7, 'Throughput',style1)
worksheet.write(1, 8, 'Serial No',style1)
worksheet.write(1, 9, 'Processor Serial No',style1)
worksheet.write(1, 10, 'Device Type',style1)
worksheet.write(1, 11, 'Tunnel Available?',style1)
# worksheet.write(1, 12, '',style1)
worksheet.write(1, 13, 'Telnet Enabled?',style1)
worksheet.write(1, 14, 'Authentication',style1)
worksheet.write(1, 15, '',style1)
worksheet.write(1, 16, '',style1)
worksheet.write(1, 17, '',style1)
worksheet.write(1, 18, '',style1)

workbook.save(new_folder_name+'/'+output_file_name)





for index,login_ip in enumerate(login_hosts):
	print("k",index)
	
	position = index+2
	if index == 0:
		primary_login_ip = login_ip.strip()
	
	#print(login_ip,type(login_ip),len(login_ip))
	login_ip_i = login_ip[:-2]
	#print("login_ip_i",login_ip_i)
	if bool(re.search(login_ip[:-2],login_hosts[0] )) is True:
		login_status = "Global"
	else:
		login_status = "Global"
	#print("login_status",login_status)
	incrementor_support = 0
	if isUp(login_ip.strip()) == True:
		try:
			if login_status == "Local":
				print("primary_login_ip",primary_login_ip)
				tel = telnetlib.Telnet(primary_login_ip)
				worksheet.write(position, 13, 'Enabled', style2)
				workbook.save(new_folder_name + '/' + output_file_name)
			elif login_status == "Global":
				tel = telnetlib.Telnet(login_ip.strip())
				worksheet.write(position, 13, 'Enabled', style2)
				workbook.save(new_folder_name + '/' + output_file_name)
		except:
			worksheet.write(position, 13, 'Not Enabled', style1)
			workbook.save(new_folder_name + '/' + output_file_name)
			#print("please enable telnet")
			continue

		# print(ip)
		
		if auto_router_login() == True:
			worksheet.write(position, 14, 'success', style2)
			workbook.save(new_folder_name + '/' + output_file_name)
			fp = os.path.join(new_folder_name) + "/log.txt"
			with open(fp, "a") as file:
				file.write("\n")
				file.close()
			
			#print("Authendication success 457")
		else:
			worksheet.write(position, 14, 'failed', style1)
			workbook.save(new_folder_name + '/' + output_file_name)
			fp = os.path.join(new_folder_name) + "/log.txt"
			with open(fp, "a") as file:
				file.write("Authendication failed on " + host_ip + " \n")
				file.close()
			#print("Authendication failed 465")

	
	
	# worksheet.write(j, 1, 'Enabled',style2)
	# workbook.save(new_folder_name+'/Result.xls')
	# except:
	# 	worksheet.write(j, 1, 'Not Enabled',style1)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	print("please enable telnet")
	# 	continue
		
		#print(ip)
	# status = "validation"
	# if auto_router_login() == True:
	# 	fp = os.path.join(new_folder_name) +"/log.txt"
	# 	with open(fp, "a") as file:
	# 		file.write("\n")
	# 		file.close()
	# 	worksheet.write(j, 3, 'success',style2)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	print ("Authendication success")
	# else:
	# 	worksheet.write(j, 3, 'failed',style1)
	# 	workbook.save(new_folder_name+'/Result.xls')
	# 	fp = os.path.join(new_folder_name) +"/log.txt"
	# 	with open(fp, "a") as file:
	# 		file.write("Authendication failed on "+host_ip+" \n")
	# 		file.close()
	# 	print ("Authendication failed")

workbook.save(new_folder_name+'/'+output_file_name)
file_save_path = new_folder_name+'/'+output_file_name+'x'

#dir = "Result"
download_path = new_folder_name.replace("uploads","logs")
dir = new_folder_name.replace("/var/www/html/test_tart/invetory/uploads/","")
dir_name = dir+"/"
zip = "cd /var/www/html/test_tart/invetory/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/test_tart/invetory/logs/ > /dev/null" %(dir,dir_name,dir)
os.system(zip)
#dir_name = '/var/www/html/test_tart/failovertests'
#zip = "cd /var/www/html/test_tart/failovertests/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/failovertests/logs/ 2> /dev/null" %(dir,dir_name,dir)
#os.system(zip)
#print("File saved path : ",file_save_path)

print("File saved path : ",download_path+".tar.gz")



