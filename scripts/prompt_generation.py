import json
import tkinter as tk
from tkinter import filedialog

def prompt_user_for_input(extracted_documents):
    """
    Create a Tkinter GUI to prompt the user for input for each extracted document.
    """
    prompt_data = []

    def save_prompt():
        prompt = prompt_entry.get()
        expected_output = output_entry.get()
        prompt_data.append({
            "document": extracted_documents[len(prompt_data)]['file_name'],
            "prompt": prompt,
            "expected_output": expected_output
        })
        prompt_entry.delete(0, tk.END)
        output_entry.delete(0, tk.END)
        if len(prompt_data) < len(extracted_documents):
            document_label.config(text=f"Document: {extracted_documents[len(prompt_data)]['file_name']}")
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            text_box.insert(tk.END, extracted_documents[len(prompt_data)]['text'])
            text_box.config(state=tk.DISABLED)
        else:
            save_prompt_data(prompt_data)

    def save_prompt_data(prompt_data):
        output_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if output_file:
            with open(output_file, 'w') as file:
                json.dump(prompt_data, file, indent=4)
            print(f"Prompt data saved to {output_file}")
            root.destroy()

    root = tk.Tk()
    root.title("Prompt Generation")

    document_label = tk.Label(root, text=f"Document: {extracted_documents[0]['file_name']}")
    document_label.pack()

    text_box = tk.Text(root, height=10, width=50)
    text_box.insert(tk.END, extracted_documents[0]['text'])
    text_box.config(state=tk.DISABLED)
    text_box.pack()

    prompt_label = tk.Label(root, text="Enter your prompt:")
    prompt_label.pack()

    prompt_entry = tk.Entry(root)
    prompt_entry.pack()

    output_label = tk.Label(root, text="Enter the expected output:")
    output_label.pack()

    output_entry = tk.Entry(root)
    output_entry.pack()

    save_button = tk.Button(root, text="Save Prompt", command=save_prompt)
    save_button.pack()

    root.mainloop()

# Assuming extracted_documents is obtained from the previous extraction process
extracted_documents = [
    {"file_name": "doc1.docx", "text": "Extracted text from doc1."},
    {"file_name": "doc2.docx", "text": "Extracted text from doc2."}
]

# Prompt the user for input using the Tkinter GUI
prompt_user_for_input(extracted_documents)