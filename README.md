# Polyglot - Multilingual Learning Assistant

![Polyglot Logo](https://img.shields.io/badge/🌍-Polyglot-0066FF)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)

Polyglot is an adaptive language learning application that provides personalized tutoring based on the user's target language and proficiency level (A1-C1). It offers translations, grammar explanations, vocabulary exercises, and supports learning from various file formats.

## Features

🌍 **Multilingual Support**
- Support for multiple languages including Finnish, Spanish, French, German, Japanese, and more
- Easy language switching with persistent user progress
- Language-specific grammar and vocabulary content

🎯 **Level-Adaptive Learning**
- Content adaptation based on CEFR levels (A1, A2, B1, B2, C1)
- Visual level indicators throughout the application
- Personalized feedback appropriate to learner's level
- Level progression tracking for each language

📝 **Core Learning Features**
- Translations between target language and English
- Grammar concept breakdowns with visual aids
- Vocabulary building with level-appropriate words
- Reading and writing exercises
- Interactive quizzes with immediate feedback

📁 **Multi-format Content Support**
- Upload text files, documents, images, and more
- Automatic content extraction and processing
- Image-based learning (extract text from images)
- Level-appropriate exercises from uploaded content

🧠 **Personalization**
- Topic tracking to personalize examples
- Spaced repetition for challenging concepts
- Chat history export for review
- Adaptive difficulty based on user performance

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/polyglot-language-tutor.git
cd polyglot-language-tutor
```

### Step 2: Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On MacOS/Linux
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set up Streamlit secrets
Create a `.streamlit/secrets.toml` file in your project directory:
```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

Edit the `secrets.toml` file and add your OpenAI API key:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

> **Note**: Streamlit's secrets management securely stores sensitive information without requiring environment variables or .env files. The secrets are accessible in the app via `st.secrets`.

### Step 5: Run the application
```bash
streamlit run app.py
```

## Usage Guide

### 1. Select Your Target Language
Choose your target language from the dropdown in the sidebar. The app supports multiple languages including:
- Finnish
- Spanish
- French
- German
- Italian
- Japanese
- Chinese
- Russian
- And more...

### 2. Select Your Proficiency Level
Choose your CEFR level (A1-C1) from the sidebar to ensure all content is appropriate for your current proficiency.

### 3. Learning Methods

#### Text-Based Learning
- Type `T: [text]` to translate text between your target language and English
- Ask grammar questions like "Explain verb conjugation" or "How do possessives work?"
- Request vocabulary on specific topics: "Vocabulary about food in Spanish"

#### Exercise-Based Learning
- Ask for level-appropriate exercises: "Give me a reading exercise about hobbies"
- Try writing exercises: "Create a writing exercise about daily routines"
- Test yourself with quizzes: "Quiz me on basic verbs"

#### File-Based Learning
- Upload images containing text in your target language
- Upload text documents with content in your target language
- Polyglot will extract text, provide translations, and create exercises based on the content

### 4. Session Management
- Reset the conversation at any time using the sidebar button
- Export your chat history as a Markdown file for later review
- Track your level progression in the sidebar for each language

## Project Structure

```
polyglot-language-tutor/
├── app.py                  # Main Streamlit application
├── chatbot.py              # LLM integration and chat processing
├── utils.py                # Utility functions and helpers
├── requirements.txt        # Project dependencies
├── .streamlit/             # Streamlit configuration
│   └── secrets.toml        # API keys (not in repository)
└── README.md               # This file
```

## Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: Large language model integration
- **OpenAI API**: GPT model for language tutoring
- **Python**: Core programming language

## Extending the Application

### Adding New Languages
To add support for new languages:
1. Add the language to the `SUPPORTED_LANGUAGES` dictionary in `app.py`
2. Add appropriate greetings to the `LANGUAGE_GREETINGS` dictionary
3. Add language-specific grammar features in `utils.py`
4. Add level-appropriate content for the language in `utils.py`

### Adding New Features
The modular architecture makes it easy to add new features:
1. UI components can be added to `app.py`
2. Language processing logic can be extended in `chatbot.py`
3. Utility functions can be added to `utils.py`

## Streamlit Secrets Management

The application uses Streamlit's built-in secrets management system instead of environment variables or .env files. Configuration is stored in the `.streamlit/secrets.toml` file:

```toml
# Required
OPENAI_API_KEY = "your-openai-api-key"

# Optional - change model
MODEL_NAME = "gpt-4.1-mini-2025-04-14"  # Default GPT model
```

In the application code, these secrets are accessed using:
```python
api_key = st.secrets.get("OPENAI_API_KEY", "")
model_name = st.secrets.get("MODEL_NAME", "gpt-4.1-mini-2025-04-14")
```

For local development, ensure your `.streamlit/secrets.toml` file is in the project root. For deployment on Streamlit Cloud, add these secrets in the app settings.

> **Important**: Never commit your secrets.toml file to version control. It is included in .gitignore by default.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Common European Framework of Reference for Languages (CEFR) for level guidelines
- Streamlit for the interactive web application framework
- OpenAI for the underlying language model