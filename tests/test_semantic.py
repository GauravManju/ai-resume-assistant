from src.semantic import calculate_semantic_similarity


def test_similar_texts_score_higher_than_unrelated_texts():
    resume = "Experienced Python developer skilled in machine learning and data pipelines."
    matching_job = "Looking for a Python developer with machine learning experience."
    unrelated_job = "Seeking a pastry chef with experience in French baking techniques."

    matching_score = calculate_semantic_similarity(resume, matching_job)
    unrelated_score = calculate_semantic_similarity(resume, unrelated_job)

    assert matching_score > unrelated_score
