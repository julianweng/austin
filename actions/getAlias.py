import pandas as pd


def getAlias(questions, alias, indVar, dispatcher):
    questionsCopy = questions.copy()
    selVar = ""
    for index, row in alias.iterrows():
        differents = row["Alias"].split(",")
        for i in differents:
            if (i == indVar):
                selVar = row["Symbol"]
    questions = []
    for i in questionsCopy:
        if selVar in i.questionTexts.keys():
            questions.append(i)
    if (questions == []):
        questions = questionsCopy
        if indVar is not None:
            dispatcher.utter_message("This variable is not found")
    return(questions)
