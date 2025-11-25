import random
from datetime import datetime, timedelta
import pandas as pd
import pytz
from ulid import ULID


def generate_content_titles(lesson_title, description, category_name):
    """
    Generate meaningful content titles based on the lesson title, description, and category.
    Returns a list of 4-5 content titles that would logically be part of this course.
    """
    lesson_title = lesson_title.lower()
    description = description.lower()

    # Define content templates based on keywords
    content_templates = {
        "Computer Science": {
            "python": [
                "Introduction to Python",
                "Variables and Operators",
                "Data Types",
                "Control Structures",
                "Functions",
            ],
            "programming": [
                "Introduction to Programming",
                "Variables and Operators",
                "Data Types",
                "Control Structures",
                "Functions",
            ],
            "artificial intelligence": [
                "Introduction to AI",
                "Machine Learning",
                "Deep Learning",
                "Natural Language Processing",
                "Computer Vision",
            ],
            "computer science": [
                "Introduction to Computer Science",
                "Data Types",
                "Control Structures",
                "Functions",
                "Problem Solving",
            ],
            "web development": [
                "HTML Fundamentals",
                "CSS Styling",
                "JavaScript Basics",
                "DOM Manipulation",
                "Web Development Frameworks",
            ],
            "data structures": [
                "Introduction to Data Structures",
                "Arrays and Lists",
                "Stacks and Queues",
                "Trees and Graphs",
                "Hash Tables and Dictionaries",
            ],
            "algorithms": [
                "Algorithm Basics",
                "Sorting Algorithms",
                "Search Algorithms",
                "Graph Algorithms",
                "Algorithm Complexity",
            ],
            "default": [
                "Introduction to Programming",
                "Basic Concepts",
                "Data Handling",
                "Problem Solving",
                "Project Implementation",
            ],
        },
        "Business & Management": {
            "marketing": [
                "Marketing Fundamentals",
                "Market Research",
                "Consumer Behavior",
                "Digital Marketing",
                "Marketing Strategy",
            ],
            "project management": [
                "Project Planning",
                "Resource Management",
                "Risk Assessment",
                "Quality Control",
                "Project Execution",
            ],
            "finance": [
                "Financial Basics",
                "Investment Principles",
                "Risk Management",
                "Financial Markets",
                "Portfolio Management",
            ],
            "leadership": [
                "Leadership Fundamentals",
                "Team Building",
                "Communication Skills",
                "Decision Making",
                "Strategic Leadership",
            ],
            "default": [
                "Business Fundamentals",
                "Organizational Structure",
                "Business Strategy",
                "Market Analysis",
                "Business Operations",
            ],
        },
        "Data Analysis & Statistics": {
            "data analysis": [
                "Introduction to Data Analysis",
                "Data Collection",
                "Data Cleaning",
                "Statistical Analysis",
                "Data Visualization",
            ],
            "statistics": [
                "Introduction to Statistics",
                "Probability Theory",
                "Statistical Inference",
                "Hypothesis Testing",
                "Regression Analysis",
            ],
            "machine learning": [
                "Introduction to Machine Learning",
                "Supervised Learning",
                "Unsupervised Learning",
                "Model Evaluation",
                "Deep Learning Basics",
            ],
            "data science": [
                "Data Science Fundamentals",
                "Data Mining",
                "Statistical Modeling",
                "Data Visualization",
                "Big Data Technologies",
            ],
            "default": [
                "Introduction to Data",
                "Data Exploration",
                "Data Processing",
                "Data Analysis",
                "Data Presentation",
            ],
        },
        "Education & Teacher Training": {
            "teaching": [
                "Teaching Fundamentals",
                "Learning Styles",
                "Teaching Methods",
                "Classroom Management",
                "Educational Assessment",
            ],
            "education": [
                "Introduction to Education",
                "Educational Psychology",
                "Curriculum Design",
                "Teaching Methods",
                "Educational Technology",
            ],
            "default": [
                "Education Fundamentals",
                "Learning Theories",
                "Teaching Strategies",
                "Assessment Methods",
                "Educational Technology",
            ],
        },
        "Health & Safety": {
            "health": [
                "Introduction to Health",
                "Health Promotion",
                "Disease Prevention",
                "Healthcare Systems",
                "Public Health",
            ],
            "mental health": [
                "Introduction to Mental Health",
                "Psychological Well-being",
                "Stress Management",
                "Mental Disorders",
                "Therapeutic Approaches",
            ],
            "safety": [
                "Safety Fundamentals",
                "Risk Assessment",
                "Safety Protocols",
                "Emergency Response",
                "Safety Management",
            ],
            "default": [
                "Introduction to Health",
                "Wellness Basics",
                "Health Promotion",
                "Disease Prevention",
                "Healthcare Systems",
            ],
        },
        "Communication": {
            "communication": [
                "Communication Basics",
                "Interpersonal Skills",
                "Group Communication",
                "Public Speaking",
                "Digital Communication",
            ],
            "writing": [
                "Writing Fundamentals",
                "Writing Process",
                "Writing Styles",
                "Editing and Proofreading",
                "Publishing",
            ],
            "default": [
                "Communication Fundamentals",
                "Interpersonal Communication",
                "Group Dynamics",
                "Public Speaking",
                "Digital Communication",
            ],
        },
        "Humanities": {
            "philosophy": [
                "Introduction to Philosophy",
                "Ethics",
                "Logic",
                "Metaphysics",
                "Philosophy of Mind",
            ],
            "justice": [
                "Introduction to Justice",
                "Legal System",
                "Criminal Law",
                "Civil Law",
                "Ethics and Justice",
            ],
            "history": [
                "Introduction to History",
                "Historical Methods",
                "World History",
                "Cultural History",
                "Historical Analysis",
            ],
            "art": [
                "Introduction to Art",
                "Art History",
                "Art Movements",
                "Art Appreciation",
                "Art Creation",
            ],
            "default": [
                "Introduction to Humanities",
                "Cultural Studies",
                "Historical Context",
                "Art and Expression",
                "Critical Thinking",
            ],
        },
        "Science": {
            "biology": [
                "Introduction to Biology",
                "Cell Biology",
                "Genetics",
                "Evolution",
                "Ecology",
            ],
            "chemistry": [
                "Introduction to Chemistry",
                "Atomic Structure",
                "Chemical Bonds",
                "Chemical Reactions",
                "Organic Chemistry",
            ],
            "physics": [
                "Introduction to Physics",
                "Mechanics",
                "Thermodynamics",
                "Electromagnetism",
                "Quantum Physics",
            ],
            "environmental": [
                "Environmental Science",
                "Ecosystems",
                "Climate Change",
                "Conservation",
                "Sustainability",
            ],
            "default": [
                "Introduction to Science",
                "Scientific Method",
                "Basic Principles",
                "Scientific Applications",
                "Science in Society",
            ],
        },
        "Languages": {
            "chinese": [
                "Introduction to Mandarin Chinese",
                "Pinyin and Characters",
                "Grammar and Sentence Structure",
                "Reading and Writing",
                "Listening and Speaking",
            ],
            "mandarin": [
                "Introduction to Mandarin Chinese",
                "Pinyin and Characters",
                "Grammar and Sentence Structure",
                "Reading and Writing",
                "Listening and Speaking",
            ],
            "spanish": [
                "Introduction to Spanish",
                "Spanish Pronunciation",
                "Grammar and Vocabulary",
                "Reading Comprehension",
                "Conversation Skills",
            ],
            "french": [
                "Introduction to French",
                "French Pronunciation",
                "Grammar and Vocabulary",
                "Reading Comprehension",
                "Conversation Skills",
            ],
            "german": [
                "Introduction to German",
                "German Pronunciation",
                "Grammar and Vocabulary",
                "Reading Comprehension",
                "Conversation Skills",
            ],
            "japanese": [
                "Introduction to Japanese",
                "Hiragana and Katakana",
                "Grammar and Vocabulary",
                "Reading and Writing",
                "Conversation Skills",
            ],
            "arabic": [
                "Introduction to Arabic",
                "Arabic Alphabet",
                "Grammar and Vocabulary",
                "Reading and Writing",
                "Conversation Skills",
            ],
            "default": [
                "Introduction to Language",
                "Basic Pronunciation",
                "Grammar Fundamentals",
                "Reading and Writing",
                "Listening and Speaking",
            ],
        },
    }

    # Combine lesson title and description for keyword analysis
    # Create a combined text for more comprehensive keyword matching
    combined_text = lesson_title + " " + description

    # Get the appropriate content templates for the category
    category_templates = content_templates.get(
        category_name, content_templates["Computer Science"]
    )

    # Special handling for language courses which might be in different categories
    if (
        "chinese" in lesson_title.lower()
        or "mandarin" in lesson_title.lower()
        or "spanish" in lesson_title.lower()
        or "french" in lesson_title.lower()
        or "german" in lesson_title.lower()
        or "japanese" in lesson_title.lower()
        or "arabic" in lesson_title.lower()
        or "language" in lesson_title.lower()
    ):
        category_templates = content_templates["Languages"]

    # If category is "Communication" and we detect language keywords, use Languages category instead
    if category_name == "Communication" and any(
        lang in combined_text
        for lang in [
            "mandarin",
            "chinese",
            "spanish",
            "french",
            "german",
            "japanese",
            "arabic",
            "english",
            "language",
        ]
    ):
        category_templates = content_templates["Languages"]

    # Check if any keyword matches in the combined text, prioritizing more specific terms
    # Create a priority list of keywords to check first
    priority_keywords = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "justice",
        "philosophy",
        "history",
        "art",
        "writing",
        "chinese",
        "mandarin",
        "spanish",
        "french",
        "german",
        "japanese",
        "arabic",
    ]

    # Check priority keywords first
    for keyword in priority_keywords:
        if keyword in category_templates and keyword in combined_text:
            return category_templates[keyword]

    # Then check the remaining keywords
    for keyword, templates in category_templates.items():
        if (
            keyword != "default"
            and keyword in combined_text
            and keyword not in priority_keywords
        ):
            return templates

    # If no specific match, return the default templates
    return category_templates["default"]


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
