# Whatsapp chat to JSON parser

## How to run
- Install python (3 or above)
- Open Terminal or cmd
- run `python chat_to_json -f <file_path> <optional args>`

```
usage: chat_to_json.py [-h] --f F [--ignoreOmmited IGNOREOMMITED] [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --f F                 Path to chat txt file
  --ignoreOmmited IGNOREOMMITED
                        Ignore messages for ommited attachments (when exported without media)
  --output OUTPUT       Output File where the json will be stored
  ```

Output JSON Structure:
```json
{
    "participants": [
        "User-1",
        "user-2",
        "---"
    ],
    "attachment_extensions": [
        "mp4",
        "docx",
        "jpg",
        "opus",
        "pdf",
        "webp",
        "---"
    ],
    "chats": [
        {
            "date_time": "<Date>",
            "user": "User-1",
            "message": "<Message>",
            "attachment": "<Attachment File Name>"
        },
        ....
    ]
```