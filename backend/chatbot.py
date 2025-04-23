import json
import difflib

def load_faq():
    with open('faq_data.json') as f:
        return json.load(f)

def generate_schedule(year):
    schedules = {
        "freshman": {
            "Fall": ["CSE 1010", "MATH 1131Q", "PHYS 1401Q", "ENGL 1007", "UNIV 1800"],
            "Spring": ["CSE 1729", "MATH 1132Q", "PHYS 1402Q", "Gen Ed (Content Area I or II)"]
        },
        "sophomore": {
            "Fall": ["CSE 2050", "CSE 2500", "MATH 2110Q", "Gen Ed"],
            "Spring": ["CSE 2100", "CSE 2300W", "MATH 2210Q", "Gen Ed (Content Area IV or elective)"]
        },
        "junior": {
            "Fall": ["CSE 3500", "STAT 3025Q or 3345Q", "CSE Elective", "Gen Ed"],
            "Spring": ["CSE 3000", "CSE Elective", "CSE Elective (3000+)", "Gen Ed"]
        },
        "senior": {
            "Fall": ["CSE 4939W", "CSE Elective (3000+)", "Open Elective", "Gen Ed"],
            "Spring": ["CSE 4940", "CSE Elective (3000+)", "Open Elective", "Free Elective"]
        }
    }

    if year in schedules:
        semesters = schedules[year]
        response = f"{year.capitalize()} Year Schedule:\n"
        for semester, courses in semesters.items():
            response += f"\n{semester}:\n" + "\n".join(f"• {c}" for c in courses)
        return response
    else:
        return "Sorry, I don't recognize that year. Please choose Freshman, Sophomore, Junior, or Senior."

def find_answer(user_input, faq_data):
    user_input = user_input.lower()

    # Handle schedule requests
    if "schedule" in user_input or "plan" in user_input or "classes" in user_input:
        for year in ["freshman", "sophomore", "junior", "senior"]:
            if year in user_input:
                return generate_schedule(year)
        return "Sure! Which year are you in? (Freshman, Sophomore, Junior, or Senior)"

    # Fuzzy matching
    questions = [faq["question"].lower() for faq in faq_data]
    close_matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
    if close_matches:
        match = close_matches[0]
        for faq in faq_data:
            if faq["question"].lower() == match:
                return faq["answer"]

    return "I'm sorry, I couldn't find an answer for that. Try rephrasing or ask about your courses, schedule, or plan of study."
