import os
import json

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def describe_image(image_path):

    image = Image.open(image_path)

    prompt = """
Analyze this image.

Return ONLY valid JSON in this exact format:

{
    "description":"...",
    "objects":["..."],
    "tags":["..."]
}

Do not write markdown.
Do not use ```json.
Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return json.loads(response.text)