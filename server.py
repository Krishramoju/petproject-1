from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

responses = {
    "application": "To apply to college, you'll need to fill out an application form, which usually includes your personal information, academic history, and possibly essays or recommendation letters.",
    "deadline": "College application deadlines vary by school. Generally, early application deadlines are around November, while regular deadlines are usually in January or February. Check the specific deadlines for each college you are interested in.",
    "test scores": "Most colleges require standardized test scores like the SAT or ACT. Make sure to check the specific requirements of the colleges you are applying to.",
    "essay": "College applications often require personal essays. This is your chance to showcase your personality, experiences, and goals. Be sure to write clearly and authentically.",
    "recommendation letters": "You'll typically need one or more letters of recommendation from teachers, mentors, or other people who know you well. Ask them well in advance to give them time to write a strong letter.",
    "financial aid": "Financial aid can come in the form of grants, loans, and scholarships. Fill out the FAFSA (Free Application for Federal Student Aid) to apply for federal financial aid, and search for scholarships based on your achievements and needs.",
    "major": "Choosing a major is an important part of the college application process. Consider what subjects you are passionate about and what career paths interest you.",
    "campus life": "Campus life can vary widely between colleges. It's a good idea to visit campuses if possible, talk to current students, and research the extracurricular activities, housing, and other aspects of campus life.",
    "bye": "Goodbye! Good luck with your college applications and have a great day!"
}

synonyms = {
    "application": ["apply", "application form", "applying"],
    "deadline": ["deadline", "due date", "submission date"],
    "test scores": ["test scores", "SAT", "ACT"],
    "essay": ["essay", "personal statement", "writing"],
    "recommendation letters": ["recommendation letters", "reference letters", "letters of recommendation"],
    "financial aid": ["financial aid", "scholarships", "grants", "loans"],
    "major": ["major", "field of study", "course"],
    "campus life": ["campus life", "student life", "campus experience"],
    "bye": ["bye", "goodbye", "see you later"]
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def simple_fuzzy_match(text, keywords):
    for keyword in keywords:
        if keyword in text:
            return True
    return False

def find_keywords(text, synonyms):
    normalized_text = normalize_text(text)
    matched_keywords = []
    synonym_list = [(keyword, synonym) for keyword, synonyms in synonyms.items() for synonym in synonyms]
    for keyword, synonym in synonym_list:
        if simple_fuzzy_match(normalized_text, [synonym]):
            matched_keywords.append(keyword)
            break
    return matched_keywords

def chatbot_response(user_input):
    matched_keywords = find_keywords(user_input, synonyms)
    if matched_keywords:
        response_key = matched_keywords[0]
        return responses[response_key]
    else:
        return "Sorry, I didn't understand that. Please ask about college admissions or type 'bye' to exit."

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    bot_response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = chatbot_response(user_input)
    return render_template_string('''
        <html>
            <body>
                <h1>College Admissions Chatbot</h1>
                <form method="post">
                    <label for="user_input">You:</label>
                    <input type="text" id="user_input" name="user_input">
                    <input type="submit" value="Send">
                </form>
                <p>Chatbot: {{bot_response}}</p>
            </body>
        </html>
    ''', bot_response=bot_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
