import asyncio
from modules import database

resource_list = [
  {
    "name": "Empower Yolo",
    "description": "Provides comprehensive services for victims of domestic violence, sexual assault, stalking, and human trafficking in Yolo County. Offers 24/7 crisis lines, emergency shelter, counseling, legal assistance, resource centers, and more.",
    "phone": "530-661-6336 (Main) / 530-662-1133 (Crisis)",
    "website": "https://empoweryolo.org/",
    "address": "441 D St, Davis, CA 95616 (Davis Resource Center) / 175 Walnut St, Woodland, CA 95695 (Main Office)",
    "image_url": "https://img.logo.dev/empoweryolo.org",
    "focus": ["Domestic Violence", "Sexual Assault", "Human Trafficking", "Shelter", "Counseling", "Legal Aid", "Crisis", "Yolo County"]
  },
  {
    "name": "UC Davis CARE (Center for Advocacy, Resources & Education)",
    "description": "Provides confidential advocacy, support, education, and healing services specifically for UC Davis students, staff, and faculty impacted by sexual harassment, sexual violence, intimate partner violence, and stalking.",
    "phone": "530-752-3299",
    "website": "https://care.ucdavis.edu/",
    "address": "Confidential Location on UC Davis Campus",
    "image_url": "https://img.logo.dev/ucdavis.edu",
    "focus": ["Sexual Assault", "Domestic Violence", "Stalking", "Harassment", "Advocacy", "UC Davis Students"]
  },
  {
    "name": "Yolo County HHSA - Mental Health Services",
    "description": "Offers county mental health services for adults and children, crisis intervention services, substance use disorder services, and connections to other behavioral health programs.",
    "phone": "1-888-965-6647 (24/7 Crisis & Access Line)",
    "website": "https://www.yolocounty.gov/government/general-government-departments/health-human-services/mental-health",
    "address": "137 N Cottonwood St, Woodland, CA 95695 / 600 A St, Davis, CA 95616",
    "image_url": "https://img.logo.dev/yolocounty.gov",
    "focus": ["Mental Health", "Crisis", "Counseling", "Substance Use", "Yolo County"]
  },
  {
    "name": "CommuniCare+OLE Health Centers (Davis Community Clinic)",
    "description": "Provides integrated behavioral health services including therapy, psychiatry, substance use counseling, support groups, and care coordination for patients, often on a sliding scale basis. Insurance not required for some services.",
    "phone": "530-758-2060",
    "website": "https://communicareole.org/services/behavioral-health/",
    "address": "2051 John Jones Road, Davis, CA 95616",
    "image_url": "https://img.logo.dev/communicareole.org",
    "focus": ["Mental Health", "Counseling", "Psychiatry", "Substance Use", "Sliding Scale", "Primary Care", "Davis"]
  },
  {
    "name": "Yolo County District Attorney - Victim Services",
    "description": "Assists victims and witnesses of crime through the criminal justice process. Provides information, court accompaniment, assistance with victim impact statements, referrals, and help applying for the CA Victim Compensation Board (CalVCB).",
    "phone": "530-666-8187",
    "website": "https://yoloda.org/victim-assistance-family-protection/",
    "address": "301 2nd St, Woodland, CA 95695",
    "image_url": "https://img.logo.dev/yoloda.org",
    "focus": ["Crime Victims", "Criminal Justice System", "Advocacy", "Restitution", "Yolo County"]
  },
  {
    "name": "Legal Services of Northern California (LSNC) - Woodland Office",
    "description": "Provides free civil legal assistance to low-income residents of Yolo County, including help with housing, public benefits, healthcare access, and potentially elder abuse or domestic violence related civil matters.",
    "phone": "530-662-1065",
    "website": "https://lsnc.net/office/woodland",
    "address": "619 North St, Woodland, CA 95695",
    "image_url": "https://img.logo.dev/lsnc.net",
    "focus": ["Legal Aid", "Low Income", "Civil Law", "Housing", "Benefits", "Yolo County"]
  },
   {
    "name": "Legal Services of Northern California (LSNC) - Sacramento Office",
    "description": "Provides free civil legal aid to low-income residents in Sacramento County. Operates the Senior Legal Hotline and may offer different or specialized services.",
    "phone": "916-551-2150",
    "website": "https://lsnc.net/office/sacramento",
    "address": "515 - 12th Street, Sacramento, CA 95814",
    "image_url": "https://img.logo.dev/lsnc.net",
    "focus": ["Legal Aid", "Low Income", "Civil Law", "Housing", "Benefits", "Seniors", "Sacramento County"]
  },
  {
    "name": "Davis Community Meals and Housing (Paul's Place)",
    "description": "Provides housing assistance (emergency, transitional, permanent supportive), a resource center with day services (showers, laundry), employment support, and free community meals to homeless and low-income individuals and families.",
    "phone": "530-753-9204",
    "website": "https://daviscommunitymeals.org/",
    "address": "1111 H St, Davis, CA 95616 (Resource Center) / 640 Hawthorn Ln, Davis, CA 95616 (Meal Location)",
    "image_url": "https://img.logo.dev/daviscommunitymeals.org",
    "focus": ["Housing", "Shelter", "Food", "Basic Needs", "Homelessness", "Davis"]
  },
  {
    "name": "Yolo Food Bank",
    "description": "Distributes food county-wide through various programs and partner agencies. Website features a 'Find Food' tool listing distribution locations and times.",
    "phone": "530-668-0690",
    "website": "https://yolofoodbank.org/",
    "address": "233 Harter Ave, Woodland, CA 95776 (Main Warehouse)",
    "image_url": "https://img.logo.dev/yolofoodbank.org",
    "focus": ["Food", "Basic Needs", "Yolo County"]
  },
  {
    "name": "Short Term Emergency Aid Committee (STEAC)",
    "description": "Provides immediate short-term emergency aid (food assistance/food closet, rental/utility assistance, clothing, job readiness support) to low-income Yolo County families and individuals.",
    "phone": "530-758-8435",
    "website": "https://steac.org/",
    "address": "1712 Picasso Avenue, Unit D, Davis, CA 95618",
    "image_url": "https://img.logo.dev/steac.org",
    "focus": ["Emergency Aid", "Financial Assistance", "Food", "Basic Needs", "Low Income", "Yolo County"]
  },
  {
    "name": "NAMI Yolo County",
    "description": "Offers peer-led support groups, classes, and educational resources for individuals living with mental health conditions and their families in Yolo County.",
    "phone": "530-756-8181 (Helpline - Not 24/7)",
    "website": "https://namiyolo.org/",
    "address": "P.O. Box 447, Davis, CA 95617 (Mail)",
    "image_url": "https://img.logo.dev/namiyolo.org",
    "focus": ["Mental Health", "Support Group", "Education", "Family Support", "Peer Support", "Yolo County"]
  },
  {
    "name": "Yolo County Children's Alliance (YCCA)",
    "description": "Provides resource and referral services, application assistance for CalFresh & Medi-Cal/Covered CA, parent education, youth programs, and operates Family Resource Centers.",
    "phone": "916-572-0560 (West Sac FRC) / 530-757-5558 (Davis Office)",
    "website": "https://www.yolokids.org/",
    "address": "1200 Anna St, West Sacramento, CA 95605 / 409 Lincoln Ave, Woodland CA 95695",
    "image_url": "https://img.logo.dev/yolokids.org",
    "focus": ["Family Support", "Resource & Referral", "CalFresh", "Medi-Cal", "Youth Programs", "Parenting", "Yolo County"]
  },
   {
    "name": "Aggie Compass Basic Needs Center",
    "description": "Provides UC Davis students with support for basic needs including food security (food pantry, CalFresh assistance), housing stability, financial wellness, and mental wellness resources.",
    "phone": "530-752-9254",
    "website": "https://aggiecompass.ucdavis.edu/",
    "address": "Memorial Union, East Wing, 1 Shields Ave, Davis, CA 95616",
    "image_url": "https://img.logo.dev/ucdavis.edu",
    "focus": ["Basic Needs", "Food", "Housing", "Financial Aid", "Mental Wellness", "UC Davis Students"]
   },
   {
    "name": "2-1-1 Yolo",
    "description": "Information and referral hotline/website connecting Yolo County residents to a wide range of health and human services.",
    "phone": "Dial 211 (or 855-866-1783)",
    "website": "https://www.211sacramento.org/211/2-1-1-yolo-county/",
    "address": "Phone / Web Based",
    "image_url": "https://img.logo.dev/211sacramento.org",
    "focus": ["Information & Referral", "Health Services", "Human Services", "Basic Needs", "Crisis", "Yolo County"]
   },
  {
    "name": "UC Davis Student Health and Counseling Services (SHCS)",
    "description": "Provides UC Davis students with medical, mental health, and wellness services, including individual counseling, group therapy, psychiatry, crisis support, and urgent care.",
    "phone": "530-752-2349",
    "website": "https://shcs.ucdavis.edu/",
    "address": "930 Orchard Road, Davis, CA 95616",
    "image_url": "https://img.logo.dev/ucdavis.edu",
    "focus": ["Students", "Medical", "Mental Health", "Counseling", "Crisis", "UC Davis Students"]
  },
  {
    "name": "Agency on Aging Area 4 (AAA4)",
    "description": "Connects older adults, people with disabilities, and caregivers in Yolo County and surrounding areas to various services.",
    "phone": "1-800-211-4545",
    "website": "https://www.agencyonaging4.org/yolo-county",
    "address": "1401 El Camino Avenue, 4th Floor, Sacramento, CA 95815",
    "image_url": "https://img.logo.dev/agencyonaging4.org",
    "focus": ["Seniors", "Disability", "Caregiver Support", "Information & Referral", "Benefits Assistance", "Regional"]
  },
  {
    "name": "Aging and Disability Resource Connection (ADRC) of Yolo County",
    "description": "A 'No Wrong Door' service connecting older adults and people with disabilities (and their caregivers) to long-term services and supports.",
    "phone": "1-800-211-4545",
    "website": "https://www.adrc4.org/adrc-of-yolo-county",
    "address": "Connect via Phone/Web (via AAA4)",
    "image_url": "https://img.logo.dev/adrc4.org",
    "focus": ["Seniors", "Disability", "Long Term Care", "Information & Referral", "Yolo County"]
  },
  {
    "name": "Del Oro Caregiver Resource Center",
    "description": "Provides support services for family caregivers of brain-impaired adults and the frail elderly.",
    "phone": "1-800-635-0220",
    "website": "https://www.deloro.org/",
    "address": "8421 Auburn Blvd., Suite 265, Citrus Heights, CA 95610",
    "image_url": "https://img.logo.dev/deloro.org",
    "focus": ["Caregiver Support", "Brain Injury", "Dementia", "Seniors", "Respite", "Regional"]
  },
  {
    "name": "Yolo County In-Home Supportive Services (IHSS)",
    "description": "Provides assistance to eligible aged, blind, and disabled individuals receiving Medi-Cal, helping them remain safely in their own homes.",
    "phone": "530-661-2955 (Intake Line)",
    "website": "https://www.yolocounty.gov/government/general-government-departments/health-human-services/adults/in-home-supportive-services",
    "address": "25 N Cottonwood St, Woodland, CA 95695",
    "image_url": "https://img.logo.dev/yolocounty.gov",
    "focus": ["Seniors", "Disability", "In-Home Care", "Medi-Cal", "Yolo County"]
  },
  {
    "name": "Fourth & Hope",
    "description": "Provides emergency shelter, meals, respite services, alcohol & drug treatment programs, and pathways to stability for homeless individuals.",
    "phone": "530-661-1218",
    "website": "https://fourthandhope.org/",
    "address": "1901 E Beamer St, Woodland, CA 95776",
    "image_url": "https://img.logo.dev/fourthandhope.org",
    "focus": ["Homelessness", "Shelter", "Food", "Substance Use Treatment", "Woodland"]
  },
  {
    "name": "Yolo County Housing",
    "description": "Administers public housing programs, Section 8 Housing Choice Vouchers, and develops affordable housing within Yolo County.",
    "phone": "530-662-5428",
    "website": "https://www.ych.ca.gov/",
    "address": "147 W Main St, Woodland, CA 95695",
    "image_url": "https://img.logo.dev/ych.ca.gov",
    "focus": ["Affordable Housing", "Public Housing", "Section 8", "Yolo County"]
  },
  {
    "name": "Turning Point Community Programs (Davis Community Care Center)",
    "description": "Offers behavioral health services, housing support services, and employment services for individuals with psychiatric disabilities.",
    "phone": "530-757-4888",
    "website": "https://www.tpcp.org/",
    "address": "212 I St, Davis, CA 95616",
    "image_url": "https://img.logo.dev/tpcp.org",
    "focus": ["Mental Health", "Behavioral Health", "Housing Support", "Davis"]
  },
  {
    "name": "Yolo Adult Day Health Center (Dignity Health)",
    "description": "Provides day programs with nursing, therapy, social services, meals, and activities for adults with medical or cognitive challenges.",
    "phone": "530-666-8828",
    "website": "https://www.dignityhealth.org/sacramento/services/yolo-adult-day-health-services/yolo-adult-day-health-center",
    "address": "20 N Cottonwood St, Woodland, CA 95695",
    "image_url": "https://img.logo.dev/dignityhealth.org",
    "focus": ["Seniors", "Adults with Disabilities", "Day Program", "Health Monitoring", "Therapy", "Woodland"]
  },
  {
    "name": "Ability Tools",
    "description": "California's Assistive Technology Act Program. Offers device lending libraries, financial loans for assistive technology (AT), an AT exchange marketplace, information & referral, and reuse programs.",
    "phone": "1-800-390-2699",
    "website": "https://abilitytools.org/",
    "address": "Statewide Network",
    "image_url": "https://img.logo.dev/abilitytools.org",
    "focus": ["Disability", "Assistive Technology", "Statewide"]
  },
  {
    "name": "WEAVE (Sacramento)",
    "description": "Major regional provider of crisis intervention services for survivors of domestic violence, sexual assault, and sex trafficking in Sacramento County.",
    "phone": "916-920-2952 (24/7 Support Line)",
    "website": "https://www.weaveinc.org/",
    "address": "1900 K St, Sacramento, CA 95811",
    "image_url": "https://img.logo.dev/weaveinc.org",
    "focus": ["Domestic Violence", "Sexual Assault", "Sex Trafficking", "Crisis", "Shelter", "Counseling", "Sacramento County"]
  },
  {
    "name": "My Sister's House (Sacramento)",
    "description": "Serves Asian and Pacific Islander and other underserved women and children impacted by domestic violence, sexual assault, and human trafficking with culturally specific support.",
    "phone": "916-428-3271 (24/7 Multilingual Support Line)",
    "website": "https://www.my-sisters-house.org/",
    "address": "3053 Freeport Blvd., #120, Sacramento, CA 95818 (Mailing)",
    "image_url": "https://img.logo.dev/my-sisters-house.org",
    "focus": ["Domestic Violence", "Sexual Assault", "Human Trafficking", "AAPI Community", "Cultural Specific", "Shelter", "Sacramento County"]
  },
  {
    "name": "Sacramento LGBT Community Center",
    "description": "Regional center offering resources, support groups, health services, youth programs, and community engagement opportunities for LGBTQ+ individuals.",
    "phone": "916-442-0185",
    "website": "https://saccenter.org/",
    "address": "1021 10th St, Sacramento, CA 95814",
    "image_url": "https://img.logo.dev/saccenter.org",
    "focus": ["LGBTQ+", "Community Center", "Support Groups", "Health Services", "Youth Programs", "Sacramento County"]
  },
  {
    "name": "Sierra Vista Hospital (Sacramento / Davis Clinic)",
    "description": "Private behavioral health facility providing inpatient/outpatient psychiatric and chemical dependency treatment for adults/adolescents. Operates an outpatient clinic in Davis.",
    "phone": "916-288-0300 (Main) / 530-231-4800 (Davis Clinic)",
    "website": "https://sierravistahospital.com/",
    "address": "8001 Bruceville Road, Sacramento, CA 95823 / 2840 5th Street, Davis, CA 95618",
    "image_url": "https://img.logo.dev/sierravistahospital.com",
    "focus": ["Mental Health", "Behavioral Health", "Chemical Dependency", "Inpatient", "Outpatient", "Psychiatry", "Sacramento", "Davis Clinic"]
  },
  {
    "name": "Heritage Oaks Hospital (Sacramento)",
    "description": "Acute psychiatric hospital providing inpatient/outpatient programs for adolescents, adults, and seniors in the Sacramento region.",
    "phone": "916-489-3336",
    "website": "https://heritageoakshospital.com/",
    "address": "4250 Auburn Blvd, Sacramento, CA 95841",
    "image_url": "https://img.logo.dev/heritageoakshospital.com",
    "focus": ["Mental Health", "Behavioral Health", "Psychiatry", "Inpatient", "Outpatient", "Seniors", "Adolescents", "Sacramento"]
  },
  {
    "name": "Shores of Hope (West Sacramento)",
    "description": "Provides support services in West Sacramento including food, clothing, and programs assisting at-risk/homeless foster youth (ages 18-24).",
    "phone": "916-372-0200",
    "website": "http://shoresofhope.org/",
    "address": "110 6th St, West Sacramento, CA 95605",
    "image_url": "https://img.logo.dev/shoresofhope.org",
    "focus": ["Basic Needs", "Food", "Clothing", "Homelessness", "Foster Youth Support", "West Sacramento"]
  },
  {
    "name": "Wind Youth Services (Sacramento)",
    "description": "Provides support services, street outreach, drop-in center, and emergency shelters for homeless and runaway youth (typically ages 12-24) in the Sacramento region.",
    "phone": "916-504-3313 (Drop-in Center)",
    "website": "https://www.windyouthservices.org/",
    "address": "Check Website for Locations",
    "image_url": "https://img.logo.dev/windyouthservices.org",
    "focus": ["Homeless Youth", "Runaway Youth", "Shelter", "Drop-in Center", "Sacramento Region"]
  },
  {
    "name": "UC Davis Health Patient Support Groups",
    "description": "Offers numerous support groups for patients and families dealing with specific health conditions (e.g., cancer, burn recovery, bereavement) at the Sacramento medical campus.",
    "phone": "Contact varies by group (see website)",
    "website": "https://health.ucdavis.edu/patients-visitors/support-groups/",
    "address": "UC Davis Medical Center, 2315 Stockton Blvd, Sacramento, CA 95817",
    "image_url": "https://img.logo.dev/ucdavis.edu",
    "focus": ["Health Conditions", "Patient Support", "Family Support", "Peer Support", "UC Davis Health Patients"]
  }
]

async def main():
    for resource in resource_list:
        await database.add_resource(resource)
        print(f"Added {resource['name']} to database")

if __name__ == "__main__":
    asyncio.run(main())
