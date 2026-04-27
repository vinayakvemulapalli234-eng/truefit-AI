import pandas as pd
import os

data = [
    # Data Scientist
    ("python machine learning data analysis numpy pandas", "analytical problem solving teamwork", "btech computer science", "internship projects", "ai data science", "Data Scientist"),
    ("python machine learning scikit-learn statistics", "analytical research teamwork", "mtech data science", "2 years ml", "data science", "Data Scientist"),
    ("python pandas numpy machine learning regression", "problem solving analytical communication", "btech computer science", "1 year data science", "machine learning", "Data Scientist"),
    ("r python statistics data mining machine learning", "analytical research problem solving", "msc statistics", "phd research", "data science research", "Data Scientist"),
    ("python tensorflow keras neural network", "analytical research teamwork", "mtech ai", "2 years deep learning", "ai machine learning", "Data Scientist"),

    # Software Engineer
    ("python flask web development html css javascript", "communication teamwork creativity", "btech computer science", "2 years web development", "software development", "Software Engineer"),
    ("java spring boot microservices rest api", "problem solving leadership teamwork", "btech information technology", "3 years java", "software development", "Software Engineer"),
    ("python django backend api database", "problem solving teamwork communication", "btech computer science", "2 years backend", "software development", "Software Engineer"),
    ("c++ java python algorithms data structures", "analytical problem solving teamwork", "btech computer science", "2 years software", "software engineering", "Software Engineer"),
    ("javascript nodejs python backend microservices", "communication teamwork problem solving", "btech computer science", "3 years fullstack", "software development", "Software Engineer"),

    # AI/ML Engineer
    ("python tensorflow keras deep learning computer vision", "analytical research problem solving", "mtech ai", "research projects", "ai machine learning", "AI/ML Engineer"),
    ("python pytorch deep learning neural networks", "research analytical problem solving", "mtech computer science", "2 years deep learning", "ai machine learning", "AI/ML Engineer"),
    ("machine learning python scikit tensorflow model deployment", "analytical problem solving teamwork", "mtech ai ml", "2 years ml engineering", "ai engineering", "AI/ML Engineer"),
    ("python mlops docker kubernetes machine learning pipeline", "analytical problem solving teamwork", "btech computer science", "3 years ml", "machine learning ops", "AI/ML Engineer"),
    ("deep learning computer vision nlp python tensorflow", "research analytical creativity", "mtech ai", "2 years research", "ai research", "AI/ML Engineer"),

    # Frontend Developer
    ("react javascript html css nodejs typescript", "creativity communication teamwork", "btech computer science", "2 years frontend", "web development", "Frontend Developer"),
    ("angular vue react javascript html css", "creativity problem solving communication", "btech computer science", "3 years frontend", "web development", "Frontend Developer"),
    ("javascript typescript react redux html css", "creativity teamwork communication", "btech computer science", "2 years react", "frontend development", "Frontend Developer"),
    ("html css javascript bootstrap jquery responsive", "creativity communication problem solving", "btech computer science", "1 year frontend", "web design development", "Frontend Developer"),
    ("react nextjs javascript tailwind css", "creativity teamwork problem solving", "btech computer science", "2 years react", "frontend web", "Frontend Developer"),

    # Backend Developer
    ("java spring boot hibernate sql rest api", "problem solving analytical teamwork", "btech computer science", "3 years java backend", "backend development", "Backend Developer"),
    ("python django flask postgresql rest api", "problem solving teamwork communication", "btech computer science", "2 years python backend", "backend software", "Backend Developer"),
    ("nodejs express mongodb rest api javascript", "problem solving analytical teamwork", "btech computer science", "2 years nodejs", "backend development", "Backend Developer"),
    ("java microservices docker kubernetes sql", "analytical problem solving teamwork", "btech information technology", "3 years backend", "software backend", "Backend Developer"),
    ("golang python backend api microservices", "analytical problem solving communication", "btech computer science", "2 years backend", "backend development", "Backend Developer"),

    # Data Analyst
    ("python data analysis excel tableau power bi", "analytical attention detail communication", "bsc statistics", "2 years analysis", "data analysis", "Data Analyst"),
    ("sql excel tableau data analysis reporting", "analytical problem solving communication", "bcom statistics", "3 years analyst", "business data analysis", "Data Analyst"),
    ("power bi tableau excel sql data visualization", "analytical communication attention detail", "bsc mathematics", "2 years data analyst", "data visualization", "Data Analyst"),
    ("python r statistics data analysis visualization", "analytical research communication", "msc statistics", "2 years analyst", "statistical analysis", "Data Analyst"),
    ("sql python excel business intelligence reporting", "analytical teamwork communication", "btech computer science", "2 years analyst", "business analysis", "Data Analyst"),

    # Cloud Engineer
    ("aws cloud computing docker kubernetes terraform", "problem solving teamwork communication", "btech computer science", "3 years cloud", "cloud computing", "Cloud Engineer"),
    ("azure cloud computing devops kubernetes", "analytical problem solving teamwork", "btech computer science", "2 years azure", "cloud infrastructure", "Cloud Engineer"),
    ("gcp google cloud kubernetes docker terraform", "problem solving analytical teamwork", "btech computer science", "2 years gcp", "cloud engineering", "Cloud Engineer"),
    ("aws azure cloud architecture microservices", "analytical communication teamwork", "btech computer science", "3 years cloud", "cloud solutions", "Cloud Engineer"),
    ("cloud computing aws devops ci cd pipeline", "analytical problem solving teamwork", "btech computer science", "2 years cloud devops", "cloud development", "Cloud Engineer"),

    # DevOps Engineer
    ("devops jenkins cicd docker kubernetes terraform", "problem solving teamwork analytical", "btech computer science", "3 years devops", "devops cloud", "DevOps Engineer"),
    ("docker kubernetes jenkins git cicd linux", "analytical problem solving teamwork", "btech computer science", "2 years devops", "devops automation", "DevOps Engineer"),
    ("ansible terraform aws devops automation", "problem solving analytical communication", "btech computer science", "3 years devops", "infrastructure automation", "DevOps Engineer"),
    ("linux bash scripting devops monitoring automation", "analytical problem solving teamwork", "btech computer science", "2 years linux devops", "devops engineering", "DevOps Engineer"),
    ("kubernetes docker helm cicd devops cloud", "analytical teamwork problem solving", "btech computer science", "2 years kubernetes", "cloud devops", "DevOps Engineer"),

    # Cybersecurity Analyst
    ("cybersecurity ethical hacking penetration testing network", "analytical problem solving attention detail", "btech cybersecurity", "2 years security", "cybersecurity", "Cybersecurity Analyst"),
    ("network security firewall intrusion detection", "problem solving analytical attention detail", "btech computer science", "2 years network security", "network cybersecurity", "Cybersecurity Analyst"),
    ("ethical hacking kali linux penetration testing", "analytical problem solving teamwork", "btech cybersecurity", "2 years ethical hacking", "security penetration", "Cybersecurity Analyst"),
    ("siem security operations center threat analysis", "analytical attention detail problem solving", "btech computer science", "2 years soc", "security operations", "Cybersecurity Analyst"),
    ("cybersecurity risk assessment compliance iso27001", "analytical communication problem solving", "btech cybersecurity mba", "3 years security", "cybersecurity compliance", "Cybersecurity Analyst"),

    # UI/UX Designer
    ("ui ux design figma adobe xd wireframing prototyping", "creativity communication empathy", "bdes design", "2 years design", "design ux", "UI/UX Designer"),
    ("figma sketch adobe xd user research prototyping", "creativity empathy communication", "bdes", "2 years ux", "user experience design", "UI/UX Designer"),
    ("ui design figma css html user interface", "creativity problem solving communication", "bdes computer science", "2 years ui", "interface design", "UI/UX Designer"),
    ("ux research usability testing wireframing figma", "empathy analytical communication", "bdes psychology", "2 years ux research", "ux research design", "UI/UX Designer"),
    ("product design figma user research prototyping", "creativity empathy teamwork", "bdes", "3 years product design", "product ux design", "UI/UX Designer"),

    # Android Developer
    ("android java kotlin mobile app development", "creativity problem solving teamwork", "btech computer science", "2 years android", "mobile development", "Android Developer"),
    ("kotlin android jetpack compose mobile development", "creativity communication problem solving", "btech computer science", "2 years kotlin", "android kotlin", "Android Developer"),
    ("android java firebase mobile app rest api", "creativity problem solving teamwork", "btech computer science", "2 years android firebase", "mobile android", "Android Developer"),
    ("android kotlin mvvm architecture mobile", "analytical problem solving creativity", "btech computer science", "2 years android", "android development", "Android Developer"),
    ("mobile android java kotlin play store", "creativity teamwork problem solving", "btech computer science", "3 years mobile", "android apps", "Android Developer"),

    # Product Manager
    ("product management agile scrum roadmap user research", "leadership communication analytical", "btech mba", "3 years product", "product management", "Product Manager"),
    ("agile scrum product roadmap user research market", "leadership analytical communication", "mba btech", "4 years product", "product strategy", "Product Manager"),
    ("product strategy analytics user research agile", "leadership communication problem solving", "mba", "4 years product management", "product leadership", "Product Manager"),
    ("product management jira confluence roadmap metrics", "leadership teamwork communication", "btech mba", "3 years product", "product development", "Product Manager"),
    ("product analytics user stories sprint planning", "leadership communication analytical", "mba", "3 years product", "product management", "Product Manager"),

    # Financial Analyst
    ("financial analysis investment portfolio management excel", "analytical problem solving communication", "mba finance", "2 years finance", "finance investment", "Financial Analyst"),
    ("financial modeling valuation excel bloomberg", "analytical problem solving communication", "mba finance ca", "3 years financial analysis", "finance investment banking", "Financial Analyst"),
    ("equity research financial analysis stock market", "analytical research communication", "mba finance", "2 years equity research", "finance research", "Financial Analyst"),
    ("financial planning budgeting forecasting excel", "analytical communication teamwork", "mba finance", "2 years finance", "financial planning", "Financial Analyst"),
    ("investment banking financial modeling merger acquisition", "analytical leadership communication", "mba finance", "3 years investment banking", "finance investment", "Financial Analyst"),

    # Digital Marketing Manager
    ("digital marketing seo sem google ads social media", "creativity communication analytical", "mba marketing", "2 years marketing", "digital marketing", "Digital Marketing Manager"),
    ("seo content marketing social media analytics", "creativity communication leadership", "mba marketing", "3 years digital marketing", "marketing digital", "Digital Marketing Manager"),
    ("google ads facebook ads ppc campaigns analytics", "creativity analytical communication", "mba marketing", "2 years paid marketing", "paid digital marketing", "Digital Marketing Manager"),
    ("content strategy social media email marketing", "creativity communication teamwork", "mba marketing ba", "2 years content marketing", "content digital marketing", "Digital Marketing Manager"),
    ("digital marketing growth hacking analytics seo", "creativity analytical leadership", "mba marketing", "3 years growth", "growth marketing", "Digital Marketing Manager"),

    # HR Manager
    ("hr recruitment talent management payroll", "communication empathy leadership", "mba hr", "2 years hr", "human resources", "HR Manager"),
    ("talent acquisition recruitment hrms payroll", "communication empathy problem solving", "mba hr", "3 years recruitment", "hr talent", "HR Manager"),
    ("hr operations employee engagement training development", "communication leadership empathy", "mba hr", "3 years hr", "hr operations", "HR Manager"),
    ("performance management hr policy compensation benefits", "communication analytical leadership", "mba hr", "3 years hr management", "hr management", "HR Manager"),
    ("hr business partner talent management organization", "leadership communication empathy", "mba hr", "4 years hrbp", "hr business", "HR Manager"),

    # Project Manager
    ("project management agile scrum pmp jira", "leadership communication problem solving", "btech mba", "4 years project management", "management", "Project Manager"),
    ("project planning risk management stakeholder budget", "leadership communication analytical", "btech mba", "4 years projects", "project leadership", "Project Manager"),
    ("pmp agile waterfall project delivery team management", "leadership problem solving communication", "btech", "5 years project management", "project delivery", "Project Manager"),
    ("scrum master agile coaching sprint planning", "leadership communication teamwork", "btech", "3 years scrum", "agile project", "Project Manager"),
    ("project coordination budget timeline stakeholder", "leadership communication organization", "mba btech", "3 years coordination", "project management", "Project Manager"),

    # NLP Engineer
    ("python nlp text mining bert transformers spacy", "analytical research problem solving", "mtech ai ml", "research nlp", "ai nlp", "NLP Engineer"),
    ("nlp bert gpt transformers text classification", "analytical research problem solving", "mtech computer science", "2 years nlp", "natural language processing", "NLP Engineer"),
    ("python nlp machine learning text analysis sentiment", "research analytical teamwork", "mtech ai", "2 years nlp research", "nlp ai research", "NLP Engineer"),
    ("huggingface transformers nlp python pytorch", "analytical research problem solving", "mtech ai ml", "2 years nlp", "nlp deep learning", "NLP Engineer"),
    ("speech recognition nlp text to speech python", "analytical research problem solving", "mtech ai", "research speech nlp", "speech nlp", "NLP Engineer"),

    # Blockchain Developer
    ("blockchain solidity ethereum smart contracts web3", "analytical problem solving creativity", "btech computer science", "2 years blockchain", "blockchain web3", "Blockchain Developer"),
    ("solidity ethereum smart contracts defi nft", "problem solving analytical creativity", "btech computer science", "2 years ethereum", "blockchain ethereum", "Blockchain Developer"),
    ("web3 blockchain javascript solidity react", "creativity problem solving analytical", "btech computer science", "2 years web3", "blockchain development", "Blockchain Developer"),
    ("hyperledger fabric blockchain enterprise", "analytical problem solving teamwork", "btech computer science", "2 years blockchain", "enterprise blockchain", "Blockchain Developer"),
    ("defi smart contracts solidity python blockchain", "analytical creativity problem solving", "btech computer science", "2 years defi", "defi blockchain", "Blockchain Developer"),

    # QA Engineer
    ("python automation testing selenium pytest quality", "analytical problem solving attention detail", "btech computer science", "2 years testing", "software testing qa", "QA Engineer"),
    ("selenium webdriver automation testing java", "analytical problem solving attention detail", "btech computer science", "2 years selenium", "test automation", "QA Engineer"),
    ("manual testing automation api testing postman", "analytical attention detail teamwork", "btech computer science", "2 years qa", "quality assurance", "QA Engineer"),
    ("cypress playwright javascript test automation", "analytical problem solving teamwork", "btech computer science", "2 years automation", "frontend testing", "QA Engineer"),
    ("performance testing jmeter load testing quality", "analytical problem solving attention detail", "btech computer science", "2 years performance testing", "performance qa", "QA Engineer"),

    # Graphic Designer
    ("graphic design photoshop illustrator branding", "creativity communication attention to detail", "bfa design", "3 years graphic design", "design", "Graphic Designer"),
    ("adobe photoshop illustrator indesign branding", "creativity attention detail communication", "bfa bdes design", "2 years graphic design", "graphic branding design", "Graphic Designer"),
    ("logo design branding typography visual identity", "creativity communication problem solving", "bdes bfa", "3 years branding", "brand design", "Graphic Designer"),
    ("motion graphics after effects premiere video", "creativity communication teamwork", "bdes multimedia", "2 years motion design", "motion graphic design", "Graphic Designer"),
    ("print digital design photoshop illustrator", "creativity attention detail teamwork", "bfa design", "2 years design", "graphic print design", "Graphic Designer"),

    # Content Writer
    ("content writing blogging seo copywriting", "creativity communication research", "ba english", "2 years writing", "content media", "Content Writer"),
    ("seo content writing blog social media copy", "creativity communication research", "ba english journalism", "2 years content", "digital content writing", "Content Writer"),
    ("technical writing documentation api content", "communication research analytical", "btech english", "2 years technical writing", "technical content", "Content Writer"),
    ("copywriting marketing content brand voice", "creativity communication persuasion", "ba marketing english", "2 years copywriting", "marketing content", "Content Writer"),
    ("content strategy editorial writing research", "creativity communication analytical", "ba journalism english", "3 years editorial", "editorial content", "Content Writer"),

    # Civil Engineer
    ("civil engineering autocad structural design", "analytical problem solving attention to detail", "btech civil", "3 years civil", "civil engineering", "Civil Engineer"),
    ("structural engineering autocad staad pro", "analytical problem solving attention detail", "btech civil", "3 years structural", "structural civil engineering", "Civil Engineer"),
    ("construction management project site supervision", "leadership problem solving communication", "btech civil", "3 years construction", "construction management", "Civil Engineer"),
    ("autocad revit bim civil design drafting", "analytical attention detail problem solving", "btech civil", "2 years design drafting", "civil design", "Civil Engineer"),
    ("geotechnical soil testing foundation design", "analytical research problem solving", "mtech civil geotechnical", "2 years geotechnical", "geotechnical civil", "Civil Engineer"),

    # Mechanical Engineer
    ("mechanical engineering solidworks cad manufacturing", "analytical problem solving teamwork", "btech mechanical", "3 years mechanical", "mechanical engineering", "Mechanical Engineer"),
    ("cad cam solidworks catia mechanical design", "analytical problem solving attention detail", "btech mechanical", "2 years cad design", "mechanical design", "Mechanical Engineer"),
    ("thermal engineering hvac energy analysis", "analytical problem solving teamwork", "btech mechanical", "2 years thermal", "thermal mechanical", "Mechanical Engineer"),
    ("manufacturing process lean six sigma quality", "analytical problem solving teamwork", "btech mechanical", "3 years manufacturing", "manufacturing engineering", "Mechanical Engineer"),
    ("robotics automation plc mechanical engineering", "analytical problem solving creativity", "btech mechanical", "2 years automation", "robotics mechanical", "Mechanical Engineer"),

    # Teacher
    ("teaching curriculum development education psychology", "communication patience empathy", "bed education", "3 years teaching", "education", "Teacher"),
    ("teaching mathematics science curriculum", "communication patience empathy", "bsc bed education", "3 years teaching", "education teaching", "Teacher"),
    ("online teaching edtech e-learning curriculum", "communication creativity patience", "bed education", "2 years online teaching", "online education", "Teacher"),
    ("teaching english language arts literature", "communication empathy patience", "ba english bed", "2 years english teaching", "english education", "Teacher"),
    ("special education inclusive teaching learning", "empathy patience communication", "bed special education", "3 years special ed", "special education", "Teacher"),

    # Event Manager
    ("event management planning coordination logistics", "communication leadership organization", "bba events", "2 years events", "event management", "Event Manager"),
    ("event planning wedding corporate management", "communication leadership creativity", "bba hospitality", "2 years event planning", "event planning", "Event Manager"),
    ("conference exhibition management logistics vendor", "leadership communication organization", "bba events management", "3 years conference", "corporate events", "Event Manager"),
    ("social media marketing event promotion planning", "creativity communication leadership", "bba marketing events", "2 years event marketing", "event marketing", "Event Manager"),
    ("event production logistics budget management", "leadership organization communication", "bba events", "3 years production", "event production", "Event Manager"),
]

columns = ['technical_skills', 'soft_skills', 'education', 'experience', 'career_interest', 'career']
df = pd.DataFrame(data, columns=columns)

os.makedirs('model', exist_ok=True)
df.to_csv('model/dataset.csv', index=False)
print(f"✅ Dataset created: {len(df)} rows, {df['career'].nunique()} careers")
print(df['career'].value_counts())