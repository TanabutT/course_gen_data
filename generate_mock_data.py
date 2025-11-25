import json
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import pytz
import requests
from dotenv import load_dotenv
from ulid import ULID

# Load environment variables from .env file
load_dotenv()


# Function to get API key from multiple sources
def get_api_key():
    # First check environment variable
    api_key = os.environ.get("GLM_API_KEY")
    if api_key:
        return api_key

    # Then check .env file
    try:
        with open(".env/GLM_API_KEY.env", "r") as f:
            for line in f:
                if line.startswith("GLM_API_KEY="):
                    return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        pass

    return None


def generate_content_titles(lesson_title, description, category_name):
    """
    Generate meaningful content titles using the GLM-4.6 API to analyze lesson title and description.
    The function:
    1. Analyzes the lesson title and short description to break into contents
    2. Identifies the main topic and subtopics within the content
    3. Uses GLM-4.6 to generate a list of 4-5 relevant content titles that logically belong in the course
    4. Special handling for language courses with dedicated prompts for Chinese, Spanish, French, German, Japanese, and Arabic

    ## Implementation Note
    This function uses the GLM-4.6 API to generate content titles dynamically based on the lesson title and description.
    The system:
    1. Analyzes the lesson title and short description to break into contents
    2. Identifies the main topic and subtopics within the content
    3. Generates a list of 4-5 relevant content titles that logically belong in the course
    4. Special handling for language courses with dedicated templates for Chinese, Spanish, French, German, Japanese, and Arabic
    4. Special handling for language courses with dedicated templates for Chinese, Spanish, French, German, Japanese, and Arabic
    """
    try:
        # Get API key from multiple sources
        api_key = get_api_key()
        if not api_key:
            print(
                "Warning: GLM_API_KEY not found in environment variables or .env file. Using fallback content generation."
            )
            return generate_fallback_content_titles(
                lesson_title, description, category_name
            )

        # API endpoint
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # Determine if it's a language course for special handling
        language_keywords = {
            "chinese": ["chinese", "mandarin", "中文", "汉语"],
            "spanish": ["spanish", "español", "español"],
            "french": ["french", "français", "français"],
            "german": ["german", "deutsch"],
            "japanese": ["japanese", "日本語", "日本語"],
            "arabic": ["arabic", "العربية"],
        }

        combined_text = f"{lesson_title} {description}".lower()

        # Check if it's a language course
        language_course = None
        for language, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in combined_text:
                    language_course = language
                    break
            if language_course:
                break

        # Create specialized prompt based on whether it's a language course
        if language_course:
            system_prompt = f"""You are a course content designer specializing in {language_course} language courses.
            Based on the lesson title and description, generate 4-5 logical content titles that would be part of this {language_course} language course.
            The titles should follow a logical progression for language learning."""
        else:
            system_prompt = """You are a course content designer. Based on the lesson title and description,
            generate 4-5 logical content titles that would be part of this course.
            The titles should follow a logical progression from basic concepts to more advanced topics."""

        # Prepare the prompt with lesson title and description
        user_prompt = f"""Lesson Title: {lesson_title}

        Description: {description}

        Category: {category_name}

        Generate 4-5 content titles that would logically be part of this course.
        Return only the titles as a JSON array, with no additional text."""

        # Prepare the request payload
        payload = {
            "model": "glm-4.6",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 500,
            "response_format": {
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "titles": {"type": "array", "items": {"type": "string"}}
                    },
                },
            },
        }

        # Make the API call
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        # Parse the response
        result = response.json()

        # Extract the titles
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            try:
                # Try to parse as JSON
                content_data = json.loads(content)
                if "titles" in content_data and len(content_data["titles"]) > 0:
                    return content_data["titles"][
                        :5
                    ]  # Ensure we return at most 5 titles
            except json.JSONDecodeError:
                # Fallback: try to extract titles from text response
                titles = []
                lines = content.strip().split("\n")
                for line in lines:
                    line = line.strip()
                    # Remove potential numbering or bullets
                    if line.startswith(("-", "*", "1.", "2.", "3.", "4.", "5.")):
                        line = (
                            line[1:].strip()
                            if line.startswith("-", "*")
                            else line[2:].strip()
                        )
                    if line and len(line) > 0:
                        titles.append(line)
                        if len(titles) >= 5:
                            break
                if titles:
                    return titles

        # If all else fails, use fallback
        return generate_fallback_content_titles(
            lesson_title, description, category_name
        )

    except Exception as e:
        print(f"Error generating content titles with GLM-4.6 API: {str(e)}")
        return generate_fallback_content_titles(
            lesson_title, description, category_name
        )


def generate_fallback_content_titles(lesson_title, description, category_name):
    """
    Fallback method to generate content titles when API is not available.
    Uses rule-based approach similar to the original implementation.
    """
    # Convert to lowercase for case-insensitive matching
    lesson_title = lesson_title.lower()
    description = description.lower()

    # Combine lesson title and description for comprehensive analysis
    combined_text = f"{lesson_title} {description}"

    # Extract main topic using keyword analysis
    main_topic = identify_main_topic(combined_text, category_name)

    # Extract subtopics from the content
    subtopics = identify_subtopics(combined_text, main_topic)

    # Generate content titles based on the identified topic and subtopics
    content_titles = generate_titles_for_topic(main_topic, subtopics)

    return content_titles


def identify_main_topic(combined_text, category_name):
    """
    Identify the main topic of the course based on keyword analysis.
    Special handling for language courses.
    """
    # Check for language courses first as they have special handling
    language_keywords = {
        "chinese": ["chinese", "mandarin", "中文", "汉语"],
        "spanish": ["spanish", "español", "español"],
        "french": ["french", "français", "français"],
        "german": ["german", "deutsch"],
        "japanese": ["japanese", "日本語", "日本語"],
        "arabic": ["arabic", "العربية"],
    }

    # Check for specific language keywords
    for language, keywords in language_keywords.items():
        for keyword in keywords:
            if keyword in combined_text:
                return language

    # Define topic keywords for different categories
    topic_keywords = {
        "Computer Science": [
            ("python", "Python"),
            ("programming", "Programming"),
            ("javascript", "JavaScript"),
            ("java", "Java"),
            ("web development", "Web Development"),
            ("artificial intelligence", "Artificial Intelligence"),
            ("ai", "Artificial Intelligence"),
            ("machine learning", "Machine Learning"),
            ("ml", "Machine Learning"),
            ("deep learning", "Deep Learning"),
            ("data science", "Data Science"),
            ("data structures", "Data Structures"),
            ("algorithms", "Algorithms"),
            ("computer science", "Computer Science"),
            ("cybersecurity", "Cybersecurity"),
        ],
        "Business & Management": [
            ("marketing", "Marketing"),
            ("project management", "Project Management"),
            ("finance", "Finance"),
            ("accounting", "Accounting"),
            ("leadership", "Leadership"),
            ("entrepreneurship", "Entrepreneurship"),
            ("business", "Business"),
        ],
        "Data Analysis & Statistics": [
            ("data analysis", "Data Analysis"),
            ("statistics", "Statistics"),
            ("data visualization", "Data Visualization"),
            ("analytics", "Analytics"),
        ],
        "Education & Teacher Training": [
            ("teaching", "Teaching"),
            ("education", "Education"),
            ("pedagogy", "Pedagogy"),
        ],
        "Health & Safety": [
            ("health", "Health"),
            ("mental health", "Mental Health"),
            ("safety", "Safety"),
            ("first aid", "First Aid"),
            ("nutrition", "Nutrition"),
        ],
        "Communication": [
            ("communication", "Communication"),
            ("public speaking", "Public Speaking"),
            ("writing", "Writing"),
            ("journalism", "Journalism"),
        ],
        "Humanities": [
            ("philosophy", "Philosophy"),
            ("history", "History"),
            ("art", "Art"),
            ("music", "Music"),
            ("literature", "Literature"),
            ("justice", "Justice"),
            ("law", "Law"),
            ("ethics", "Ethics"),
        ],
        "Science": [
            ("biology", "Biology"),
            ("chemistry", "Chemistry"),
            ("physics", "Physics"),
            ("environmental science", "Environmental Science"),
            ("astronomy", "Astronomy"),
            ("psychology", "Psychology"),
        ],
    }

    # Get the appropriate keyword list for the category
    category_keywords = topic_keywords.get(category_name, [])

    # Check for keywords in the combined text
    for keyword, topic in category_keywords:
        if keyword in combined_text:
            return topic

    # If no specific topic is identified, use a default based on category
    return category_name if category_name else "General"


def identify_subtopics(combined_text, main_topic):
    """
    Identify subtopics within the content based on keyword analysis.
    """
    subtopics = []

    # Common subtopic patterns
    subtopic_patterns = {
        "Python": [
            "variables",
            "data types",
            "control flow",
            "functions",
            "object-oriented programming",
            "modules",
            "libraries",
            "debugging",
        ],
        "Programming": [
            "variables",
            "data types",
            "control structures",
            "functions",
            "error handling",
            "testing",
            "debugging",
        ],
        "Artificial Intelligence": [
            "machine learning",
            "neural networks",
            "deep learning",
            "natural language processing",
            "computer vision",
            "ethics",
        ],
        "Web Development": [
            "html",
            "css",
            "javascript",
            "responsive design",
            "backend development",
            "frontend frameworks",
        ],
        "Data Science": [
            "data collection",
            "data cleaning",
            "data analysis",
            "data visualization",
            "machine learning",
        ],
        "Marketing": [
            "market research",
            "consumer behavior",
            "digital marketing",
            "content strategy",
            "branding",
        ],
        "Finance": [
            "financial planning",
            "investment",
            "risk management",
            "financial analysis",
            "budgeting",
        ],
        "Leadership": [
            "team building",
            "communication",
            "decision making",
            "conflict resolution",
            "motivation",
        ],
        "Data Analysis": [
            "data collection",
            "statistical analysis",
            "data visualization",
            "data interpretation",
            "reporting",
        ],
        "Statistics": [
            "probability theory",
            "statistical inference",
            "hypothesis testing",
            "regression analysis",
            "bayesian statistics",
        ],
        "Teaching": [
            "lesson planning",
            "classroom management",
            "assessment techniques",
            "educational psychology",
            "inclusive teaching",
        ],
        "Health": [
            "nutrition",
            "exercise",
            "mental wellness",
            "disease prevention",
            "healthcare systems",
        ],
        "Communication": [
            "verbal communication",
            "nonverbal communication",
            "interpersonal skills",
            "public speaking",
            "digital communication",
        ],
        "Philosophy": [
            "metaphysics",
            "epistemology",
            "ethics",
            "logic",
            "political philosophy",
        ],
        "History": [
            "historical methods",
            "ancient history",
            "medieval history",
            "modern history",
            "cultural history",
        ],
        "Art": [
            "art history",
            "drawing techniques",
            "color theory",
            "art movements",
            "art appreciation",
        ],
        "Justice": [
            "legal systems",
            "criminal law",
            "civil law",
            "international law",
            "ethics in justice",
        ],
        "Biology": [
            "cell biology",
            "genetics",
            "evolution",
            "ecology",
            "human anatomy",
        ],
        "Chemistry": [
            "atomic structure",
            "chemical bonds",
            "chemical reactions",
            "organic chemistry",
            "biochemistry",
        ],
        "Physics": [
            "mechanics",
            "thermodynamics",
            "electromagnetism",
            "quantum physics",
            "relativity",
        ],
        "chinese": [
            "pinyin",
            "characters",
            "grammar",
            "listening",
            "speaking",
            "reading",
            "writing",
        ],
        "spanish": [
            "pronunciation",
            "grammar",
            "vocabulary",
            "reading",
            "writing",
            "listening",
            "speaking",
        ],
        "french": [
            "pronunciation",
            "grammar",
            "vocabulary",
            "reading",
            "writing",
            "listening",
            "speaking",
        ],
        "german": [
            "pronunciation",
            "grammar",
            "vocabulary",
            "reading",
            "writing",
            "listening",
            "speaking",
        ],
        "japanese": [
            "hiragana",
            "katakana",
            "kanji",
            "grammar",
            "vocabulary",
            "reading",
            "writing",
            "listening",
            "speaking",
        ],
        "arabic": [
            "alphabet",
            "pronunciation",
            "grammar",
            "vocabulary",
            "reading",
            "writing",
            "listening",
            "speaking",
        ],
    }

    # Get subtopic patterns for the main topic
    patterns = subtopic_patterns.get(main_topic, [])

    # Check for subtopics in the combined text
    for pattern in patterns:
        if pattern in combined_text:
            subtopics.append(pattern)

    return subtopics


def generate_titles_for_topic(main_topic, subtopics):
    """
    Generate 4-5 content titles based on the main topic and identified subtopics.
    """
    # Define templates for each topic
    topic_templates = {
        "Python": [
            "Introduction to Python",
            "Python Variables and Data Types",
            "Python Control Structures",
            "Python Functions",
            "Python Object-Oriented Programming",
        ],
        "Programming": [
            "Introduction to Programming",
            "Variables and Data Types",
            "Control Structures",
            "Functions and Methods",
            "Error Handling and Debugging",
        ],
        "Artificial Intelligence": [
            "Introduction to Artificial Intelligence",
            "Machine Learning Fundamentals",
            "Neural Networks and Deep Learning",
            "Natural Language Processing",
            "Computer Vision Applications",
        ],
        "Web Development": [
            "HTML and CSS Fundamentals",
            "JavaScript Essentials",
            "Responsive Web Design",
            "Frontend Frameworks",
            "Backend Development",
        ],
        "Data Science": [
            "Introduction to Data Science",
            "Data Collection and Cleaning",
            "Statistical Analysis",
            "Data Visualization",
            "Machine Learning Applications",
        ],
        "Marketing": [
            "Marketing Fundamentals",
            "Market Research and Analysis",
            "Consumer Behavior",
            "Digital Marketing Strategies",
            "Marketing Campaign Planning",
        ],
        "Finance": [
            "Introduction to Finance",
            "Financial Planning and Analysis",
            "Investment Strategies",
            "Risk Management",
            "Portfolio Management",
        ],
        "Leadership": [
            "Leadership Fundamentals",
            "Team Building and Management",
            "Effective Communication",
            "Decision Making and Problem Solving",
            "Strategic Leadership",
        ],
        "Data Analysis": [
            "Introduction to Data Analysis",
            "Data Collection Methods",
            "Statistical Analysis Techniques",
            "Data Visualization",
            "Data Interpretation and Reporting",
        ],
        "Statistics": [
            "Introduction to Statistics",
            "Probability Theory",
            "Statistical Inference",
            "Hypothesis Testing",
            "Regression Analysis",
        ],
        "Teaching": [
            "Introduction to Teaching",
            "Lesson Planning and Design",
            "Classroom Management Techniques",
            "Assessment and Evaluation",
            "Educational Technology",
        ],
        "Health": [
            "Introduction to Health and Wellness",
            "Nutrition and Diet",
            "Exercise and Physical Activity",
            "Mental Health and Stress Management",
            "Disease Prevention",
        ],
        "Communication": [
            "Communication Fundamentals",
            "Verbal and Nonverbal Communication",
            "Interpersonal Skills",
            "Public Speaking",
            "Digital Communication",
        ],
        "Philosophy": [
            "Introduction to Philosoph",
            "Ethics and Moral Philosoph",
            "Logic and Critical Thinking",
            "Metaphysics and Epistemology",
            "Philosophy of Mind",
        ],
        "History": [
            "Introduction to History",
            "Historical Methods and Research",
            "World History Overview",
            "Cultural History",
            "Historical Analysis and Interpretation",
        ],
        "Art": [
            "Introduction to Art",
            "Art History and Movements",
            "Drawing Techniques",
            "Color Theory",
            "Art Appreciation",
        ],
        "Justice": [
            "Introduction to Justice Systems",
            "Criminal Law",
            "Civil Law",
            "International Law",
            "Ethics in Justice",
        ],
        "Biology": [
            "Introduction to Biology",
            "Cell Biology",
            "Genetics and Evolution",
            "Ecology and Ecosystems",
            "Human Biology",
        ],
        "Chemistry": [
            "Introduction to Chemistry",
            "Atomic Structure and Periodic Table",
            "Chemical Bonds and Reactions",
            "Organic Chemistry",
            "Biochemistry",
        ],
        "Physics": [
            "Introduction to Physics",
            "Mechanics",
            "Thermodynamics",
            "Electromagnetism",
            "Quantum Physics",
        ],
        "chinese": [
            "Introduction to Mandarin Chinese",
            "Pinyin and Pronunciation",
            "Chinese Characters and Writing",
            "Basic Grammar and Sentence Structure",
            "Everyday Conversation Practice",
        ],
        "spanish": [
            "Introduction to Spanish",
            "Spanish Pronunciation",
            "Basic Spanish Grammar",
            "Vocabulary Building",
            "Conversation Practice",
        ],
        "french": [
            "Introduction to French",
            "French Pronunciation",
            "Basic French Grammar",
            "Vocabulary Building",
            "Conversation Practice",
        ],
        "german": [
            "Introduction to German",
            "German Pronunciation",
            "Basic German Grammar",
            "Vocabulary Building",
            "Conversation Practice",
        ],
        "japanese": [
            "Introduction to Japanese",
            "Hiragana and Katakana",
            "Basic Japanese Grammar",
            "Kanji and Vocabulary Building",
            "Conversation Practice",
        ],
        "arabic": [
            "Introduction to Arabic",
            "Arabic Alphabet and Pronunciation",
            "Basic Arabic Grammar",
            "Vocabulary Building",
            "Conversation Practice",
        ],
    }

    # Get the appropriate template for the main topic
    templates = topic_templates.get(
        main_topic,
        [
            "Introduction to Course",
            "Basic Concepts",
            "Intermediate Topics",
            "Advanced Topics",
            "Practical Applications",
        ],
    )

    # If we have identified subtopics, try to incorporate them into the templates
    if subtopics:
        # For each subtopic, create a more specific content title
        for i, subtopic in enumerate(subtopics[:4]):  # Limit to first 4 subtopics
            if i < len(templates):
                # Create a more specific title based on the subtopic
                templates[i] = f"{main_topic}: {subtopic.title()}"

    return templates[:5]  # Return 4-5 titles


def generate_fallback_content_titles(lesson_title, description, category_name):
    """
    Fallback method to generate content titles when API is not available.
    Uses rule-based approach similar to the original implementation.
    """
    # Convert to lowercase for case-insensitive matching
    lesson_title = lesson_title.lower()
    description = description.lower()

    # Combine lesson title and description for comprehensive analysis
    combined_text = f"{lesson_title} {description}"

    # Extract main topic using keyword analysis
    main_topic = identify_main_topic(combined_text, category_name)

    # Extract subtopics from the content
    subtopics = identify_subtopics(combined_text, main_topic)

    # Generate content titles based on the identified topic and subtopics
    content_titles = generate_titles_for_topic(main_topic, subtopics)

    return content_titles


def generate_mock_data():
    """
    Generate mock data from EdX CSV file according to the specifications in plan.md

    The function:
    1. Reads the EdX.csv file using pandas
    2. Maps columns from the original CSV to the output CSV
    3. Generates additional mock data for missing columns
    4. Saves the result to COURSE_CATALOG.csv
    """

    # Step 1: Read the CSV file using pandas library
    df = pd.read_csv("./EdX.csv")

    # Prepare the output dataframe with the required columns
    output_columns = [
        "id",
        "lessontitle",
        "contentTitle",
        "skillName",
        "level",
        "categoryId",
        "catName",
        "subCatName",
        "coverImageId",
        "previewVideoId",
        "createdAt",
        "updatedAt",
        "deletedAt",
        "status",
        "shortDescription",
        "description",
        "university",
        "link",
    ]

    # Initialize the output dataframe
    output_df = pd.DataFrame(columns=output_columns)

    # Define timezone for Thailand/Bangkok
    thailand_tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(thailand_tz)

    # Mock categories and skills
    categories = [
        {
            "id": "cat001",
            "name": "Computer Science",
            "skills": [
                "Programming",
                "Algorithms",
                "Data Structures",
                "Software Engineering",
                "Computer Science",
                "Python",
                "JavaScript",
                "Web Development",
            ],
        },
        {
            "id": "cat002",
            "name": "Business & Management",
            "skills": [
                "Leadership",
                "Project Management",
                "Marketing",
                "Finance",
                "Management",
                "Business",
                "Strategy",
                "Organizational Behavior",
            ],
        },
        {
            "id": "cat003",
            "name": "Data Analysis & Statistics",
            "skills": [
                "Data Analysis",
                "Statistics",
                "Machine Learning",
                "Data Visualization",
                "Analytics",
                "Data Science",
                "R",
                "Big Data",
            ],
        },
        {
            "id": "cat004",
            "name": "Education & Teacher Training",
            "skills": [
                "Teaching",
                "Curriculum Design",
                "Educational Technology",
                "Assessment",
                "Education",
                "Learning",
                "Training",
                "Instructional Design",
            ],
        },
        {
            "id": "cat005",
            "name": "Health & Safety",
            "skills": [
                "Public Health",
                "Mental Health",
                "Safety",
                "Wellness",
                "Health",
                "Psychology",
                "Medicine",
                "Healthcare",
            ],
        },
        {
            "id": "cat006",
            "name": "Communication",
            "skills": [
                "Public Speaking",
                "Writing",
                "Interpersonal Communication",
                "Digital Communication",
                "Communication",
                "Presentation",
                "Negotiation",
                "Media",
            ],
        },
        {
            "id": "cat007",
            "name": "Humanities",
            "skills": [
                "History",
                "Philosophy",
                "Literature",
                "Art",
                "Culture",
                "Society",
                "Ethics",
                "Critical Thinking",
            ],
        },
        {
            "id": "cat008",
            "name": "Science",
            "skills": [
                "Biology",
                "Chemistry",
                "Physics",
                "Environmental Science",
                "Research",
                "Mathematics",
                "Engineering",
                "Scientific Method",
            ],
        },
    ]

    # Sub-categories with keywords for matching, organized by category
    sub_categories = {
        "Computer Science": [
            {
                "name": "Programming Fundamentals",
                "keywords": [
                    "programming",
                    "coding",
                    "variables",
                    "loops",
                    "functions",
                    "basics",
                ],
            },
            {
                "name": "Algorithms & Data Structures",
                "keywords": [
                    "algorithm",
                    "data structure",
                    "efficiency",
                    "optimization",
                    "sorting",
                ],
            },
            {
                "name": "Web Development",
                "keywords": ["web", "html", "css", "javascript", "frontend", "backend"],
            },
            {
                "name": "Software Engineering",
                "keywords": [
                    "software engineering",
                    "development lifecycle",
                    "testing",
                    "debugging",
                    "version control",
                ],
            },
            {
                "name": "Computer Architecture",
                "keywords": [
                    "computer architecture",
                    "hardware",
                    "systems",
                    "low-level",
                    "assembly",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Business & Management": [
            {
                "name": "Leadership",
                "keywords": [
                    "leadership",
                    "leading",
                    "managing teams",
                    "influence",
                    "motivation",
                ],
            },
            {
                "name": "Project Management",
                "keywords": [
                    "project management",
                    "planning",
                    "execution",
                    "milestones",
                    "timeline",
                ],
            },
            {
                "name": "Marketing",
                "keywords": [
                    "marketing",
                    "promotion",
                    "branding",
                    "customer acquisition",
                    "market research",
                ],
            },
            {
                "name": "Finance",
                "keywords": [
                    "finance",
                    "financial",
                    "budgeting",
                    "investment",
                    "accounting",
                ],
            },
            {
                "name": "Strategy",
                "keywords": [
                    "strategy",
                    "strategic planning",
                    "competitive advantage",
                    "business model",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Data Analysis & Statistics": [
            {
                "name": "Statistical Analysis",
                "keywords": [
                    "statistics",
                    "statistical",
                    "probability",
                    "distribution",
                    "hypothesis testing",
                ],
            },
            {
                "name": "Machine Learning",
                "keywords": [
                    "machine learning",
                    "ml",
                    "prediction",
                    "classification",
                    "regression",
                    "clustering",
                ],
            },
            {
                "name": "Data Visualization",
                "keywords": [
                    "visualization",
                    "charts",
                    "graphs",
                    "dashboard",
                    "presentation",
                ],
            },
            {
                "name": "Data Processing",
                "keywords": [
                    "data processing",
                    "cleaning",
                    "transformation",
                    "wrangling",
                    "preprocessing",
                ],
            },
            {
                "name": "Big Data",
                "keywords": [
                    "big data",
                    "large scale",
                    "distributed computing",
                    "hadoop",
                    "spark",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Education & Teacher Training": [
            {
                "name": "Teaching Methods",
                "keywords": [
                    "teaching",
                    "instruction",
                    "pedagogy",
                    "lesson planning",
                    "classroom",
                ],
            },
            {
                "name": "Educational Technology",
                "keywords": [
                    "educational technology",
                    "edtech",
                    "digital learning",
                    "online education",
                ],
            },
            {
                "name": "Assessment",
                "keywords": [
                    "assessment",
                    "evaluation",
                    "testing",
                    "feedback",
                    "grading",
                ],
            },
            {
                "name": "Curriculum Design",
                "keywords": [
                    "curriculum",
                    "syllabus",
                    "course design",
                    "learning objectives",
                ],
            },
            {
                "name": "Learning Theory",
                "keywords": [
                    "learning theory",
                    "educational psychology",
                    "cognition",
                    "knowledge acquisition",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Health & Safety": [
            {
                "name": "Public Health",
                "keywords": [
                    "public health",
                    "population health",
                    "epidemiology",
                    "health policy",
                ],
            },
            {
                "name": "Mental Health",
                "keywords": [
                    "mental health",
                    "psychology",
                    "wellbeing",
                    "stress",
                    "mindfulness",
                ],
            },
            {
                "name": "Safety",
                "keywords": [
                    "safety",
                    "risk assessment",
                    "hazard prevention",
                    "workplace safety",
                ],
            },
            {
                "name": "Healthcare",
                "keywords": [
                    "healthcare",
                    "medicine",
                    "clinical",
                    "patient care",
                    "health systems",
                ],
            },
            {
                "name": "Wellness",
                "keywords": [
                    "wellness",
                    "health promotion",
                    "lifestyle",
                    "prevention",
                    "self-care",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Communication": [
            {
                "name": "Public Speaking",
                "keywords": [
                    "public speaking",
                    "presentation",
                    "speaking",
                    "audience",
                    "delivery",
                ],
            },
            {
                "name": "Writing",
                "keywords": [
                    "writing",
                    "composition",
                    "grammar",
                    "style",
                    "content creation",
                ],
            },
            {
                "name": "Interpersonal Communication",
                "keywords": [
                    "interpersonal",
                    "conversation",
                    "listening",
                    "empathy",
                    "relationships",
                ],
            },
            {
                "name": "Digital Communication",
                "keywords": [
                    "digital communication",
                    "social media",
                    "online",
                    "virtual",
                    "remote",
                ],
            },
            {
                "name": "Media Studies",
                "keywords": [
                    "media",
                    "journalism",
                    "content creation",
                    "broadcasting",
                    "publishing",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Humanities": [
            {
                "name": "History",
                "keywords": [
                    "history",
                    "historical",
                    "past",
                    "civilization",
                    "chronology",
                ],
            },
            {
                "name": "Philosophy",
                "keywords": [
                    "philosophy",
                    "philosophical",
                    "ethics",
                    "logic",
                    "metaphysics",
                ],
            },
            {
                "name": "Literature",
                "keywords": ["literature", "literary", "fiction", "poetry", "drama"],
            },
            {
                "name": "Art",
                "keywords": [
                    "art",
                    "artistic",
                    "aesthetics",
                    "creative expression",
                    "visual arts",
                ],
            },
            {
                "name": "Cultural Studies",
                "keywords": [
                    "culture",
                    "cultural",
                    "society",
                    "anthropology",
                    "social studies",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
        "Science": [
            {
                "name": "Biology",
                "keywords": [
                    "biology",
                    "biological",
                    "organism",
                    "ecosystem",
                    "genetics",
                ],
            },
            {
                "name": "Chemistry",
                "keywords": [
                    "chemistry",
                    "chemical",
                    "molecular",
                    "reaction",
                    "compounds",
                ],
            },
            {
                "name": "Physics",
                "keywords": ["physics", "physical", "energy", "motion", "forces"],
            },
            {
                "name": "Environmental Science",
                "keywords": [
                    "environmental",
                    "climate",
                    "sustainability",
                    "ecology",
                    "conservation",
                ],
            },
            {
                "name": "Scientific Method",
                "keywords": [
                    "scientific method",
                    "research",
                    "experimentation",
                    "hypothesis",
                    "analysis",
                ],
            },
            {
                "name": "Introduction",
                "keywords": [
                    "intro",
                    "introduction",
                    "beginner",
                    "basic",
                    "getting started",
                ],
            },
        ],
    }

    # Function to detect category from description
    def detect_category(description, about):
        """
        Detect the most relevant category based on keywords in description and about fields
        Returns the category object
        """
        text = (str(description) + " " + str(about)).lower()

        # Count matches for each category
        category_scores = []
        for category in categories:
            score = 0
            for skill in category["skills"]:
                # Check for exact skill name
                if skill.lower() in text:
                    score += 3
                # Check for partial matches
                skill_words = skill.lower().split()
                for word in skill_words:
                    if word in text and len(word) > 3:  # Skip short words
                        score += 1
            category_scores.append((category, score))

        # Sort by score (descending) and return the highest scoring category
        category_scores.sort(key=lambda x: x[1], reverse=True)

        # If no category has a score, return a default
        if category_scores[0][1] == 0:
            return categories[0]  # Default to Computer Science

        return category_scores[0][0]

    # Function to detect subcategory from description
    def detect_subcategories(description, about, category_name):
        """
        Detect relevant subcategories based on keywords in description and about fields
        within the context of the detected category
        Returns a list of subcategory names
        """
        text = (str(description) + " " + str(about)).lower()
        detected_subcategories = []
        category_subcategories = sub_categories.get(
            category_name, sub_categories["Computer Science"]
        )

        # Score each subcategory based on keyword matches
        subcategory_scores = []
        for subcat in category_subcategories:
            score = 0
            for keyword in subcat["keywords"]:
                if keyword in text:
                    score += 1
            subcategory_scores.append((subcat["name"], score))

        # Sort by score (descending)
        subcategory_scores.sort(key=lambda x: x[1], reverse=True)

        # Add all subcategories with non-zero score to the list
        for name, score in subcategory_scores:
            if score > 0:
                detected_subcategories.append(name)

        # If no subcategories detected, include "Introduction" as default
        if not detected_subcategories:
            detected_subcategories.append("Introduction")

        # Ensure we return at least one subcategory
        if not detected_subcategories:
            detected_subcategories.append("Introduction")

        return detected_subcategories

    # Step 2: Generate mock data
    for index, row in df.iterrows():
        # Generate a new ULID for the id
        ulid = str(ULID())

        # Map columns from original CSV to output
        lessontitle = row["Name"]
        level = row["Difficulty Level"]
        short_description = row["About"] if pd.notna(row["About"]) else ""
        description = (
            row["Course Description"] if pd.notna(row["Course Description"]) else ""
        )
        university = row["University"] if pd.notna(row["University"]) else ""
        link = row["Link"] if pd.notna(row["Link"]) else ""

        # Detect the most relevant category from description and about
        category = detect_category(description, short_description)

        # Detect relevant subcategories from description and about within the context of the category
        detected_subcategories = detect_subcategories(
            description, short_description, category["name"]
        )
        sub_category_list = detected_subcategories  # Store as a list of strings
        sub_category = ", ".join(
            detected_subcategories
        )  # Join for single string display

        # Extract skill/subject from description based on the detected category
        skill_name = ""
        if pd.notna(description):
            # Try to find a skill from the description within the detected category
            desc_text = str(description).lower()
            for skill in category["skills"]:
                if skill.lower() in desc_text:
                    skill_name = skill
                    break

        # Default skill if none found
        if not skill_name:
            skill_name = category["skills"][0]  # Use the first skill from the category

        # Generate mock IDs
        cover_image_id = f"img_{ulid[:8]}"
        preview_video_id = f"vid_{ulid[:8]}"

        # Generate timestamps with Thailand timezone
        days_ago = random.randint(1, 365)
        created_at = (current_time - timedelta(days=days_ago)).replace(tzinfo=None)
        updated_at = (created_at + timedelta(days=random.randint(0, 30))).replace(
            tzinfo=None
        )
        deleted_at = None  # Default to None (not deleted)

        # Generate a status
        status = random.choice(["active", "draft", "archived"])

        # Generate meaningful content titles based on lesson title, description, and category
        content_title = generate_content_titles(
            lessontitle, description, category["name"]
        )

        # Add the row to the output dataframe
        output_df.loc[index] = [
            ulid,  # id
            lessontitle,  # lessontitle
            content_title,  # contentTitle
            skill_name,  # skillName
            level,  # level
            category["id"],  # categoryId
            category["name"],  # catName
            sub_category_list,  # subCatName (as list of strings)
            cover_image_id,  # coverImageId
            preview_video_id,  # previewVideoId
            created_at,  # createdAt
            updated_at,  # updatedAt
            deleted_at,  # deletedAt
            status,  # status
            short_description,  # shortDescription
            description,  # description
            university,  # university (additional column)
            link,  # link (additional column)
        ]

    # Format timestamps to ISO format
    output_df["createdAt"] = output_df["createdAt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    output_df["updatedAt"] = output_df["updatedAt"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Step 3: Save the mock data to a new csv file
    output_df.to_csv("./COURSE_CATALOG.csv", index=False)
    print("Mock data saved to COURSE_CATALOG.csv")


if __name__ == "__main__":
    generate_mock_data()
