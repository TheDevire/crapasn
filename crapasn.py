#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
from  termcolor import colored
from pyfiglet import Figlet
import sys


# if you want to change the headers go ahead who's stopping you
headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6",
    }

f = Figlet(font="smshadow")
print(colored(f.renderText('ASN-SCRAPPER'),'green'))
print(f"\t\t\t{colored('Created by Devire','red',attrs=['bold'])}")
print('\n')



asn_only = '-asn'
cidr = '-cidr'


def usage():
   return """    Usage: crapasn [flag]
        
    Flags:
        -asn: To print only asn numbers of the organization
        -cidr: To print only cidr notations organization
         
        P.S: you can use both flags to print both output
        """
   
if (len(sys.argv) == 1 ) or ((asn_only not in sys.argv) and (cidr not in sys.argv)):
     usage = usage()
     print(usage)
else:
    query = str(input('Enter the Organization name: '))
    parsed_query = query.replace(" ", "+")
    url = f'https://bgp.he.net/search?search%5Bsearch%5D={parsed_query}&commit=Search'
    def requesting():
        print(f'You searched for: {parsed_query}')
        r = requests.get(url, headers=headers)
        response = r.content
        soup = BeautifulSoup(response,'lxml')
        new = soup.select("tbody > tr")
        return new
        

    data = requesting()

    def results(data):
        print("\n")
        print(f"        {colored('ASN Numbers & IP ROUTES', 'green',attrs=['bold'])}         {colored('OWNED BY','green',attrs=['bold'])}           ")
        print("\n")
        data_result = []
        if len(data) != 0:
            for result in data:
                total_len = 25
                result_list = list(result)
                asn = result_list[1].text.replace("AS","")
                asn_length = len(asn)
                owner = result_list[4].text.upper()
                upper = 0
                if query.upper() in owner:
                    upper += 1
                if (asn_length != 0) and (query.upper() in owner):
                    calc = total_len - asn_length
                    asn += calc * " "
                    data_result.append([asn,owner])
                

        elif len(data) == 0:
            print("\t \t\t No Result Found!!!")


        if ((asn_only in sys.argv) and (cidr in sys.argv)) or ((asn_only not in sys.argv) and (cidr not in sys.argv)):
            if len(data_result) > 50:
                getting_in = str(input("There are more than 50 results do you want to print them all,if no all the output will be added to asn-output file [y/n]: "))
                if getting_in == 'y':
                    for i in data_result:
                        asn = i[0]
                        owner = i[1]       
                        print(f"\t{asn}|\t{owner}  ")
                
                else:
                    print("Adding them to asn-output file")
                    for i in data_result:
                        with open("crapasn-output",'w')as output:      
                            output.write(f"\t{i[0]}|\t{i[1]}\n")
            elif len(data_result) < 50:
                for i in data_result:
                    asn = i[0]
                    owner = i[1]       
                    print(f"\t{asn}|\t{owner}  ")
        elif asn_only in sys.argv:
            asn_list = []
            for result in data_result:
                stripped = result[0].strip()
                if len(stripped) < 8:
                    asn_list.append([result[0],result[1]])
            if len(asn_list) > 50:
                getting_in = str(input("There are more than 50 results do you want to print them all,if no all the output will be added to crapasn-output file [y/n]: "))
                if getting_in == 'y':
                    for i in asn_list:
                        asn = i[0]
                        owner = i[1]       
                        print(f"\t{asn}|\t{owner}  ")
                
                else:
                    print("Adding them to crapasn-output file")
                    for i in data_result:
                        with open("crapasn-output",'w')as output:      
                            output.write(f"\t{i[0]}|\t{i[1]}\n")
            elif len(asn_list) < 50:
                for i in asn_list:
                    asn = i[0]
                    owner = i[1]       
                    print(f"\t{asn}|\t{owner}  ")
        elif cidr in sys.argv:
            asn_list = []
            for result in data_result:
                stripped = result[0].strip()
                if len(stripped) >= 8:
                    asn_list.append([result[0],result[1]])
            if len(asn_list) > 50:
                getting_in = str(input("There are more than 50 results do you want to print them all,if no all the output will be added to crapasn-output file [y/n]: "))
                if getting_in == 'y':
                    for i in asn_list:
                        asn = i[0]
                        owner = i[1]       
                        print(f"\t{asn}|\t{owner}  ")
                
                else:
                    print("Adding them to crapasn-output file")
                    for i in data_result:
                        with open("crapasn-output",'w')as output:      
                            output.write(f"\t{i[0]}|\t{i[1]}\n")
            elif len(asn_list) < 50:
                for i in asn_list:
                    asn = i[0]
                    owner = i[1]       
                    print(f"\t{asn}|\t{owner}  ")
            

    results(data)
