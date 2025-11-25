# Course Catalog Mock Data Generator

Act as data engineer and data scientist to gen mock data from csv file ./Edx.csv in this repo

language:python 3.12 and other compatible libraries
  use venv to create a virtual environment and activate it
  install required packages build requirements.txt and install requirements.txt

## Implementation Details

The implementation successfully generates context-aware mock data with:
- Smart categorization based on course content analysis
- Meaningful content titles derived from lesson titles and descriptions
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
      1. Analyzes the lessontitle + description field for specific topic keywords
      2. Matches keywords against predefined content templates for each category
      3. Prioritizes specific terms (e.g., "artificial intelligence") over general terms (e.g., "python")
      4. Returns a list of 4-5 relevant topic titles that logically belong in the course
      5. Special handling for language courses with dedicated templates for Chinese, Spanish, French, German, Japanese, and Arabic
        
step 2: Generate mock data
  id field use ULID
  note: row of data no need to increase just increase the number of columns that missing eg. id, createdAt, updatedAt, deletedAt, status, shortDescription, description, previewVideoId, coverImageId
  
  ## Implementation Details
  - Virtual environment created with Python 3.12
  - Dependencies installed: pandas, python-ulid, pytz, typing_extensions
  - Smart categorization algorithm implemented to detect categories and subcategories
  - Content title generation system created with templates for 8 major categories plus language courses
  - All timestamps generated using Thailand/Bangkok timezone
  - Special keyword prioritization for accurate content matching
  
      
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
