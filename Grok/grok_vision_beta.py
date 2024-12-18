import requests
import json
import base64
from urllib.parse import urlparse
from pathlib import Path

API_KEY = "xai-5hcRxgPhPRasXDiDAsVZEYbaS5nlZddRVcImSjGkTrdLpkpbiLIuRywoxn6QSBMM6Jz78KejeBLKlkzI"
BASE_URL = "https://api.x.ai/v1/chat/completions"

def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def is_valid_url(url):
    """Check if string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def ask_question(input_text, image_path=None):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant that can understand both text and images."}
    ]

    # Handle image input if provided
    if image_path:
        if is_valid_url(image_path):
            # If image_path is a URL
            image_message = {
                "type": "image_url",
                "image_url": {"url": image_path}
            }
        else:
            # If image_path is a local file
            try:
                base64_image = encode_image(image_path)
                image_message = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            except Exception as e:
                print(f"Error processing image: {e}")
                return None

        messages.append({
            "role": "user",
            "content": [
                image_message,
                {"type": "text", "text": input_text}
            ]
        })
    else:
        # Text-only message
        messages.append({"role": "user", "content": input_text})

    payload = {
        "model": "grok-vision-beta",
        "messages": messages,
        "stream": False,
        "temperature": 0.7
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        return None

if __name__ == "__main__":
    print("Ask me anything! You can also analyze images.")
    print("To analyze an image, use the format: 'IMAGE:path_to_image Question about the image'")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Check if input contains image path
        if user_input.startswith("IMAGE:"):
            parts = user_input.split(" ", 1)
            if len(parts) < 2:
                print("Please provide both an image path and a question.")
                continue
            
            image_path = parts[0].replace("IMAGE:", "").strip()
            question = parts[1].strip()
            result = ask_question(question, image_path)
        else:
            result = ask_question(user_input)

        if result and 'choices' in result:
            answer = result['choices'][0]['message']['content']
            print(f"Grok's Answer: {answer}")
        else:
            print("Failed to get a valid response.")
