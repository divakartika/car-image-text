import base64
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to encode the image
def encode_image(image_path):
    if type(image_path) == str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    else:
        return base64.b64encode(image_path.read()).decode("utf-8")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = uploaded_file
else:
    image = "example/1534.png"

col1, col2 = st.columns(2)
col1.image(image)

# Getting the Base64 string

base64_image = encode_image(image)


response = client.responses.create(
    model="gpt-5-mini",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "describe the car in the image, focusing the condition (closed/opened) of its hood, front doors, and rear doors." },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

col2.markdown(response.output_text)