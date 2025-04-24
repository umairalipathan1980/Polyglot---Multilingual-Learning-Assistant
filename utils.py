import streamlit as st
import base64
from io import BytesIO
import re
import mimetypes

# Level-specific color scheme
def get_level_color(level_code):
    """
    Get the color associated with a specific CEFR level
    
    Parameters:
    - level_code: The language level code (A1, A2, etc.)
    
    Returns:
    - Hex color code
    """
    level_colors = {
        "A1": "#4CAF50",  # Green for beginner
        "A2": "#8BC34A",  # Light green for elementary
        "B1": "#2196F3",  # Blue for intermediate
        "B2": "#3F51B5",  # Indigo for upper intermediate
        "C1": "#9C27B0"   # Purple for advanced
    }
    return level_colors.get(level_code, "#0066FF")

# Function to create HTML level badge
def format_level_badge(level_code):
    """
    Create an HTML-formatted level badge
    
    Parameters:
    - level_code: The language level code (A1, A2, etc.)
    
    Returns:
    - HTML string for the formatted badge
    """
    color = get_level_color(level_code)
    return f'<span class="level-badge {level_code}" style="background-color: {color};">{level_code}</span>'

# Function to process uploaded files (any type)
def process_uploaded_file(uploaded_file):
    """
    Process an uploaded file of any type to prepare it for analysis by the LLM
    """
    if uploaded_file is None:
        return None
    
    # Read the file
    bytes_data = uploaded_file.getvalue()
    
    # Convert to base64 for displaying or sending to API
    base64_file = base64.b64encode(bytes_data).decode('utf-8')
    
    # Attempt to detect file type if not provided
    file_type = uploaded_file.type
    if not file_type:
        # Try to guess the MIME type based on filename
        guessed_type, _ = mimetypes.guess_type(uploaded_file.name)
        if guessed_type:
            file_type = guessed_type
        else:
            # Default to binary if can't determine
            file_type = "application/octet-stream"
    
    # Determine if file is text-based for potential direct content extraction
    is_text_file = file_type.startswith(('text/', 'application/json', 'application/xml'))
    
    # For text files, try to extract content
    text_content = None
    if is_text_file:
        try:
            text_content = bytes_data.decode('utf-8')
        except UnicodeDecodeError:
            # If UTF-8 fails, try other common encodings
            try:
                text_content = bytes_data.decode('latin-1')
            except:
                # If still can't decode, leave as None
                pass
    
    # Include the current language level and language in the processed file data
    # This ensures both are available when processing the file
    current_level = st.session_state.selected_level
    level_code = current_level.split()[0]  # Extract just the level code (A1, A2, etc.)
    
    # Get current language
    language_code = st.session_state.selected_language if hasattr(st.session_state, 'selected_language') else "fin"
    
    return {
        "name": uploaded_file.name,
        "data": bytes_data,
        "base64": base64_file,
        "type": file_type,
        "is_text_file": is_text_file,
        "text_content": text_content,
        "language_level": current_level,
        "level_code": level_code,
        "language_code": language_code
    }

# Legacy function for backward compatibility
def process_uploaded_image(uploaded_file):
    """
    Legacy function that calls the more generic process_uploaded_file
    Kept for backward compatibility
    """
    return process_uploaded_file(uploaded_file)

# Function to format grammar tables with proper styling
def format_grammar_table(headers, rows, level_code=None):
    """
    Create an HTML table with proper styling for grammar explanations
    
    Parameters:
    - headers: List of column headers
    - rows: List of rows, where each row is a list of values
    - level_code: Optional level code to style the table appropriately
    
    Returns:
    - HTML string for the formatted table
    """
    # If level code is provided, use its color for the table header
    header_color = get_level_color(level_code) if level_code else "#0066FF"
    
    html = f'<table class="grammar-table" style="border-top: 3px solid {header_color};">'
    
    # Add headers
    html += f'<thead><tr style="background-color: {header_color};">'
    for header in headers:
        html += f'<th>{header}</th>'
    html += '</tr></thead>'
    
    # Add rows
    html += '<tbody>'
    for row in rows:
        html += '<tr>'
        for cell in row:
            html += f'<td>{cell}</td>'
        html += '</tr>'
    html += '</tbody>'
    
    html += '</table>'
    return html

# Function to highlight important grammar points
def highlight_text(text, highlight_type="info", level_code=None):
    """
    Create a highlighted text box for important information
    
    Parameters:
    - text: The text to highlight
    - highlight_type: "info", "warning", or "success"
    - level_code: Optional level code to style the highlight appropriately
    
    Returns:
    - HTML string for the highlighted text
    """
    if level_code:
        # Use level-specific color if level code is provided
        level_color = get_level_color(level_code)
        colors = {
            "info": (f"rgba({','.join(str(int(c * 255)) for c in level_color.strip('#').lstrip('0')[::2])}, 0.1)", level_color),
            "warning": ("#fff3e6", "#ff9500"),
            "success": ("#e6fff0", "#00cc66")
        }
    else:
        colors = {
            "info": ("#e6f7ff", "#0066FF"),  # Light blue background, blue border
            "warning": ("#fff3e6", "#ff9500"),  # Light orange background, orange border
            "success": ("#e6fff0", "#00cc66")  # Light green background, green border
        }
    
    bg_color, border_color = colors.get(highlight_type, colors["info"])
    
    # Add level badge if level code is provided
    level_badge = format_level_badge(level_code) + " " if level_code else ""
    
    html = f"""
    <div style="background-color: {bg_color}; 
                border-left: 4px solid {border_color}; 
                padding: 10px; 
                border-radius: 4px; 
                margin: 10px 0;">
        {level_badge}{text}
    </div>
    """
    return html

# Function to format vocabulary lists in a visually appealing way
def format_vocabulary_list(vocab_pairs, level, language_name=None):
    """
    Create an HTML formatted vocabulary list with level-appropriate styling
    
    Parameters:
    - vocab_pairs: List of tuples (target_word, english_translation)
    - level: The language level (A1, A2, etc.) or full level string
    - language_name: Optional language name to display
    
    Returns:
    - HTML string for the formatted vocabulary list
    """
    # Extract level code if full level string is provided
    if "(" in level:
        level_code = level.split()[0]
    else:
        level_code = level
    
    # Set color based on level
    color = get_level_color(level_code)
    
    # Default to 'Vocabulary' if no language name is provided
    title = f"{language_name} Vocabulary List" if language_name else "Vocabulary List"
    
    html = f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; border-top: 3px solid {color};">'
    
    # Add level badge
    level_badge = format_level_badge(level_code)
    html += f'<h3 style="margin-top: 0; color: {color};">{level_badge} {title}</h3>'
    
    # Add level-specific note
    level_notes = {
        "A1": "Basic, high-frequency words for beginners",
        "A2": "Common everyday vocabulary",
        "B1": "More varied vocabulary for familiar topics",
        "B2": "Broader vocabulary including some specialized terms",
        "C1": "Advanced vocabulary including idiomatic expressions"
    }
    note = level_notes.get(level_code, "")
    if note:
        html += f'<p style="font-style: italic; margin-bottom: 15px;">{note}</p>'
    
    html += '<ul style="list-style-type: none; padding: 0;">'
    
    for target_word, english in vocab_pairs:
        html += f"""
        <li style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;">
            <strong>{target_word}</strong> - {english}
        </li>
        """
    
    html += '</ul></div>'
    return html

# Function to detect language of text (simplified version)
def detect_language(text):
    """
    Simple detection to guess the language of text
    
    Parameters:
    - text: Text to analyze
    
    Returns:
    - Most likely language code
    """
    # Check for character sets that are distinctive to certain languages
    # This is a simplified approach
    
    # Check for Finnish-specific characters
    if re.search(r'[äöå]', text.lower()):
        return "fin"
    
    # Check for Spanish-specific characters/patterns
    if re.search(r'[áéíóúüñ¿¡]', text.lower()):
        return "spa"
    
    # Check for French-specific characters/patterns
    if re.search(r'[àâçéèêëîïôùûüÿœæ]', text.lower()):
        return "fra"
    
    # Check for German-specific characters
    if re.search(r'[äöüß]', text.lower()):
        return "deu"
    
    # Check for Russian Cyrillic
    if re.search(r'[а-яА-Я]', text):
        return "rus"
    
    # Check for Japanese characters
    if re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]', text):
        return "jpn"
    
    # Check for Chinese characters
    if re.search(r'[\u4e00-\u9fff]', text) and not re.search(r'[\u3040-\u30ff]', text):
        return "zho"
    
    # Check for Korean Hangul
    if re.search(r'[\uac00-\ud7a3]', text):
        return "kor"
    
    # Check for Arabic
    if re.search(r'[\u0600-\u06ff]', text):
        return "ara"
    
    # Default to English if no specific patterns are found
    return "eng"

# Function to extract exercise-related parameters from user input
def extract_exercise_parameters(text):
    """
    Extract exercise type and other parameters from user request
    
    Parameters:
    - text: User's request text
    
    Returns:
    - Dictionary with detected parameters
    """
    params = {
        "exercise_type": None,
        "language_direction": None,
        "topic": None
    }
    
    # Detect exercise type
    if re.search(r'\b(reading|read)\b', text, re.IGNORECASE):
        params["exercise_type"] = "reading"
    elif re.search(r'\b(writing|write)\b', text, re.IGNORECASE):
        params["exercise_type"] = "writing"
    elif re.search(r'\b(vocabulary|vocab|words)\b', text, re.IGNORECASE):
        params["exercise_type"] = "vocabulary"
    elif re.search(r'\b(quiz|test|practice)\b', text, re.IGNORECASE):
        params["exercise_type"] = "quiz"
    
    # Detect language direction (generalized)
    from_to_match = re.search(r'\b(from|to)\s+(\w+)\b', text, re.IGNORECASE)
    if from_to_match:
        direction = from_to_match.group(1).lower()
        language = from_to_match.group(2).lower()
        
        if direction == "to" and language == "english":
            params["language_direction"] = "target-to-english"
        elif direction == "from" and language == "english":
            params["language_direction"] = "english-to-target"
    
    # Extract potential topic (this is simplified)
    topic_match = re.search(r'about\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
    if topic_match:
        params["topic"] = topic_match.group(1).strip()
    
    return params

# Function to get language-specific grammar features
def get_language_grammar_features(lang_code):
    """
    Returns specific grammar features for a language
    
    Parameters:
    - lang_code: The language code (fin, spa, etc.)
    
    Returns:
    - Dictionary with grammar features
    """
    grammar_features = {
        "fin": {
            "cases": ["nominative", "genitive", "partitive", "inessive", "elative", "illative", 
                      "adessive", "ablative", "allative", "essive", "translative", "comitative", "instructive"],
            "verb_types": ["Type 1", "Type 2", "Type 3", "Type 4", "Type 5", "Type 6"],
            "special_features": ["consonant gradation", "vowel harmony", "partitive objects"]
        },
        "spa": {
            "tenses": ["presente", "pretérito", "imperfecto", "futuro", "condicional", "perfecto", "pluscuamperfecto"],
            "moods": ["indicativo", "subjuntivo", "imperativo", "condicional"],
            "special_features": ["ser vs estar", "por vs para", "reflexive verbs"]
        },
        "fra": {
            "tenses": ["présent", "passé composé", "imparfait", "futur simple", "conditionnel"],
            "moods": ["indicatif", "subjonctif", "impératif", "conditionnel"],
            "special_features": ["gender agreement", "partitive articles", "negation"]
        },
        "deu": {
            "cases": ["nominativ", "akkusativ", "dativ", "genitiv"],
            "tenses": ["präsens", "präteritum", "perfekt", "futur I", "futur II"],
            "special_features": ["word order", "separable verbs", "modal verbs"]
        },
        "jpn": {
            "particles": ["は", "が", "を", "に", "で", "と", "も"],
            "verb_forms": ["masu form", "dictionary form", "te form", "ta form", "potential form", "passive form"],
            "special_features": ["keigo (politeness levels)", "counter words", "no adjectives"]
        },
        "zho": {
            "particles": ["了", "过", "着", "的", "得", "地"],
            "measure_words": ["个", "只", "张", "条", "块"],
            "special_features": ["tones", "topic-comment structure", "lack of tenses"]
        },
        "rus": {
            "cases": ["nominative", "genitive", "dative", "accusative", "instrumental", "prepositional"],
            "aspects": ["perfective", "imperfective"],
            "special_features": ["verbal aspects", "motion verbs", "hard/soft consonants"]
        }
    }
    
    # Return language-specific features or empty dict if language not found
    return grammar_features.get(lang_code, {})

# Function to get level-appropriate content for a specific language
def get_level_appropriate_content(level_code, language_code="fin"):
    """
    Get vocabulary and grammar structures appropriate for each CEFR level and language
    
    Parameters:
    - level_code: The language level code (A1, A2, etc.)
    - language_code: The language code (fin, spa, etc.)
    
    Returns:
    - Dictionary with level-appropriate content guidelines
    """
    # Base content that's relatively language-agnostic
    base_content = {
        "A1": {
            "grammar": [
                "Basic present tense",
                "Simple questions",
                "Basic negation",
                "Personal pronouns",
                "Numbers 1-100",
                "Basic prepositions"
            ],
            "vocabulary": [
                "Basic greetings and introductions",
                "Family members",
                "Numbers and time expressions",
                "Food and drinks",
                "Basic everyday items",
                "Simple adjectives (good, bad, big, small)",
                "Basic verbs (to be, to have, to go, to come)"
            ],
            "example_sentences": [
                "My name is...",
                "I have a...",
                "She/he goes to...",
                "What are you doing?"
            ]
        },
        "A2": {
            "grammar": [
                "Past tense (simple)",
                "More question forms",
                "Possessives",
                "Plural forms",
                "Comparative forms",
                "More prepositions"
            ],
            "vocabulary": [
                "Weather and seasons",
                "Clothing",
                "Parts of the body",
                "Hobbies and free time",
                "Traveling and transportation",
                "Shopping and services",
                "House and home"
            ],
            "example_sentences": [
                "I went to the store yesterday.",
                "When did you arrive?",
                "My house is bigger than yours.",
                "In summer we go to the beach."
            ]
        },
        "B1": {
            "grammar": [
                "Perfect tenses",
                "Future tense",
                "Conditional forms",
                "Passive voice (simple)",
                "More complex sentence structures",
                "Relative clauses"
            ],
            "vocabulary": [
                "Work and professional life",
                "Education and studies",
                "Media and current events",
                "Health and wellbeing",
                "Nature and environment",
                "Emotions and feelings",
                "Abstract concepts"
            ],
            "example_sentences": [
                "If I had more time, I would study more.",
                "Have you already visited the new museum?",
                "This book was written by a famous author.",
                "Could you explain this again?"
            ]
        },
        "B2": {
            "grammar": [
                "All tenses",
                "Complex verbal constructions",
                "Reported speech",
                "Advanced conditional forms",
                "Expressing hypothesis",
                "Complex modifiers"
            ],
            "vocabulary": [
                "Political and social issues",
                "Science and technology",
                "Economics and business",
                "Arts and culture",
                "Idiomatic expressions",
                "Academic vocabulary",
                "Specialized terminology"
            ],
            "example_sentences": [
                "Experts claim that climate change significantly affects our planet.",
                "Without your help, I wouldn't have been able to solve this problem.",
                "If only I had studied harder!",
                "The matter will be announced later."
            ]
        },
        "C1": {
            "grammar": [
                "All grammatical structures",
                "Complex constructions",
                "Nuanced tense and mood usage",
                "Literary and formal structures",
                "Sophisticated syntax",
                "Dialectal variations"
            ],
            "vocabulary": [
                "Specialized professional terminology",
                "Literary and poetic language",
                "Colloquial and dialectal expressions",
                "Cultural references",
                "Humor and wordplay",
                "Philosophical concepts",
                "Very specific domain knowledge"
            ],
            "example_sentences": [
                "Had the government approved the bill, we would have had to change our entire operating model.",
                "The questions that emerged in the research will be addressed in more detail in future publications.",
                "His/her works reflect the transition period of society in the post-war era.",
                "Having said that, I realized I had made a mistake."
            ]
        }
    }
    
    # Language-specific content
    language_specific = {
        "fin": {
            "A1": {
                "grammar": [
                    "Basic present tense verb conjugation",
                    "Simple noun cases: nominative, partitive, genitive",
                    "Personal pronouns",
                    "Simple questions with question words",
                    "Basic negative sentences",
                    "Numbers 1-100",
                    "Simple consonant gradation (kk-k, pp-p, tt-t)"
                ],
                "vocabulary": [
                    "Basic greetings and introductions",
                    "Family members",
                    "Numbers and time expressions",
                    "Food and drinks",
                    "Basic everyday items",
                    "Simple adjectives (hyvä, paha, iso, pieni)",
                    "Basic verbs (olla, olla jollakin, mennä, tulla)"
                ],
                "example_sentences": [
                    "Minä olen Anna. (I am Anna.)",
                    "Minulla on koira. (I have a dog.)",
                    "Hän menee kauppaan. (He/she goes to the store.)",
                    "Mitä sinä teet? (What are you doing?)"
                ]
            },
            "A2": {
                "grammar": [
                    "All verb types in present tense",
                    "Past tense (imperfect)",
                    "Consonant gradation (more patterns)",
                    "Locative cases (inessive, elative, illative)",
                    "More question forms",
                    "Possessive suffixes (basic use)",
                    "Plural forms of nouns"
                ],
                "vocabulary": [
                    "Weather and seasons",
                    "Clothing",
                    "Parts of the body",
                    "Hobbies and free time",
                    "Traveling and transportation",
                    "Shopping and services",
                    "House and home"
                ],
                "example_sentences": [
                    "Minä kävin eilen kaupassa. (I went to the store yesterday.)",
                    "Milloin sinä tulit Suomeen? (When did you come to Finland?)",
                    "Minun autoni on sininen. (My car is blue.)",
                    "Kesällä me menemme mökille. (In summer we go to the cottage.)"
                ]
            }
        },
        "spa": {
            "A1": {
                "grammar": [
                    "Present tense of regular -ar, -er, -ir verbs",
                    "Present tense of common irregular verbs (ser, estar, ir, tener)",
                    "Gender and number agreement",
                    "Definite and indefinite articles",
                    "Basic prepositions",
                    "Subject pronouns",
                    "Basic question words"
                ],
                "vocabulary": [
                    "Greetings and farewells",
                    "Family and relationships",
                    "Numbers and time",
                    "Food and restaurants",
                    "Daily activities",
                    "Basic adjectives",
                    "Countries and nationalities"
                ],
                "example_sentences": [
                    "Me llamo Juan. (My name is Juan.)",
                    "¿De dónde eres? (Where are you from?)",
                    "Tengo dos hermanos. (I have two siblings.)",
                    "Me gusta el café. (I like coffee.)"
                ]
            },
            "A2": {
                "grammar": [
                    "Preterite tense of regular verbs",
                    "Preterite of common irregular verbs",
                    "Imperfect tense",
                    "Reflexive verbs",
                    "Direct and indirect object pronouns",
                    "Comparatives and superlatives",
                    "Simple commands (tú form)"
                ],
                "vocabulary": [
                    "Shopping and clothing",
                    "Travel and transportation",
                    "House and furniture",
                    "Daily routines",
                    "Weather and seasons",
                    "Health and body parts",
                    "City and directions"
                ],
                "example_sentences": [
                    "Ayer fui al cine. (Yesterday I went to the movies.)",
                    "Cuando era niño, jugaba al fútbol. (When I was a child, I used to play soccer.)",
                    "Me duele la cabeza. (My head hurts.)",
                    "¿Cómo llego al museo? (How do I get to the museum?)"
                ]
            }
        }
    }
    
    # Start with base content for the level
    content = base_content.get(level_code, {})
    
    # If we have language-specific content for this level, override with it
    if language_code in language_specific and level_code in language_specific[language_code]:
        for key, value in language_specific[language_code][level_code].items():
            content[key] = value
    
    return content













# import streamlit as st
# import base64
# from io import BytesIO
# import re
# import mimetypes

# # Level-specific color scheme
# def get_level_color(level_code):
#     """
#     Get the color associated with a specific CEFR level
    
#     Parameters:
#     - level_code: The Finnish language level code (A1, A2, etc.)
    
#     Returns:
#     - Hex color code
#     """
#     level_colors = {
#         "A1": "#4CAF50",  # Green for beginner
#         "A2": "#8BC34A",  # Light green for elementary
#         "B1": "#2196F3",  # Blue for intermediate
#         "B2": "#3F51B5",  # Indigo for upper intermediate
#         "C1": "#9C27B0"   # Purple for advanced
#     }
#     return level_colors.get(level_code, "#0066FF")

# # Function to create HTML level badge
# def format_level_badge(level_code):
#     """
#     Create an HTML-formatted level badge
    
#     Parameters:
#     - level_code: The Finnish language level code (A1, A2, etc.)
    
#     Returns:
#     - HTML string for the formatted badge
#     """
#     color = get_level_color(level_code)
#     return f'<span class="level-badge {level_code}" style="background-color: {color};">{level_code}</span>'

# # Function to process uploaded files (any type)
# def process_uploaded_file(uploaded_file):
#     """
#     Process an uploaded file of any type to prepare it for analysis by the LLM
#     """
#     if uploaded_file is None:
#         return None
    
#     # Read the file
#     bytes_data = uploaded_file.getvalue()
    
#     # Convert to base64 for displaying or sending to API
#     base64_file = base64.b64encode(bytes_data).decode('utf-8')
    
#     # Attempt to detect file type if not provided
#     file_type = uploaded_file.type
#     if not file_type:
#         # Try to guess the MIME type based on filename
#         guessed_type, _ = mimetypes.guess_type(uploaded_file.name)
#         if guessed_type:
#             file_type = guessed_type
#         else:
#             # Default to binary if can't determine
#             file_type = "application/octet-stream"
    
#     # Determine if file is text-based for potential direct content extraction
#     is_text_file = file_type.startswith(('text/', 'application/json', 'application/xml'))
    
#     # For text files, try to extract content
#     text_content = None
#     if is_text_file:
#         try:
#             text_content = bytes_data.decode('utf-8')
#         except UnicodeDecodeError:
#             # If UTF-8 fails, try other common encodings
#             try:
#                 text_content = bytes_data.decode('latin-1')
#             except:
#                 # If still can't decode, leave as None
#                 pass
    
#     # Include the current language level in the processed file data
#     # This ensures the level is available when processing the file
#     current_level = st.session_state.selected_level
#     level_code = current_level.split()[0]  # Extract just the level code (A1, A2, etc.)
    
#     return {
#         "name": uploaded_file.name,
#         "data": bytes_data,
#         "base64": base64_file,
#         "type": file_type,
#         "is_text_file": is_text_file,
#         "text_content": text_content,
#         "language_level": current_level,
#         "level_code": level_code
#     }

# # Legacy function for backward compatibility
# def process_uploaded_image(uploaded_file):
#     """
#     Legacy function that calls the more generic process_uploaded_file
#     Kept for backward compatibility
#     """
#     return process_uploaded_file(uploaded_file)

# # Function to format grammar tables with proper styling
# def format_grammar_table(headers, rows, level_code=None):
#     """
#     Create an HTML table with proper styling for grammar explanations
    
#     Parameters:
#     - headers: List of column headers
#     - rows: List of rows, where each row is a list of values
#     - level_code: Optional level code to style the table appropriately
    
#     Returns:
#     - HTML string for the formatted table
#     """
#     # If level code is provided, use its color for the table header
#     header_color = get_level_color(level_code) if level_code else "#0066FF"
    
#     html = f'<table class="grammar-table" style="border-top: 3px solid {header_color};">'
    
#     # Add headers
#     html += f'<thead><tr style="background-color: {header_color};">'
#     for header in headers:
#         html += f'<th>{header}</th>'
#     html += '</tr></thead>'
    
#     # Add rows
#     html += '<tbody>'
#     for row in rows:
#         html += '<tr>'
#         for cell in row:
#             html += f'<td>{cell}</td>'
#         html += '</tr>'
#     html += '</tbody>'
    
#     html += '</table>'
#     return html

# # Function to highlight important grammar points
# def highlight_text(text, highlight_type="info", level_code=None):
#     """
#     Create a highlighted text box for important information
    
#     Parameters:
#     - text: The text to highlight
#     - highlight_type: "info", "warning", or "success"
#     - level_code: Optional level code to style the highlight appropriately
    
#     Returns:
#     - HTML string for the highlighted text
#     """
#     if level_code:
#         # Use level-specific color if level code is provided
#         level_color = get_level_color(level_code)
#         colors = {
#             "info": (f"rgba({','.join(str(int(c * 255)) for c in level_color.strip('#').lstrip('0')[::2])}, 0.1)", level_color),
#             "warning": ("#fff3e6", "#ff9500"),
#             "success": ("#e6fff0", "#00cc66")
#         }
#     else:
#         colors = {
#             "info": ("#e6f7ff", "#0066FF"),  # Light blue background, blue border
#             "warning": ("#fff3e6", "#ff9500"),  # Light orange background, orange border
#             "success": ("#e6fff0", "#00cc66")  # Light green background, green border
#         }
    
#     bg_color, border_color = colors.get(highlight_type, colors["info"])
    
#     # Add level badge if level code is provided
#     level_badge = format_level_badge(level_code) + " " if level_code else ""
    
#     html = f"""
#     <div style="background-color: {bg_color}; 
#                 border-left: 4px solid {border_color}; 
#                 padding: 10px; 
#                 border-radius: 4px; 
#                 margin: 10px 0;">
#         {level_badge}{text}
#     </div>
#     """
#     return html

# # Function to format vocabulary lists in a visually appealing way
# def format_vocabulary_list(vocab_pairs, level):
#     """
#     Create an HTML formatted vocabulary list with level-appropriate styling
    
#     Parameters:
#     - vocab_pairs: List of tuples (finnish_word, english_translation)
#     - level: The Finnish language level (A1, A2, etc.) or full level string
    
#     Returns:
#     - HTML string for the formatted vocabulary list
#     """
#     # Extract level code if full level string is provided
#     if "(" in level:
#         level_code = level.split()[0]
#     else:
#         level_code = level
    
#     # Set color based on level
#     color = get_level_color(level_code)
    
#     html = f'<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0; border-top: 3px solid {color};">'
    
#     # Add level badge
#     level_badge = format_level_badge(level_code)
#     html += f'<h3 style="margin-top: 0; color: {color};">{level_badge} Vocabulary List</h3>'
    
#     # Add level-specific note
#     level_notes = {
#         "A1": "Basic, high-frequency words for beginners",
#         "A2": "Common everyday vocabulary",
#         "B1": "More varied vocabulary for familiar topics",
#         "B2": "Broader vocabulary including some specialized terms",
#         "C1": "Advanced vocabulary including idiomatic expressions"
#     }
#     note = level_notes.get(level_code, "")
#     if note:
#         html += f'<p style="font-style: italic; margin-bottom: 15px;">{note}</p>'
    
#     html += '<ul style="list-style-type: none; padding: 0;">'
    
#     for finnish, english in vocab_pairs:
#         html += f"""
#         <li style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;">
#             <strong>{finnish}</strong> - {english}
#         </li>
#         """
    
#     html += '</ul></div>'
#     return html

# # Function to detect language of text
# def detect_language(text):
#     """
#     Simple detection to guess if text is Finnish or English
    
#     Parameters:
#     - text: Text to analyze
    
#     Returns:
#     - "finnish" or "english" based on character frequency
#     """
#     # Count Finnish-specific characters
#     finnish_chars = ['ä', 'ö', 'å']
#     finnish_char_count = sum(text.lower().count(c) for c in finnish_chars)
    
#     # If Finnish characters present, likely Finnish
#     if finnish_char_count > 0:
#         return "finnish"
    
#     # Otherwise assume English (this is very simplified)
#     return "english"

# # Function to extract exercise-related parameters from user input
# def extract_exercise_parameters(text):
#     """
#     Extract exercise type and other parameters from user request
    
#     Parameters:
#     - text: User's request text
    
#     Returns:
#     - Dictionary with detected parameters
#     """
#     params = {
#         "exercise_type": None,
#         "language_direction": None,
#         "topic": None
#     }
    
#     # Detect exercise type
#     if re.search(r'\b(reading|read)\b', text, re.IGNORECASE):
#         params["exercise_type"] = "reading"
#     elif re.search(r'\b(writing|write)\b', text, re.IGNORECASE):
#         params["exercise_type"] = "writing"
#     elif re.search(r'\b(vocabulary|vocab|words)\b', text, re.IGNORECASE):
#         params["exercise_type"] = "vocabulary"
#     elif re.search(r'\b(quiz|test|practice)\b', text, re.IGNORECASE):
#         params["exercise_type"] = "quiz"
    
#     # Detect language direction
#     if re.search(r'\b(finnish to english|fin to eng|finnish-english)\b', text, re.IGNORECASE):
#         params["language_direction"] = "finnish-to-english"
#     elif re.search(r'\b(english to finnish|eng to fin|english-finnish)\b', text, re.IGNORECASE):
#         params["language_direction"] = "english-to-finnish"
    
#     # Extract potential topic (this is simplified)
#     topic_match = re.search(r'about\s+([a-zA-Z\s]+)', text, re.IGNORECASE)
#     if topic_match:
#         params["topic"] = topic_match.group(1).strip()
    
#     return params

# # Function to get level-appropriate vocabulary and grammar
# def get_level_appropriate_content(level_code):
#     """
#     Get vocabulary and grammar structures appropriate for each CEFR level
    
#     Parameters:
#     - level_code: The Finnish language level code (A1, A2, etc.)
    
#     Returns:
#     - Dictionary with level-appropriate content guidelines
#     """
#     level_content = {
#         "A1": {
#             "grammar": [
#                 "Basic present tense verb conjugation",
#                 "Simple noun cases: nominative, partitive, genitive",
#                 "Personal pronouns",
#                 "Simple questions with question words",
#                 "Basic negative sentences",
#                 "Numbers 1-100",
#                 "Simple consonant gradation (kk-k, pp-p, tt-t)"
#             ],
#             "vocabulary": [
#                 "Basic greetings and introductions",
#                 "Family members",
#                 "Numbers and time expressions",
#                 "Food and drinks",
#                 "Basic everyday items",
#                 "Simple adjectives (good, bad, big, small)",
#                 "Basic verbs (to be, to have, to go, to come)"
#             ],
#             "example_sentences": [
#                 "Minä olen Anna. (I am Anna.)",
#                 "Minulla on koira. (I have a dog.)",
#                 "Hän menee kauppaan. (He/she goes to the store.)",
#                 "Mitä sinä teet? (What are you doing?)"
#             ]
#         },
#         "A2": {
#             "grammar": [
#                 "All verb types in present tense",
#                 "Past tense (imperfect)",
#                 "Consonant gradation (more patterns)",
#                 "Locative cases (inessive, elative, illative)",
#                 "More question forms",
#                 "Possessive suffixes (basic use)",
#                 "Plural forms of nouns"
#             ],
#             "vocabulary": [
#                 "Weather and seasons",
#                 "Clothing",
#                 "Parts of the body",
#                 "Hobbies and free time",
#                 "Traveling and transportation",
#                 "Shopping and services",
#                 "House and home"
#             ],
#             "example_sentences": [
#                 "Minä kävin eilen kaupassa. (I went to the store yesterday.)",
#                 "Milloin sinä tulit Suomeen? (When did you come to Finland?)",
#                 "Minun autoni on sininen. (My car is blue.)",
#                 "Kesällä me menemme mökille. (In summer we go to the cottage.)"
#             ]
#         },
#         "B1": {
#             "grammar": [
#                 "Perfect and pluperfect tenses",
#                 "Conditional mood",
#                 "Object cases rules",
#                 "More complex sentence structures",
#                 "Comparative and superlative forms",
#                 "All locative cases (also adessive, ablative, allative)",
#                 "Passive voice (present and past)"
#             ],
#             "vocabulary": [
#                 "Work and professional life",
#                 "Education and studies",
#                 "Media and current events",
#                 "Health and wellbeing",
#                 "Nature and environment",
#                 "Emotions and feelings",
#                 "Abstract concepts"
#             ],
#             "example_sentences": [
#                 "Jos minulla olisi enemmän aikaa, opiskelisin enemmän suomea. (If I had more time, I would study more Finnish.)",
#                 "Oletko jo käynyt uudessa museossa? (Have you already visited the new museum?)",
#                 "Suomessa luetaan paljon kirjoja. (In Finland, people read a lot of books [passive].)",
#                 "Voisitko selittää tämän uudestaan? (Could you explain this again?)"
#             ]
#         },
#         "B2": {
#             "grammar": [
#                 "Potential mood",
#                 "Participles and infinitive forms",
#                 "Complex sentence structures",
#                 "Imperative forms (all persons)",
#                 "Indirect speech",
#                 "Complex object rules",
#                 "Expressing hypothetical situations"
#             ],
#             "vocabulary": [
#                 "Political and social issues",
#                 "Science and technology",
#                 "Economics and business",
#                 "Arts and culture",
#                 "Idiomatic expressions",
#                 "Academic vocabulary",
#                 "Specialized terminology"
#             ],
#             "example_sentences": [
#                 "Asiantuntijat väittävät, että ilmastonmuutos vaikuttaa merkittävästi Suomen luontoon. (Experts claim that climate change significantly affects Finland's nature.)",
#                 "Ilman sinun apuasi en olisi pystynyt ratkaisemaan tätä ongelmaa. (Without your help, I wouldn't have been able to solve this problem.)",
#                 "Kunpa olisin opiskellut ahkerammin! (If only I had studied harder!)",
#                 "Asiasta tiedotetaan myöhemmin. (The matter will be announced later [passive].)"
#             ]
#         },
#         "C1": {
#             "grammar": [
#                 "All verb forms and moods",
#                 "Complex participle constructions",
#                 "Rare case uses",
#                 "Subtle differences in meaning",
#                 "Complex compound words",
#                 "Advanced sentence structures",
#                 "Literary and formal language"
#             ],
#             "vocabulary": [
#                 "Specialized professional terminology",
#                 "Literary and poetic language",
#                 "Colloquial and dialectal expressions",
#                 "Cultural references",
#                 "Humor and wordplay",
#                 "Philosophical concepts",
#                 "Very specific domain knowledge"
#             ],
#             "example_sentences": [
#                 "Mikäli hallitus olisi hyväksynyt lakiesityksen, olisimme joutuneet muuttamaan koko toimintamalliamme. (Had the government approved the bill, we would have had to change our entire operating model.)",
#                 "Tutkimuksessa esiin nousseita kysymyksiä käsitellään tarkemmin tulevissa julkaisuissa. (The questions that emerged in the research will be addressed in more detail in future publications.)",
#                 "Hänen teoksensa kuvastavat suomalaisen yhteiskunnan murrosvaihetta sodanjälkeisessä Suomessa. (His/her works reflect the transition period of Finnish society in post-war Finland.)",
#                 "Sanottuani sen tajusin tehneeni virheen. (Having said that, I realized I had made a mistake.)"
#             ]
#         }
#     }
    
#     return level_content.get(level_code, {})
