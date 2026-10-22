from django.core.management.base import BaseCommand
from core.models import Role, Skill, RoleSkill, Resource

class Command(BaseCommand):
    help = "Seeds standard sample roles, skills, role requirements, and learning resources."

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data for SkillBridge...")

        # 1. Define Skills by Category
        skills_data = [
            # Web & Frontend
            ("HTML5 & Semantics", "Frontend"),
            ("Modern CSS & Responsive Design", "Frontend"),
            ("JavaScript & DOM Manipulation", "Frontend"),
            # Backend
            ("Python Programming", "Backend"),
            ("Django Framework", "Backend"),
            ("RESTful APIs & JSON", "Backend"),
            # Database
            ("SQL & Relational Databases", "Database"),
            ("Database Normalization & Indexing", "Database"),
            # Mobile
            ("Kotlin / Java", "Mobile"),
            ("Android SDK & Jetpack", "Mobile"),
            ("Mobile UI & Lifecycle", "Mobile"),
            # Data & Analytics
            ("Data Analysis with Pandas", "Data Science"),
            ("Statistics & Probability", "Data Science"),
            ("Data Visualization", "Data Science"),
            ("Advanced Excel & Spreadsheets", "Data Science"),
            # Core Engineering & Tools
            ("Git & GitHub Version Control", "Core Engineering"),
            ("Data Structures & Algorithms", "Core Engineering"),
            ("Problem Solving & Debugging", "Core Engineering"),
            ("Technical Communication", "Professional"),
        ]

        skill_objs = {}
        for name, category in skills_data:
            skill, _ = Skill.objects.get_or_create(name=name, defaults={'category': category})
            skill_objs[name] = skill

        # 2. Define Roles
        roles_data = [
            (
                "Full Stack Developer",
                "Designs and builds complete web applications across frontend user interfaces, backend business logic, and relational database management."
            ),
            (
                "Data Analyst",
                "Collects, cleans, analyzes, and visualizes complex datasets to help organizations derive actionable insights and strategic business intelligence."
            ),
            (
                "Android Developer",
                "Architects and creates robust, high-performance mobile applications for Android smartphones, tablets, and embedded devices using modern SDKs."
            )
        ]

        role_objs = {}
        for name, desc in roles_data:
            role, _ = Role.objects.get_or_create(name=name, defaults={'description': desc})
            role_objs[name] = role

        # 3. Define RoleSkill Mappings (8 to 10 skills per role, required level 2 to 5)
        role_skills_map = {
            "Full Stack Developer": [
                ("HTML5 & Semantics", 4),
                ("Modern CSS & Responsive Design", 4),
                ("JavaScript & DOM Manipulation", 4),
                ("Python Programming", 5),
                ("Django Framework", 5),
                ("RESTful APIs & JSON", 4),
                ("SQL & Relational Databases", 4),
                ("Git & GitHub Version Control", 4),
                ("Data Structures & Algorithms", 3),
                ("Problem Solving & Debugging", 4),
            ],
            "Data Analyst": [
                ("Python Programming", 4),
                ("SQL & Relational Databases", 5),
                ("Database Normalization & Indexing", 3),
                ("Data Analysis with Pandas", 5),
                ("Statistics & Probability", 4),
                ("Data Visualization", 4),
                ("Advanced Excel & Spreadsheets", 4),
                ("Git & GitHub Version Control", 3),
                ("Problem Solving & Debugging", 4),
                ("Technical Communication", 4),
            ],
            "Android Developer": [
                ("Kotlin / Java", 5),
                ("Android SDK & Jetpack", 5),
                ("Mobile UI & Lifecycle", 4),
                ("RESTful APIs & JSON", 4),
                ("SQL & Relational Databases", 3),
                ("Git & GitHub Version Control", 4),
                ("Data Structures & Algorithms", 4),
                ("Problem Solving & Debugging", 4),
                ("Technical Communication", 3),
            ]
        }

        for role_name, skills in role_skills_map.items():
            role = role_objs[role_name]
            for skill_name, req_level in skills:
                skill = skill_objs[skill_name]
                RoleSkill.objects.update_or_create(
                    role=role,
                    skill=skill,
                    defaults={'required_level': req_level}
                )

        # 4. Define Curated Resources (2 to 3 per skill)
        resources_data = [
            ("HTML5 & Semantics", [
                ("MDN Web Docs: HTML Elements Reference", "https://developer.mozilla.org/en-US/docs/Web/HTML", "Article"),
                ("freeCodeCamp Responsive Web Design Certification", "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "Course"),
                ("HTML Crash Course for Beginners (Traversy Media)", "https://www.youtube.com/watch?v=UB1O30fR-EE", "Video"),
            ]),
            ("Modern CSS & Responsive Design", [
                ("CSS-Tricks: Complete Guide to Flexbox & Grid", "https://css-tricks.com/snippets/css/a-guide-to-flexbox/", "Article"),
                ("Modern CSS Deep Dive Course", "https://web.dev/learn/css/", "Course"),
                ("Kevin Powell: Responsive Web Design Masterclass", "https://www.youtube.com/@KevinPowell", "Video"),
            ]),
            ("JavaScript & DOM Manipulation", [
                ("JavaScript.info: The Modern JavaScript Tutorial", "https://javascript.info/", "Book"),
                ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "Article"),
                ("freeCodeCamp: JavaScript Algorithms and Data Structures", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/", "Course"),
            ]),
            ("Python Programming", [
                ("Official Python 3 Documentation Tutorial", "https://docs.python.org/3/tutorial/", "Article"),
                ("Automate the Boring Stuff with Python", "https://automatetheboringstuff.com/", "Book"),
                ("Corey Schafer: Python Programming Full Tutorial Series", "https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhCo42U038gACE", "Video"),
            ]),
            ("Django Framework", [
                ("Official Django Tutorial: Writing Your First Django App", "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "Article"),
                ("Dennis Ivy: Django for Beginners to Advanced Course", "https://www.youtube.com/watch?v=PtQiiknWUcI", "Video"),
                ("Django for Professionals (William S. Vincent)", "https://djangoforprofessionals.com/", "Book"),
            ]),
            ("RESTful APIs & JSON", [
                ("REST API Design Best Practices (Stack Overflow / RedHat)", "https://www.redhat.com/en/topics/api/what-is-a-rest-api", "Article"),
                ("Understanding JSON & Web Services (freeCodeCamp)", "https://www.freecodecamp.org/news/what-is-json-a-json-file-example/", "Article"),
                ("Postman Student API Expert Training", "https://academy.postman.com/", "Course"),
            ]),
            ("SQL & Relational Databases", [
                ("SQLZoo Interactive SQL Tutorials & Exercises", "https://sqlzoo.net/", "Course"),
                ("Mode Analytics SQL Tutorial for Data Analysis", "https://mode.com/sql-tutorial/", "Course"),
                ("CMU 15-445: Database Systems Lecture Series", "https://www.youtube.com/playlist?list=PLSE8ODhjZXjaKScG3l0nuOiDTTqpfnWFf", "Video"),
            ]),
            ("Database Normalization & Indexing", [
                ("Database Normalization (1NF, 2NF, 3NF, BCNF) Explained", "https://www.geeksforgeeks.org/database-normalization-introduction/", "Article"),
                ("Use The Index, Luke! A Guide to Database Performance", "https://use-the-index-luke.com/", "Book"),
            ]),
            ("Data Analysis with Pandas", [
                ("Python for Data Analysis (Wes McKinney)", "https://wesmckinney.com/book/", "Book"),
                ("Pandas Official 10-Minute User Guide", "https://pandas.pydata.org/docs/user_guide/10min.html", "Article"),
                ("Keith Galli: Pandas Data Analysis Bootcamp", "https://www.youtube.com/watch?v=vmEHCJofslg", "Video"),
            ]),
            ("Statistics & Probability", [
                ("Khan Academy: College Statistics & Probability Course", "https://www.khanacademy.org/math/statistics-probability", "Course"),
                ("StatQuest with Josh Starmer", "https://www.youtube.com/@statquest", "Video"),
            ]),
            ("Data Visualization", [
                ("Data Visualization with Matplotlib & Seaborn", "https://seaborn.pydata.org/tutorial.html", "Article"),
                ("Storytelling with Data (Cole Nussbaumer Knaflic)", "https://www.storytellingwithdata.com/", "Book"),
            ]),
            ("Advanced Excel & Spreadsheets", [
                ("Excel Exposure: Free Online Excel Video Training", "https://excelexposure.com/", "Course"),
                ("Chandoo.org: Excel Formulas, Pivot Tables, and Dashboards", "https://chandoo.org/", "Article"),
            ]),
            ("Kotlin / Java", [
                ("Kotlin Hands-on Tour & Official Docs", "https://kotlinlang.org/docs/home.html", "Article"),
                ("Head First Kotlin (Dawn & David Griffiths)", "https://www.oreilly.com/library/view/head-first-kotlin/9781491999295/", "Book"),
                ("freeCodeCamp: Kotlin Course for Beginners", "https://www.youtube.com/watch?v=F9UC958K274", "Video"),
            ]),
            ("Android SDK & Jetpack", [
                ("Google Developers: Android Basics with Compose", "https://developer.android.com/courses/android-basics-compose/course", "Course"),
                ("Philipp Lackner: Android Development Mastery", "https://www.youtube.com/@PhilippLackner", "Video"),
            ]),
            ("Mobile UI & Lifecycle", [
                ("Android Activity & Fragment Lifecycle Guide", "https://developer.android.com/guide/components/activities/activity-lifecycle", "Article"),
                ("Material Design 3 Guidelines for Mobile", "https://m3.material.io/", "Article"),
            ]),
            ("Git & GitHub Version Control", [
                ("Pro Git Book by Scott Chacon and Ben Straub", "https://git-scm.com/book/en/v2", "Book"),
                ("Missing Semester of Your CS Education: Version Control (MIT)", "https://missing.csail.mit.edu/2020/version-control/", "Video"),
            ]),
            ("Data Structures & Algorithms", [
                ("NeetCode 150 - Roadmap & Solutions", "https://neetcode.io/", "Course"),
                ("MIT 6.006: Introduction to Algorithms", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/", "Course"),
            ]),
            ("Problem Solving & Debugging", [
                ("The Pragmatic Programmer (David Thomas, Andrew Hunt)", "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/", "Book"),
                ("Effective Debugging Principles and Practices", "https://www.geeksforgeeks.org/effective-debugging-techniques-for-programmers/", "Article"),
            ]),
            ("Technical Communication", [
                ("Google Technical Writing Courses for Engineers", "https://developers.google.com/tech-writing", "Course"),
                ("Writing for Engineers and Computer Scientists", "https://cs.stanford.edu/people/widom/paper-writing.html", "Article"),
            ])
        ]

        for skill_name, res_list in resources_data:
            if skill_name in skill_objs:
                skill = skill_objs[skill_name]
                for title, link, r_type in res_list:
                    Resource.objects.get_or_create(
                        skill=skill,
                        title=title,
                        defaults={'link': link, 'type': r_type}
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {Role.objects.count()} roles, {Skill.objects.count()} skills, "
            f"{RoleSkill.objects.count()} role requirements, and {Resource.objects.count()} resources!"
        ))
