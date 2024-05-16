import streamlit as st
import requests
import json

st.title("Courses")

# Function to fetch content data
def fetch_content_data(subtopic_name, subject_name):
    # Define the API endpoint for content
    CONTENT_API_URL = 'https://api.hyperleap.ai/prompts'

    # Define your API key
    API_KEY = 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='

    # Define the payload for content generation
    payload = {
        "promptId": "f937db13-4d95-43f0-9e71-1dda1dc146ea",
        "promptVersionId": "2e58658d-e8ca-44ee-814e-29c4a81095be",
        "replacements": {
            "subtopic": subtopic_name,
            "subject": subject_name
        }
    }

    # Define headers
    headers = {
        "accept": "application/json",
        "x-hl-api-key": API_KEY,
        "content-type": "application/json"
    }

    # Make the POST request
    response = requests.post(CONTENT_API_URL, data=json.dumps(payload), headers=headers)
    return response

# Text input for course name
name = st.text_input("Enter the course name:")

# Submit button
if st.button("Submit"):
    # Print the name below the input field
    #st.write(f"Your name is: {name}")

    # Define the API endpoint
    url = 'https://api.hyperleap.ai/prompts'

    # Define your API key
    api_key = 'M2Y2OTE3MTQzZGUxNDE5ZmFjNWI0YmRmNzE4NzU5NWY='

    # Convert the name to a string
    name_str = str(name)

    # Define the request body
    payload = {
        "promptId": "81590497-4e97-42e3-b8d7-901c65d24f1f",
        "promptVersionId": "989d1c23-1cb3-4092-ba9b-4fcd456fdd08",
        "replacements": {
            "subject": name_str
        }
    }

    # Define headers
    headers = {
        'Content-Type': 'application/json',
        'x-hl-api-key': api_key
    }

    def fetch_course_data():
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        return response

    res = fetch_course_data()

    # Check if the request was successful (status code 200)
    if res.status_code == 200:
        # Parse the JSON response
        course_data = json.loads(res.json()["choices"][0]["message"]["content"])
        
        # Store course data and name in session state to persist between reruns
        st.session_state['course_data'] = course_data
        st.session_state['course_name'] = name_str

# Load course data from session state if available
if 'course_data' in st.session_state:
    course_data = st.session_state['course_data']
    course_name = st.session_state['course_name']
    
    # Get a list of chapter names
    chapter_names = [chapter["chapterName"] for chapter in course_data[0]["chapters"]]

    # Create dropdown menu for chapters
    selected_chapter_index = st.selectbox("Select a chapter:", range(len(chapter_names)), format_func=lambda x: chapter_names[x])

    # Access the selected chapter data using the selected index
    selected_chapter = course_data[0]["chapters"][selected_chapter_index]

    # Display subtopics 
    st.write(f"Subtopics for {selected_chapter['chapterName']}:")

    for subtopic in selected_chapter["subTopics"]:
        # Add a button or clickable element for each subtopic
        if st.button(subtopic):
            # Fetch and display content data when the subtopic button is clicked
            res = fetch_content_data(subtopic, course_name)
            st.write("Response status code:", res.status_code)  # Debugging statement
            #st.write("Response content:", res.content)  # Debugging statement

            if res.status_code == 200:
                try:
                    # Decode the bytes content into a string
                    content_str = res.content.decode('utf-8')
                    res_json = json.loads(content_str)
                    
                    # Get the content message from the JSON response
                    content_message = res_json["choices"][0]["message"]["content"]

                    # Display the generated content
                    st.header(subtopic)
                    st.write(content_message)
                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Failed to parse content data: {str(e)}")
            else:
                st.error(f"Failed to fetch content data. Status code: {res.status_code}")
else:
    st.write("No course data available. Please submit a course name.")