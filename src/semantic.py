import streamlit as st
from sentence_transformers import SentenceTransformer, util


@st.cache_resource(show_spinner=False)
def _load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_description_text):
    model = _load_model()
    resume_embedding = model.encode(resume_text)
    job_embedding = model.encode(job_description_text)

    similarity = util.cos_sim(resume_embedding, job_embedding)

    return float(similarity[0][0])