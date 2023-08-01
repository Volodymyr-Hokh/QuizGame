import requests


def translate_question(text):
    json_data = {
        'params': {
            'texts': [
                {
                    'text': text,
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
            'timestamp': 1690879803854,
        },
        'id': 952322565,
        'jsonrpc': '2.0',
        'method': 'LMT_handle_texts',
    }

    response = requests.post('https://www2.deepl.com/jsonrpc', json=json_data)
    return response.json()["result"]["texts"][0]["text"]


print(translate_question("Hello"))