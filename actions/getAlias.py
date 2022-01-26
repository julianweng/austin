import pandas as pd


def getAlias(questions, alias, indVar, selectedVariables, dispatcher):
    questionsCopy = questions.copy()
    selVar = ""
    for index, row in alias.iterrows():
        differents = row["Alias"].split(",")
        for i in differents:
            if (i == indVar):
                selVar = row["Symbol"]
                selectedVariables.append(row["Symbol"])
    questions = []
    for i in questionsCopy:
        for j in selectedVariables:
            if j in i.questionTexts.keys():
                questions.append(i)
    if (questions == []):
        questions = questionsCopy
        if indVar is not None:
            dispatcher.utter_message("This variable is not found")
    return(questions)

def getCategory(questions, indVar):  #LOOP THROUGH ALL QFORMATS AND ADD ALL WHICH MATCH WITH CATEGORIES
    questionsCopy = questions.copy()
    questions = []
    for q in questionsCopy:
        if q.category == indVar:
            questions.append(q)
    return questions