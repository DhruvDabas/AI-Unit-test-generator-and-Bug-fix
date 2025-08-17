import os
import ollama
import openai
from openai import OpenAI
import gradio as gr

OLLAMA_API = "http://localhost:11434/api/chat"
MODEL = "gemma3:4b"

ollama_via_openai = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

system_message = (
    "You are a helpful coding assistant for company Code Q&A. "
    "Given code, generate comprehensive test cases for the code provided. "
    "Always be accurate. Only generate test case code without explanations."
)

def generate_test_cases(code_input):

    if not code_input or not code_input.strip():
        return "Please provide code to generate test cases."
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": code_input}
    ]
    
    try:
        response = ollama_via_openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating test cases: {str(e)}"

def chat_test_generator(message, history):

    messages = [{"role": "system", "content": system_message}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if bot_msg:
            messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})

    response_text = ""
    try:
        stream = ollama_via_openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and "content" in chunk.choices[0].delta:
                response_text += chunk.choices[0].delta["content"]
                yield response_text
    except Exception as e:
        yield f"Error: {str(e)}"
