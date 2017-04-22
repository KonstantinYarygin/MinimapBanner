import sublime, sublime_plugin
import string
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
LETTER_WIDTH = 7

def load_banner_letters():
    symbols = string.ascii_uppercase + string.digits + string.punctuation
    symbol2image = {}
    letters_path = os.path.join(SCRIPT_DIR, 'banner_letters.txt')
    with open(letters_path, 'r') as f:
        for symbol in symbols:
            chunk = [f.readline().strip('\n') for _ in range(LETTER_WIDTH)]
            max_len = max(len(line) for line in chunk)
            chunk = [line.ljust(max_len) for line in chunk]
            symbol2image[symbol] = chunk
    return symbol2image

def make_banner(text, symbol2image):
    text = text.upper()
    banner = ['' for _ in range(LETTER_WIDTH)]
    for symbol in text:
        if symbol in symbol2image:
            for row in range(LETTER_WIDTH):
                banner[row] += symbol2image[symbol][row] + ' '
        else:
            for row in range(LETTER_WIDTH):
                banner[row] += 3 * ' ' + ' '
    banner = [line + '\n' for line in banner]
    banner[-1] = banner[-1][:-1]
    return banner

def add_comment_prefix(text, view, pos):
    shell_vars = view.meta_info("shellVariables", pos)
    var_dict = {}
    for x in shell_vars:
        if 'name' in x and 'value' in x:
            var_dict[x['name']] = x['value']
    if 'TM_COMMENT_START' in var_dict:
        comment_prefix = var_dict['TM_COMMENT_START']
        return comment_prefix + text
    else:
        return text

class ConvertToBannerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        symbol2image = load_banner_letters()
        sels = self.view.sel()
        for sel in sels:
            text = self.view.substr(sel)
            line_banner = make_banner(text, symbol2image)
            pos = sel.begin()
            self.view.erase(edit, sel)
            for line in line_banner[::-1]:
                comm_line = add_comment_prefix(line, self.view, pos)
                self.view.insert(edit, pos, comm_line)
