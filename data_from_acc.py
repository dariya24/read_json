def data_from_acc(acct, verbouse=False, keyword=None):
    """
    str, bool, None -> str
    Return custom data from given account
    """
    import urllib.request, urllib.parse, urllib.error
    import twurl
    import json
    import ssl
    # https://apps.twitter.com/
    # Create App and get the four strings, put them in hidden.py
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '200'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    print("This is the we've got: \n")
    if verbouse:
        try:
            for person in js['users']:
                print(person['name'], end="----->\n")
                for element in keyword:
                    print(person[element], end=", ")
                print("")
        except:
            return "Wrong keyword"
    else:
        for person in js['users']:
            print(person['name'] + "," + person['location'])

    print("To get more data: enter one keyword from the list below, or Enter to finish.")
    temp = 1
    for person in js['users']:
        if temp == 1:
            for key in person:
                print(key)
        temp += 1
    resp = str(input('Enter keyword seperated by space: ')).split()
    if resp:
        data_from_acc(acct,  verbouse=True, keyword=resp)
