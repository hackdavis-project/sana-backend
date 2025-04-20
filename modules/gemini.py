from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import types
from modules import database

import json
import os

load_dotenv()

class Classification(BaseModel):
    category: str

class Resource(BaseModel):
    name: str
    description: str
    phone: str
    website: str
    address: str
    image_url: str
    focus: list[str]

class Resources(BaseModel):
    resources: list[Resource]

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

classification_config = types.GenerateContentConfig(
    response_schema=Classification,
    response_mime_type='application/json'
)

resources_config = types.GenerateContentConfig(
    response_schema=Resources,
    response_mime_type='application/json',
    temperature=0.2
)



async def classify(journal_entry: str) -> Classification:
    """
    Takes a journal and classifies the trauma into a category.
    """
    base_prompt = f"""
You are an AI assistant analyzing anonymous journal entries for a mental health support application. The users may be writing about difficult experiences, including various forms of abuse, trauma, or significant emotional distress. Your task is to classify the PRIMARY theme of the following journal entry into ONE of the categories listed below.

**Categories and Brief Definitions:**
* **Domestic Violence / Intimate Partner Violence:** Entry primarily discusses abuse (physical, emotional, financial, sexual) by a current or former partner/spouse.
* **Child Abuse / Neglect:** Entry primarily discusses abuse (physical, emotional, sexual) or neglect experienced during childhood (under 18) by a parent, guardian, or another adult.
* **Sexual Assault / Harassment:** Entry primarily discusses experiences of unwanted sexual contact, sexual violence, coercion, or harassment.
* **Emotional / Verbal Abuse:** Entry primarily discusses non-physical abuse patterns like manipulation, degradation, intimidation, control, isolation, or constant criticism (can overlap with other categories but is the main focus).
* **Elder Abuse:** Entry primarily discusses abuse (physical, emotional, financial, neglect) targeting an older adult (typically 60+).
* **Bullying:** Entry primarily discusses repeated harassment, intimidation, or aggression from peers, often in school, workplace, or online settings.
* **Grief / Loss:** Entry primarily focuses on the emotional pain resulting from death, separation, or other significant loss.
* **General Trauma / Distress:** Entry describes significant emotional pain, upsetting events (like accidents, disasters, witnessing violence), or mental health struggles *without* clearly detailing a specific type of abuse listed above.
* **Uncategorized:** Use this category ONLY if the entry is too short to classify, lacks sufficient detail to identify a primary theme, or is clearly off-topic (e.g., a grocery list).

**Instructions:**
1.  Read the provided journal entry carefully.
2.  Identify the single most prominent theme discussed.
3.  If a specific type of abuse is the clear focus, choose that category.
4.  If multiple types are mentioned, choose the one that seems central to the entry's narrative or emotional weight.
5.  If the entry details significant distress or a traumatic event but doesn't specify a type of interpersonal abuse from the list, use "General Trauma / Distress".
6.  If the entry is too vague, short, or off-topic, use "Uncategorized".
7.  Output *only* the category name from the list above. Do not include any additional text or explanation.

**Journal Entry Text:**
{journal_entry}
    """

    response = await client.aio.models.generate_content(
        model='gemini-2.0-flash',
        contents=[base_prompt],
        config=classification_config
    )

    classification = Classification(**json.loads(response.text))
    return classification


async def find_resources(journal_entry: str) -> Resources:
    base_prompt = f"""
You are an AI assistant embedded in a supportive journaling app. Your task is to analyze the following anonymous journal entry and select 1 to 3 relevant support resources from the provided list that could be most helpful to the user.

**Prioritization Guidelines:**
1.  **Crisis First:** If the journal entry contains language suggesting suicidal ideation, immediate danger, or severe acute crisis, prioritize suggesting national crisis hotlines (like 988, Crisis Text Line, RAINN, NDVH) from the list FIRST.
2.  **Local Relevance:** Given the user context is likely Yolo County, CA, prioritize relevant 'Local' resources (like Empower Yolo, Yolo HHSA Mental Health, UC Davis CARE for students) for issues like ongoing support, counseling, shelter, or basic needs, *after* considering any immediate crisis needs.
3.  **Thematic Matching:** Match resources based on the primary themes identified in the journal entry (e.g., mentions of partner abuse -> Domestic Violence resources; mentions of childhood trauma -> Child Abuse resources; mentions of anxiety/depression -> Mental Health services; mentions of food/housing insecurity -> Basic Needs/Housing resources).
4.  **Specificity:** Prefer resources that directly address the core issue mentioned over general resources, unless only general distress is expressed or a crisis hotline is needed.

**Available Resources:**

{await database.get_resources()}

**Journal Entry:**
{journal_entry}
    """

    print(base_prompt)
    
    response = await client.aio.models.generate_content(
        model='gemini-2.0-flash',
        contents=[base_prompt],
        config=resources_config
    )

    print(response.text)

    resources = Resources(**json.loads(response.text))
    return resources
