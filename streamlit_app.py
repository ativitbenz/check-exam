import streamlit as st
import openai
from dotenv import dotenv_values

# Set your OpenAI API key
config = dotenv_values('.env')
openai.api_key = config['OPENAI_API_KEY']

def evaluate_student_answer(exam_question, student_answer, additional_rules="", seed=None):
    prompt = f"""A sixth-grade English Teacher was asked: {exam_question}
                Student's Answer: {student_answer}

                **Evaluation Summary:**

                1. **Introduction:**
                - Clarity, Relevance, Completeness.

                2. **Body:**
                - Evidence, Structure, Coherence.

                3. **Conclusion:**
                - Summarization, Completeness, Connection.

                4. **Grammar and Language:**
                - Grammatical Correctness, Language Usage, Clarity.

                5. **Additional Rules Adherence:**
                - Consideration of {additional_rules}.
                - Adherence to specified rules.

                6. **Overall Assessment:**
                - Highlight Strengths.
                - Areas for Improvement.
                - Rule Bricks Scoring.

                7. **Summary:**
                - Concise strengths and improvement areas.

                8. **Total Assessment:**
                - Overall point assessment.
                - Detailed explanations.

                **Feedback:**
                Provide constructive guidance for improvement.

                """

    # Include the seed parameter for consistent results
    parameters = {
        "engine": "text-davinci-003",  # Using gpt-3.5-turbo
        "prompt": prompt,
        "max_tokens": 2000,  # Adjust as needed
        "temperature": 0.7,  # Adjust as needed (higher values for more randomness)
    }

    if seed is not None:
        parameters["seed"] = seed

    # Requesting a completion from the OpenAI GPT-3 model
    response = openai.Completion.create(**parameters)

    # Extracting the bot's reply
    feedback = response.choices[0].text.strip()

    return feedback
    # *** config the best result of seed value but free account limit for this ***
    
    # for seed in range(5):  # You can adjust the range based on the number of attempts
    #     parameters = {
    #         "engine": "text-davinci-003",  # Using gpt-3.5-turbo
    #         "prompt": prompt,
    #         "max_tokens": 3000,  # Adjust as needed
    #         "temperature": 0.7,  # Adjust as needed (higher values for more randomness)
    #         "seed": seed,
    #     }

    #     response = openai.Completion.create(**parameters)
    #     feedback = response.choices[0].text.strip()

    #     if not best_feedback or len(feedback) < len(best_feedback):
    #         best_feedback = feedback

    # return best_feedback

def main():
    st.title("English Exam Evaluation Bot")

    # Input for the exam question with a larger box size
    exam_question = st.text_area("Enter the exam question:", height=150)

    # Additional rules input
    additional_rules = st.text_area("Enter additional rules (if any):")

    # Input for the student's answer
    student_answer = st.text_area("Enter the student's answer:")

    # Seed input for controlling randomness
    seed = st.number_input("Enter a seed value (optional):", min_value=0, step=1)

    # Evaluate button
    if st.button("Evaluate"):
        if not exam_question or not student_answer:
            st.warning("Please enter both the exam question and the student's answer.")
        else:
            # Evaluating the student's answer
            feedback = evaluate_student_answer(exam_question, additional_rules, student_answer, seed)

            # Displaying the result
            st.subheader("Feedback:")
            st.write(feedback)

    # About section
    st.sidebar.markdown("## About")
    st.sidebar.info(
        "This is a simple English Exam Evaluation Bot powered by OpenAI's GPT-3.5-turbo. "
        "Enter an exam question,  additional rules (if any), a student's answer, click the 'Evaluate' button, and receive feedback."
    )

    # Instructions section
    st.sidebar.markdown("## Instructions")
    st.sidebar.text("1. Enter the exam question in the first text area.")
    st.sidebar.text("2. Optionally, enter additional rules in the third text area.")
    st.sidebar.text("3. Enter the student's answer in the second text area.")
    st.sidebar.text("4. Optionally, enter a seed value to control randomness.")
    st.sidebar.text("5. Click the 'Evaluate' button.")
    st.sidebar.text("6. Review the feedback provided by the bot.")

if __name__ == "__main__":
    main()
