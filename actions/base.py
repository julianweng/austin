from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
mname = 'facebook/blenderbot-400M-distill'
bbmodel = BlenderbotForConditionalGeneration.from_pretrained(mname)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)

""" not used for now. use first sentence instead
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
sumname = "snrspeaks/t5-one-line-summary"
summodel = AutoModelForSeq2SeqLM.from_pretrained(sumname)
sumtokenizer = AutoTokenizer.from_pretrained(sumname)

def SumMessage(msg):
    input_ids = sumtokenizer.encode("summarize: " + msg, return_tensors="pt", add_special_tokens=True, max_length=1024, truncation=True)
    generated_ids = summodel.generate( input_ids=input_ids,num_beams=5,max_length=200,repetition_penalty=2.5,length_penalty=1,early_stopping=True,num_return_sequences=2)
    preds = [sumtokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    print(preds)
    return preds[0]
"""


def SumMessage(msg):
    return msg


def BBMessage(msg):
    inputs = tokenizer([msg], return_tensors='pt')
    reply_ids = bbmodel.generate(**inputs)
    msg = tokenizer.batch_decode(reply_ids)[0].replace(
        "<s>", "").replace("</s>", "")
    return msg


class ActionDefault(Action):

    def name(self) -> Text:
        return "action_default"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        res = BBMessage(tracker.latest_message['text'])
        dispatcher.utter_message(text=res)
        return []
