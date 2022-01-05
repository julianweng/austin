from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from requests import get
from json import loads
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary

from actions.base import BBMessage, SumMessage

class ActionWiki(Action):
    def name(self) -> Text:
        return "action_wiki"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject = tracker.get_slot('subject')
        SlotSet("subject", None)
        print("Looking up " + subject)
        if subject is None:
            dispatcher.utter_message(text="Sorry I can't help you with this")
        else:
            try:
                """
                if (len(subject.split()) > 1): # multiple words, hit the wiki
                    ret = self.wiki(subject)
                else: # otherwise, hit the pydictionary
                    ret = self.lookup(subject)
                    if ret is None:
                        ret = self.wiki(subject)
                """
                ret = self.wiki(subject)
                dispatcher.utter_message(text=ret)
            except Exception as inst:
                print(inst)
                res = BBMessage(tracker.latest_message['text'])
                dispatcher.utter_message(text=res)
        return []
    def lookup(self, subject):
        print("searching dictionary")
        dictionary=PyDictionary()
        m = dictionary.meaning(subject)
        if m is None:
            return None
        else:
            ret = ""
            for i in m:
                ret += i + ": " + m[i][0] + '\n'
            return subject + ", " + ret
    def wiki(self, subject):
        data = get("https://en.wikipedia.org/w/api.php?action=opensearch&search="+subject+"&limit=1&namespace=0&format=json")
        a = loads(data.text)
        print(a)
        print("retrieving "+a[1][0])
        data = get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&titles="+a[1][0]+"&format=json")
        p = loads(data.text)["query"]["pages"]
        print(p)
        for i in p:
            txt = BeautifulSoup(p[i]["extract"],features="lxml").getText()
            print(txt)
            if (txt is None or len(txt) <= 5):
                continue
            return txt
            """ now we let the font-end to decide what to do
            print("txt="+txt)
            ret = txt
            if len(ret) > 200:
                ret = SumMessage(ret)
                if len(ret) < 50: # if it's too short, use original abstractfrom wiki
                    ret = txt
            ## url is a[3][0]
            if "." in ret:
                return ret[:ret.index(".")]
            else:
                return ret
            """
        return "Sorry I don't know what "+subject+" is."
