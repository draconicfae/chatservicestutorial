from sdtd_chatbot import SdtdChatServiceBase

import dbus

#TODO : change from SdtdChatEmpty to your class name
class SdtdChatEmpty(SdtdChatServiceBase):            
    def __init__(self, name, path):
        super().__init__(name, path)
        
        #TODO : if needed, add match algos here
        
    #TODO : either use this, the default handler, or add your own 
    #handler function(s)
    def handle_zavi_request(self, uniqueid, chatdict, body):
        #TODO : remember to let the chat dispatch know if you've 
        #handled something so it doesn't time out.  The second 
        #parameter is a string that the chat dispatch will say
        #self.dispatch_iface.EventHandled(uniqueid, '')
        pass
    
if __name__ == "__main__":                
    sdtd_chat_empty_service = SdtdChatEmpty('com.tutorial.empty', '/empty')
    sdtd_chat_empty_service.run()
    
