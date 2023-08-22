import re
import json
import sys
from datetime import datetime
import argparse
import os

def parse_chat_line(line, ignoreOmmittedMessage):
    pattern = r'\[(.*?)\]\s(.*?):\s(.*)'
    match = re.search(pattern, line)
    if match:
        date_time_str = match.group(1)
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y, %I:%M:%S %p')
        user = match.group(2)
        message = match.group(3)
        attachment = None
        if '<attached:' in message:
            attachment = message.split('<attached:')[1].split('>')[0].strip()
            message = None
        elif 'image omitted' in message and ignoreOmmittedMessage:
            return None
        return {'date_time': date_time_obj.isoformat(), 'user': user, 'message': message, 'attachment': attachment}
    else:
        return None

def parse_chat_file(file_path, ignoreOmmittedMessage):
    chat_data = []
    participants = set()
    attachment_extensions = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
        for line in lines:
            chat_line = parse_chat_line(line, ignoreOmmittedMessage)
            if chat_line:
                participants.add(chat_line['user'])
                if chat_line['attachment']:
                    attachment_extensions.add(chat_line['attachment'].split('.')[-1])
                chat_data.append(chat_line)
    return {'participants': list(participants), 'attachment_extensions': list(attachment_extensions), 'chats': chat_data}

def write_to_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="Path to chat txt file", required=True)
    parser.add_argument("--ignoreOmmited", help="Ignore messages for ommited attachments (when exported without media)", default=False)
    parser.add_argument('--output', help="Output File where the json will be stored", default='output.json')
    args = parser.parse_args()

    if (not args.output.endswith('.json')):
        print("Invalid putput file. Please provide a name with json extension")
        exit()
    
    if ('/' in args.output):
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

    chat_data = parse_chat_file(args.f, args.ignoreOmmited)
    write_to_json_file(chat_data, args.output)
    print("Successful!")

if __name__ == "__main__":
    main()