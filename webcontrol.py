from datetime import datetime
import schedule
import time

end_time = datetime(2025, 5, 30, 20)

sites_to_block = ['youtube.com', 'www.youtube.com']

hosts_path = "/etc/hosts"
#hosts_path_win = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"

loop = True

def block_sites():
    if(datetime.now() < end_time):
        print("Bloqueado")
        with open(hosts_path, 'r+') as hostsfile:
            hosts_content = hostsfile.read()
            for site in sites_to_block:
                if any(site in line and redirect in line for line in hosts_content.splitlines()):
                    continue
                else:
                    hostsfile.write(redirect + " " + site + "\n")
    else:
        print("Desbloqueado")
        with open(hosts_path, 'r+') as hostsfile:
            lines = hostsfile.readlines()
            hostsfile.seek(0)
            for line in lines:
                if not any(site in line for site in sites_to_block):
                    hostsfile.write(line)
            hostsfile.truncate()
        global loop 
        loop = False
        schedule.cancel_job(job)
   

job = schedule.every(10).minutes.do(block_sites)
block_sites()

while loop:
    schedule.run_pending()
    print(loop)
    time.sleep(1)
              