import openai
from constants import OPENAI_AUDIO_MODEL
from config import OPENAI_API_KEY
from utils import clean_json

class OpenAIHandler:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        openai.api_key = self.api_key

    def post_chat(self, model, messages, functions_list=None):
        response = openai.ChatCompletion.create(model=model, messages=messages, functions=functions_list)
        #response_data = response.json()
        response_data = response

        return_data = {}
        errors = []

        if 'error' in response_data:
            errors.append(f"API Error: {response_data['error']['message']}")
        elif 'choices' in response_data and len(response_data['choices']) > 0:
            choice = response_data['choices'][0]
            return_data['message'] = choice['message']

            finish_reason = choice.get('finish_reason', '')
            if finish_reason == 'length':
                errors.append('The model output reached the maximum length')
            elif finish_reason == 'content_filter':
                errors.append('The model output was flagged by the content filter')
            elif finish_reason not in ['stop', 'function_call']:
                errors.append(f"Unknown finish reason: {finish_reason}")
        else:
            errors.append('No answer from model in API response')

        if 'function_call' in return_data.get('message', {}) and 'arguments' in return_data['message']['function_call']:
            return_data['message']['function_call']['arguments'] = clean_json(return_data['message']['function_call']['arguments'])

        usage = {}
        if 'usage' in response_data:
            usage['prompt_tokens'] = response_data['usage']['prompt_tokens']
            usage['completion_tokens'] = response_data['usage']['completion_tokens']
            usage['total_tokens'] = response_data['usage']['total_tokens']
            #prices = estimate_price("MODEL_NAME_HERE", usage['prompt_tokens'], usage['completion_tokens']) # Replace "MODEL_NAME_HERE" with the appropriate model name

            return_data['usage'] = usage
            #return_data['cost'] = prices

        if len(errors) > 0:
            return_data['errors'] = errors

        #return_data['full_response'] = response_data
        return return_data
    
    def post_audio(self, model, file_path, response_format=None):
        openai.api_key = self.api_key
        audiofile = open(file_path, "rb")
        transcript = openai.Audio.transcribe(model, audiofile, response_format)
        print(transcript)
        return transcript['text']