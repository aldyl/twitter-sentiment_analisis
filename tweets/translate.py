#!/bin/python3

from deep_translator.google import GoogleTranslator
import asyncio


class TranslateGoogle:

    def __init__(self, source='auto', tarjet='en') -> None:

        self.babylon = GoogleTranslator(source, tarjet)
        self.loop = asyncio.get_event_loop()

    def translate(self, text):

        try:
            result = self.babylon.translate(text)
            self.lang = 'english'
        except:
            print("Some error in translate")
            result = text
            self.lang = 'spanish'

        return result, self.lang

    async def translate_tweet(self, tweet):
        try:
            content_translated = await self.loop.run_in_executor(None, self.babylon.translate, tweet)
            print("#",end="")
            return content_translated
        except Exception as e:
            print(f"Translation failed: {e}")
            return ""

    async def translate_tweets(self, tweets):

        translated_tweets = []
        tasks = [asyncio.ensure_future(self.translate_tweet(tweet)) for tweet in tweets]
        completed_tasks, _ = await asyncio.wait(tasks)
        
        for task in completed_tasks:
            translated_tweets.append(task.result())
        
        return translated_tweets
    
    
    def async_translate(self, tweets):
        translated_tweets = self.loop.run_until_complete(self.translate_tweets(tweets))
        return translated_tweets


    def translate_file(self, file_src):
        result = ""

        try:
            result = self.babylon.translate_file(file_src)
            self.lang = 'english'
        except:
            print("Some error in translate")
            result = "error"
            self.lang = 'spanish'

        return result

    def translate_batch(self, list):
        result = []

        try:
            result = self.babylon.translate_batch(list)
            self.lang = 'english'
        except:
            print("Some error in translate")
            result = list
            self.lang = 'spanish'

        return result
