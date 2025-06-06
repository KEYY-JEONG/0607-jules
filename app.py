import os
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory
from werkzeug.utils import secure_filename
import fitz # PyMuPDF
import anthropic
from docx import Document
from datetime import datetime
import shutil # For copying placeholder image
import google.generativeai as genai # For Gemini API (placeholder)

UPLOAD_FOLDER = 'uploads'
DOCS_FOLDER = 'docs' # For saving summaries
# Define DOCS_DIR for send_from_directory
DOCS_DIR = os.path.abspath(DOCS_FOLDER)

STATIC_IMAGES_FOLDER = 'static/images' # For saving visualizations

ALLOWED_EXTENSIONS = {'pdf'}
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") # User must set this env var

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GEMINI_API_KEY'] = os.environ.get("GEMINI_API_KEY") # User must set this
app.secret_key = 'super secret key'  # Needed for session management

# Create upload, docs, and static/images folders if they don't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
os.makedirs(DOCS_FOLDER, exist_ok=True) # DOCS_DIR is derived from this
# app.static_folder is 'static' by default. We want 'static/images'
os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_structured_summary(summary_text):
    """Parses a string summary into a dictionary by section headers."""
    parsed = {}
    current_section = None
    current_content = []

    if not isinstance(summary_text, str): # Handle cases where summary might not be a string
        return {"Error": "Summary was not in expected string format."}

    for line in summary_text.strip().split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith("Abstract:") or \
           line_stripped.startswith("Introduction:") or \
           line_stripped.startswith("Results:") or \
           line_stripped.startswith("Discussion:"):
            if current_section and current_content:
                parsed[current_section] = " ".join(current_content).strip()

            parts = line_stripped.split(":", 1)
            current_section = parts[0].strip()
            current_content = [parts[1].strip()] if len(parts) > 1 else []
        elif current_section:
            current_content.append(line_stripped)

    if current_section and current_content: # Add the last section
        parsed[current_section] = " ".join(current_content).strip()

    if not parsed: # If no sections were found, return the original text under a generic key
        return {"Full Summary": summary_text}

    return parsed

def generate_visualization_prompt(summary_text):
    """Generates a prompt for AI image generation based on summary."""
    if isinstance(summary_text, dict): # If summary is already parsed
        # Try to get content from Abstract or Introduction for the prompt
        prompt_base = summary_text.get("Abstract", "") or summary_text.get("Introduction", "")
        if not prompt_base: # Fallback if specific sections not found
            prompt_base = " ".join(summary_text.values())
        return f"Create a visual representation of the key findings from this research: {prompt_base[:200]}..."
    # Fallback for string summary
    return f"Create a visual representation of the key findings from this research: {str(summary_text)[:200]}..."

def generate_image_with_ai(prompt, base_filename_prefix="visualization"):
    """
    Generates an image using an AI model (Gemini placeholder).
    Currently copies a placeholder image.
    """
    gemini_api_key = app.config.get('GEMINI_API_KEY')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prefix = os.path.splitext(base_filename_prefix)[0]
    img_filename = f"{safe_prefix}_{timestamp}.png"
    dest_image_subpath = os.path.join('images', img_filename)
    dest_abs_path = os.path.join(app.static_folder, dest_image_subpath)

    # Common logic for copying placeholder
    def copy_placeholder():
        src_placeholder_path = os.path.join(app.static_folder, 'images', 'placeholder.png')
        if not os.path.exists(src_placeholder_path):
            print(f"Placeholder image not found at {src_placeholder_path}")
            return None
        try:
            shutil.copy(src_placeholder_path, dest_abs_path)
            print(f"Placeholder image copied to {dest_abs_path}")
            return dest_image_subpath
        except Exception as e:
            print(f"Error copying placeholder image: {e}")
            return None

    if not gemini_api_key:
        print("GEMINI_API_KEY not found. Using placeholder image.")
        return copy_placeholder()

    # --- Commented out: Actual Gemini API call ---
    # print(f"Attempting to generate image with Gemini using prompt: {prompt}")
    # try:
    #     # ... (Gemini API call logic) ...
    #     # if successful:
    #     #     return dest_image_subpath
    # except Exception as e:
    #     print(f"Error with Gemini API (conceptual): {e}")
    #     # Fall through to placeholder on error or if not implemented
    # --- End Commented out ---

    print("Gemini API key is present, but live generation logic is placeholder or not yet complete. Using placeholder image.")
    return copy_placeholder()


def save_summary_to_files(summary_text, base_filename_prefix="summary"):
    """Saves the summary text to Markdown and DOCX files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prefix = os.path.splitext(base_filename_prefix)[0]
    base_filename = f"{safe_prefix}_{timestamp}"

    # Store both full path (for logging/internal use) and just filename (for downloads)
    saved_file_details = {'md': None, 'docx': None}

    # Save as Markdown
    md_filename_only = f"{base_filename}.md"
    md_filepath_full = os.path.join(DOCS_FOLDER, md_filename_only)
    try:
        with open(md_filepath_full, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        saved_file_details['md'] = {'full_path': md_filepath_full, 'filename': md_filename_only}
        print(f"Summary saved to {md_filepath_full}")
    except Exception as e:
        print(f"Error saving Markdown file: {e}")

    # Save as DOCX
    docx_filename_only = f"{base_filename}.docx"
    docx_filepath_full = os.path.join(DOCS_FOLDER, docx_filename_only)
    try:
        doc = Document()
        # Using the new parser for potentially structured summary
        parsed_summary_for_docx = parse_structured_summary(summary_text)
        if "Full Summary" in parsed_summary_for_docx and len(parsed_summary_for_docx.keys()) == 1:
            # If it's just a single block of text
            doc.add_paragraph(parsed_summary_for_docx["Full Summary"])
        else: # Attempt to add with headings
            for section, content in parsed_summary_for_docx.items():
                if section != "Error": # Skip error messages
                    doc.add_heading(section, level=1)
                    doc.add_paragraph(content)

        if not doc.paragraphs and not doc.sections: # If nothing was added (e.g. empty summary_text)
             doc.add_paragraph(summary_text) # Fallback to raw text

        doc.save(docx_filepath_full)
        saved_file_details['docx'] = {'full_path': docx_filepath_full, 'filename': docx_filename_only}
        print(f"Summary saved to {docx_filepath_full}")
    except Exception as e:
        print(f"Error saving DOCX file: {e}")

    return saved_file_details


def summarize_text_with_ai(text_to_summarize):
    """
    Summarizes the given text using an AI model.
    Currently returns a mock summary.
    """
    if not ANTHROPIC_API_KEY:
        print("ANTHROPIC_API_KEY not found in environment variables. Returning mock summary.")
        return """Abstract: API key not found. This is a mock abstract.
Introduction: The system requires an Anthropic API key for real summarization.
Results: Mock results are shown.
Discussion: Please set the ANTHROPIC_API_KEY environment variable for actual AI processing.
"""

    # client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f"""Please summarize the following text. Structure your summary into these exact sections: "Abstract", "Introduction", "Results", and "Discussion". Ensure the output is clearly delineated for easy parsing.

Text to summarize:
{text_to_summarize}
"""
    # ... (Anthropic API call code placeholder) ...

    # Returning mock summary with clear section delineation
    return """Abstract: This is a mock abstract from the AI placeholder.
Introduction: This mock introduction explains the process.
Results: The mock results section outlines findings.
Discussion: This mock discussion part considers implications.
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session['original_filename'] = filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                doc = fitz.open(filepath)
                extracted_text = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    extracted_text += page.get_text("text")
                doc.close()
                session['extracted_text'] = extracted_text
                return redirect(url_for('process_and_summarize')) # Changed from display_summary to results
            except Exception as e:
                print(f"Error extracting text: {e}")
                return redirect(request.url)
        else:
            return redirect(request.url)
    return render_template('index.html')

@app.route('/process_and_summarize')
def process_and_summarize():
    extracted_text = session.pop('extracted_text', None)
    if not extracted_text:
        return redirect(url_for('upload_file'))

    structured_summary_text = summarize_text_with_ai(extracted_text)
    session['structured_summary_text'] = structured_summary_text # Store raw text for parsing later

    original_pdf_filename = session.get('original_filename', 'uploaded_pdf')
    summary_file_prefix = os.path.splitext(original_pdf_filename)[0]

    # save_summary_to_files now returns a dict with 'full_path' and 'filename' for each type
    saved_file_details = save_summary_to_files(structured_summary_text, base_filename_prefix=summary_file_prefix)
    session['saved_summary_details'] = saved_file_details # e.g. {'md': {'full_path': '...', 'filename': '...'}, ...}

    # Generate and store visualization (placeholder)
    # Pass the raw summary string to generate_visualization_prompt
    vis_prompt = generate_visualization_prompt(structured_summary_text)
    session['visualization_prompt'] = vis_prompt

    image_filename_prefix = os.path.splitext(original_pdf_filename)[0]
    generated_image_path = generate_image_with_ai(vis_prompt, base_filename_prefix=image_filename_prefix)
    session['visualization_image_path'] = generated_image_path

    return redirect(url_for('results')) # Changed from display_summary to results

@app.route('/results') # Renamed from display_summary
def results():
    summary_text = session.get('structured_summary_text', 'No summary generated.')
    saved_details = session.get('saved_summary_details', {}) # e.g. {'md': {'filename': '...'}, ...}
    vis_prompt = session.get('visualization_prompt', 'No visualization prompt generated.')
    image_path = session.get('visualization_image_path', None)

    parsed_summary = parse_structured_summary(summary_text)

    md_fn = saved_details.get('md', {}).get('filename') if saved_details.get('md') else None
    docx_fn = saved_details.get('docx', {}).get('filename') if saved_details.get('docx') else None

    # For display in template, could also pass full paths if needed for messages
    # md_full_path = saved_details.get('md', {}).get('full_path')
    # docx_full_path = saved_details.get('docx', {}).get('full_path')


    return render_template('result.html',
                           summary_data=parsed_summary,
                           visualization_prompt=vis_prompt,
                           visualization_image_path=image_path,
                           md_filename=md_fn,
                           docx_filename=docx_fn)

@app.route('/download_doc/<path:filename>')
def download_doc(filename):
    return send_from_directory(DOCS_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
