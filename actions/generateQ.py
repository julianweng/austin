import random
import pandas as pd
from rasa_sdk.executor import CollectingDispatcher
from sympy import *
import math


def miscAlias():
    global aliasDict
    aliasDict = {}
    alias = pd.read_csv("actions/quiz/alias.csv")
    for index, row in alias.iterrows():
        differents = row["Alias"].split(",")
        # insert check if symbol is in the equation, if not, don't add it
        # also insert check to see if it repeats
        for i in differents:
            aliasDict[i] = row["Symbol"]


def oneDec(st):
    a = st.split('.')
    if(len(a) > 1):
        if(len(a[1]) > 1):
            return a[0] + '.' + a[1][0]
        else:
            return a[0] + '.' + a[1]
    else:
        return a[0] + '.0'


class Question:
    questionText = {}
    wrongAnswers = []
    correctAnswer = ""
    answersNum = 0
    otherVariables = {}
    selectedVariable = ""
    dispatcher = None

    def __init__(self, form, independentVar, dispatcher):
        self.form = form
        self.selectedVariable = independentVar
        self.dispatcher = dispatcher

    def generate(self):
        questionTexts = self.form.questionTexts
        equation = self.form.equation
        vars = list(questionTexts.keys())

        if(self.selectedVariable is None):
            self.selectedVariable = random.choice(vars)

        self.questionText = questionTexts[self.selectedVariable]
        vars.remove(self.selectedVariable)
        eq = Eq(*map(S, equation.split('=', 1)))

        variableSymbols = dict([(i.name, i) for i in eq.free_symbols])

        for i in vars:
            rando = random.randint(2, 20)
            self.otherVariables[i] = rando
            self.questionText = self.questionText.replace("&"+i, str(rando))
            eq = eq.subs(variableSymbols[i], rando)

        solution = solve(eq, variableSymbols[self.selectedVariable])
        bestSolution = N(solution[0], 1)
        for i in solution:
            solved = N(i, 4)
            if(solved > 0):
                bestSolution = solved
        self.correctAnswer = oneDec(str(bestSolution))
        self.wrongAnswers = []
        for i in range(4):
            # self.wrongAnswers.append(str(0))
            ra = round(random.uniform(-3, 3), 2)
            while (abs(ra) < 0.2):
                ra = round(random.uniform(-3, 3), 2)
            # rounded = (math.trunc(10.0*(bestSolution + ra)))/10.0

            self.wrongAnswers.append(
                oneDec(str(abs(bestSolution + ra)))
            )


class QFormat:
    questionTexts = {  # variables are the keys
        "M": "It takes &F N to accelerate a ball &A m/s/s. What is its mass?",
        "A": "A force of &F N is applied on a ball of &M kg mass. What is its acceleration?",
        "F": "Krishin pushes a toddler of &M kg mass, accelerating him &A m/s/s down the stairs. What is the force required?"
    }
    equation = "F=M*A"
    alias = ["F equals m a", "Force equals mass times acceleration"]
    category = "Kinematics"
    index = None

    def __init__(self, equation, category, alias, questionTexts, index):
        self.questionTexts = questionTexts
        self.category = category
        self.alias = alias
        self.equation = equation
        self.index = index
