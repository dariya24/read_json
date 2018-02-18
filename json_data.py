def data_from_json(file_path, verbouse=False, keyword=None):
    """
    str, bool, None -> str
    """
    import json
    f = open(file_path, "r")
    data = f.read()
    f.close()
    js = json.loads(data)
    f = open("results.txt", "w")
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
            print(person['name'] + ","+ person['location'])

    print("To get more data: enter one keyword from the list below, or Enter to finish.")
    temp = 1
    for person in js['users']:
        if temp == 1:
            for key in person:
                print(key)
        temp+=1
    resp = str(input('Enter keyword seperated by space: ')).split()
    if resp:
         data_from_json(file_path,  verbouse=True, keyword=resp)
