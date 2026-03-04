import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="LogicMaster Pro", layout="wide")

# -----------------------------
# Question Generators
# -----------------------------

def generate_math_questions(n=100):
    questions = []
    for i in range(n):
        a = random.randint(1, 50)
        b = random.randint(1, 50)
        op = random.choice(["+", "-", "*"])
        
        if op == "+":
            ans = a + b
        elif op == "-":
            ans = a - b
        else:
            ans = a * b
            
        questions.append({
            "question": f"What is {a} {op} {b}?",
            "answer": str(ans)
        })
    return questions


def generate_logic_questions(n=100):
    questions = []
    for i in range(n):
        num = random.randint(2, 10)
        series = [num * j for j in range(1, 5)]
        answer = num * 5
        
        questions.append({
            "question": f"Find next number: {series}",
            "answer": str(answer)
        })
    return questions


def generate_reasoning_questions(n=100):
    questions = []
    for i in range(n):
        age = random.randint(10, 40)
        future = age + 5
        
        questions.append({
            "question": f"Rahul is {age} years old. How old will he be in 5 years?",
            "answer": str(future)
        })
    return questions


def generate_critical_questions(n=100):
    questions = []
    for i in range(n):
        questions.append({
            "question": "If all cats are animals and some animals are black, are all cats black? (Yes/No)",
            "answer": "No"
        })
    return questions


# -----------------------------
# Initialize Questions
# -----------------------------

if "math" not in st.session_state:
    st.session_state.math = generate_math_questions()

if "logic" not in st.session_state:
    st.session_state.logic = generate_logic_questions()

if "reasoning" not in st.session_state:
    st.session_state.reasoning = generate_reasoning_questions()

if "critical" not in st.session_state:
    st.session_state.critical = generate_critical_questions()

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Math": 0,
        "Logic": 0,
        "Reasoning": 0,
        "Critical": 0
    }

# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Select Section", 
                        ["Math", "Logic", "Reasoning", "Critical Thinking", "Dashboard"])

# -----------------------------
# Quiz Section
# -----------------------------

def quiz_section(title, question_list):
    st.title(title)
    score = 0
    
    with st.form(key=title):
        user_answers = []
        
        for i, q in enumerate(question_list):
            ans = st.text_input(f"Q{i+1}: {q['question']}", key=f"{title}{i}")
            user_answers.append(ans)
        
        submit = st.form_submit_button("Submit Answers")
        
        if submit:
            for i, q in enumerate(question_list):
                if user_answers[i].strip().lower() == q["answer"].lower():
                    score += 1
                    
            st.success(f"Your Score: {score}/100")
            st.session_state.scores[title] = score


# -----------------------------
# Menu Handling
# -----------------------------

if menu == "Math":
    quiz_section("Math", st.session_state.math)

elif menu == "Logic":
    quiz_section("Logic", st.session_state.logic)

elif menu == "Reasoning":
    quiz_section("Reasoning", st.session_state.reasoning)

elif menu == "Critical Thinking":
    quiz_section("Critical", st.session_state.critical)

elif menu == "Dashboard":
    st.title("📊 Performance Dashboard")
    
    df = pd.DataFrame(list(st.session_state.scores.items()), 
                      columns=["Category", "Score"])
    
    st.dataframe(df)
    st.bar_chart(df.set_index("Category"))
    
    total = sum(st.session_state.scores.values())
    st.metric("Total Score (Out of 400)", total)