import json

class MessageParser():
    def __init__(self):
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload, msgrec):
        payload = payload.replace("[", "{")
        payload = payload.replace("]", "}")
        #print payload
        payload = json.loads(payload) # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload, msgrec)
        else:
            return "Unknown response " + payload['response'];

    def parse_error(self, payload, msgrec):
        return "Error: " + payload['content']
    
    def parse_info(self, payload, msgrec):
        return "Info: " + payload['content']

    def parse_message(self, payload, msgrec):
        return "Message from " + payload['sender'] + ": " + payload['content']

    def parse_history(self, payload, msgrec):
        for json_msg in payload['content'].split("}"):
                if len(json_msg) > 5:
                    msgrec.client.receive_message(self.parse(json_msg + "}", msgrec))
        return ""
    
    # Include more methods for handling the different responses... 
