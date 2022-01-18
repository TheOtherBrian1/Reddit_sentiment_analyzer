import requests
import json
import time
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



def count_comments(user_name, time_frame_in_weeks):
    base_url = f'https://api.pushshift.io/reddit/search/comment/?author={user_name}'
    comment_count = 0
    data = None
    con = 1
    collect_text = ''
    for week in range(1,time_frame_in_weeks+1):
        request_url = base_url + f'&size=500&after={7*week}d&before={7*week - 7}d'
        response = requests.get(request_url)
        data = response.json()['data']
        
        for comment in data:
            print(f'{con}\n\n', comment['body'])
            con+=1
            collect_text += comment['body'] + " "
        comment_count += len(data)
        time.sleep(.5)
    return [comment_count, collect_text]
   
def count_posts(user_name, time_frame_in_weeks):
    base_url = f'https://api.pushshift.io/reddit/search/submission/?author={user_name}'
    post_count = 1
    data = None
    for week in range(1,time_frame_in_weeks+1):
        request_url = base_url + f'&size=500&after={7*week}d&before={7*week - 7}d'
        response = requests.get(request_url)
        data = response.json()['data']
        post_count += len(data)
        time.sleep(.5)
    return post_count

def emotionAnalysis(text):
    authenticator = IAMAuthenticator('4uXz1_-vBcEKqNit9BaztlZ-S3UWxim91H5t07c32Coe')
    natural_language_understanding = NaturalLanguageUnderstandingV1( version='2020-08-01', authenticator = authenticator)
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b6c48743-410e-41d0-9fd2-f940ecec8342')
    result = natural_language_understanding.analyze(text = text, features = Features(sentiment = SentimentOptions(document=True), emotion = EmotionOptions(document=True)))
    emotions = result.__dict__['result']['emotion']['document']['emotion']
    sentiments = result.__dict__['result']['sentiment']['document']
    return [emotions, sentiments]

def main():
    
    weeks_to_check = int(input('weeks to check(no more than 24): '))
    username = input('insert username: ')
    [numb_comments, comment_text] = count_comments(username, weeks_to_check)
    numb_posts = count_posts(username, weeks_to_check)
    [emotions, sentiments] = emotionAnalysis(comment_text)
    print(
        f"\n\ncomments: {numb_comments}\n", 
        f"posts: {numb_posts}\n", 
        f"emotions: {emotions}\n", 
        f"sentiment score: {sentiments['score']}\n",
        f"sentiment label: {sentiments['label']}"
    )
    
main()