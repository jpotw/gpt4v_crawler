from openai import OpenAI
import subprocess
import base64
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenAI()
model.timeout = 30

# input: image, output: Python String
def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()

# input: url(아래 파이썬 스크립트에 있음), output: b64 encoded Str of screenshot
def url2screenshot(url):
    print(f"Crawling {url}")

    if os.path.exists("screenshot.jpg"):
        os.remove("screenshot.jpg")

    result = subprocess.run(
        ["node", "screenshot.js", url],
        capture_output=True,
        text=True
    )
    exitcode = result.returncode
    output = result.stdout

    if not os.path.exists("screenshot.jpg"):
        print("ERROR")
        return "Failed to scrape the website"
    
    b64_image = image_b64("screenshot.jpg")
    return b64_image

# input: b64 encoded Str of screenshot, Str | output: return & print message_text
def visionExtract(b64_image, prompt):
    response = model.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You a web scraper, your job is to extract information based on a screenshot of a website & user's instruction. You MUST answer in Korean.",
            }
        ] + [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
            }
        ],
        max_tokens=1024,
    )

    message_text = response.choices[0].message.content

    if "ANSWER_NOT_FOUND" in message_text:
        print("ERROR: Answer not found")
        return "I was unable to find the answer on that website. Please pick another one"
    else:
        return message_text

def visionCrawl(url, prompt):
    b64_image = url2screenshot(url)

    print("Image captured")
    
    if b64_image == "Failed to scrape the website":
        return "크롤링에 실패했습니다. 다른 URL을 입력해주세요"
    else:
        return visionExtract(b64_image, prompt)

#87에 링크 수정하면 됨
response = visionCrawl("https://github.com/jpotw/jpotw", "Extract the information")
print(response)