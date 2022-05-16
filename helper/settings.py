import json

from .message import Message
from .messages import Messages
import re
import os

from .messanger import Messanger


class Filter:
    MEDIA = "media"
    TEXT = "text"

    def __init__(self, jsonObject):
        if jsonObject.get("contains"):
            self.contains = re.compile(jsonObject.get("contains"))
        else:
            self.contains = None
        
        if jsonObject.get("excludes"):
            self.excludes = re.compile(jsonObject.get("excludes"))
        else:
            self.excludes = None
        self.type = jsonObject.get("type")

    def __isMediaType(self):
        return self.type and self.type == Filter.MEDIA

    def isUsefulMessage(self, message: Message) -> bool:
        
        isValid: bool = False
        ## perform text operation iff text content present
        
        if  message.text and self.contains:
            isValid = self.contains.search(message.text) != None

        if self.__isMediaType() and message.isMedia:
            isValid = True

        if message.text and self.excludes:
            isValid = isValid  and  self.excludes.search(message.text) == None


        return isValid



class Setting:

    def __init__(self, jsonData: dict) -> None:
        self.channelId = jsonData.get("channelId")
        self.filters =  [] 
        for filter in jsonData.get("filter"):
            self.filters.append(Filter(filter))
        self.desination = Messanger(jsonData.get("destination"))

    def getValidMessages(self, messages: Messages):
        if self.channelId != messages.channelId:
            return None
        
        validMessages = Messages(channelId = messages.channelId, messages = [])

        for message in messages.messages:
            for filter in self.filters:
                if filter.isUsefulMessage(message):
                    validMessages.appendMessage(message)
                    break
        
        return validMessages


class SettingHelper:

    SETTING_HELPER = None
    ### walk all folder and create settings
    def __init__(self, folder) -> None:
        self.folder = folder
        self.settings = {} 

        for file in os.listdir(folder):
            if file.endswith(".json"):
                path = os.path.join(folder, file)
                
                with open(path, 'r') as jsonData:
                    setting = Setting(json.load(jsonData))

                    self.settings[setting.channelId] = setting
    
    @staticmethod
    def initAndGet(folder = './helper/setting-data'):
        if SettingHelper.SETTING_HELPER == None:
            SettingHelper.SETTING_HELPER = SettingHelper(folder=folder)
        return SettingHelper.SETTING_HELPER        

    @staticmethod
    def filterMessages(messages: Messages):
        helper = SettingHelper.initAndGet()

        ## No configuration found
        channelId = messages.channelId
        if channelId not in helper.settings:
            print("missing configuration")
            return None, None
        

        setting:Setting = helper.settings[channelId]
        return setting, setting.getValidMessages(messages=messages)
            
