from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUttered, FollowupAction, ActionExecuted
import random
import requests
import json
from actions.base import BBMessage
import pandas as pd
import sys
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


incorrect = []
ind = 0


class ActionAnswer(Action):
    def name(self) -> Text:
        return "action_answer"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sql = 'INSERT INTO USER (qid, var, right) values(?, ?, ?)'
        response = tracker.get_slot('answer')  # the given answer
        SlotSet("answer", "None")
        co = tracker.get_slot('correct')
        if response == co:
            data = [
                (QIndex, tracker.get_slot("trueVar"), 1),
            ]
            with con:
                con.executemany(sql, data)
            dispatcher.utter_message(text="Correct!")
            with con:
                con.executemany(sql, data)
            return [SlotSet("answer", None), SlotSet("independentVar", None), SlotSet("problemType", None), UserUttered(text="You got it right! (respond with 'stop' to exit)", parse_data={"intent": {"name": "demquiz", "confidence": 0.95}})] + [ActionExecuted("action_listen")]
        elif response == "stop":
            dispatcher.utter_message(text="Stopping!")
            return[SlotSet("answer", None),SlotSet("independentVar", None), SlotSet("problemType", None),]
        else:
            data = [
                (QIndex, tracker.get_slot("trueVar"), 0),
            ]
            with con:
                con.executemany(sql, data)
            dispatcher.utter_message(text="Wrong! Correct answer is '"+co+"'")
            return [SlotSet("answer", None), SlotSet("independentVar", None), SlotSet("problemType", None), UserUttered(text="You got it wrong! (respond with 'stop' to exit)", parse_data={"intent": {"name": "demquiz", "confidence": 0.95}})] + [ActionExecuted("action_listen")]


class ActionQuestion(Action):
    def name(self) -> Text:
        return "action_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # testFormat = gq.QFormat()
        global questions
        questions = []
        miscQuestions()
        global selectedVariable
        selectedVariable = None
        indVar = tracker.get_slot('independentVar')
        questions = ga.getAlias(questions.copy(), pd.read_csv(
            "actions/quiz/alias.csv"), indVar, dispatcher)
        testFormat = random.choice(questions)
        if (tracker.get_slot('problemType') is not None):  # Get most similar problem type
            testFormat = cq.compareQuestions(
                questions, tracker.get_slot('problemType'))

        global QIndex
        QIndex = testFormat.index
        testQuestion = 0
        testQuestion = gq.Question(
            testFormat, selectedVariable, dispatcher)
        testQuestion.generate()
        question = testQuestion.questionText
        incorrect = testQuestion.wrongAnswers
        cor = testQuestion.correctAnswer
        correct_answer = random.randrange(0, len(incorrect))
        le = len(incorrect) + 1
        buttons = []
        for i in range(0, correct_answer):
            buttons.append({"payload": incorrect[i], "title": incorrect[i]})
        buttons.append({"payload": cor, "title": cor})
        for d in range(correct_answer+1, le):
            buttons.append(
                {"payload": incorrect[d-1], "title": incorrect[d-1]})
        dispatcher.utter_message(text=question, buttons=buttons)

        return [SlotSet("correct", cor), SlotSet("problemType", None), SlotSet("trueVar", testQuestion.selectedVariable)]
