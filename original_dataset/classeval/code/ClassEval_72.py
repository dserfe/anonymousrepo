import re

class RegexUtils:

    def match(self, pattern, text):
        ans = re.match(pattern, text)
        if ans:
            return True
        else:
            return False

    def findall(self, pattern, text):
        return re.findall(pattern, text)

    def split(self, pattern, text):
        return re.split(pattern, text)

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        pattern = '\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
        return pattern

    def generate_phone_number_pattern(self):
        pattern = '\\b\\d{3}-\\d{3}-\\d{4}\\b'
        return pattern

    def generate_split_sentences_pattern(self):
        pattern = '[.!?][\\s]{1,2}(?=[A-Z])'
        return pattern

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        return self.split(pattern, text)

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)