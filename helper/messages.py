
from dataclasses import dataclass
from typing import List
from . import Message

@dataclass
class Messages:
    channelId: str
    messages: List[Message]

    def appendMessage(self, message):
        if not self.messages:
            self.messages = []
        
        self.messages.append(message)