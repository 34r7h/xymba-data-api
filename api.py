
import requests




access_token = 'EAAv2hPX5KfMBAIbZCdaz4Bi9jrLZBnjKfoihQvwZAOGhPCWa5ATVwoE3ZCtN9Im1sn0uyVaRZBZCu21AHg2MVsneF7aXeG3S7Pe6lI7tNQfdnRZBmtowhxEAImbc6XLL0PPwMeIsTeQ71BqOUB3NpZBrix3tDS3pUmJwoZB4hZATwC9TRO4ZC8KkgAag8OdZCkbbXOcOzvcWBZBTV8vYJqOGaxZAln4peFejZBK0ZBV1Ll6cqFeSAwZDZD'

access_token = 'EAAv2hPX5KfMBAFGRLHLkld6qlIC3alLGew698ZAvCd7wUpbtTLhePZBvQ8w3bzj6NpNVZBDlZBlakIXPAKoDcmZALuqHnY33jsnAUBhvBZBoCam7NqjltvynPB7ma3Qaji2ZBrPrWQ1BUGn2dXguK5S5vAcbtKXDliKXXj3aZCkjEwZDZD'

def getuserdata(access_token = access_token) :
    url = "https://graph.facebook.com/v5.0/me"


    PARAMS = {'fields':'photos,likes','access_token':access_token}
    r = requests.get(url = url, params = PARAMS)


    data = r.json()
    return data



user_data = getuserdata()

#print 'received user data is ', user_data






def insertIntoMongo(ip = 'localhost', port = 27017, database = 'xymba_data', collection = 'data', record = {}) :
    import pymongo
  

    myclient = pymongo.MongoClient("mongodb://%s:%d/"%(ip,port))   
    


    mydb = myclient[database]
    mycollection = mydb[collection]

    x = mycollection.insert_one(record)
    return x


def generatekey() :
    import random
    key = ''.join(chr(random.randint(0, 0xFF)) for i in range(32))
    return key

def ecb_encrypt(message):
    from Crypto.Cipher import AES
    import base64
    key = generatekey()
    aes = AES.new(key, AES.MODE_ECB)
    n = len(message)
    if n == 0:
        return ''
    elif n % 16 != 0:
        message += ' ' * (16 - n % 16)
    return base64.b64encode(key), base64.b64encode(aes.encrypt(message)).decode()


def ecb_decrypt(encrypted, key):
    from Crypto.Cipher import AES
    import base64

    aes = AES.new(base64.b64decode(key), AES.MODE_ECB)
    return aes.decrypt(base64.b64decode(encrypted))


key, base_encoded = ecb_encrypt(str(user_data))
#print 'Encoded Message IS: ' + base_encoded

decoded = ecb_decrypt(base_encoded, key)
#print 'Decoded message is: ' + decoded

insertIntoMongo('localhost', 27017, 'xymba_data', 'data', {'key':key,'data':base_encoded,'user_id':4444})


def get_data_from_db(ip = 'localhost', port = 27017, database = 'xymba_data', collection = 'data',user_id = 0):
    import pymongo
  
    myclient = pymongo.MongoClient("mongodb://%s:%d/"%(ip,port))   
    
    mydb = myclient[database]
    mycollection = mydb[collection]
    results = []
    for record in mycollection.find({"user_id": user_id}):
        results += [record]
    return results


print get_data_from_db(user_id=4444)






