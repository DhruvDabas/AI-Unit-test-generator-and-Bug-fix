import gradio as gr
import os
import tempfile
import shutil
from test_case_generator import generate_test_cases
from bug_finder import find_bugs_in_code
from chat import chat_with_llm

def upload_repo(file):
    if file is None:
        return "No file uploaded."
    
    # make search-folder if it doesn't exist
    search_folder = "search-folder"
    if not os.path.exists(search_folder):
        os.makedirs(search_folder)
    
    # If it's a directory, copy its contents
    if os.path.isdir(file.name):
        try:
            # Copy all files from uploaded directory to search-folder
            for item in os.listdir(file.name):
                source = os.path.join(file.name, item)
                destination = os.path.join(search_folder, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, destination)
            return f"✅ Repo contents copied to '{search_folder}' successfully."
        except Exception as e:
            return f"❌ Error copying repo: {str(e)}"
    else:
        # If it's a single file, copy it to search-folder
        try:
            shutil.copy2(file.name, search_folder)
            return f"✅ File copied to '{search_folder}' successfully."
        except Exception as e:
            return f"❌ Error copying file: {str(e)}"

def find_bugs():
    try:
        from bug_finder import find_bugs_in_code
        bug_report = find_bugs_in_code()
        return bug_report
    except Exception as e:
        return f"❌ Error scanning for bugs: {str(e)}"

def generate_tests(code_input):
    """Generate test cases for the provided code."""
    return generate_test_cases(code_input)

with gr.Blocks() as app:
    gr.Markdown("# Code Q&A ")
    
    
    with gr.Tab("💬 Ask Questions"):
        chatbot = gr.Chatbot(label="Chat History")
        question_input = gr.Textbox(label="Ask about the codebase", placeholder="Type your question here...")
        ask_btn = gr.Button("Ask")
        clear_btn = gr.Button("Clear Chat")
        
        def respond(message, chat_history):
            bot_message = chat_with_llm(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history
        
        ask_btn.click(respond, [question_input, chatbot], [question_input, chatbot])
        question_input.submit(respond, [question_input, chatbot], [question_input, chatbot])
        
        def clear_chat():
            return []
        
        clear_btn.click(clear_chat, None, chatbot)
    
    with gr.Tab("🐞 Find Bugs"):
        bug_btn = gr.Button("Scan for Bugs")
        bug_output = gr.Textbox(label="Bug Report", lines=20)
        bug_btn.click(find_bugs, outputs=[bug_output])
    
    with gr.Tab("🧪 Generate Tests"):
        test_code_input = gr.Textbox(label="Enter code for which test case needs to be generated", lines=10)
        test_btn = gr.Button("Generate Unit Tests")
        test_output = gr.Textbox(label="Generated Tests", lines=15)
        test_btn.click(generate_tests, inputs=[test_code_input], outputs=[test_output])

if __name__ == "__main__":
    app.launch()