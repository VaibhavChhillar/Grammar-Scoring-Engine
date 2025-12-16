#Demonstration :- https://drive.google.com/file/d/1d_5oHVP3XHxugWX3zwZi-Qru_VitvFEB/view?usp=sharing
#Github :- https://github.com/DarshanKagi/Grammar-Scoring-Engine

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import whisper                     # For transcribing audio using OpenAI’s Whisper model
import language_tool_python        # For grammar and style checking
import sounddevice as sd           # For audio recording
import soundfile as sf             # For audio file handling
import numpy as np                 # For numerical operations on audio data
import os                          # For file operations
import time                        # For timing and recording duration
import textstat                    # For advanced readability and style metrics

# ---------------------------
# Global Constants & Helpers
# ---------------------------

# Error weights used to calculate a weighted penalty for different error categories.
ERROR_WEIGHTS = {
    'GRAMMAR': 3,
    'TYPOS': 2,
    'PUNCTUATION': 1,
    'STYLE': 1.5
}

# List of filler words to count in the transcript.
FILLER_WORDS = ["um", "uh", "like", "you know", "ah", "er"]

# Dictionary to store inline error matches using tag names in the transcript text widget.
inline_errors = {}

def classify_error(match):
    """
    Classify a grammar/style error (match) into one of the categories:
    'GRAMMAR', 'TYPOS', 'PUNCTUATION', or 'STYLE'
    
    Args:
        match: A language_tool_python match object containing error details.
    
    Returns:
        A string representing the error category.
    """
    rule_id = match.ruleId
    message = match.message.lower()
    # Classify as typo based on rule id or if message mentions spelling
    if rule_id == "MORFOLOGIK_RULE_EN_US" or "spelling" in message:
        return "TYPOS"
    # Classify as punctuation if message contains punctuation keywords
    elif "punctuation" in message:
        return "PUNCTUATION"
    # Classify as style if message indicates style or readability issues
    elif "style" in message or "readability" in message:
        return "STYLE"
    # Default category is grammar
    else:
        return "GRAMMAR"

def compute_metrics(transcript, audio_duration, error_breakdown, overall_score):
    """
    Compute various metrics from the transcript including:
      - Word count
      - Speaking rate (words per minute)
      - Filler word count
      - Error counts
    
    Args:
        transcript: The transcribed text from the audio.
        audio_duration: Duration of the audio recording (in seconds).
        error_breakdown: Dictionary containing counts of errors by category.
        overall_score: Final overall grammar score after penalties.
    
    Returns:
        A dictionary of computed metrics.
    """
    # Split transcript into words and count them
    words = transcript.split()
    word_count = len(words)
    # Calculate words per minute (WPM)
    wpm = round(word_count / (audio_duration / 60), 2) if audio_duration > 0 else 0
    transcript_lower = transcript.lower()
    # Count occurrences of each filler word in the transcript
    filler_count = sum(transcript_lower.count(filler) for filler in FILLER_WORDS)
    
    metrics = {
        "score": overall_score,
        "word_count": word_count,
        "wpm": wpm,
        "filler_count": filler_count,
        "errors": {
            "GRAMMAR": error_breakdown.get("GRAMMAR", 0),
            "TYPOS": error_breakdown.get("TYPOS", 0),
            "PUNCTUATION": error_breakdown.get("PUNCTUATION", 0)
        }
    }
    return metrics

def advanced_style_analysis(text):
    """
    Analyze the style and readability of the text using various readability indices.
    
    Args:
        text: The input text (transcript) to analyze.
    
    Returns:
        A dictionary containing advanced readability metrics and style recommendations.
    """
    # Calculate Flesch Reading Ease, Flesch-Kincaid Grade, and Gunning Fog index
    fre = textstat.flesch_reading_ease(text)
    fk_grade = textstat.flesch_kincaid_grade(text)
    gunning = textstat.gunning_fog(text)
    
    # Determine a general comment based on the Flesch Reading Ease score
    if fre > 60:
        comment = "The text is clear and easily understandable."
    elif fre > 40:
        comment = "The text is moderately complex; consider simplifying sentences for clarity."
    else:
        comment = "The text is hard to read; consider revising for improved clarity and tone."
    
    # Provide suggestions to improve readability based on indices
    suggestions = []
    if fk_grade > 10:
        suggestions.append("Simplify sentence structure to lower the reading grade level.")
    if gunning > 12:
        suggestions.append("Reduce vocabulary complexity to lower the Gunning Fog Index.")
    if not suggestions:
        suggestions.append("Your writing style is effective.")
    
    recommendations = " ".join(suggestions)
    
    return {
        "flesch_reading_ease": fre,
        "flesch_kincaid_grade": fk_grade,
        "gunning_fog": gunning,
        "style_comment": comment,
        "advanced_recommendations": recommendations
    }

def contextual_language_feedback(text, error_details):
    """
    Provide personalized feedback based on the types of errors detected.
    
    Args:
        text: The original transcript text.
        error_details: A list of error detail strings from the grammar checker.
    
    Returns:
        A string containing aggregated contextual feedback.
    """
    suggestions = []
    for detail in error_details:
        # Append suggestions based on detected error categories
        if "Category: TYPOS" in detail:
            suggestions.append("Review suggested corrections for typos and consider using a spell-checker.")
        if "Category: GRAMMAR" in detail:
            suggestions.append("Review grammar suggestions and study common grammatical patterns.")
        if "Category: PUNCTUATION" in detail:
            suggestions.append("Review punctuation guidelines to improve sentence clarity.")
        if "Category: STYLE" in detail:
            suggestions.append("Consider revising stylistically ambiguous sentences for better readability.")
    
    # Remove duplicate suggestions while preserving order
    suggestions = list(dict.fromkeys(suggestions))
    if suggestions:
        return " ".join(suggestions)
    else:
        return "No additional contextual feedback available."

def generate_report(metrics, advanced_style, contextual_feedback):
    """
    Generate a comprehensive report combining all computed metrics, style analysis,
    and contextual feedback.
    
    Args:
        metrics: Dictionary containing basic metrics such as score, word count, etc.
        advanced_style: Dictionary containing advanced readability and style metrics.
        contextual_feedback: A string containing additional feedback based on errors.
    
    Returns:
        A formatted string report summarizing the analysis.
    """
    report = (
        "Grammar Analysis Report\n"
        "--------------------------\n"
        f"Overall Score: {metrics['score']}/100\n"
        f"Word Count: {metrics['word_count']}\n"
        f"Speaking Rate: {metrics['wpm']} WPM\n"
        f"Filler Words: {metrics['filler_count']}\n\n"
        "Error Breakdown:\n"
        f"- Grammar: {metrics['errors'].get('GRAMMAR', 0)}\n"
        f"- Spelling: {metrics['errors'].get('TYPOS', 0)}\n"
        f"- Punctuation: {metrics['errors'].get('PUNCTUATION', 0)}\n\n"
        "Advanced Style Metrics:\n"
        f"- Flesch Reading Ease: {advanced_style['flesch_reading_ease']:.2f}\n"
        f"- Flesch-Kincaid Grade Level: {advanced_style['flesch_kincaid_grade']:.2f}\n"
        f"- Gunning Fog Index: {advanced_style['gunning_fog']:.2f}\n"
        f"Style Comment: {advanced_style['style_comment']}\n"
        f"Recommendations: {advanced_style['advanced_recommendations']}\n\n"
        "Contextual Language Feedback:\n"
        f"{contextual_feedback}\n"
    )
    return report

# ---------------------------
# Initialize Models & Tools
# ---------------------------

# Load the Whisper model for audio transcription (using the "base" model variant)
model = whisper.load_model("base")
# Initialize the language tool for US English
tool = language_tool_python.LanguageTool('en-US')

# ---------------------------
# Audio Recording Setup
# ---------------------------

# Set the sample rate for audio recording (in Hertz)
SAMPLE_RATE = 44100
# Temporary file name for saving recorded audio
TEMP_AUDIO_FILE = "temp_recording.wav"
# Variables for managing audio recording state
recording_stream = None
recorded_frames = []
recording_start_time = None
timer_job = None

def audio_callback(indata, frames, time_info, status):
    """
    Callback function for the audio input stream.
    
    Args:
        indata: Recorded audio data.
        frames: Number of frames.
        time_info: Dictionary containing timing information.
        status: Status of the recording.
    """
    if status:
        print("Recording Status:", status)
    # Append a copy of the current audio chunk to recorded_frames
    recorded_frames.append(indata.copy())

def transcribe_audio(file_path):
    """
    Transcribe an audio file using the Whisper model.
    
    Args:
        file_path: Path to the audio file.
    
    Returns:
        The transcribed text.
    """
    try:
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        messagebox.showerror("Transcription Error", f"Error during transcription: {e}")
        return ""

def check_grammar(text):
    """
    Check the provided text for grammar and style issues using LanguageTool.
    
    Args:
        text: The transcript text to check.
    
    Returns:
        A tuple containing:
         - overall_score: The final score after applying weighted penalties.
         - error_details: A list of formatted error details.
         - error_breakdown: A dictionary with error counts by category.
         - total_errors: The total number of errors detected.
    """
    matches = tool.check(text)
    error_details = []
    error_breakdown = {"GRAMMAR": 0, "TYPOS": 0, "PUNCTUATION": 0, "STYLE": 0}
    
    # Process each error match from LanguageTool
    for match in matches:
        category = classify_error(match)
        error_breakdown[category] += 1
        # Use the first suggested correction if available
        suggestion = match.replacements[0] if match.replacements else "No suggestion available"
        explanation = f"This error occurs because: {match.message}. Context: '{match.context}'."
        error_info = (
            f"Error: {match.message}\n"
            f"Category: {category}\n"
            f"Context: '{match.context}'\n"
            f"Suggested Correction: {suggestion}\n"
            f"Explanation: {explanation}\n"
            "-----"
        )
        error_details.append(error_info)
    
    # Calculate weighted penalty based on error counts and predefined weights
    weighted_penalty = sum(ERROR_WEIGHTS[cat] * count for cat, count in error_breakdown.items())
    overall_score = max(100 - weighted_penalty, 0)
    return overall_score, error_details, error_breakdown, len(matches)

def process_file():
    """
    Process an audio file selected from disk:
      - Transcribe audio using Whisper.
      - Compute grammar errors and style metrics.
      - Update GUI text widgets with transcript, score, error details, style analysis, and report.
    """
    # Open file dialog to select an audio file
    file_path = filedialog.askopenfilename(title="Select Audio File",
                                           filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")])
    if file_path:
        # Transcribe the audio file
        transcript = transcribe_audio(file_path)
        try:
            info = sf.info(file_path)
            audio_duration = info.duration
        except Exception:
            audio_duration = 0
        # Check grammar and style on the transcript
        overall_score, error_details, error_breakdown, total_errors = check_grammar(transcript)
        advanced_style = advanced_style_analysis(transcript)
        contextual_feedback = contextual_language_feedback(transcript, error_details)
        metrics = compute_metrics(transcript, audio_duration, error_breakdown, overall_score)
        report = generate_report(metrics, advanced_style, contextual_feedback)
        
        # Update the transcript text widget with the transcription result
        transcript_text.delete(1.0, tk.END)
        transcript_text.insert(tk.END, transcript)
        # Update the score label with overall grammar score and error count
        score_label.config(text=f"Grammar Score: {overall_score} (Total Errors: {total_errors})")
        # Update the errors text widget with detailed error information
        errors_text.delete(1.0, tk.END)
        if error_details:
            errors_text.insert(tk.END, "\n\n".join(error_details))
        else:
            errors_text.insert(tk.END, "No grammatical errors found.")
        # Update the style analysis text widget with advanced readability metrics
        style_text.delete(1.0, tk.END)
        style_text.insert(tk.END, 
            f"Flesch Reading Ease Score: {advanced_style['flesch_reading_ease']:.2f}\n"
            f"Flesch-Kincaid Grade Level: {advanced_style['flesch_kincaid_grade']:.2f}\n"
            f"Gunning Fog Index: {advanced_style['gunning_fog']:.2f}\n"
            f"Style Comment: {advanced_style['style_comment']}\n"
            f"Recommendations: {advanced_style['advanced_recommendations']}"
        )
        # Update the comprehensive report text widget
        report_text.delete(1.0, tk.END)
        report_text.insert(tk.END, report)
        # Clear any previous inline error highlights
        clear_inline_errors()

def update_timer():
    """
    Update the recording timer label every second to show elapsed recording time.
    """
    global timer_job
    if recording_start_time is not None:
        elapsed = int(time.time() - recording_start_time)
        timer_label.config(text=f"Recording Time: {elapsed} sec")
        timer_job = root.after(1000, update_timer)

def start_recording():
    """
    Start audio recording using sounddevice and update the timer.
    """
    global recording_stream, recorded_frames, recording_start_time, timer_job
    recorded_frames = []  # Reset the recorded frames
    recording_start_time = time.time()  # Record the start time
    update_timer()  # Begin updating the timer
    try:
        # Start a new input stream for recording audio
        recording_stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback)
        recording_stream.start()
    except Exception as e:
        messagebox.showerror("Recording Error", f"Error starting recording: {e}")

def stop_recording():
    """
    Stop audio recording, process the recorded audio, and generate the analysis report.
    """
    global recording_stream, recorded_frames, recording_start_time, timer_job
    try:
        if recording_stream is not None:
            # Stop and close the recording stream
            recording_stream.stop()
            recording_stream.close()
            recording_stream = None
            if timer_job:
                root.after_cancel(timer_job)
                timer_job = None
            # Calculate the duration of the recorded audio
            audio_duration = time.time() - recording_start_time
            if recorded_frames:
                # Concatenate recorded frames and save to a temporary audio file
                audio_data = np.concatenate(recorded_frames, axis=0)
                sf.write(TEMP_AUDIO_FILE, audio_data, SAMPLE_RATE)
                timer_label.config(text="Recording Stopped")
                
                # Transcribe the recorded audio
                transcript = transcribe_audio(TEMP_AUDIO_FILE)
                overall_score, error_details, error_breakdown, total_errors = check_grammar(transcript)
                advanced_style = advanced_style_analysis(transcript)
                contextual_feedback = contextual_language_feedback(transcript, error_details)
                metrics = compute_metrics(transcript, audio_duration, error_breakdown, overall_score)
                report = generate_report(metrics, advanced_style, contextual_feedback)
                
                # Update GUI with the results
                transcript_text.delete(1.0, tk.END)
                transcript_text.insert(tk.END, transcript)
                score_label.config(text=f"Grammar Score: {overall_score} (Total Errors: {total_errors})")
                errors_text.delete(1.0, tk.END)
                if error_details:
                    errors_text.insert(tk.END, "\n\n".join(error_details))
                else:
                    errors_text.insert(tk.END, "No grammatical errors found.")
                style_text.delete(1.0, tk.END)
                style_text.insert(tk.END, 
                    f"Flesch Reading Ease Score: {advanced_style['flesch_reading_ease']:.2f}\n"
                    f"Flesch-Kincaid Grade Level: {advanced_style['flesch_kincaid_grade']:.2f}\n"
                    f"Gunning Fog Index: {advanced_style['gunning_fog']:.2f}\n"
                    f"Style Comment: {advanced_style['style_comment']}\n"
                    f"Recommendations: {advanced_style['advanced_recommendations']}"
                )
                report_text.delete(1.0, tk.END)
                report_text.insert(tk.END, report)
                # Clear any inline error highlights from previous analysis
                clear_inline_errors()
                
                # Clean up temporary audio file
                try:
                    os.remove(TEMP_AUDIO_FILE)
                except Exception:
                    pass
            else:
                timer_label.config(text="No audio data recorded.")
        else:
            timer_label.config(text="Recording was not started.")
    except Exception as e:
        messagebox.showerror("Recording Error", f"Error stopping recording: {e}")

def clear_inline_errors():
    """
    Remove all inline error tags from the transcript text widget and clear the inline_errors dictionary.
    """
    for tag in list(inline_errors.keys()):
        transcript_text.tag_delete(tag)
    inline_errors.clear()

def error_click_callback(event, tag):
    """
    Callback function triggered when a highlighted error is clicked.
    Opens a popup with error details and suggested corrections.
    
    Args:
        event: The Tkinter event object.
        tag: The tag identifier for the error.
    """
    match = inline_errors.get(tag)
    if not match:
        return

    # Create a popup window for displaying error details and suggestions
    popup = tk.Toplevel(root)
    popup.title("Error Correction")
    popup.geometry("400x250")
    
    # Display error message and context in the popup
    error_info = f"Error: {match.message}\nContext: '{match.context}'"
    tk.Label(popup, text=error_info, wraplength=380, justify="left").pack(pady=10)
    
    suggestion_var = tk.StringVar(value="")
    
    # If suggestions are available, display them as radio buttons for selection
    if match.replacements:
        tk.Label(popup, text="Select a suggestion:").pack()
        for suggestion in match.replacements:
            tk.Radiobutton(popup, text=suggestion, variable=suggestion_var, value=suggestion).pack(anchor="w")
    else:
        tk.Label(popup, text="No suggestions available for this error.").pack()
    
    def apply_correction():
        """
        Apply the selected correction by replacing the error text in the transcript.
        """
        suggestion = suggestion_var.get()
        if suggestion:
            # Get current indices of the error tag in the transcript text widget
            ranges = transcript_text.tag_ranges(tag)
            if ranges:
                start_index = ranges[0]
                end_index = ranges[1]
                # Replace the error text with the chosen suggestion
                transcript_text.delete(start_index, end_index)
                transcript_text.insert(start_index, suggestion)
                # Remove the tag after correction
                transcript_text.tag_delete(tag)
                if tag in inline_errors:
                    del inline_errors[tag]
            popup.destroy()
        else:
            messagebox.showinfo("No Selection", "Please select a suggestion or cancel.")
    
    tk.Button(popup, text="Apply Correction", command=apply_correction).pack(pady=10)
    tk.Button(popup, text="Cancel", command=popup.destroy).pack()

def inline_error_correction():
    """
    Highlight errors directly in the transcript text widget.
    Each highlighted error is clickable, allowing the user to view details and choose a correction.
    """
    clear_inline_errors()  # Clear any existing highlights
    transcript = transcript_text.get("1.0", "end-1c")
    matches = tool.check(transcript)
    for i, match in enumerate(matches):
        # Calculate the text indices where the error occurs using offset and error length
        start_index = f"1.0+{match.offset}c"
        end_index = f"1.0+{match.offset + match.errorLength}c"
        tag = f"error_{i}"
        transcript_text.tag_add(tag, start_index, end_index)
        # Configure the tag to have a light yellow background and underline for visibility
        transcript_text.tag_config(tag, background="lightyellow", underline=1)
        # Bind a left-click event on the tag to trigger the error correction popup
        transcript_text.tag_bind(tag, "<Button-1>", lambda event, tag=tag: error_click_callback(event, tag))
        inline_errors[tag] = match

def show_comparison_mode():
    """
    Open a new window that shows a side-by-side comparison of the original transcript
    and the corrected version. This helps the user see improvements.
    """
    original = transcript_text.get("1.0", "end-1c")
    corrected = tool.correct(original)
    
    # Create a new top-level window for comparison
    comp_window = tk.Toplevel(root)
    comp_window.title("Transcript Comparison")
    comp_window.geometry("900x500")
    
    # Left frame for the original transcript
    left_frame = tk.Frame(comp_window)
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    # Right frame for the corrected transcript
    right_frame = tk.Frame(comp_window)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    tk.Label(left_frame, text="Original Transcript").pack()
    orig_text = tk.Text(left_frame, wrap="word", width=45, height=25)
    orig_text.pack(fill="both", expand=True)
    orig_text.insert(tk.END, original)
    
    tk.Label(right_frame, text="Corrected Transcript").pack()
    corr_text = tk.Text(right_frame, wrap="word", width=45, height=25)
    corr_text.pack(fill="both", expand=True)
    corr_text.insert(tk.END, corrected)

def correct_transcript():
    """
    Perform a full correction of the transcript by replacing its entire contents
    with the corrected version from LanguageTool.
    """
    transcript = transcript_text.get("1.0", tk.END).strip()
    if not transcript:
        messagebox.showinfo("Correction", "No transcript available to correct.")
        return
    try:
        corrected = tool.correct(transcript)
        transcript_text.delete("1.0", tk.END)
        transcript_text.insert(tk.END, corrected)
        messagebox.showinfo("Correction", "Transcript has been corrected.")
        clear_inline_errors()
    except Exception as e:
        messagebox.showerror("Correction Error", f"Error during correction: {e}")

# ---------------------------
# GUI Construction with Scrollable Canvas
# ---------------------------

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Enhanced Grammar & Style Analysis Engine")

# Create a canvas and a vertical scrollbar to support scrolling for the entire GUI
main_canvas = tk.Canvas(root, borderwidth=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas)

# Update the scroll region when the frame's size changes
scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

# Place the scrollable frame inside the canvas
main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    """
    Bind the mouse wheel event to scroll the canvas.
    """
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ---------------------------
# GUI Control Buttons and Text Areas
# ---------------------------

# Create a frame for control buttons
control_frame = tk.Frame(scrollable_frame)
control_frame.pack(pady=15)

# Button to load and process an audio file from disk
load_button = tk.Button(control_frame, text="Select & Process Audio File", command=process_file)
load_button.grid(row=0, column=0, padx=10)

# Buttons for starting and stopping audio recording
start_rec_button = tk.Button(control_frame, text="Start Recording", command=start_recording)
start_rec_button.grid(row=0, column=1, padx=10)

stop_rec_button = tk.Button(control_frame, text="Stop Recording", command=stop_recording)
stop_rec_button.grid(row=0, column=2, padx=10)

# Buttons for transcript correction tools
correct_button = tk.Button(control_frame, text="Full Correction", command=correct_transcript)
correct_button.grid(row=0, column=3, padx=10)

inline_button = tk.Button(control_frame, text="Inline Correction", command=inline_error_correction)
inline_button.grid(row=0, column=4, padx=10)

compare_button = tk.Button(control_frame, text="Comparison Mode", command=show_comparison_mode)
compare_button.grid(row=0, column=5, padx=10)

# Label to display recording timer updates
timer_label = tk.Label(scrollable_frame, text="Recording Time: 0 sec")
timer_label.pack(pady=10)

def create_scrollable_text(master, height, width):
    """
    Utility function to create a scrollable text widget.
    
    Args:
        master: The parent widget.
        height: The height of the text widget.
        width: The width of the text widget.
    
    Returns:
        The created text widget.
    """
    frame = tk.Frame(master)
    text_widget = tk.Text(frame, wrap="word", height=height, width=width)
    widget_scrollbar = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=widget_scrollbar.set)
    text_widget.pack(side="left", fill="both", expand=True)
    widget_scrollbar.pack(side="right", fill="y")
    frame.pack(pady=5)
    return text_widget

# ---------------------------
# GUI Sections for Output Display
# ---------------------------

# Transcript Section
transcript_label = tk.Label(scrollable_frame, text="Transcript:")
transcript_label.pack(pady=(20, 5))
transcript_text = create_scrollable_text(scrollable_frame, height=10, width=90)

# Grammar Score Label
score_label = tk.Label(scrollable_frame, text="Grammar Score: N/A")
score_label.pack(pady=10)

# Grammar Errors and Suggestions Section
errors_label = tk.Label(scrollable_frame, text="Grammar Errors & Suggestions:")
errors_label.pack(pady=(20, 5))
errors_text = create_scrollable_text(scrollable_frame, height=10, width=90)

# Style Analysis Section
style_label = tk.Label(scrollable_frame, text="Style Analysis:")
style_label.pack(pady=(20, 5))
style_text = create_scrollable_text(scrollable_frame, height=7, width=90)

# Comprehensive Report Section
report_label = tk.Label(scrollable_frame, text="Comprehensive Report:")
report_label.pack(pady=(20, 5))
report_text = create_scrollable_text(scrollable_frame, height=8, width=90)

# Start the Tkinter main event loop
root.mainloop()
