import ConfigParser

class Parser:
    _secretKey = ""
    _username = ""
    _password = ""
    _clientId = ""
    
    configParser = ConfigParser.RawConfigParser()

    def __init__(self, filepath):
        self._configFilePath = filepath
        print 'Using File : ', filepath

        try:
            self.configParser.readfp(open(filepath, 'r'))
        except:
            print 'Invalid cofig file path, Cannot open', filepath

        try:
            print "Reading fields..."
            self._clientId = self.configParser.get('User_Config','ClientId')
            self._secretKey =  self.configParser.get('User_Config','Secret')
            self._username = self.configParser.get('User_Config','Username')
            self._password = self.configParser.get('User_Config','Password')

        except:
            print 'Invalid configuration'


    def getId(self):
        return self._clientId
    def getSecret(self):
        return self._secretKey
    def getUsername(self):
        return self._username
    def getPassword(self):
        return self._password

    def printAll(self):
        print "client: " + self._clientId
        print "secret: " + self._secretKey
        print "username: " + self._username



