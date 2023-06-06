import requests, csv, subprocess
import ipaddress

#source=Abuse CH
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text
rule="netsh advfirewall firewall delete rule name='BadIP'"
subprocess.Popen(['powershell.exe', "-Command", rule])
mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.splitlines()))

for row in mycsv:
    ip = row[1]
    try:
        ipaddress.IPv4Network(ip)

    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as e:
        valid = False
        msg = "Provided string is not a valid network: {}.".format(e)

    else:
        valid = True
        msg = "String is a network."
        if(ip)!=("dst_ip"):
            print("Added Rule to block:", ip)
            rule="netsh advfirewall firewall add rule name='BadIP' Dir=Out Action=Block RemoteIP="+ip
            subprocess.Popen(['powershell.exe', "-Command", rule])
            rule="netsh advfirewall firewall add rule name='BadIP' Dir=In Action=Block RemoteIP="+ip
            subprocess.Popen(['powershell.exe', "-Command", rule])
