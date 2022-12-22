from sdtd_chatbot import SdtdChatServiceBase

import dbus

class SdtdChatTimers(SdtdChatServiceBase):            
    BEERQUESTION = "how many bottles of beer on the wall?"
    BEERCONFIG = "beersong "
    BEERSTOP = "shut up about beer"
    
    def __init__(self, name, path):
        super().__init__(name, path)

        self.register_match_algo(self.string_starts, self.BEERQUESTION, self.initiate_bottles_of_beer)
        self.register_match_algo(self.string_starts_trim, self.BEERCONFIG, self.initiate_bottles_of_beer_specific)
        self.register_match_algo(self.string_starts, self.BEERSTOP, self.terminate_bottles_of_beer)

    def initiate_bottles(self, uniqueid, origin, beernum):        
        saystr = self.ok_prepend(origin) + ", beer song initiated starting from " + str(beernum)
        self.beer_remaining = beernum
        self.register_timer('beersong', 3.0)        
        self.dispatch_iface.EventHandled(uniqueid, saystr)
    
    def initiate_bottles_of_beer(self, uniqueid, chatdict, body):
        origin_name = chatdict['name_from']
            
        self.initiate_bottles(uniqueid, origin_name, 99)
        
    def initiate_bottles_of_beer_specific(self, uniqueid, chatdict, beernum):
        origin_name = chatdict['name_from']
            
        self.initiate_bottles(uniqueid, origin_name, int(beernum))
    
    def terminate_bottles_of_beer(self, uniqueid, chatdict, body):
        origin_name = chatdict['name_from']
        
        saystr = self.sorry_prepend(origin_name) + ", I didn't know it was annoying you"
        self.unregister_timer('beersong')
        self.dispatch_iface.EventHandled(uniqueid, saystr)


    def handle_timer(self, timername):
        saystr = str(self.beer_remaining) + " bottles of beer on the wall! " + str(self.beer_remaining) + " bottles of beer!  Take one down, pass it around, " + str(self.beer_remaining-1) + " bottles of beer on the wall!"
        self.beer_remaining -= 1
        self.dispatch_iface.perform_say(saystr)
        if self.beer_remaining == 0:
            self.unregister_timer('beersong')
                                        
if __name__ == "__main__":                
    sdtd_chat_timers_service = SdtdChatTimers('com.tutorial.timers', '/timers')
    sdtd_chat_timers_service.run()
    
