from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from requests import get
from actions.base import BBMessage
from json import loads
class ActionInspire(Action):
    def name(self) -> Text:
        return "action_inspire"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message["intent"]["name"]
        print("action_inspire processing "+intent_name)
        try:
            response = get('http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en')
            dispatcher.utter_message(text='{quoteText} - {quoteAuthor}'.format(**loads(response.text)))
        except Exception as inst:
            print(inst)
            res = BBMessage(tracker.latest_message['text'])
            dispatcher.utter_message(text=res)
            # dispatcher.utter_message(text='Ask me again tomorrow')
        return []

class ActionJoke(Action):
    def name(self) -> Text:
        return "action_joke"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message["intent"]["name"]
        print("action_joke processing "+intent_name)
        try:
            data = get("https://official-joke-api.appspot.com/random_joke")
            a = loads(data.text)
            dispatcher.utter_message(text=a["setup"]+"\n"+a["punchline"])
        except Exception as inst:
            print(inst)
            res = BBMessage(tracker.latest_message['text'])
            dispatcher.utter_message(text=res)
            # dispatcher.utter_message(text='Why do chickens cross the road?')
        return []