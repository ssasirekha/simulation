import streamlit as st
import pandas as pd

st.set_page_config(page_title="Responsible AI Decision Lab", page_icon="⚖️", layout="wide")

# ---------- Session ----------
defaults = {
    "score": 0,
    "completed": set(),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def complete(case_id, points=10):
    if case_id not in st.session_state.completed:
        st.session_state.completed.add(case_id)
        st.session_state.score += points

def principle_box(title, text):
    st.info(f"**Responsible AI principle: {title}**\n\n{text}")

# ---------- Header ----------
st.title("⚖️ Responsible AI Decision Lab")
st.subheader("Can an AI system be accurate—and still be irresponsible?")
st.write(
    "In this simulation, you are responsible for deciding whether AI systems should be "
    "deployed. Make a decision first, observe its consequences, identify the ethical issue, "
    "and then improve the system."
)

with st.expander("Learning outcomes"):
    st.markdown("""
By the end of the simulation, you should be able to:
- identify fairness and bias risks;
- recognize the need for transparency and explainability;
- apply privacy and data-governance thinking;
- explain the importance of safety, accountability and human oversight;
- use generative AI responsibly in education; and
- apply Ethics-by-Design across the AI lifecycle.
""")

st.caption(f"Progress: {len(st.session_state.completed)}/6 activities completed")

tabs = st.tabs([
    "1. Recruitment",
    "2. Loan Decision",
    "3. Student Analytics",
    "4. Healthcare",
    "5. Generative AI",
    "6. Ethics-by-Design",
    "Reflection"
])

# ---------- CASE 1 ----------
with tabs[0]:
    st.header("Case 1 — AI Recruitment: The Best Candidate?")
    st.write(
        "A company receives 1,000 applications. An AI model trained on historical hiring "
        "decisions is used to shortlist candidates. The model reports **92% historical accuracy**."
    )
    df = pd.DataFrame({
        "Candidate": ["A", "B", "C", "D"],
        "Experience (years)": [5, 6, 4, 7],
        "Technical Score": [86, 91, 82, 94],
        "Career Break": ["No", "2 years", "No", "3 years"],
        "AI Decision": ["Shortlisted", "Rejected", "Shortlisted", "Rejected"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

    decision = st.radio(
        "You are responsible for deployment. What will you do?",
        ["Select an option", "Deploy the model", "Investigate further"],
        key="recruit"
    )
    if decision != "Select an option":
        complete("recruit")
        if decision == "Deploy the model":
            st.error("⚠️ A high accuracy score has hidden an important fairness problem.")
        else:
            st.success("Good investigation step. Aggregate accuracy alone does not establish fairness.")

        st.markdown("### What the audit reveals")
        st.write(
            "Historical hiring data contained fewer successful applicants with career breaks. "
            "The model learned this historical pattern and treated career breaks as a negative signal."
        )
        st.warning(
            "The developers did not explicitly instruct the model to discriminate. Bias can nevertheless "
            "be reproduced through training data."
        )

        if st.button("Apply fairness mitigation", key="fairfix"):
            after = df.copy()
            after.loc[after["Candidate"] == "B", "AI Decision"] = "Shortlisted"
            after.loc[after["Candidate"] == "D", "AI Decision"] = "Review Required"
