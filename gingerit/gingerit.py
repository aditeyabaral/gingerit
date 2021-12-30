# -*- coding: utf-8 -*-
import re
import json
import requests
import argparse
from pathlib import Path

URL = "https://services.gingersoftware.com/Ginger/correct/jsonSecured/GingerTheTextFull"  # noqa
API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"


class GingerIt(object):
    def __init__(self):
        self.url = URL
        self.api_key = API_KEY
        self.api_version = "2.0"
        self.lang = "US"

    def parse(self, text, verify=True):
        session = requests.Session()
        request = session.get(
            self.url,
            params={
                "lang": self.lang,
                "apiKey": self.api_key,
                "clientVersion": self.api_version,
                "text": text,
            },
            verify=verify,
        )
        data = request.json()
        return self._process_data(text, data)

    @staticmethod
    def _change_char(original_text, from_position, to_position, change_with):
        return "{}{}{}".format(
            original_text[:from_position], change_with, original_text[to_position + 1:]
        )

    def _process_data(self, text, data):
        result = text
        corrections = []

        for suggestion in reversed(data["Corrections"]):
            start = suggestion["From"]
            end = suggestion["To"]

            if suggestion["Suggestions"]:
                suggest = suggestion["Suggestions"][0]
                result = self._change_char(result, start, end, suggest["Text"])

                corrections.append(
                    {
                        "start": start,
                        "text": text[start: end + 1],
                        "correct": suggest.get("Text", None),
                        "definition": suggest.get("Definition", None),
                    }
                )

        return {"text": text, "result": result, "corrections": corrections}


def get_text_content(_input, truncation_strategy):
    '''
    Obtain text content from command line input or from a text file
    '''
    if Path(_input).is_file():
        with open(_input, 'r') as f:
            text = f.read()
    else:
        text = _input
    text = text.strip()

    text_length = len(text)
    text_list = list()  # list of text chunks
    delimiter_list = list()  # list of delimiters

    if text_length > 600:
        '''
        Since the API call supports only 600 characters, we need to split the text. Truncation strategies are to either:
        1. Split the text into multiple chunks
        2. Truncate the text to 600 characters
        '''
        if truncation_strategy == 'truncate':
            # use only the first 600 characters
            text_list.append(text[:600])
            delimiter_list.append('')

        elif truncation_strategy == 'split':
            '''
            Split the text into multiple chunks and store the delimiters.
            Obtain paragraphs from the text. If a paragraph is too big, split it into multiple sentences.
            '''
            paragraphs = text.split('\n')
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if len(paragraph) > 600:
                    # split on sentence boundaries
                    sentences = re.split(r'[.?!]+', paragraph)
                    sentence_delimiters = re.findall(
                        r'[.?!]+', paragraph)  # store sentence delimiters
                    for sentence, delimiter in zip(sentences, sentence_delimiters):
                        sentence = sentence.strip()
                        if sentence:
                            text_list.append(sentence)
                            delimiter_list.append(delimiter)
                else:
                    text_list.append(paragraph)
                    delimiter_list.append('\n')
    else:
        text_list.append(text)
        delimiter_list.append('')

    return text_list, delimiter_list


def main():
    G = GingerIt()
    parser = argparse.ArgumentParser(description='Gingerit CLI')
    parser.add_argument(
        '-i', '--input', help='Input text or path to text file', required=True)
    parser.add_argument('-o', '--output', help='Print detailed output',
                        default=False, action='store_true')
    parser.add_argument(
        '-f', '--file', help='Redirect to output file', default=None)
    parser.add_argument('-t', '--truncation', help='Truncation strategy if the text length exceeds 600 characters',
                        default='split', choices=['split', 'truncate'])
    parser.add_argument('-v', '--verify', default=True)
    args = parser.parse_args()

    text_list, delimiter_list = get_text_content(
        args.input, args.truncation)   # get all text chunks
    corrections = list()
    corrected_text = str()
    for text, delimiter in zip(text_list, delimiter_list):
        gingerit_parsed_output = G.parse(text)
        # store all correction dictionaries returned by API
        corrections.append(gingerit_parsed_output)
        # get corrected text chunk
        gingerit_parsed_correction = gingerit_parsed_output['result']
        # append current corrected text chunk to the complete corrected text along with the delimiter
        corrected_text = f"{corrected_text}{gingerit_parsed_correction}{delimiter} "

    if args.output:
        _output = corrections   # print detailed output
    else:
        _output = corrected_text    # print corrected text only

    if args.file is not None:   # redirect to output file
        if isinstance(_output, list):   # if detailed output is a list, convert it to a string
            _output = json.dumps(_output, indent=4)
        with open(args.file, 'w') as f:
            f.write(_output)
    else:
        print(_output)


if __name__ == "__main__":
    main()
