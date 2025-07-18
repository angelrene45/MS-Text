import pandas as pd

data = {
    "ID": [228255, 228256],
    "User_Email": [
        "stephanie.mcaleer@morganstanley.com",
        "john.doe@example.com"
    ],
    "Question": [
        "Testing question",
        "Another test question"
    ],
    "Is_Subscribed": [False, True],
    "Filters": [
        {
            "time_range": ["2020-06-09", "2025-06-09"],
            "companies": [],
            "data_sources": []
        },
        {
            "time_range": ["2020-06-09", "2025-06-09"],
            "companies": [],
            "data_sources": []
        }
    ]
}

df = pd.DataFrame(data)
print(df)
