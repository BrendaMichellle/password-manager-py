import random
import pyperclip

NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
           'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T',
           'U', 'V', 'W', 'X', 'Y', 'Z']
SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')']
ALL_CHARS = {'NUMBERS': NUMBERS,
             'LETTERS': LETTERS,
             'SYMBOLS': SYMBOLS}


class PasswordGenerator:

    def generate_password(self, has_symbols, has_letters, has_numbers, pass_length):
        password = ''
        my_list = []
        if has_symbols:
            my_list.append('SYMBOLS')
        if has_letters:
            my_list.append('LETTERS')
        if has_numbers:
            my_list.append('NUMBERS')
        for _ in range(pass_length):
            which_char = random.choice(my_list)
            that_list = ALL_CHARS[which_char]
            char_to_add = random.choice(that_list)
            password += char_to_add
        pyperclip.copy(password)
        return password
