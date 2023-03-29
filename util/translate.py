#!/bin/python3

from deep_translator.google import GoogleTranslator

class Translate:
    def __init__(self, source='es', tarjet='en') -> None:
        self.babylon = GoogleTranslator(source, tarjet)

    def translate(self, text):
        return self.babylon.translate(text)

    def translate_file(self, file_src):
        return self.babylon.translate_file(file_src)

    def translate_batch(self, list):
        return self.babylon.translate_batch(list)