# (c) regextypofix lib, uses wikipedia regex replacement
import os
import regex as re
import logging

log = logging.getLogger('regextypofix')
logging.basicConfig(
  level=logging.ERROR,
  format='%(message)s'
)

def create_dictionary (typoFolder = None):
    """
    Loads all typo files and converts to a array
    dictionary = [
    [word, find, replace]
    ]
    """
    regex = r"\s(.*?)\=\"(.*?)\""
    path = os.path.join(os.path.dirname(__file__), 'typos') if typoFolder is None else typoFolder
    text_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.txt')]
    dictionary = []
    for file in text_files:
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith('<Typo'):
                    continue
            matches = re.findall(regex, line)
            t = []
            for i, (_, m) in enumerate(matches):
                if i == 1:
                    t.append(re.compile(m))
                elif i == 2:
                    t.append(m.replace('$', '\\'))
                else:
                    t.append(m)
            if len(t) != 3: logging.error(f"Parsing error in {line}")
            dictionary.append(t)
    logging.info('Total words in dictionary %s', len(dictionary))
    return dictionary

def correct (text, dictionary=None):
    # global default_dictionary
    if dictionary is None:
        return
    # dictionary = default_dictionary
    for word, find, replace in dictionary:
        try:
            text, doneFlag = find.subn(replace, text)
            if doneFlag:
                log.debug("%s: replaced", word)
        except re.error as err:
            log.error("error replacing %s (%r=>%r): %s", word, find, replace, err)
    return text

# Create a default dictionary upon import
# default_dictionary = create_dictionary()

if __name__ == "__main__":
    print (correct('whiel selled'))