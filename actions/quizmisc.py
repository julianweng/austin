from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUttered, FollowupAction, ActionExecuted
import random
import requests
import json
from bs4 import BeautifulSoup
from PyDictionary import PyDictionary
from actions.base import BBMessage
import pandas as pd
import sys
from . import generateQ as gq
from sentence_transformers import SentenceTransformer, util
from . import generateQ as gq
from . import compareQuestions as cq
from . import getAlias as ga
import sqlite3 as sl
con = sl.connect('quizhistory.db')


def miscQuestions():
    # global questionsDict
    # questionsDict = {}
    questionData = pd.read_csv("actions/quiz/questions.csv")
    for index, row in questionData.iterrows():
        for index, row in questionData.iterrows():
            equation = row["Equation"]
            category = row["Category"]
            alias = row["Alias"].split(",")
            questionTextsRaw = row["QuestionTexts"].split("#")
            questionTexts = {}
            for i in questionTextsRaw:
                pair = i.split(":")
                questionTexts[pair[0].strip(" ")] = pair[1]
            questions.append(gq.QFormat(
                equation, category, alias, questionTexts, index))


class ActionQuizProgress(Action):  # not really used
    def name(self) -> Text:
        return "action_quizprogress"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            global questions
            questions = []
            miscQuestions()
            testFormat = cq.compareQuestions(
                questions, tracker.get_slot('problemType'))
            intent_name = tracker.latest_message["intent"]["name"]
            dispatcher.utter_message("chungus")
            if (tracker.get_slot('problemType') is not None and tracker.get_slot('independentVar') is None):
                with con:
                    df = pd.read_sql(
                        "SELECT * FROM USER WHERE qid == " + str(testFormat.index), con)
            if (tracker.get_slot('problemType') is None and tracker.get_slot('independentVar') is not None):
                indVar = tracker.get_slot('independentVar')
                alias = pd.read_csv("actions/quiz/alias.csv")
                selVar = ""
                for index, row in alias.iterrows():
                    differents = row["Alias"].split(",")
                    for i in differents:
                        if (i == indVar):
                            selVar = row["Symbol"]
                with con:
                    df = pd.read_sql(
                        'SELECT * FROM USER WHERE var == "' + selVar + '"', con)
                if(len(df.index) == 0):
                    dispatcher.utter_message("Variable not found.")
                    with con:
                        df = pd.read_sql(
                            "SELECT * FROM USER", con)
            elif (tracker.get_slot('problemType') is None and tracker.get_slot('independentVar') is None):
                with con:
                    df = pd.read_sql(
                        "SELECT * FROM USER", con)

            right = 0
            total = 0
            for index, row in df.iterrows():
                right += row["right"]
                total += 1

            print(df)
            dispatcher.utter_message(
                "You have gotten " + gq.oneDec(str(100*right/total))+"% of these questions right")

        except Exception as inst:
            print(inst)
            res = BBMessage(tracker.latest_message['text'])
            dispatcher.utter_message(text=res)
            # dispatcher.utter_message(text='Ask me again tomorrow')
        return []
