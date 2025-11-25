import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import pytz
from ulid import ULID

# Set timezone for Thailand/Bangkok
TIMEZONE = pytz.timezone("Asia/Bangkok")

# Category detection keywords
CATEGORIES = {
    "Computer Science": [
        "programming",
        "python",
        "java",
        "software",
        "development",
        "coding",
        "algorithm",
        "data structure",
        "web development",
        "app development",
        "database",
        "computer",
        "tech",
        "software engineering",
    ],
    "Data Science": [
        "data",
        "analytics",
        "machine learning",
        "statistics",
        "visualization",
        "big data",
        "data mining",
        "predictive",
        "modeling",
        "artificial intelligence",
    ],
    "Business": [
        "business",
        "management",
        "marketing",
        "entrepreneurship",
        "finance",
        "accounting",
        "leadership",
        "strategy",
        "economics",
        "project management",
    ],
    "Humanities": [
        "history",
        "philosophy",
        "literature",
        "art",
        "music",
        "culture",
        "ethics",
        "religion",
        "language",
        "writing",
    ],
    "Science": [
        "biology",
        "chemistry",
        "physics",
        "mathematics",
        "environmental",
        "health",
        "medicine",
        "psychology",
        "neuroscience",
        "research",
    ],
    "Social Sciences": [
        "sociology",
        "political science",
        "psychology",
        "anthropology",
        "economics",
        "law",
        "justice",
        "policy",
        "social",
        "education",
    ],
    "Engineering": [
        "engineering",
        "electrical",
        "mechanical",
        "civil",
        "chemical",
        "biomedical",
        "aerospace",
        "robotics",
        "materials",
        "systems",
    ],
    "Language Learning": [
        "language",
        "chinese",
        "spanish",
        "french",
        "german",
        "japanese",
        "arabic",
        "english",
        "korean",
        "italian",
        "portuguese",
        "russian",
    ],
}

# Subcategories based on categories
SUBCATEGORIES = {
    "Computer Science": [
        "Programming Languages",
        "Software Development",
        "Web Development",
        "Data Structures",
        "Algorithms",
        "Database Management",
        "Computer Architecture",
    ],
    "Data Science": [
        "Data Analysis",
        "Machine Learning",
        "Data Visualization",
        "Statistics",
        "Predictive Modeling",
        "Big Data Technologies",
    ],
    "Business": [
        "Management",
        "Marketing",
        "Entrepreneurship",
        "Finance",
        "Accounting",
        "Leadership",
        "Business Strategy",
        "Project Management",
    ],
    "Humanities": [
        "History",
        "Philosophy",
        "Literature",
        "Art History",
        "Music",
        "Cultural Studies",
        "Ethics",
        "Religious Studies",
    ],
    "Science": [
        "Biology",
        "Chemistry",
        "Physics",
        "Mathematics",
        "Environmental Science",
        "Health Sciences",
        "Psychology",
        "Neuroscience",
    ],
    "Social Sciences": [
        "Sociology",
        "Political Science",
        "Anthropology",
        "Economics",
        "Law",
        "Education",
        "Public Policy",
    ],
    "Engineering": [
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Biomedical Engineering",
        "Robotics",
    ],
    "Language Learning": [
        "Chinese",
        "Spanish",
        "French",
        "German",
        "Japanese",
        "Arabic",
        "English",
        "Korean",
        "Italian",
        "Portuguese",
    ],
}

# Content title templates for different categories
CONTENT_TEMPLATES = {
    "Computer Science": [
        "Introduction to {topic}",
        "Variables and Data Types",
        "Control Structures",
        "Functions and Methods",
        "Advanced {topic}",
    ],
    "Data Science": [
        "Introduction to {topic}",
        "Data Collection and Cleaning",
        "Exploratory Data Analysis",
        "Model Building",
        "Advanced {topic} Techniques",
    ],
    "Business": [
        "Introduction to {topic}",
        "Core Concepts",
        "Strategic Implementation",
        "Case Studies",
        "Advanced {topic}",
    ],
    "Humanities": [
        "Introduction to {topic}",
        "Historical Context",
        "Key Concepts",
        "Cultural Impact",
        "Modern {topic}",
    ],
    "Science": [
        "Introduction to {topic}",
        "Fundamental Principles",
        "Experimental Methods",
        "Applications",
        "Advanced {topic} Topics",
    ],
    "Social Sciences": [
        "Introduction to {topic}",
        "Theoretical Frameworks",
        "Research Methods",
        "Case Studies",
        "Contemporary {topic}",
    ],
    "Engineering": [
        "Introduction to {topic}",
        "Design Principles",
        "Analysis Methods",
        "Implementation",
        "Advanced {topic}",
    ],
    "Language Learning": [
        "Introduction to {language}",
        "Pinyin and Characters",
        "Grammar and Sentence Structure",
        "Reading and Writing",
        "Listening and Speaking",
    ],
}

# Language-specific templates
LANGUAGE_TEMPLATES = {
    "Chinese": [
        "Introduction to Mandarin Chinese",
        "Pinyin and Characters",
        "Grammar and Sentence Structure",
        "Reading and Writing",
        "Listening and Speaking",
    ],
    "Spanish": [
        "Introduction to Spanish",
        "Basic Vocabulary",
        "Grammar Essentials",
        "Reading Comprehension",
        "Conversation Practice",
    ],
    "French": [
        "Introduction to French",
        "Pronunciation Basics",
        "Grammar Fundamentals",
        "Reading Texts",
        "Speaking Exercises",
    ],
    "German": [
        "Introduction to German",
        "Basic Phrases",
        "Grammar Rules",
        "Reading Practice",
        "Listening Comprehension",
    ],
    "Japanese": [
        "Introduction to Japanese",
        "Hiragana and Katakana",
        "Basic Grammar",
        "Reading Practice",
        "Speaking Practice",
    ],
    "Arabic": [
        "Introduction to Arabic",
        "Arabic Alphabet",
        "Basic Grammar",
        "Reading Skills",
        "Conversational Arabic",
    ],
}


def detect_category(description: str, title: str) -> str:
    """Detect category based on description and title"""
    text = (description + " " + title).lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            scores[category] = score

    if not scores:
        return "Humanities"  # Default category

    return max(scores, key=scores.get)


def detect_subcategory(description: str, category: str) -> str:
    """Detect subcategory based on description and category"""
    if category not in SUBCATEGORIES:
        return "General"

    subcategories = SUBCATEGORIES[category]
    text = description.lower()
    scores = {}

    for subcategory in subcategories:
        # Extract key terms from subcategory
        key_terms = subcategory.lower().split()
        score = sum(1 for term in key_terms if term in text)
        if score > 0:
            scores[subcategory] = score

    if not scores:
        # If no match, return the first subcategory of the category
        return subcategories[0]

    return max(scores, key=scores.get)


def extract_main_topic(title: str) -> str:
    """Extract the main topic from a course title"""
    # Try to extract the main topic by removing parenthetical explanations
    main_topic = re.sub(r"\([^)]*\)", "", title).strip()

    # Further clean up
    main_topic = re.sub(r"Level \d+", "", main_topic).strip()
    main_topic = re.sub(r"\d+", "", main_topic).strip()
    main_topic = re.sub(r":.*", "", main_topic).strip()

    # If the title contains "Introduction to", extract what follows
    if "introduction to" in main_topic.lower():
        return re.sub(r".*introduction to", "", main_topic, flags=re.IGNORECASE).strip()

    # For language courses, extract the language
    for language in ["Chinese", "Spanish", "French", "German", "Japanese", "Arabic"]:
        if language in main_topic:
            return language

    # Otherwise, try to get the first meaningful term
    words = main_topic.split()
    if len(words) >= 2:
        return words[-2] + " " + words[-1]
    elif len(words) >= 1:
        return words[0]

    return main_topic


def generate_content_titles(title: str, description: str, category: str) -> str:
    """Generate 4-5 content titles as a comma-separated string based on the course title and description"""

    # Check if it's a language course first
    for language, template in LANGUAGE_TEMPLATES.items():
        if language.lower() in title.lower():
            return ",".join(template)

    # Extract main topic for template substitution
    main_topic = extract_main_topic(title)

    # Get the appropriate template
    if category in CONTENT_TEMPLATES:
        template = CONTENT_TEMPLATES[category]
    else:
        template = CONTENT_TEMPLATES["Humanities"]  # Default template

    # Generate titles by applying the template
    content_titles = []
    for item in template:
        if "{topic}" in item:
            content_titles.append(item.format(topic=main_topic))
        elif "{language}" in item:
            content_titles.append(item.format(language=main_topic))
        else:
            content_titles.append(item)

    return ",".join(content_titles[:5])  # Ensure we only return 5 titles


def generate_id() -> str:
    """Generate a ULID for the id field"""
    return str(ULID())


def generate_timestamps() -> Tuple[str, str, str]:
    """Generate createdAt, updatedAt timestamps in Thailand timezone"""
    now = datetime.now(TIMEZONE)
    created_at = now - timedelta(days=random.randint(1, 365))
    updated_at = now - timedelta(days=random.randint(0, 30))
    deleted_at = None  # Most courses are not deleted

    return (
        created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        deleted_at,
    )


def generate_random_id() -> str:
    """Generate a random ID for coverImageId and previewVideoId"""
    return str(ULID())


def main():
    """Main function to process the CSV and generate mock data"""
    # Read the original CSV file
    try:
        df = pd.read_csv("./Edx.csv")
    except FileNotFoundError:
        print(
            "Error: ./Edx.csv file not found. Please ensure the file exists in the current directory."
        )
        return

    # Create a new DataFrame with the required columns
    output_data = []

    for _, row in df.iterrows():
        # Extract data from the original row
        lessontitle = row["Name"]
        university = row["University"]
        level = row["Difficulty Level"]
        link = row["Link"]
        short_description = row["About"]
        description = row["Course Description"]

        # Handle missing values
        if pd.isna(short_description):
            short_description = (
                description[:100] + "..." if not pd.isna(description) else ""
            )
        if pd.isna(description):
            description = short_description

        # Detect category and subcategory
        category = detect_category(description, lessontitle)
        subcategory = detect_subcategory(description, category)

        # Generate content titles as comma-separated string
        content_titles_str = generate_content_titles(lessontitle, description, category)

        # Generate timestamps
        created_at, updated_at, deleted_at = generate_timestamps()

        # Generate IDs
        id = generate_id()
        cover_image_id = generate_random_id()
        preview_video_id = generate_random_id()

        # Set status (most courses are active)
        status = "active"

        # Create the output row
        output_row = {
            "id": id,
            "lessontitle": lessontitle,
            "contentTitle": content_titles_str,  # Now using comma-separated string
            "skillName": f"{category} Skills",
            "level": level,
            "categoryId": f"cat_{category.replace(' ', '_').lower()}",
            "catName": category,
            "subCatName": subcategory,
            "coverImageId": cover_image_id,
            "previewVideoId": preview_video_id,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "deletedAt": deleted_at,
            "status": status,
            "shortDescription": short_description,
            "description": description,
            "university": university,
            "link": link,
        }

        output_data.append(output_row)

    # Create a new DataFrame with the output data
    output_df = pd.DataFrame(output_data)

    # Save to CSV
    output_df.to_csv("./COURSE_CATALOG.csv", index=False)
    print(
        f"Successfully generated COURSE_CATALOG.csv with {len(output_df)} rows of data."
    )


if __name__ == "__main__":
    main()
