# Gmail email reader

This script allows you to check if you have any new mails and print out your unread mails from the last 7 days in a text file.

## Installation

Simply download the code or use the git clone command to clone the repository

```bash
git clone https://github.com/akrotag/gmail-checkForNewMails.git
```

## Usage

first open the file with any text editor you want and repalce the first three lines with your email and password, it should look something like that:
```python
###-Sets account's password and adress-###
addr = "yourEmailAdress@gmail.com"
passwrd = "yourGmailPassword"
```
(for Linux)
```bash
python3 mail-checker.py
```
or simply open it directly if you're on windows and have python installed

## Limitations
This script has some limitations: it can't read some mails because of their encoding, and because I couldn't test it on every mail system. it is tested on mails from gmail and hotmail/outlook (anything coming from microsoft)

## Requirements
- Python (duh)
- binascii
- platform
- imaplib
- os
- requests
- subprocess
- email
- datetime
- base64
- quopri

all of these packages can be installed using the appropriate py -m pip install command on windows and pip3 install command on linux

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

I would just ask you to please comment your code, not necessarily as much as I did but at least for it to be understandable by a beginner

Please make sure to update tests as appropriate.
