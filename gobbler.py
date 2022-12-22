from sdtd_chatbot import SdtdChatServiceBase

import dbus

class SdtdChatGobbler(SdtdChatServiceBase):            
    def __init__(self, name, path):
        super().__init__(name, path)
                
    #we eat everything we're given, no match algorithms
    def handle_zavi_request(self, uniqueid, chatdict, body):
        origin_name = chatdict['name_from']
        saystr = self.ok_prepend(origin_name) + ", gobbler has eaten '" + body + "'"
        self.dispatch_iface.EventHandled(uniqueid, saystr)
    
if __name__ == "__main__":                
    sdtd_chat_gobbler_service = SdtdChatGobbler('com.tutorial.gobbler', '/gobbler')
    sdtd_chat_gobbler_service.run()
    
