import streamlit as st



# Set Streamlit page configuration
st.set_page_config(page_title="Email Harmony")
st.title("Email Harmony")
# st.subheader("Problem Statement:")
# st.markdown('''<p>The increasing volume of emails poses a significant challenge for users, leading to email overload, missed deadlines, and reduced productivity.
#             Existing email management solutions lack a unified approach and struggle to adapt to individual preferences, hindering efficient organization and response times.</p>''', unsafe_allow_html=True)

# st.subheader("Solution Overview:")
# st.markdown('''<p>Email Harmony is an innovative email management platform that integrates seamlessly with Gmail and other email platforms using Mail APIs. This solution goes beyond conventional email clients by leveraging Mail's unified API to provide a holistic, personalized, 
#             and intelligent email management experience. Key features include advanced categorization, real-time updates, and integration with artificial intelligence for smart insights.</p>''',unsafe_allow_html=True)

# st.subheader("Impact:")
# st.markdown('''<p>Email Harmony aims to revolutionize how users interact with their emails, offering a solution that adapts to individual preferences and behaviors. By intelligently categorizing emails, providing real-time updates, and incorporating AI-driven insights, the platform empowers users to regain control 
#             over their email inboxes, leading to improved efficiency, reduced stress, and enhanced overall productivity.</p>''',usage_allow_html=True)

# st.subheader("Innovation:")
# st.markdown('''<p>The innovation lies in the combination of Mail's powerful API capabilities and the integration of artificial intelligence. Email Harmony employs advanced NLP models for context-aware email understanding, sentiment analysis for personalized responses, and machine learning algorithms 
#             that evolve based on individual user preferences. This amalgamation results in a dynamic and user-centric email management solution.</p>''',usage_allow_html=True)

# st.subheader("Feasibility:")
#st.markdown('''<p>The feasibility of Email Harmony is bolstered by the robust infrastructure provided by Mail API's. Leveraging Mail ensures compatibility with a variety of email platforms, reducing development complexity. The platform can be incrementally developed, with an initial focus on essential features
            # and subsequent enhancements based on user feedback. The scalability is inherent, allowing the solution to accommodate an increasing user base seamlessly.</p>''',usage_allow_html=True)
st.header("Objective:")
st.markdown('''The primary goal of our project is to enhance the Gmail experience by integrating artificial intelligence (AI) capabilities. We have identified three main features to achieve this objective:''')
st.header("Automation using Webhooks:")
st.markdown('''Description:\n\nWebhooks provide a mechanism for automating processes in real-time based on events that occur in Gmail. Through this feature, users can set up triggers and actions to automate various tasks, improving efficiency and reducing manual efforts.\n
Functionality:\n''')
bullet_points = [
"Users can define specific events (e.g., new email received, email marked as important) as triggers.",
"Define corresponding actions to be taken automatically in response to the triggers (e.g., forward email to another address, categorize emails, etc.).",
"Real-time automation ensures seamless and efficient processing of emails."]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))
st.header("Ask Mail - Natural Language Query:")
st.markdown("Description:")
st.markdown('''The "Ask Mail" feature leverages natural language processing (NLP) to enable users to interact with their Gmail account using human-like queries. The system understands user intent and retrieves relevant information from emails.''')
st.markdown("Functionality:")
bullet_points = [
"Users can ask questions or provide commands in natural language, and the system interprets these queries.",
"NLP algorithms process the queries to understand user intent, allowing for tasks such as searching for specific emails, filtering emails by criteria, and extracting information.",
"The system responds with relevant information or performs actions based on the user's request, providing a conversational and user-friendly experience."]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.header("Chat - Intelligent Email Interaction:")
st.markdown("Description:")
st.markdown('''The Chat feature introduces a conversational interface that enables users to interact with their Gmail account in a chat-like manner. The system understands specific intents related to fetching, sending emails, and managing events.''')
st.markdown("Functionality:")
st.markdown("Fetch Mail:")
bullet_points = [
    "Users can instruct the system to retrieve specific emails based on criteria such as sender, subject, or date range.",
    "The system communicates with Gmail, fetches the relevant emails, and presents them to the user in a chat-like format."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))
st.markdown("Send Mail:")
bullet_points = [
    "Users can compose and send emails by providing instructions in a conversational format.",
    "The system processes the instructions, creates the email, and sends it on behalf of the user.",
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.markdown("Fetch All Unread:")
bullet_points = [
    "Users can request the system to retrieve all unread emails from their Gmail inbox.",
    "The system fetches the unread emails and presents them in a conversational manner for the user."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))

st.markdown("Fetch Events:")
bullet_points = [
    "Users can inquire about upcoming events or appointments from their calendar linked to Gmail.",
    "The system interacts with the calendar data, retrieves the relevant information, and presents it in the chat interface."
]
st.markdown("\n".join([f"- {point}" for point in bullet_points]))