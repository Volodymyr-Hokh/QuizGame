from datetime import datetime
import html
import requests

_id = 952322567

class Question:

    def __init__(self, q_text, q_answer):
        self.text = html.unescape(q_text)
        self.answer = q_answer == "True"

    def translate_question(self, q_text):
        global _id
        _id += 1

        json_data = {
            'params': {
                'texts': [
                    {
                        'text': q_text,
                        'requestAlternatives': 0,
                    },
                ],
                'splitting': 'newlines',
                'commonJobParams': {
                    'wasSpoken': False,
                },
                'lang': {
                    'target_lang': 'uk',
                    'source_lang_user_selected': 'en',
                },
                'timestamp': int(datetime.now().timestamp()*1000),
            },
            'id': _id,
            'jsonrpc': '2.0',
            'method': 'LMT_handle_texts',
        }
        

        response = requests.post('https://www2.deepl.com/jsonrpc', json=json_data)
        print(response.json())
        return response.json()["result"]["texts"][0]["text"]
