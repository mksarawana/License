#!/usr/bin/python

from __future__ import unicode_literals
from __future__ import print_function
import telnetlib
import sys
import os
import platform
import datetime
import glob
import re
import paramiko
import getpass
import time
import ipaddress
import netaddr
from netaddr import *
import requests

users_list = []
default_router_password = ''
default_enable_password = ''
rvname = ""
# save_file_path = '/home/sarava/failover/'
temp_array = []
fstip = []
secip = []
temp_ip = []
primary_ip = []
secondary_ip = []
first_delay = []
second_delay = []
fstint = []
secint = []
fstvlanint = []
secvlanint = []
pri_chk = []
exit = []
server_ip = []
source_interface = []
success_server = []
actual_server = []
pre_result_chk = []
pre_test_resss = ""
acl_subnets = []
vlan_subnets = []
vlan_interfaces = []
extra_interface = []
lan_interfaces = []
primary_vlan_interfaces = []
secondary_vlan_interfaces = []
actual_result_chk = []
primary_interface = []
success_interfaces = []
failed_interfaces = []
eigrp_interfaces = []
vrf_names = ["CDK", "INTERNET", "Mgmt-intf", "ORD", "LAS"]
act_vrf_name = []
vrf_aware = []
fstvrfaware = []
secvrfaware = []
primary_vrf_aware = []
vrf_temp = []
vrf_name = ""

ip = sys.argv[1]
license_name = sys.argv[2]
filenam = sys.argv[3]
tool_folder_name = "invetory"

reachability_success = []
# print(filenam)
new_folder_name = "/var/www/html/test_tart/"+tool_folder_name+"/uploads/" + filenam
if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
# print("folder created")
save_file_path = new_folder_name + "/"
filename = new_folder_name.replace("/var/www/html/test_tart/"+tool_folder_name+"/uploads/", "")
fp = os.path.join(save_file_path) + "log.txt"
with open(fp, "a") as file:
        # file.write('Authentication success on: '+ip+'\n')
        file.close()


# print("log file created on ",fp)
# print("filename",filename)

#################################### timer funtionality ###############################

# clock()
##################### single site ######################
# *******************CPE - FUNCTION BLOCK TO CHECK BETWEEN 2 DIFFERENT LOGIN ACCOUNTS AND GIVE ENABLE ACCESS********************
def auto_router_login(status):
        tryy = 0
        for x in users_list:
                r1_bool = False
                time.sleep(1)
                tel_res = tel.read_until("sername: ".encode('ascii'), 2)  # Regular login attempt
                time.sleep(1)
                tel.write((x + '\r').encode('ascii'))
                tel.read_until('assword: '.encode('ascii'))
                tel.write((default_router_password + '\r' + '\n \n').encode('ascii'))
                tryy = tryy + 1
                login_status = tel.read_until(">".encode('ascii'), 2)
                if bool(re.search(">", login_status.decode("utf-8"))) is True:
                        r1_bool = True
                        enab(status)
                        break
                else:
                        print("username '" + x + "' did not work on: " + ip)
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("username " + x + " did not work \n")
                                file.close()
                        r1_bool = False
        return r1_bool


# ********************CPE - FUNCTION BLOCK TO MANUALLY ENTER THE CUSTOM CLIENT ROUTER CREDENTIALS********************
def manual_router_login(status):
        r2_bool = False
        #       print ("manual login")
        run_time_user_id = raw_input('Please provide the CUSTOM ROUTER USERNAME: ')
        run_time_password = raw_input('Please provide the CUSTOM ROUTER PASSWORD: ')
        # tel = telnetlib.Telnet(vlan75_ip)
        tel.read_until("sername: ".encode('ascii'))  # Regular login attempt
        tel.write((run_time_user_id + '\r').encode('ascii'))
        tel.read_until('assword: '.encode('ascii'))
        tel.write((run_time_password + '\r' + '\n \n').encode('ascii'))
        # time.sleep(1.2)
        login_state = tel.read_until(">".encode('ascii'), 2)
        #       print(login_state.decode("utf-8"))
        if bool(re.search(">", login_state.decode("utf-8"))) is True:
                print("Manual Login Successful. Need to try ENABLE LOGIN")
                r2_bool = True
                enab(status)
        
        else:
                print("Incorrect Credentials. MAXIMUM TRIES REACHED. Exiting in 3.......2.......1..\n")
                r2_bool = False
        # print "r2_bool value is: ", r2_bool
        return r2_bool


# ********************CPE - FUNCTION BLOCK FOR DEFAULT ENABLE PASSWORD AUTHENTICATION********************
def enab(status):
        enab_bool = False
        # print ("Trying Enable login now")
        tel.write("en\r".encode('ascii'))
        # print(tel.read_until('assword: '.encode('ascii'),2))
        tel.read_until('assword: '.encode('ascii'), 2)
        tel.write((default_enable_password + '\r').encode('ascii'))
        enab_status = tel.read_until("#".encode('ascii'), 2)
        if bool(re.search("#", enab_status.decode("utf-8"))) is True:
                print("Athentication success on: ", ip)
                
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write('Authentication success on: ' + ip + '\n')
                        file.close()
                enab_bool = True
                #		print("status",status)
                if status == "validation":
                        license_upgrade()
                elif status == "post_test":
                        post_test()
                else:
                        print("")
        else:
                print("ERROR IN ENABLE PASSWORD on: ", ip)
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write('ERROR IN ENABLE PASSWORD on: ' + ip + '\n')
                        file.close()
                exit.append("ENABLE CREDENTIALS DID NOT WORK on ip: " + ip)
                # print("exit enable",exit)
                enab_bool = False
        return enab_bool


# ********************CPE - FUNCTION BLOCK TO CHECK IF THE VLAN 75 IP IS RECHABLE FROM THE HOST SYSTEM********************
def isUp(hostname):
        response = ""
        #	print(hostname)
        if platform.system() == "Windows":
                #       print ("Pinging Windows")
                response = os.system("ping " + hostname + "> /dev/null")
                #               print ("\nPing from WINDOWS PC is successful. \nThe client " + hostname + " is LIVE!\n")
        else:
                #      print ("Pinging Linux")
                response = os.system("ping -c 1 " + hostname + " > /dev/null")
                print("up response",response)
                #             print ("\nPing from LINUX PC is successful. \nThe client " + hostname + " is LIVE!\n")
        isUpBool = ""
        if response == 0:
                print (hostname, 'is up!')
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write(hostname+ 'is up!\n')
                        file.close()
                isUpBool = True
        else:
                print(hostname, 'is down!')
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write(hostname+ 'is down!\n')
                        file.close()
        return isUpBool


# ********************************* Validation **************************************

def license_upgrade():
        
        license_bool = "False"
        
        
        tel.write(("ter len 0\r").encode('ascii'))
        tel.read_until("#".encode('ascii'))
        tel.write(("sh ver | i Configuration register\r").encode('ascii'))
        conf_reg_output = tel.read_until("#".encode('ascii'))
        
        tel.write(("sh run | i hostname \r").encode('ascii'))
        hostname_output = tel.read_until("#".encode('ascii'))

        hostname_extract = hostname_output.splitlines()[1:][:-1]
        hostname = str(hostname_extract).replace("hostname", "").replace("'","").replace("[","").replace("]","")+ "#"
        print("hostname", hostname,type(hostname),len(hostname))

        tel.write(("show lic udi \r").encode('ascii'))
        udi_output = tel.read_until(hostname.strip())
        
        tel.write(("sh ver \r").encode('ascii'))
        pre_version_output = tel.read_until("#".encode('ascii'))
        tel.write(("sh run \r").encode('ascii'))
        pre_runnig_config_output = tel.read_until("#".encode('ascii'))
        tel.write(("\r").encode('ascii'))
        print(tel.read_until("#".encode('ascii')))

        fp = os.path.join(save_file_path) + "Pre_backup"
        with open(fp, "a") as file:
                file.write(pre_version_output.decode('utf-8') + " \n")
                file.write(udi_output.decode('utf-8') + " \n")
                file.write(pre_runnig_config_output.decode('utf-8') + " \n")
                file.close()
        
        
       
        conf_reg_extract = conf_reg_output.splitlines()[1:][:-1]
        conf_reg_number = str(conf_reg_extract).replace("Configuration register is","").replace("'","").replace("[","").replace("]","")
        print("conf_reg_find",conf_reg_number)

        udi_name = ''
        #print("udi_output",udi_output.decode("utf-8"))
        udi_extract = udi_output.decode('utf-8').strip().splitlines()[3:][:-2]
        #print('udi_extract',udi_extract,type(udi_extract),len(udi_extract))
        for index,udi in enumerate(str(udi_extract).split()):
                print(index,udi)
                if index == 2:
                        udi_name = udi
        
        if udi_name and bool(re.search(udi_name,license_name)) is True:
                print("License name matches with UDI SN")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("License name matches with UDI SN "+udi_name+" \n")
                        file.close()
                license_bool = "True"
        else:
                print("UDI SN match not found ")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("License match not found with udi SN "+udi_name+" \n")
                        file.close()
        print("udi_name",udi_name)
        
        if license_bool == "True":
                print("upgrading license")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("License name matches with UDI SN " + udi_name + " \n")
                        file.close()
                tel.write(("copy http://adpnis:ftps3rv3r@50.249.117.18/ISR4kLIC/"+license_name+" flash\r").encode('ascii'))
                tel.read_until("?".encode('ascii'),2)
                tel.write(("\r").encode('ascii'))
                warning_validator = tel.read_until("#".encode('ascii'),2)
                print(warning_validator)
               
                if bool(re.search("%Warning",warning_validator.decode("utf-8"),re.I)) is True:
                        print("license Already copied")
                        tel.write(("n").encode('ascii'))
                        licence_copy_output = tel.read_until("#".encode('ascii'))
                        print(licence_copy_output)
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("license file Already copied \n")
                                file.write(licence_copy_output.decode("utf-8") + "\n")
                                file.close()
                        fp = os.path.join(save_file_path) + "install.txt"
                        with open(fp, "a") as file:
                                file.write(licence_copy_output.decode("utf-8") + "\n")
                                file.close()
                else:
                        print("license copied")
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("license copied \n")
                                file.write(warning_validator.decode("utf-8")+"\n")
                                file.close()
                        fp = os.path.join(save_file_path) + "install.txt"
                        with open(fp, "a") as file:
                                file.write(warning_validator.decode("utf-8") + "\n")
                                file.close()
                
                
                tel.write(("dir\r").encode('ascii'))
                dir_output = tel.read_until("#".encode('ascii'))
                fp = os.path.join(save_file_path) + "install.txt"
                with open(fp, "a") as file:
                        file.write(dir_output.decode("utf-8") + "\n")
                        file.close()
                if bool(re.search(license_name,dir_output.decode("utf-8"))) is True:
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("license file available at flash \n")
                                file.close()
                        print("license file available at flash")
                        tel.write(("license install flash:"+license_name+"\r").encode('ascii'))
                        license_install_output = tel.read_until("#".encode('ascii'))
                        print(license_install_output)
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("license has been upgraded \n")
                                file.write(license_install_output.decode("utf-8")+"\n")
                                file.close()
                        fp = os.path.join(save_file_path) + "install.txt"
                        with open(fp, "a") as file:
                                file.write(license_install_output.decode("utf-8") + "\n")
                                file.close()
                        print("license has been upgraded")
                else:
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("Error with copy the file. \n")
                                file.write("File not available at flash \n")
                                file.close()
                        print("File not available at flash")
                        
                
                
        else:
                print("please enter the correct license value and try again")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("License name matches with UDI SN " + udi_name + " \n")
                        file.close()
        
        
        if bool(re.search("0x2102",conf_reg_output.decode("utf-8"))) is True:
                print("configured configuration reg no is: ",conf_reg_number)
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("configuration register number is  " + conf_reg_number + " \n")
                        file.close()
              
                tel.write(("wr \r").encode('ascii'))
                tel.read_until("#".encode('ascii'))
                tel.write(("sh ver \r").encode('ascii'))
                post_version_output = tel.read_until("#".encode('ascii'))
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("reloading the router \n")
                        file.close()
                # tel.write(("reload \r").encode('ascii'))
                # tel.read_until(" [confirm]".encode('ascii'))
                # tel.write(("\r").encode('ascii'))
                # tel.read_until("#".encode('ascii'),2)
                
        else:
                print("configured configuration reg no is: ", conf_reg_number)
                print("correcting the configuration")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("configured configuration reg no is:" + conf_reg_number + " \n")
                        file.write("correcting the configuration register number.... \n")
                        file.close()
                # tel.write(("no config-register " +conf_reg_number+"\r").encode('ascii'))
                # tel.read_until("#".encode('ascii'))
                # tel.write(("config-register 0x2102 \r").encode('ascii'))
                # tel.read_until("#".encode('ascii'))
                # tel.write(("end \r").encode('ascii'))
                # tel.read_until("#".encode('ascii'))
                # tel.write(("wr \r").encode('ascii'))
                # tel.read_until("#".encode('ascii'))
                tel.write(("sh ver \r").encode('ascii'))
                post_version_output = tel.read_until("#".encode('ascii'))
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("reloading the router \n")
                        file.close()
                # tel.write(("reload \r").encode('ascii'))
                # tel.read_until(" [confirm]".encode('ascii'))
                # tel.write(("\r").encode('ascii'))

        #response = os.system("ping -c 1 " + ip + " > /dev/null")
        primry_connection_reachability = "False"
        print("Wait till the router come up")
        count = 0
        while (count < 10 and primry_connection_reachability == "True"):
        
                response = os.system("ping -c 1 " + ip + " > /dev/null")
        
                if response == 0:
                        print("is ONLINE")
                        
                        primry_connection_reachability = "True"
                        reachability_success.append("True")
                        
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write(ip + " is ONLINE \n")
                                file.write(" Time expired: " + str(count) + " Seconds")
                                file.close()
                        break
                else:
                        print("is Offline")
                        
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write(ip + " is Offline \n")
                                file.write(" Time expired: " + str(count) + " seconds")
                                file.close()
        
                time.sleep(10)
                count = count + 10
                print("Time expired: ", str(count) + " seconds")

        print("license_name",license_name)
        print("filenam",filenam)

####################### Execution begins here ####################################

def post_test():
        tel.write(("sh run | i hostname \r").encode('ascii'))
        hostname_output = tel.read_until("#".encode('ascii'))
        tel.write(("sh ver \r").encode('ascii'))
        post_reload_ver = tel.read_until("#".encode('ascii'))
        tel.write(("sh run \r").encode('ascii'))
        post_reload_run = tel.read_until("#".encode('ascii'))

        hostname_extract = hostname_output.splitlines()[1:][:-1]
        hostname = str(hostname_extract).replace("hostname", "").replace("'", "").replace("[", "").replace("]","") + "#"
        print("hostname", hostname, type(hostname), len(hostname))
        
        fp = os.path.join(save_file_path) + hostname.replace("#","")
        with open(fp, "a") as file:
                file.write(post_reload_ver + "\n")
                file.write(post_reload_run + "\n")
                file.close()
        

# time.sleep(30)

if isUp(ip) == True:
        tel = telnetlib.Telnet(ip)
        status = "validation"
        if auto_router_login(status) == True:
                print("")
        else:
                exit.append("authentication issue on " + ip)
                #fp = '/var/www/html/failovertests/unauthentic.txt'
                #with open(fp, "a") as file:
                #        file.write('\n' + str(ip))
                #        file.close()
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write("authentication issue on " + ip + "\n")
                        file.close()
                
                # tel = telnetlib.Telnet(ip)
                # manual_router_login(status)
else:
        print("ip is not reachable")
        fp = os.path.join(save_file_path) + "log.txt"
        with open(fp, "a") as file:
                file.write(ip, ' is down!' + '\n')
                file.close()
        exit.append(ip, ' is down!' + '\n')
# print("exit",exit,len(exit))

if bool(re.search("True",str(reachability_success))) is True:
        if isUp(ip) == True:
                tel = telnetlib.Telnet(ip)
                status = "post_test"
                if auto_router_login(status) == True:
                        print("")
                else:
                        exit.append("authentication issue on " + ip)
                        # fp = '/var/www/html/failovertests/unauthentic.txt'
                        # with open(fp, "a") as file:
                        #        file.write('\n' + str(ip))
                        #        file.close()
                        fp = os.path.join(save_file_path) + "log.txt"
                        with open(fp, "a") as file:
                                file.write("authentication issue on " + ip + "\n")
                                file.close()
                                
                                # tel = telnetlib.Telnet(ip)
                                # manual_router_login(status)
        else:
                print("ip is not reachable")
                fp = os.path.join(save_file_path) + "log.txt"
                with open(fp, "a") as file:
                        file.write(ip, ' is down!' + '\n')
                        file.close()
                exit.append(ip, ' is down!' + '\n')

# zip = "cd /var/www/html/failovertests/uploads/; ""tar -zcvf "+new_folder_name+".tar.gz " +new_folder_name+"/"+";"+" mv "+new_folder_name+".tar.gz /var/www/html/failovertests/logs/"" 2> /dev/null"
# os.system(zip)
dir = new_folder_name.replace("/var/www/html/test_tart/"+tool_folder_name+"/uploads/", "")
dir_name = dir + "/"
zip = "cd /var/www/html/test_tart/%s/uploads/; tar -zcvf %s.tar.gz %s; cp %s.tar.gz /var/www/html/test_tart/%s/logs/ 2> /dev/null" % (tool_folder_name,dir, dir_name, dir,tool_folder_name)
os.system(zip)
save_path = "/var/www/html/test_tart/"+tool_folder_name+"/logs/"
print("File saved path : ", save_path, filename + ".tar.gz")
