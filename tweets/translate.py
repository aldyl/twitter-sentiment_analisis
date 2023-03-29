#!/bin/python3

from deep_translator.google import GoogleTranslator


class Translate:
    def __init__(self, source='auto', tarjet='en') -> None:
        self.babylon = GoogleTranslator(source, tarjet)
        self.lang = 'english'

    def translate(self, text):

        try:
            result = self.babylon.translate(text)
            self.lang = 'english'
        except:
            print("Some error in translate")
            result = text
            self.lang = 'spanish'

        return result, self.lang

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
