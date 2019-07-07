import requests

class HTTPClient:

    def __init__(self, HTTPClientSettings):
        self._HTTPClientSettings = HTTPClientSettings
        temp = requests.post(self.getTokenURL(),data=self.getAuthRequestBody()).json()
        self._token = temp["token"]

    def getHTTPClientSettings(self):
        return self._HTTPClientSettings

    def getTokenURL(self):
        return '{}/token'.format(self.getHTTPClientSettings().getDataSource())

    def getFriendCodesURL(self):
        return '{}/fc'.format(self.getHTTPClientSettings().getDataSource())

    def getAuthRequestBody(self):
        return {'grant_type':'client_credentials','client_id':self.getHTTPClientSettings().getClientId(),'client_secret':self.getHTTPClientSettings().getClientSecret()}

    def getHTTPClientSession(self):
        return self._HTTPClientSession

    def getToken(self):
        return self._token

    # Add a new friend code in the DB
    def addcode(self, chat, name, key, friendcode):
        self.getHTTPClientSession().post(self.getFriendCodesURL(),
        'chat={}&name={}&key={}&friendcode={}'.format(chat,name,key,friendcode))

    # remove a friend code from the DB
    def removecode(self, chat, name, key):
        self.getHTTPClientSession().delete(self.getFriendCodesURL(),
        'chat={}&name={}&key={}'.format(chat,name,key))

    # search a person and get all of this codes
    def queryperson(self, chat, name):
        result = []

        response = self.getHTTPClientSession().get(self.getFriendCodesURL(),
        params={"chat": chat, "name": name}).json()

        for record in response:
            result.append([record["key"], record["code"]])

        return result

    def listall(self, chat):
        result = {}

        response = self.getHTTPClientSession().get(self.getFriendCodesURL(),
        params={"chat": chat}).json()

        for user in response:
            result[user["name"]] = []

            for record in user["codes"]:
                result[user["name"]].append([record["key"], record["code"]])

        return result


class HTTPClientSettings:
    def __init__(self, dataSource, client_id, client_secret):
        self._dataSource = dataSource
        self._client_id = client_id
        self._client_secret = client_secret

    def getDataSource(self):
        return self._dataSource

    def getClientId(self):
        return self._client_id

    def getClientSecret(self):
        return self._client_secret