import streamlit as st
import requests
import json

# Function to fetch MCQ questions from the API
def fetch_questions(subject_name):
    url = 'https://api.hyperleap.ai/prompts'
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='
    }
    data = {
        "promptId": "4e51e8b3-f6eb-41bb-8f0f-e92a910e7caf",
        "promptVersionId": "7e014386-e0ff-43cd-89de-bdff820e2f3d",
        "replacements": {
            "subject": subject_name
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return None

# Function to parse questions, options, and answers
def parse_questions(content):
    questions_data = json.loads(content)  # Safely parse JSON content
    questions = questions_data['questions']
    return questions

# Streamlit App
def main():
    st.title("MCQ Test")
    
    subject_name = st.text_input("Enter the subject name:")
    
    if st.button("Fetch Questions"):
        if subject_name:
            questions_content = fetch_questions(subject_name)
            
            if questions_content:
                questions = parse_questions(questions_content)
                total_questions = len(questions)
                user_answers = {}
                score = 0

                for i, question in enumerate(questions, 1):
                    st.subheader(f"Question {i}/{total_questions}:")
                    st.write(question['question'])
                    options = question['options']
                    selected_option = st.radio("Options:", options, key=f"question_{i}")
                    user_answers[i] = selected_option
                    if selected_option == question['answer']:
                        score += 1

                st.write("Your Score:", score, "/", total_questions)
                st.write("Thanks for taking the test!")
            else:
                st.error("Failed to fetch questions. Please try again later.")
        else:
            st.warning("Please enter a subject name.")

if __name__ == "__main__":
    main()
