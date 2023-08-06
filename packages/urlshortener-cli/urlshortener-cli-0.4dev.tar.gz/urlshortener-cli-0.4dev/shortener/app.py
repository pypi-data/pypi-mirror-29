import json
import sys

import requests
import pyperclip

host = 'https://yoourl.herokuapp.com'


def main():
    custom_short_link = None
    link = ""
    end_point = host + '/api/shortener/create/'
    args = sys.argv

    if len(args) == 1:
        link = input('Enter link to be shortened : ')
    else:
        link = args[1]

    if '-c' in args:
        custom_short_link = args[args.index('-c') + 1]
    data = {'link': link}
    if custom_short_link:
        data['custom_short_link'] = custom_short_link
    response = requests.post(end_point, json=data)
    response_items = json.loads(response.text)
    if response.status_code in [200, 201]:
        shortened_link = host + '/' + response_items['shortened']
        current_clipboard_buffer = pyperclip.paste()
        if current_clipboard_buffer:
            print("Current buffer on clipboard is saved")
            with open(".clipboard.backup", "w") as f:
                f.write(current_clipboard_buffer)
        try:
            pyperclip.copy(shortened_link)
            print(shortened_link, "\n", "* Copied to clipboard *")
        except pyperclip.PyperclipException:
            print("install \"xsel\" to copy shortened url on clipboard\
                   automatically")
            print(shortened_link)
    else:
        for k, v in response_items.items():
            print(k + ' : ' + v[0])


if __name__ == '__main__':
    main()
