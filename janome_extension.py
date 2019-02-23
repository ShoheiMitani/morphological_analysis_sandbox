from janome.tokenfilter import *

class PartsOfSpeechFilter(TokenFilter):
    """
    A PartsOfSpeechFilter keeps tokens associated with part-of-speech type listed in the keep type list and removes other tokens.
    Part-of-speech type get from part_of_speech. e.g., if '一般' is given as a keep tag, '名詞,一般,*,*' and '名詞,複合,*,*' (or so) are kept.
    """

    def __init__(self, white_list):
        """
        Initialize PartsOfSpeechFilter object.
        :param white_list: keep part-of-speech type list.
        """
        self.white_list = white_list

    def apply(self, tokens):
        for token in tokens:
            if token.part_of_speech.split(',')[1] not in self.white_list:
                continue
            yield token
