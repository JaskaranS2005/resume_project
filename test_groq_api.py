import os
from utils.llm_helper import generate_feedback

def test_groq_api():
    # Force the provider to groq for this specific test
    os.environ["LLM_PROVIDER"] = "groq"
    
    # Dummy data
    resume_text = "Frontend Developer with 4 years of experience using React, Redux, and JavaScript. Built scalable web apps and improved performance."
    job_description = "Looking for a Frontend Developer experienced with React, Node.js, and API integrations."
    score = 85
    
    print("Testing Groq API Integration...")
    print(f"Mock Score: {score}%\n")
    print("Sending request to Groq API...\n")
    
    # Call the feedback function
    feedback = generate_feedback(resume_text, job_description, score)
    
    print("--- AI Feedback Output ---")
    print(feedback)
    print("--------------------------")

if __name__ == "__main__":
    test_groq_api()
