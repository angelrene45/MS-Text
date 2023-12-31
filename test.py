import re

def get_double_dollar_strings(text):
    pattern = r'\$\$([\w\d]+)'
    matches = re.findall(pattern, text)
    return matches

# Example usage with line breaks
text = """
select * from table
where id = $$var1
and name = $$var2
"""
found_strings = get_double_dollar_strings(text)
print(found_strings)


def get_sql(text):
    sql_matches = re.findall(r"```sql\n(.*?)\n```", text, re.DOTALL)
    return sql_matches[-1] if sql_matches else None
