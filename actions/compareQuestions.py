from sentence_transformers import SentenceTransformer, util

model = None
if not model:
    model = SentenceTransformer(
        'sentence-transformers/all-MiniLM-L6-v2')


def compareQuestions(qs, compare2):
    maxScore = 0
    testFormat = None
    for b in qs:
        for c in b.alias:
            v1 = str(c)
            v2 = str(compare2)
            embedding1 = model.encode(
                v1, convert_to_tensor=True, show_progress_bar=False)
            embedding2 = model.encode(
                v2, convert_to_tensor=True, show_progress_bar=False)
            # compute similarity scores of two embeddings
            cosine_scores = util.pytorch_cos_sim(
                embedding1, embedding2)
            score = cosine_scores.item()
            if (score > maxScore):
                maxScore = score
                testFormat = b
    return testFormat

def compareGeneric(word1, word2):
    embedding1 = model.encode(
        word1, convert_to_tensor=True, show_progress_bar=False)
    embedding2 = model.encode(
        word2, convert_to_tensor=True, show_progress_bar=False)
    # compute similarity scores of two embeddings
    cosine_scores = util.pytorch_cos_sim(
        embedding1, embedding2)
    score = cosine_scores.item()
    return score
