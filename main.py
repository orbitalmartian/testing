import random
import textwrap
import os
import requests
import time
import gc
from PIL import Image, ImageDraw, ImageFont

# Enable the garbage collector
gc.enable()

# Set your Instagram username and password
INSTAGRAM_USERNAME = "your_username"
INSTAGRAM_PASSWORD = "your_password"

# Set the text you want to display on the image
text = "Hello, World!"

# Set the font and size
font = ImageFont.truetype("arial.ttf", 36)

# Set the maximum width and height of the image
max_width, max_height = 800, 800

# Split the text into lines that fit within the max width
lines = textwrap.wrap(text, width=max_width)

# Determine the width and height of the final image
width = max(max_width, font.getsize(text)[0])
height = max(max_height, len(lines) * font.getsize(text)[1])

# Create a blank image with the given width and height
image = Image.new("RGB", (width, height), (255, 255, 255))

# Get a drawing context
draw = ImageDraw.Draw(image)

# Draw the text on the image
y_text = 0
for line in lines:
    draw.text((0, y_text), line, font=font, fill=(0, 0, 0))
    y_text += font.getsize(line)[1]

# Save the image to a temporary file
image.save("temp.jpg")

# Log in to Instagram
print("Logging in to Instagram...")
session = requests.Session()
login_url = "https://www.instagram.com/accounts/login/ajax/"
session.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}
session.headers.update({"Referer": "https://www.instagram.com/"})
login_data = {
    "username": INSTAGRAM_USERNAME,
    "password": INSTAGRAM_PASSWORD,
}
session.post(login_url, data=login_data)

# Check if login was successful
login_response = session.get("https://www.instagram.com/").json()
if login_response["authenticated"]:
    print("Login successful!")
else:
    print("Login failed!")

# Post the image to Instagram
with open("temp.jpg", "rb") as image_file:
    image_data = image_file.read()
    upload_url = "https://www.instagram.com/create/upload/photo/"
    session.headers.update({"Content-type": "application/octet-stream"})
    session.headers.update({"X-IG-Capabilities": "3Q4="})
    session.headers.update({"X-IG-App-ID": "124024574287414"})
    upload_data = {
        "upload_id": str(int(time.time() * 1000)),
        "image_compression": '{"lib_name":"jt","lib_version":"1.3.0","quality":"80"}',
    }
    response = session.post(upload_url, data=upload_data, files={"photo": image_data})
    media_id = response.json()["media_id"]

# Set the caption for the post
caption = "This is a random image with random text on it."

# Configure the post
configure_url = f"https://www.instagram.com/create/configure/{media_id}/"
configure_data = {
    "caption": caption,
    "usertags": '{"in":[]}',
    "custom_accessibility_caption": "",
    "location": "",
    "retry_timeout": 10,
}
session.headers.update({"Content-type": "application/x-www-form-urlencoded"})
session.post(configure_url, data=configure_data)

# Clean up
os.remove("temp.jpg")

print("Image posted to Instagram!")
