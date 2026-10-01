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
            st.markdown("#### After feature review and fairness testing")
            st.dataframe(after, use_container_width=True, hide_index=True)
            st.success("Candidate B is no longer automatically rejected; Candidate D receives human review.")

        principle_box(
            "Fairness and Bias Mitigation",
            "AI systems learn from data that may contain historical or societal bias. Fairness should be "
            "considered during data collection, development, testing and deployment."
        )
        st.markdown("**Reflect:** What could happen if nobody examined outcomes across different groups?")

# ---------- CASE 2 ----------
with tabs[1]:
    st.header("Case 2 — AI Loan Approval: Why Was I Rejected?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Applicant")
        st.metric("Monthly income", "₹75,000")
        st.metric("Credit score", "760")
        st.write("**Employment:** Permanent")
        st.write("**Existing debt:** Low")
        st.write("**Loan requested:** ₹5 lakh")
    with c2:
        st.markdown("#### AI Result")
        st.error("LOAN REJECTED")
        st.write("The applicant receives no explanation.")

    enough = st.radio(
        "Is the decision alone sufficient information for the applicant?",
        ["Select an option", "Yes", "No — an explanation is needed"],
        key="loan"
    )
    if enough != "Select an option":
        complete("loan")
        if enough == "Yes":
            st.warning("For a consequential decision, a result without an explanation may be difficult to understand or challenge.")
        else:
            st.success("Now examine the factors influencing the model.")

        if st.button("Explain AI decision", key="explainloan"):
            factors = pd.DataFrame({
                "Factor": ["Debt-to-income ratio", "Repayment history", "Credit utilization", "Residential-area proxy"],
                "Illustrative influence": ["+25%", "+20%", "+15%", "−35%"]
            })
            st.dataframe(factors, hide_index=True, use_container_width=True)
            st.error("The residential-area proxy has a surprisingly strong negative influence.")
            review = st.radio(
                "What should happen next?",
                ["Accept the result", "Review the feature and its justification", "Hide the feature from the applicant"],
                key="loanreview"
            )
            if review == "Review the feature and its justification":
                st.success("This supports scrutiny of whether the feature is relevant, justified and potentially unfair.")
            elif review != "Accept the result":
                st.warning("Hiding information does not resolve the underlying governance issue.")

        principle_box(
            "Transparency and Explainability",
            "When AI makes an important decision, affected people may need to understand why the decision was made."
        )
        st.markdown("**Reflect:** Should a person be able to question or appeal an important automated decision?")

# ---------- CASE 3 ----------
with tabs[2]:
    st.header("Case 3 — Student Analytics: Useful Data or Privacy Risk?")
    st.write(
        "An institution wants to identify students who may need academic support. "
        "Choose the data you would allow the AI system to collect."
    )

    options = [
        "Attendance",
        "Academic performance",
        "Assignment submission",
        "Location history",
        "Social-media activity",
        "Personal messages",
        "Medical information"
    ]
    selected = st.multiselect(
        "Select data sources",
        options,
        default=["Attendance", "Academic performance", "Assignment submission"],
        key="privacy"
    )

    intrusive = {"Location history", "Social-media activity", "Personal messages", "Medical information"}
    intrusive_count = len(set(selected) & intrusive)
    accuracy = min(94, 88 + len(selected))
    privacy_risk = "LOW" if intrusive_count == 0 else ("MEDIUM" if intrusive_count <= 2 else "HIGH")

    c1, c2 = st.columns(2)
    c1.metric("Illustrative prediction accuracy", f"{accuracy}%")
    c2.metric("Privacy risk", privacy_risk)

    if st.button("Evaluate my data choices", key="privacy_eval"):
        complete("privacy")
        if intrusive_count == 0:
            st.success("You selected task-relevant academic data and avoided the more intrusive sources in this scenario.")
        else:
            st.warning(
                f"You selected {intrusive_count} potentially intrusive data source(s). "
                "Ask whether each item is necessary for the stated purpose."
            )
        st.markdown("### Data-governance questions")
        st.markdown("""
- What data are we collecting?
- Why is each item necessary?
- How will it be stored?
- Who can access it?
- How will it be protected?
- How long should it be retained?
""")

    principle_box(
        "Privacy and Data Governance",
        "Responsible AI considers data necessity, purpose, storage, access and protection from the beginning of development."
    )
    st.markdown(
        "**Reflect:** If removing intrusive data slightly reduced accuracy but substantially reduced privacy risk, "
        "how would you justify your decision?"
    )

# ---------- CASE 4 ----------
with tabs[3]:
    st.header("Case 4 — Healthcare AI: AI Says 'Low Risk'")
    st.write("A clinical decision-support model evaluates a patient.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Patient")
        st.write("**Age:** 52")
        st.write("**Symptom:** Mild chest discomfort")
    with c2:
        st.markdown("#### Model output")
        st.success("Predicted cardiac risk: LOW — 12%")

    action = st.radio(
        "What should happen next?",
        ["Select an option", "Discharge based only on AI output", "Doctor reviews the patient and AI output"],
        key="health"
    )
    if action != "Select an option":
        complete("health")
        if action == "Discharge based only on AI output":
            st.error("⚠️ The decision relies on the model without sufficient human oversight.")
        else:
            st.success("Human oversight is retained for a consequential clinical decision.")

        st.markdown("### Additional information revealed")
        st.warning(
            "The patient belongs to a demographic group that was poorly represented in the model's training data."
        )
        st.write(
            "The clinician therefore considers the AI output together with clinical evidence and additional testing."
        )
        st.info("**Key idea:** Model confidence is not the same as clinical certainty.")

        principle_box(
            "Safety, Robustness, Accountability and Human Oversight",
            "AI used in critical applications should be tested for unexpected conditions and failures, while responsibility "
            "for consequential decisions remains clearly defined."
        )

# ---------- CASE 5 ----------
with tabs[4]:
    st.header("Case 5 — Generative AI in Education: It Looks Correct")
    st.write(
        "A student asks a generative AI system: **'Give me three recent research papers about AI-based adaptive learning.'**"
    )
    refs = pd.DataFrame({
        "AI-generated reference": [
            "Reference A — convincing title and journal",
            "Reference B — convincing title and journal",
            "Reference C — convincing title and journal"
        ],
        "Displayed by AI": ["Looks valid", "Looks valid", "Looks valid"]
    })
    st.dataframe(refs, hide_index=True, use_container_width=True)

    gen_action = st.radio(
        "What should the student do?",
        ["Select an option", "Use the references directly", "Verify the references before using them"],
        key="genai"
    )
    if gen_action != "Select an option":
        complete("genai")
        if gen_action == "Use the references directly":
            st.error("Appearance and fluent wording are not evidence that a reference is genuine.")
        else:
            st.success("Verification is an essential part of responsible use.")

        if st.button("Verify references", key="verifyrefs"):
            checked = pd.DataFrame({
                "Reference": ["A", "B", "C"],
                "Verification result": ["❌ Does not exist", "✅ Valid", "❌ Incorrect authors/title"]
            })
            st.dataframe(checked, hide_index=True, use_container_width=True)
            st.warning("AI-generated information can sound authoritative even when it is incorrect.")

        st.markdown("#### Responsible workflow")
        st.write("**Generate → Verify → Check original sources → Use appropriately → Cite correctly**")
        principle_box(
            "Responsible AI Use in Education",
            "Learners should verify AI-generated information, avoid plagiarism, maintain academic integrity and continue "
            "developing their own critical thinking."
        )

# ---------- CASE 6 ----------
with tabs[5]:
    st.header("Case 6 — Ethics-by-Design Challenge")
    st.write(
        "Your institution plans an AI system that predicts student performance and recommends academic interventions. "
        "Configure the safeguards **before deployment**."
    )

    safeguards = {
        "Fairness testing": st.toggle("Fairness testing", value=False),
        "Explainability": st.toggle("Explainability", value=False),
        "Privacy protection": st.toggle("Privacy protection", value=False),
        "Human oversight": st.toggle("Human oversight", value=False),
        "Security testing": st.toggle("Security testing", value=False),
        "Continuous monitoring": st.toggle("Continuous monitoring", value=False),
        "Social/environmental impact review": st.toggle("Social/environmental impact review", value=False),
    }

    n = sum(safeguards.values())
    risk = "HIGH" if n <= 2 else ("MEDIUM" if n <= 5 else "CONTROLLED")
    accountability = "Defined" if safeguards["Human oversight"] and safeguards["Continuous monitoring"] else "Unclear"
    explainability = "High" if safeguards["Explainability"] else "Low"
    privacy = "Lower" if safeguards["Privacy protection"] else "High"
    fairness = "Reviewed" if safeguards["Fairness testing"] else "Not assessed"

    st.markdown("### Responsible AI Dashboard")
    dash = pd.DataFrame({
        "Indicator": ["Technical accuracy", "Fairness risk", "Privacy risk", "Explainability", "Accountability", "Overall governance risk"],
        "Status": ["94% (illustrative)", fairness, privacy, explainability, accountability, risk]
    })
    st.dataframe(dash, hide_index=True, use_container_width=True)

    if st.button("Evaluate deployment readiness", key="ethics_eval"):
        complete("ethics")
        if n == 7:
            st.success("All seven safeguards have been considered before deployment.")
        elif n >= 5:
            st.warning("Several safeguards are present, but review the controls that remain disabled.")
        else:
            st.error("Important Responsible AI safeguards are still missing.")

        st.markdown("### Ethics-by-Design")
        st.write(
            "Ethical risks should be considered while defining the problem, selecting data, developing the model, "
            "testing, deploying and monitoring—not added only after harm occurs."
        )

    st.info("**Central message:** The most accurate AI system is not necessarily the most responsible AI system.")

# ---------- REFLECTION ----------
with tabs[6]:
    st.header("Final Reflection — Move from 'Can We?' to 'Should We?'")
    st.markdown("""
### Before deploying an AI system, ask:

**CAN we build it?**  
↓  
**SHOULD we build it?**  
↓  
**Who could be affected?**  
↓  
**Could it create unfair outcomes?**  
↓  
**How will privacy and human rights be protected?**  
↓  
**Can important decisions be explained?**  
↓  
**Who is accountable?**  
↓  
**Where is human oversight needed?**
""")

    st.markdown("---")
    st.subheader("Quick knowledge check")

    q1 = st.radio(
        "1. Why can AI produce discriminatory outcomes even without intentional bias?",
        [
            "Select an answer",
            "Because AI always makes random decisions",
            "Because training data may contain historical or societal bias",
            "Because accuracy automatically creates discrimination"
        ],
        key="q1"
    )
    q2 = st.radio(
        "2. What is the black-box problem?",
        [
            "Select an answer",
            "The difficulty of understanding how a complex model reached a decision",
            "A computer hardware failure",
            "A method for encrypting training data"
        ],
        key="q2"
    )
    q3 = st.radio(
        "3. What does Ethics-by-Design mean?",
        [
            "Select an answer",
            "Adding ethics only after deployment",
            "Avoiding AI in all high-impact applications",
            "Incorporating ethical considerations throughout the AI lifecycle"
        ],
        key="q3"
    )

    if st.button("Submit knowledge check"):
        correct = 0
        correct += q1 == "Because training data may contain historical or societal bias"
        correct += q2 == "The difficulty of understanding how a complex model reached a decision"
        correct += q3 == "Incorporating ethical considerations throughout the AI lifecycle"
        st.metric("Knowledge-check score", f"{correct}/3")
        if correct == 3:
            st.success("Excellent. You identified the core Responsible AI concepts.")
        else:
            st.info("Review the case studies and try again. Focus on bias, explainability and Ethics-by-Design.")

    st.markdown("---")
    st.subheader("Your Responsible AI Decision")
    reflection = st.text_area(
        "In 2–3 sentences, explain what you would check before deploying an AI system that affects people."
    )
    if reflection:
        st.success("Reflection recorded for this session.")

    st.markdown("### Take-away")
    st.success(
        "Responsible AI is not about preventing innovation. It is about ensuring that innovation happens responsibly—"
        "with fairness, transparency, privacy, accountability, safety, human oversight, and attention to wider social impact."
    )

st.sidebar.title("Responsible AI")
st.sidebar.metric("Activities completed", f"{len(st.session_state.completed)}/6")
st.sidebar.metric("Participation points", st.session_state.score)
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Simulation pathway**

1. Fairness & Bias  
2. Transparency & Explainability  
3. Privacy & Data Governance  
4. Safety & Human Oversight  
5. Responsible GenAI Use  
6. Ethics-by-Design
""")
st.sidebar.caption("Educational simulation: values and outcomes are illustrative.")
