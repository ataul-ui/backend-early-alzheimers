from dotenv import load_dotenv
import os

load_dotenv()
something_1 = os.getenv("host")
something_2 = os.getenv("user")

print(something_1)
print(something_2)