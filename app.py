import gradio as gr

def upload_repo(file):
    if file is None:
        return "No file uploaded."
    return f"✅ Repo '{file.name}' uploaded successfully."

def ask_codebase(question):
    if not question.strip():
        return "Please enter a question."
    return f" User Question : '{question}'."

def find_bugs():
    if( not hasattr(find_bugs, "scanned")):
        find_bugs.scanned = True
        return "🔍 Scanning for bugs... Please wait."
    else:
        " 🐞 Bug scan completed. No issues found."

def generate_tests():
    return " "

with gr.Blocks() as app:
    gr.Markdown("# 🛡️ Coder AI — Repo Q&A & Bug Finder")
    
    with gr.Tab("📂 Upload Repo"):
        repo_file = gr.File(label="Upload your repo as ZIP", file_types=[".zip"])
        upload_btn = gr.Button("Upload & Process")
        upload_output = gr.Textbox(label="Upload Status")
        upload_btn.click(upload_repo, inputs=[repo_file], outputs=[upload_output])
    
    with gr.Tab("💬 Ask Questions"):
        question_input = gr.Textbox(label="Ask about the codebase")
        ask_btn = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer")
        ask_btn.click(ask_codebase, inputs=[question_input], outputs=[answer_output])
    
    with gr.Tab("🐞 Find Bugs"):
        bug_btn = gr.Button("Scan for Bugs")
        bug_output = gr.Textbox(label="Bug Report")
        bug_btn.click(find_bugs, outputs=[bug_output])
    
    with gr.Tab("🧪 Generate Tests"):
        test_btn = gr.Button("Generate Unit Tests")
        test_output = gr.Textbox(label="Generated Tests")
        test_btn.click(generate_tests, outputs=[test_output])

if __name__ == "__main__":
    app.launch()