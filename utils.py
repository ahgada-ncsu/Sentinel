import re

def remove_special_characters(input_str):
    pattern = re.compile(r'[ÄäÖöÅåẞß]')
    cleaned_str = re.sub(pattern, '', input_str)
    return cleaned_str

def remove_duplicate_punctuation(text):
    punctuation_to_keep = r',./?\'";:{}[]\\|`~!@#$%^&*()-_+=+<>'
    pattern = r'([' + re.escape(punctuation_to_keep) + r'])\1+'
    cleaned_text = re.sub(pattern, r'\1', text)
    return cleaned_text

def limit_word_length(s):
    t = ""
    for i in s.split(" "):
        if len(i) > 16:
            t += i[:16] + " "
        else:
            t += i + " "
    return t

def remove_repeating_phrases(input_str):
    pattern = re.compile(r'(\b\w+\b)(\s+\1)+')
    output_str = re.sub(pattern, r'\1', input_str)
    return output_str


def split_tasks(input_str):
    pattern = r'[.!?\n]'
    split_str = re.split(pattern, input_str)
    return split_str