import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Set up the API key
os.environ["GEMINI_API_KEY"] = "your-gemini-api-key"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define the quiz generation function
generate_quiz_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="generateQuiz",
            description="Generates quiz questions and answers from given notes",
            parameters=content.Schema(
                type=content.Type.OBJECT,
                properties={
                    "notes": content.Schema(
                        type=content.Type.STRING,
                        description="The course notes from which to generate quiz questions."
                    ),
                },
            ),
        ),
    ],
)

# Create the model with the defined function
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    tools=[generate_quiz_tool],
    tool_config={"function_calling_config": "ANY"},
)
