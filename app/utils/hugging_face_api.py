import requests

print(f"Handle LLM model API calls")

MODEL_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
HEADERS = {
    "Authorization": "Bearer <llm_token>"
}

def get_llm_suggestions(resume_text: str, additional_files: list, job_description: str) -> str:
    """
    Send the resume text to the Hugging Face model and get suggestions based on additional files and job description.
    Ensures no structural changes to the resume.
    """
    # Combine all relevant data into one prompt
    additional_files_content = "\n".join([file['content'] for file in additional_files])  # Assuming 'content' key in each file

    combined_prompt = f"""
    Here is my current resume (only the Key Achievements section is relevant for changes):
    {resume_text}

    Job Description (only include details that apply to Key Achievements section):
    {job_description}

    Additional Reference Files (these provide additional details, languages, tools, and skills):
    {additional_files_content}

    Instructions:
    - Modify the Key Achievements section of my resume based on the job description provided.
    - You can add or modify content, but do not change the overall structure or format of my resume.
    - Use information from the additional files to add relevant details to the Key Achievements section, such as tools, skills, and experience.
    - Keep the formatting consistent with my existing resume, adding only necessary details based on the job description and additional files.
    - Please return the complete updated resume with the modifications to the Key Achievements section.
    """
    # Prepare the request data
    data = {
        "inputs": combined_prompt,  # The combined prompt to feed into the model
        "temperature": 0.5, #control randomness
        "max_tokens": 500, #control output length
        "top_p": 1.0, #control output randomness
    
    }

    # Send the request to the Hugging Face API
    response = requests.post(MODEL_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        generated_text = response.json()
        return generated_text[0]['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

