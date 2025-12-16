# Grammar Scoring Engine for Voice Samples

An interactive desktop application that records or loads voice samples, transcribes them using OpenAI’s Whisper model, checks grammar/style with LanguageTool, computes readability metrics, and generates a comprehensive report.

---

## Table of Contents

- [Project Description](#project-description)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [How to Install and Run](#how-to-install-and-run)  
- [How to Use the Project](#how-to-use-the-project)  
- [Media](#media)  
- [Future Enhancements](#future-enhancements)  
- [Contributing](#contributing)  
- [License](#license)  
- [Credits](#credits)  
- [Author](#author)  
- [Connect with Me](#connect-with-me)  

---

## Project Description

The Grammar Scoring Engine for Voice Samples is a Python/Tkinter desktop application that enables users to:

1. **Record** or **upload** an audio sample (WAV/MP3/M4A).  
2. **Transcribe** speech to text using OpenAI’s Whisper.  
3. **Analyze** the transcript for grammar, typos, punctuation, and style issues via LanguageTool.  
4. **Compute** readability metrics (Flesch, Gunning Fog, etc.) with `textstat`.  
5. **Generate** a detailed, weighted grammar score and comprehensive report.  
6. **Highlight** errors inline and allow interactive correction.  

Ideal for language learners, content creators, and researchers who need quick, quantitative feedback on spoken language fluency and writing clarity.

---

## Features

- **Real‑time Recording & File Upload**  
- **Whisper‑powered Transcription** (base model)  
- **Weighted Grammar Scoring** (grammar, typos, punctuation, style)  
- **Readability & Style Metrics** (Flesch Reading Ease, Flesch‑Kincaid Grade, Gunning Fog)  
- **Inline Error Highlighting & Click‑to‑Correct**  
- **Side‑by‑Side Comparison Mode**  
- **Comprehensive Text Report Export**  
- **Customizable Error Weights**  

---

## Prerequisites

- **Python 3.8+**  
- **FFmpeg** (for audio decoding, if not already on your system)  
- **pip**  

Python packages (install via `pip`):

```bash
pip install tkinter whisper language-tool-python sounddevice soundfile numpy textstat
```

---

## How to Install and Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/grammar-scoring-engine.git
   cd grammar-scoring-engine
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**  
   ```bash
   python main.py
   ```

---

## How to Use the Project

1. **Launch** the app via `python main.py`.  
2. **Record** your voice by clicking **Start Recording** / **Stop Recording**, or click **Select & Process Audio File** to upload.  
3. **Wait** for transcription & analysis to complete.  
4. **View**:  
   - **Transcript** pane  
   - **Grammar Score** & **Error Count**  
   - **Error Details** & **Inline Highlights**  
   - **Style Analysis** metrics  
   - **Comprehensive Report**  
5. **Interact**:  
   - Click highlighted words to see suggestions and apply corrections.  
   - Use **Comparison Mode** to see original vs. corrected text side‑by‑side.  
   - Export or copy the report as needed.

---

## Media

> **Watch a full demo:**  
> https://drive.google.com/file/d/1d_5oHVP3XHxugWX3zwZi-Qru_VitvFEB/view?usp=sharing

---

## Future Enhancements

- 🎙️ **Batch Processing CLI** for scoring multiple files.  
- 🚀 **Web‑based Dashboard** (FastAPI + React).  
- 🤖 **Customizable Whisper Model Selection** (tiny, base, large).  
- 🌐 **Multi‑language Support** with LanguageTool & Whisper.  
- 📊 **Export to CSV / JSON** for integration with analytics tools.  
- 🔄 **Continuous Recording Mode** with live streaming feedback.

---

## Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -m 'Add YourFeature'`)  
4. Push to the branch (`git push origin feature/YourFeature`)  
5. Open a Pull Request  

Please ensure all new code is covered by tests and adheres to PEP8 style.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Credits

- **OpenAI Whisper** – audio transcription engine  
- **LanguageTool** – grammar, spelling, and style checking  
- **textstat** – readability metrics  
- **Tkinter** – GUI framework  
- **NumPy** & **SoundDevice** – audio handling  

---

## Author

**Darshan Kagi**  
- Gmail: darshankagi04@gmail.com  
- LinkedIn: [darshan-kagi-938836255](https://www.linkedin.com/in/darshan-kagi-938836255)  

---

## Connect with Me

Feel free to reach out for questions, collaborations, or just to say hi!

- ✉️ Email: darshankagi04@gmail.com  
- 🔗 LinkedIn: https://www.linkedin.com/in/darshan-kagi-938836255  
