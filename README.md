# Polyglot - AI-Powered Language Learning Assistant

![Polyglot Logo](https://img.shields.io/badge/🌍-Polyglot-0066FF)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.20+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)

Polyglot is an adaptive language learning application powered by large language models that provides personalized tutoring based on the user's target language and proficiency level (A1-C1). It offers translations, grammar explanations, vocabulary exercises, and supports learning from various file formats, all while adapting content to the learner's current CEFR level.

## Key Features

### 🔍 LLM-Powered Intelligence

- **Dynamic Context Understanding**: Uses Large Language Models to understand the nuances of user requests
- **Intelligent Topic Detection**: Automatically identifies language learning topics in user queries
- **Language Detection**: Recognizes the language of text with high accuracy
- **Content Analysis**: Analyzes uploaded files to extract relevant learning materials

### 🌍 Multilingual Support

- **15+ Languages**: Support for multiple languages including Finnish, Spanish, French, German, Japanese, and more
- **Easy Language Switching**: Change target language with persistent progress tracking
- **Native Greetings**: Time-of-day appropriate greetings in the target language

### 🎯 CEFR Level Adaptation

- **Adaptive Content**: All materials dynamically adjusted to CEFR levels (A1, A2, B1, B2, C1)
- **Visual Level Indicators**: Clear badges showing current proficiency level
- **Progress Tracking**: Records level changes across different languages
- **Level-Appropriate Guidelines**: LLM-generated grammar and vocabulary guidelines for each level

### 📝 Learning Activities

- **Translations**: Between target language and English with grammar explanations
- **Grammar Breakdowns**: Detailed explanations with visual aids
- **Vocabulary Building**: Level-appropriate word lists
- **Reading and Writing Exercises**: Generated based on current proficiency
- **Interactive Quizzes**: With immediate feedback

### 📂 Multimodal Learning

- **Text Processing**: Extract learning content from uploaded documents
- **Image Analysis**: Learn from uploaded images containing text in the target language
- **File Content Analysis**: LLM-powered analysis of file contents for relevant learning material

### 🧠 Personalization

- **Topic Tracking**: Identifies user interests to provide relevant examples
- **Learning History**: Exportable chat history with level indicators
- **Exercise Parameter Detection**: Understands implicit and explicit exercise requests

## Technical Architecture

Polyglot uses a modern technical stack with:

- **Streamlit**: For the responsive web interface
- **LangChain**: To integrate with large language models
- **OpenAI API**: Powering the intelligent language tutoring
- **Function Caching**: For performance optimization
- **Real-time Content Generation**: Streaming responses for better user experience

The application is structured into three main modules:

1. **app.py**: Main application interface and user interaction
2. **chatbot.py**: LLM integration and conversation management
3. **utils.py**: LLM-powered utility functions for language learning

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
MODEL_NAME = "gpt-4.1-mini-2025-04-14"  # Optional - change model
```

### Step 5: Run the application
```bash
streamlit run app.py
```

## Usage Guide

### 1. Select Your Target Language
Choose from 15+ supported languages in the sidebar dropdown.

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
- Polyglot will analyze the content, provide translations, and create exercises based on the material

### 4. Session Management
- Reset the conversation at any time using the sidebar button
- Export your chat history as a Markdown file for later review
- Track your level progression in the sidebar for each language

## Advanced Features

### LLM-Powered NLP
Polyglot replaces traditional rule-based NLP with contextual LLM intelligence for:

1. **Topic Extraction**: Identifies learning topics in user messages
2. **Exercise Parameter Detection**: Understands the type of exercise requested
3. **Language Detection**: Identifies the language of text segments
4. **Content Guidelines**: Generates appropriate vocabulary and grammar for each level
5. **File Content Analysis**: Assesses the difficulty level and extracts learning material

### Adaptive Learning
The application optimizes the learning experience by:

1. **Level-Specific Content**: Dynamically generating level-appropriate content
2. **Personalized Examples**: Using detected topics to create relevant examples
3. **Progress Tracking**: Monitoring level changes to provide appropriate review
4. **File Analysis**: Determining if uploaded content matches the learner's level

## Extending the Application

### Adding New Languages
To add support for new languages:
1. Add the language to the `SUPPORTED_LANGUAGES` dictionary in `app.py`
2. Add appropriate greetings to the `LANGUAGE_GREETINGS` dictionary

### Adding New Features
The modular architecture makes it easy to add new features:
1. UI components can be added to `app.py`
2. LLM-based processing can be extended in `chatbot.py`
3. Utility functions can be added to `utils.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Common European Framework of Reference for Languages (CEFR) for level guidelines
- Streamlit for the interactive web application framework
- OpenAI and LangChain for the underlying language model integration











<!-- # Polyglot - Multilingual Learning Assistant

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
- OpenAI for the underlying language model -->