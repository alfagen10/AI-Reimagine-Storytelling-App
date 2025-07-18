# 📚 AI Reimagine Storytelling App

Create interactive, illustrated, multilingual children's stories using AI — complete with narration, PDF export, and QR sharing. Powered by local and cloud-based AI models for privacy and performance.

---

## ✨ Features

- 🎤 **Speech Input** — Assign story elements (character, genre, theme, style) via voice
- 📖 **Story Generation** — AI-generated children's stories using Ollama (Mistral model)
- 🖼️ **Illustrations** — Optional scene-based images via DeepAI's `text2img` API
- 🔊 **Narration** — Text-to-speech with support for multiple languages and adjustable speed
- 📄 **PDF Export** — Download your complete story with custom fonts
- 📲 **QR Sharing** — Share a story link via QR code
- 🌗 **Dark/Light Mode** — Stylish gradient UI with background imagery
- 💬 **Multilingual Support** — English, Chinese, Japanese, Malay, Hindi, Urdu, Bengali, Arabic, German, Spanish

---

## 🚀 Quick Start

---

### A. Prerequisites
Make sure these are installed:

- ✅ Python 3.9+ → Download here
- ✅ Git → Install Git
- ✅ FFmpeg (for audio) → sudo apt install ffmpeg or use ffmpeg.org
- ✅ Ollama → to run the local AI model (e.g. mistral)

---

### B. Clone the repository

```bash
git clone https://github.com/alfagen10/AI-Reimagine-Storytelling-App.git
cd ai-storytelling-app
```

### C. Install dependencies

```bash
pip install -r requirements.txt
```

### D. Add your DeepAI API key

Create a file at `.streamlit/secrets.toml`:

```toml
[api]
deepai_key = "YOUR_DEEPAI_API_KEY"
```
---
### E. 🧠 How to Run Locally with Ollama (Mistral Model)
To enable offline story generation using the Mistral LLM via Ollama, follow these steps:

⚙️ setup_ollama()

- 1. Download & Install Ollama
Visit https://ollama.com and download for your OS (Windows, macOS, or Linux)

- 2. Pull the Mistral Model
     
```bash
ollama pull mistral
```
This will download ~4.1GB

- 3. Run the Ollama Server
 
```bash
ollama run mistral
```
Starts the local LLM server

💡 Make sure Ollama is running in the background when you launch the app.

--- 

### F. Run the app

```bash
streamlit run app.py
```

---

## 🛠️ Local Requirements

- Python 3.9 or above
- [Ollama](https://ollama.com) installed and running (`mistral` model pulled)
- Internet access for DeepAI image generation
- `ffmpeg` (optional, for better audio support on some platforms)

---

## 🧠 Tech Stack

| Area           | Tech                  |
|----------------|-----------------------|
| UI             | Streamlit             |
| LLM Backend    | Ollama + Mistral      |
| Image Gen      | DeepAI (text2img)     |
| TTS            | pyttsx3 (offline)     |
| PDF Export     | FPDF                  |
| Speech Input   | speechrecognition + pydub |
| QR Code        | qrcode                |

---

## 🌍 Supported Languages

- English 🇬🇧
- Chinese 🇨🇳
- Japanese 🇯🇵
- Malay 🇲🇾
- Hindi 🇮🇳
- Urdu 🇵🇰
- Bengali 🇧🇩
- Arabic 🇸🇦
- German 🇩🇪
- Spanish 🇪🇸

---

## 📁 Project Structure

```
📦 ai-storytelling-app/
├── app.py                     # Main Streamlit app
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── secrets.toml           # Your API key (DO NOT COMMIT)
├── assets/
│   └── DejaVuSans.ttf         # Font for PDF
└── temp/                      # Optional folder for generated files
```

---

## 🧩 Future Improvements

- Consistent character illustration via ControlNet
- Save/load story workspace
- Deployable lite version using GPT API for Streamlit Cloud
- Story pack ZIP download with README and all assets
- Firebase or local database for saving stories

---

## 🤝 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- [Mistral AI](https://mistral.ai/)
- [DeepAI](https://deepai.org/)
- [pyttsx3](https://pyttsx3.readthedocs.io/)
- [Google Speech Recognition](https://pypi.org/project/SpeechRecognition/)

---


## 👤 Author

**Al Faruk Md Omor Sajeeb**  
📍 Bukit Jalil, Malaysia  
🎓 BSc (Hons) in Computer Science (Digital Forensics), Asia Pacific University (APU)  
📧 Email: alfarukmd78@gmail.com  
🔗 GitHub: [github.com/alfagen10](https://github.com/alfagen10)

---

## 🏆 Hackathon Submission

This project was developed as part of the **FutureHack AI Battlefield 2025**, hosted at Taylor’s University.  
It aims to demonstrate creative and practical use of AI for storytelling, especially in multilingual and visual formats for global engagement.

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome!

1. Fork the repository  
2. Create a feature branch: `git checkout -b feature/your-feature-name`  
3. Commit your changes: `git commit -m 'Add feature'`  
4. Push to the branch: `git push origin feature/your-feature-name`  
5. Open a pull request

---

## 🛡 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute it with proper attribution.

---

## 📌 Disclaimer

This application is developed for demonstration and educational purposes under the scope of a hackathon.  
AI-generated stories and illustrations may include fictional or random content.  
Please review all outputs before sharing.

