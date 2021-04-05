import re
from unidecode import unidecode


class Utils:

    @classmethod
    def count_words(cls, text):
        return len(re.findall(r'\w+', text))

    @classmethod
    def convert_text_to_words_lower(cls, text):
        text = unidecode(text)
        return re.sub("[^\w]", " ", text).lower().split()

    @classmethod
    def convert_text_to_set(cls, text):
        # convert text to set
        word_list = Utils.convert_text_to_words_lower(text)
        return set(word_list)

    @classmethod
    def decode_str(cls, text):
        return unidecode(text)



