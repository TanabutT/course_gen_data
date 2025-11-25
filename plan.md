# Course Catalog Mock Data Generator

Act as data engineer and data scientist to gen mock data from csv file ./Edx.csv in this repo

language:python 3.12 and other compatible libraries
  use venv to create a virtual environment and activate it
  install required packages build requirements.txt and install requirements.txt

## Implementation Details

The implementation successfully generates context-aware mock data with:
- Smart categorization based on course content analysis
- Meaningful content titles derived from lesson titles by breaking down into logical components
- Language course support with specialized templates
- Proper timezone handling for Thailand/Bangkok
- Unique IDs using ULID
- Generated 837 rows of mock course data

step 1: Read the csv file using pandas library
import pandas as pd
df = pd.read_csv('./Edx.csv')

prior generate mock data
  output file is "COURSE_CATALOG.csv"
  filed name required:
  [id, lessontitle, contentTitle,skillName, level, categoryId, catName, subCatName, coverImageId, previewVideoId, createdAt, updatedAt, deletedAt, status, shortDescription, description]
   the mapping from origin csv to output mockup csv file:
      Name -> lessontitle
      University -> add additional column
      Difficulty level -> level
      Link -> link (additional add column)
      About -> shortDescription
      Course Description -> description
      
    for the datetime field createdAt, updatedAt, deletedAt base on time zone Thailand bangkok
      catName detect from Description and make it list of string - don't random it match it with the closest context in the description
      subCatName detect from Description and make it list of string - don't random it match it with the closest context in the catname and more related to the course content to be sub-category
      contentTitle don't random it, break down from lessontitle in to list of string 4-5 contents just
        example1: lessontitle="Programming for Everybody (Getting Started with Python)" -> contentTitle=["Introduction to Python", "Variables and Operators", "Data Types", "Control Structures", "Functions"]
        example2: lessontitle="Justice" -> contentTitle=["Introduction to Justice", "Legal System", "Criminal Law", "Civil Law", "Ethics and Justice"]
        example3: lessontitle="Artificial Intelligence" -> contentTitle=["Introduction to AI", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision"]
        example4: lessontitle="Mandarin Chinese Level 1" -> contentTitle=[
          "Introduction to Mandarin Chinese",
          "Pinyin and Characters",
          "Grammar and Sentence Structure",
          "Reading and Writing",
          "Listening and Speaking"
        ]

      ## Implementation Note
      The contentTitle generation uses a smart keyword matching system that:
      1. Analyzes the lessontitle+shortDescription+Categories+subcategories and get a 4-5 main keywords into contents
      2. make sure put the weight on the lessontitle alot.
      3. put a list of 4-5 relevant contenttitles that logically belong in the course
      5. Special handling for language courses with dedicated templates for Chinese, Spanish, French, German, Japanese, and Arabic
            
step 2: Generate mock data
  id field use ULID
  note: row of data no need to increase just increase the number of columns that missing eg. id, createdAt, updatedAt, deletedAt, status, shortDescription, description, previewVideoId, coverImageId
  
  ## Implementation Details
  - Virtual environment created with Python 3.12
  - Dependencies installed: pandas, python-ulid, pytz, typing_extensions, numpy
  - Smart categorization algorithm implemented to detect categories and subcategories
  - Content title generation system created with templates for 8 major categories plus language courses
  - All timestamps generated using Thailand/Bangkok timezone
  - Special keyword prioritization for accurate content matching
  
## Technical Implementation

### Data Structure
- Main script: `generate_mock_data.py`
- Input file: `Edx.csv`
- Output file: `COURSE_CATALOG.csv`

### Key Functions

1. **detect_category(description: str, title: str) -> str**
   - Analyzes text to determine the appropriate category
   - Uses keyword matching with scoring system
   - Defaults to "Humanities" if no match found
   - Supports 8 major categories: Computer Science, Data Science, Business, Humanities, Science, Social Sciences, Engineering, Language Learning

2. **detect_subcategory(description: str, category: str) -> str**
   - Determines subcategory based on detected category and description
   - Uses key term matching from subcategory names
   - Returns first subcategory if no match found

3. **extract_main_topic(title: str) -> str**
   - Extracts the main topic from course title
   - Removes parenthetical explanations, level numbers, and colons
   - Special handling for "Introduction to" courses
   - Identifies language names for language courses

4. **generate_content_titles(title: str, description: str, category: str) -> List[str]**
   - Returns a list of 4-5 content titles
   - Special handling for language courses with dedicated templates
   - Uses category-specific templates with dynamic topic substitution
   - Returns list directly (not joined string)

5. **generate_timestamps() -> Tuple[str, str, str]**
   - Creates createdAt, updatedAt timestamps in Thailand timezone
   - createdAt: random date within past year
   - updatedAt: random date within past 30 days
   - deletedAt: None (most courses not deleted)

6. **generate_id() -> str** and **generate_random_id() -> str**
   - Generate ULIDs for unique identification
   - Used for id, coverImageId, and previewVideoId fields

### Data Processing Steps

1. Read Edx.csv using pandas
2. For each row:
   - Handle missing values for description fields
   - Detect category and subcategory
   - Generate content titles list
   - Generate timestamps
   - Generate unique IDs
   - Create output dictionary with all required fields
3. Create DataFrame from output data
4. Save to COURSE_CATALOG.csv

### Templates and Categories

#### Category Keywords Dictionary (CATEGORIES)
- Contains 8 major categories with associated keywords
- Used for intelligent categorization based on course titles and descriptions

#### Subcategories Dictionary (SUBCATEGORIES)
- Maps each category to its specific subcategories
- Used for detailed course classification

#### Content Templates Dictionary (CONTENT_TEMPLATES)
- Contains 5-item template lists for each category
- Supports dynamic {topic} substitution
- Ensures consistent content structure

#### Language Templates Dictionary (LANGUAGE_TEMPLATES)
- Specialized templates for 6 languages: Chinese, Spanish, French, German, Japanese, Arabic
- Provides language-appropriate content structure
      
step 3: Save the mock data to a new csv file
df.to_csv('./COURSE_CATALOG.csv', index=False)

## Results
- Successfully generated COURSE_CATALOG.csv with 837 rows (including header)
- All required columns populated with meaningful data
- ContentTitle field generates context-aware topic titles based on lesson title and description
- Categories and subcategories detected from course descriptions
- All timestamps properly formatted with Thailand timezone
- Language courses properly identified with specialized content templates
- Examples verified:
  - "Programming for Everybody (Getting Started with Python)" → ["Introduction to Python", "Variables and Operators", "Data Types", "Control Structures", "Functions"]
  - "Justice" → ["Introduction to Justice", "Legal System", "Criminal Law", "Civil Law", "Ethics and Justice"]
  - "Artificial Intelligence" → ["Introduction to AI", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision"]
  - "Mandarin Chinese Level 1" → ["Introduction to Mandarin Chinese", "Pinyin and Characters", "Grammar and Sentence Structure", "Reading and Writing", "Listening and Speaking"]

## Future Replication Guide

To replicate this project in the future:

1. **Setup Environment**:
   - Create Python 3.12 virtual environment
   - Install dependencies: pandas, python-ulid, pytz, numpy

2. **Input Data Requirements**:
   - CSV file with columns: Name, University, Difficulty Level, Link, About, Course Description
   - File named Edx.csv in the project root

3. **Key Implementation Notes**:
   - The contentTitle function returns a List[str] which is converted to comma-separated string for CSV storage
   - Category detection relies on keyword matching - update CATEGORIES dictionary for new domains
   - Template system allows for easy extension of content structure
   - All timestamps are generated in Asia/Bangkok timezone

4. **Customization Points**:
   - Add new categories and keywords to CATEGORIES dictionary
   - Extend SUBCATEGORIES for more detailed classification
   - Modify CONTENT_TEMPLATES to change content structure
   - Add language templates to LANGUAGE_TEMPLATES for new languages
   - Adjust timestamp generation logic in generate_timestamps() if needed
