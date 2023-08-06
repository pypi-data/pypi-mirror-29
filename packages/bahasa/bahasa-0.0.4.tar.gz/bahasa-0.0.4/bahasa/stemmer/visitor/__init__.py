class DontStemShortWord(object):
    """description of class"""

    def visit(self, context):
        if self.is_short_word(context.current_word):
            context.stop_process()

    def is_short_word(self, word):
        return len(word) <= 3
