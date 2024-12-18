import requests
import json

API_KEY = "xai-5hcRxgPhPRasXDiDAsVZEYbaS5nlZddRVcImSjGkTrdLpkpbiLIuRywoxn6QSBMM6Jz78KejeBLKlkzI"
BASE_URL = "https://api.x.ai/v1/chat/completions"

def ask_question(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-beta",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant with access to real-time information."},
            {"role": "user", "content": question}
        ],
        "stream": False,
        "temperature": 0.7
    }

    try:
        print("\nSending request to Grok API...")
        print(f"Model requested: {payload['model']}")
        
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload))
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"Error Response: {response.text}")
            return None
            
        response_data = response.json()
        
        # Check which model was actually used
        if 'model' in response_data:
            print(f"Model used: {response_data['model']}")
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        print(f"\nAPI Error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Status Code: {e.response.status_code}")
            print(f"Error Details: {e.response.text}")
        return None
    except json.JSONDecodeError as e:
        print(f"\nJSON Decode Error: {str(e)}")
        print(f"Raw Response: {response.text}")
        return None

def format_response(response_text):
    """Format the response for better readability"""
    return response_text.strip()

if __name__ == "__main__":
    print("Welcome to Grok-2! Ask me anything (type 'exit' to quit)")
    print("---------------------------------------------------")

    conversation_history = []
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("\nGoodbye! Thanks for chatting!")
            break

        result = ask_question(user_input)
        if result and 'choices' in result:
            answer = result['choices'][0]['message']['content']
            formatted_answer = format_response(answer)
            print(f"\nGrok-2: {formatted_answer}")
            
            # Store conversation history
            conversation_history.append({"user": user_input, "assistant": formatted_answer})
        else:
            print("\nFailed to get a valid response. Please try again.")