from app.services.hash_password_helper import HashPasswordHelper

users_data = [
        {
            "email": "vladimir@gmail.com",
            "username": "vladimir",
            "password": HashPasswordHelper.create_hash_password("vladimir")
        },
        {
            "email": "karina@gmail.com",
            "username": "karina",
            "password": "karina"
        },
        {
            "email": "darya@gmail.com",
            "username": "darya",
            "password": "darya"
        },
        {
            "email": "serhii@gmail.com",
            "username": "serhii",
            "password": "serhii"
        }
]

companies_data = [
        {
            "name": "BMW",
            "descriptions": "Inform about cars",
            "visibility": True,
            "owner_id": 1,
        },
        {
            "name": "Windows",
            "descriptions": "Inform about OS",
            "visibility": False,
            "owner_id": 2,
        },
        {
            "name": "Meduzzen",
            "descriptions": "Inform about web development",
            "visibility": True,
            "owner_id": 3,
        }
]

requests_data = [
        {
            "sender": "user",
            "status": "created",
            "company_id": 1,
            "user_id": 2
        },
        {
            "sender": "company",
            "status": "created",
            "company_id": 2,
            "user_id": 1
        },
        {
            "sender": "company",
            "status": "created",
            "company_id": 3,
            "user_id": 1
        }
    ]

questions_data = [
        {
            "name": "На підприємстві в процесі виробництва утворюються особливо токсичні перероблювані "
                    "промислові відходи. Запропонуйте методутилізації та знешкодження.",
            "choice_answers": [
                "Біотермічна переробка на удосконалених звалищах.",
                "Поховання в котлованах полігонів з ізоляцією дна і стінок ущільнюючимшаром глини",
                "Використання як сировини для повторної переробки.",
                "Поховання в котлованах полігонів в контейнерному тарі.",
                "Термічна обробка."
            ],
            "correct_answers": [
                3
            ],
            "quiz_id": 1
        },
        {
            "name": "Укажіть відходи, що відносяться до рідких відходів:",
            "choice_answers": [
                "Помиї від приготування їжі, миття посуду, підлоги, прання білизни",
                "Нечистоти з вигребів туалетів",
                "Господарсько-побутові стічні води",
                "Все перераховане",
                "Промислові, зливові, міські стічні води"
            ],
            "correct_answers": [
                3
            ],
            "quiz_id": 1
        },
        {
            "name": "Назвіть ступені забруднення ґрунту:",
            "choice_answers": [
                "Чистий, слабо забруднений, забруднений, сильно забруднений",
                "Безпечний, відносно безпечний, небезпечний, надзвичайно небезпечний",
                "Чистий, забруднений, безпечний, небезпечний",
                "Чистий, відносно забруднення, забруднений, недостатньо забруднений",
                "Нижче ГДК, на рівні ГДК, вище ГДК"
            ],
            "correct_answers": [
                0
            ],
            "quiz_id": 1
        },
        {
            "name": "У сільському населеному пункті з децентралізованим водопостачанням",
            "choice_answers": [
                "фтору",
                "миш'яку",
                "стронцію",
                "свинцю",
                "йоду"
            ],
            "correct_answers": [
                2
            ],
            "quiz_id": 1
        }
    ]

answers_1 = [
        {
            "question_id": 1,
            "answers": [
                0
            ]
        },
        {
            "question_id": 2,
            "answers": [
                0
            ]
        },
        {
            "question_id": 3,
            "answers": [
                0
            ]
        },
        {
            "question_id": 4,
            "answers": [
                2
            ]
        }
    ]

answers_2 = [
        {
            "question_id": 1,
            "answers": [
                3
            ]
        },
        {
            "question_id": 2,
            "answers": [
                3
            ]
        },
        {
            "question_id": 3,
            "answers": [
                0
            ]
        },
        {
            "question_id": 4,
            "answers": [
                2
            ]
        }
]

quiz_results_data = [
        {
            "user_id": 1,
            "quiz_id": 1,
            "company_id": 1,
            "number_of_questions": 10,
            "number_of_correct_answers": 7,
            "sum_questions_by_quiz": 10,
            "sum_correct_answers_by_quiz": 7,
            "sum_all_questions": 10,
            "sum_all_correct_answers": 7,
            "gpa": round(7 / 10, 3),
            "gpa_by_quiz": round(7 / 10, 3),
            "gpa_all": round(7 / 10, 3)
        },
        {
            "user_id": 1,
            "quiz_id": 1,
            "company_id": 1,
            "number_of_questions": 10,
            "number_of_correct_answers": 8,
            "sum_questions_by_quiz": 20,
            "sum_correct_answers_by_quiz": 15,
            "sum_all_questions": 20,
            "sum_all_correct_answers": 15,
            "gpa": round(8 / 10, 3),
            "gpa_by_quiz": round(15 / 20, 3),
            "gpa_all": round(15 / 20, 3)
        },
        {
            "user_id": 1,
            "quiz_id": 2,
            "company_id": 1,
            "number_of_questions": 15,
            "number_of_correct_answers": 10,
            "sum_questions_by_quiz": 15,
            "sum_correct_answers_by_quiz": 10,
            "sum_all_questions": 35,
            "sum_all_correct_answers": 25,
            "gpa": round(7 / 10, 3),
            "gpa_by_quiz": round(10 / 15, 3),
            "gpa_all": round(25 / 35, 3)
        }

    ]
