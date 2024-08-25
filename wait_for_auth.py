import time
import requests


def wait_for_fastapi():
    while True:
        try:
            response = requests.get("http://auth:8001/healthz/ready")
            if response.status_code == 200:
                print("FastAPI app is ready")
                break
        except requests.exceptions.RequestException:
            print("Waiting for FastAPI app to be ready...")
            time.sleep(1)


if __name__ == "__main__":
    wait_for_fastapi()
