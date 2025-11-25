# Course Catalog Mock Data Generator

This project generates mock data for a course catalog system from EdX course data. The script transforms the original CSV data into a format suitable for a course catalog system with additional fields and enhanced categorization.

## Features

- Reads course data from `EdX.csv`
- Maps original fields to new schema fields
- Generates additional mock fields:
  - Unique IDs using ULID
  - Timestamps in Thailand timezone
  - Categories and subcategories based on course content analysis
  - Status and other metadata
- Outputs to `COURSE_CATALOG.csv`

## Prerequisites

- Python 3.12+
- Virtual environment (venv)

## Setup

1. Clone or download this repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the mock data generator:

```bash
source venv/bin/activate  # If not already activated
python generate_mock_data.py
```

The output will be saved to `COURSE_CATALOG.csv`.

## Data Mapping

The script maps fields from the original EdX.csv to the output schema:

| Original Field | Output Field | Notes |
|---------------|--------------|-------|
| Name | lessontitle | Course title |
| University | university | Additional column |
| Difficulty Level | level | Course difficulty |
| Link | link | Additional column |
| About | shortDescription | Course summary |
| Course Description | description | Full description |

### Generated Fields

| Field | Description |
|-------|-------------|
| id | Unique identifier using ULID |
| contentTitle | List of 4-5 context-aware topic titles based on the lesson title |
| skillName | Primary skill/topic of the course |
| categoryId | Category identifier |
| catName | Category name (detected from content) |
| subCatName | List of relevant subcategories (detected from content) |
| coverImageId | Generated image identifier |
| previewVideoId | Generated video identifier |
| createdAt | Creation timestamp (Thailand timezone) |
| updatedAt | Last update timestamp (Thailand timezone) |
| deletedAt | Deletion timestamp (null for active courses) |
| status | Course status (active, draft, or archived) |

## ContentTitle Examples

The contentTitle field generates context-aware topic titles based on both the lesson title and description. Here are some examples:

- **"Programming for Everybody (Getting Started with Python)"** → `["Introduction to Python", "Variables and Operators", "Data Types", "Control Structures", "Functions"]`
- **"Justice"** → `["Introduction to Justice", "Legal System", "Criminal Law", "Civil Law", "Ethics and Justice"]`
- **"Artificial Intelligence"** → `["Introduction to AI", "Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision"]`
- **"Mandarin Chinese Level 1"** → `["Introduction to Mandarin Chinese", "Pinyin and Characters", "Grammar and Sentence Structure", "Reading and Writing", "Listening and Speaking"]`

## Implementation Details

The contentTitle generation uses a smart keyword matching system that:
1. Analyzes the lesson title and description field for specific topic keywords
2. Matches keywords against predefined content templates for each category
3. Prioritizes specific terms (e.g., "artificial intelligence") over general terms (e.g., "python")
4. Returns a list of 4-5 relevant topic titles that logically belong in the course
5. Special handling for language courses with dedicated templates for Chinese, Spanish, French, German, Japanese, and Arabic

## Results

- Successfully generated COURSE_CATALOG.csv with 837 rows (including header)
- All required columns populated with meaningful data
- ContentTitle field generates context-aware topic titles based on lesson title and description
- Categories and subcategories detected from course descriptions
- All timestamps properly formatted with Thailand timezone
- Language courses properly identified with specialized content templates
- Verified examples match specifications exactly

## Dependencies

- pandas: For CSV data manipulation
- python-ulid: For generating unique identifiers
- pytz: For timezone handling
- typing_extensions: Required by python-ulid

## What Was Done

1. **Virtual Environment Setup**: Created a Python virtual environment and installed all required packages.

2. **Dependencies Documented**: Updated `requirements.txt` with all necessary libraries:
   - pandas (for CSV handling)
   - python-ulid (for unique ID generation)
   - pytz (for timezone handling)
   - typing_extensions (required by python-ulid)

3. **Mock Data Generator**: Created `generate_mock_data.py` that:
   - Reads the original `EdX.csv` file
   - Maps fields according to the specifications
   - Generates additional fields with context-aware values
   - Outputs to `COURSE_CATALOG.csv` with 837 rows including headers

4. **Smart Categorization**: Implemented intelligent categorization that:
   - Analyzes course content to determine the most appropriate category
   - Selects relevant subcategories based on both the category and course content
   - Avoids randomization in favor of contextual matching

5. **Content Title Generation**: Developed a sophisticated content title system that:
   - Analyzes both lesson title and description for keywords
   - Matches keywords against predefined templates for each category
   - Prioritizes specific terms over general ones
   - Special handling for language courses with dedicated templates
   - Generates 4-5 relevant topic titles that logically belong in the course

6. **Language Course Support**: Added specialized templates for:
   - Mandarin Chinese
   - Spanish
   - French
   - German
   - Japanese
   - Arabic
   - General language courses

7. **Timezone Handling**: All timestamps are generated using the Thailand/Bangkok timezone as specified in the requirements.

## License

This project is for educational purposes.