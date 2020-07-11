import json
import requests
from flask_babel import _
from app import current_app


def translate(text, original_language, target_language):
    if not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
            'Ocp-Apim-Subscription-Region': 'westeurope'}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, original_language, target_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    try:
        return json.loads(r.content.decode('utf-8-sig'))
    except:
        return _('Not a valid language!')
