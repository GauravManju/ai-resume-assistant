from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_semantic_similarity(resume_text, job_description_text):
    resume_embedding = model.encode(resume_text)
    job_embedding = model.encode(job_description_text)

    similarity = util.cos_sim(resume_embedding, job_embedding)

    return float(similarity[0][0])