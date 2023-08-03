import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():  # Check for empty input
        return None

    URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    response = requests.post(URL, json=input_json, headers=headers)
    formatted_response = json.loads(response.text)
    
    if response.status_code == 200:
        status_code = response.status_code
    else:
        status_code = 400

    if status_code == 400:
        formatted_output = { 'anger': None,
                             'disgust': None,
                             'fear': None,
                             'joy': None,
                             'sadness': None,
                             'dominant_emotion': None }
    else:
        response_dict = json.loads(response.text)
        emotions = response_dict['emotionPredictions'][0]['emotion']
        dominant_emotion = ''
        for emotion, score in emotions.items():
            if dominant_emotion == '' or score > emotions[dominant_emotion]:
                dominant_emotion = emotion
        emotions['dominant_emotion'] = dominant_emotion
        return emotions
