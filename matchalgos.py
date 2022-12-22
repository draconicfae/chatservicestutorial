from sdtd_chatbot import SdtdChatServiceBase

import dbus

class SdtdChatMatchAlgos(SdtdChatServiceBase):            
    #match strings always need to be lower case because the string 
    #you're sent will have been set to lower case no matter what the
    #original text was.
    HOWAREYOU = "how are you doing?"    
    GIFT = "i bought you this high quality "
    SAIDTHAT = "can't believe you said that"
    COMPLIMENTS = ["you're the best", "nobody makes pancakes as well as you", "i'm glad we're friends"]
    HAVE = ['i have ', 'cups and ', ' forks']
    
    def __init__(self, name, path):
        super().__init__(name, path)

        self.register_match_algo(self.string_starts, self.HOWAREYOU, self.handle_how_are_you)
        self.register_match_algo(self.string_starts_trim, self.GIFT, self.handle_gift)
        self.register_match_algo(self.string_in, self.SAIDTHAT, self.handle_said_that)
        self.register_match_algo(self.reverse_in, self.COMPLIMENTS, self.handle_compliment)
        self.register_match_algo(self.list_in_trim, self.HAVE, self.handle_have)


    #example strings:
    #   Hey zavi, how are you doing?
    #   Hey zavi, how are you doing? I'm doing fine.
    #   Hey zavi, how are you doing? I heard you got a promotion!
    def handle_how_are_you(self, uniqueid, chatdict, body):
        origin_name = chatdict['name_from']
        
        saystr = "Thanks for asking, " + origin_name + ", I'm doing well!"
        self.dispatch_iface.EventHandled(uniqueid, saystr)

    #example strings and what the resulting function parameter would 
    #be
    #   "Hey zavi, I bought you this high quality boomerang" -> boomerang
    #   "Hey zavi, I bought you this high quality computer" -> computer
    #   "Hey zavi, I bought you this high quality set of steak knives" -> set of steak knives
    def handle_gift(self, uniqueid, chatdict, gift):
        origin_name = chatdict['name_from']
        
        saystr = self.ok_prepend(origin_name) + ", I've always wanted a " + gift 
        self.dispatch_iface.EventHandled(uniqueid, saystr)

    #example strings:
    #   Hey zavi, That's completely outrageous!  I can't believe you said that to me
    #   Hey zavi, can't believe you said that
    #   Hey zavi, Are you really telling me 'I can't believe you said that'
    def handle_said_that(self, uniqueid, chatdict, gift):
        origin_name = chatdict['name_from']
        
        saystr = self.sorry_prepend(origin_name) + ", I did say that."
        self.dispatch_iface.EventHandled(uniqueid, saystr)

    #in this case, a match needs to be exactly in the compliments 
    #list, so "Hey zavi, you're the best" would match but "Hey Zavi, 
    #you're the best at chess" would not.
    def handle_compliment(self, uniqueid, chatdict, body):
        saystr = "that's very nice of you"
        self.dispatch_iface.EventHandled(uniqueid, saystr)
    
    #example strings and what the resulting function parameter would
    #be
    #   "Hey zavi, I have 3 cups and 2 forks" -> "3 2"
    #   "Hey zavi, I have 32 cups and 28 forks" -> "32 28"
    #   "Hey zavi, I think I have to go get some cups and forks" -> "i think to go get some "
    #   "Hey zavi, cups and forks are what I have" -> " are what "
    #The last two examples showcase 1) you aren't limited to using 
    #this kind of match for quantities 2) you don't have to have the 
    #list in the specified order for it to match, it just needs all 
    #the individual items to be "somewhere" in the string
    def handle_have(self, uniqueid, chatdict, remainderstring):
        origin_name = chatdict['name_from']
        
        saystr = self.ok_prepend(origin_name) + ", thanks for letting me know what you have: '" + remainderstring + "'"
        self.dispatch_iface.EventHandled(uniqueid, saystr)        
                                    
if __name__ == "__main__":                
    sdtd_chat_matchalgos_service = SdtdChatMatchAlgos('com.tutorial.matchalgos', '/matchalgos')
    sdtd_chat_matchalgos_service.run()
    
