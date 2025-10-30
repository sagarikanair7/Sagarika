import openai
import base64
import sys
import requests
from PIL import Image

def main():
    s = input("Enter file name or URL: \n")
    check(s)
    image_data = encode(s)
    display(image_data)
def check(s):
    if "http" in s:
        try:
            r = requests.get(s)
            if "image" not in r.headers.get('Content-Type', ''):
                sys.exit("Invalid URL: Not an image")
            else:
                return True
        except requests.exceptions.RequestException:
            sys.exit("Invalid URL")
    else:
        try:
            with Image.open(s) as img:
                img.verify()
                return True
        except IOError:
            sys.exit("Invalid input: Not an image file")

def encode(s):
    if "http" in s:
        response = requests.get(s)
        return base64.b64encode(response.content).decode('utf-8')
    else:
        with open(s, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
def display(image):
    while True:
        ans=input("enter l for long description and s for short description\n")
        if ans.casefold() not in("s", "l"):
            print("invalid input")
            continue
        else:
            break
    if ans =="s":
        pr="describe the image at a glance"
    else:
        pr="describe the image in great detail"
    print(describe(image, pr))
    while True:
        answer=input("any follow up questions?, press y for yes and n for no")
        if answer.casefold() not in("y", "n"):
            print("invalid input")
            continue
        if answer.casefold()=="y":
            q=input("enter question\n")
            print(describe(image, q))
            continue
        else:
            break
def describe(image, pr):
    openai.api_key = ""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",                
                    "content": [
                    {"type": "text", "text": pr},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
    
if __name__ == "__main__":
    main()
