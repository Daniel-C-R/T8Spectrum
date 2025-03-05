import os

from dotenv import load_dotenv

load_dotenv()

T8_USER = os.getenv("T8_USER")
T8_PASSWORD = os.getenv("T8_PASSWORD")

if __name__ == "__main__":
    print(T8_USER, T8_PASSWORD)