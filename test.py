import json


def main():

    tes = {"personalizations": [{"to": [{"email": "GGG"}]}],"from": {"email": "ucce.bin.monitoring@gmail.com"},"subject": "subject","content": [{"type": "text/plain", "value": "message"}]}
    #y = json.loads(tes)
    print(tes["from"])
    
main()