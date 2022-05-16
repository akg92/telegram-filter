
from dataclasses import dataclass
import json

@dataclass
class Credential:
    user: str
    appId: str
    apiHash: str

    @staticmethod
    def getTelegramCredential():
        with open('./helper/credentials.json') as fr:
            data = json.load(fr)['telegram']
            return Credential(user=data['user'], appId=data['appId'], apiHash=data['apiHash'])
