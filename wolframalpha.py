#!/usr/bin/env ./venv/bin/python
# coding: utf-8

__version__ = '1.1'

import requests
import re
import os
from urllib.parse import quote
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def read_key_from_file():
    try:
        with open(os.path.expanduser("~/.wolframalpha_appid"), "r") as _file:
            wolframalpha_appid = "".join(_file.readlines()).strip()
        return wolframalpha_appid
    except Exception as e:
        print('Invalid or empty API key!\nGet one at https://developer.wolframalpha.com/portal/apisignup.html')
        api_key = input('Enter your WolframAlpha AppID: ')
        wolframalpha_appid = api_key
        with open(os.path.expanduser("~/.wolframalpha_appid"), "w") as _file:
            _file.writelines(api_key)
        return wolframalpha_appid

def main():
    parser = argparse.ArgumentParser(description="WolframAlpha CLI")
    parser.add_argument("QUERY", nargs='+', help="Query to search in WolframAlpha")
    parser.add_argument("--appid", help="WolframAlpha AppID - If not informed will be asked and saved in a file for future use")

    args = parser.parse_args()
    query = " ".join(args.QUERY)

    if args.appid:
        wolframalpha_appid = args.appid
    else:
        wolframalpha_appid = read_key_from_file()

    url = f'https://api.wolframalpha.com/v2/query?input={quote(query)}&appid={wolframalpha_appid}&format=plaintext'

    resp = requests.get(url)
    all_pods = re.findall(r'<pod.+?>.+?</pod>', resp.text, re.S)

    for pod in all_pods:
        if 'Result' in pod:
            for inner in re.findall(r'<plaintext>(.*?)</plaintext>', pod, re.S):
                lines = inner.strip().split('\n')
                if lines:
                    result = " ".join(lines[0].strip().split())
                    print(Fore.MAGENTA + Style.BRIGHT + result)
                    return

    print("No results")

if __name__ == '__main__':
    main()
