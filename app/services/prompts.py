import json

def question_prompt(level, age):
    return f"""
Create 4 fun questions for a {age}-year-old child.
Level: {level}

Return ONLY JSON:

{{
 "questions":[
  {{ "type":"mcq","question":"...","options":["A","B","C","D"],"answer":0 }},
  {{ "type":"match","left":["A","B"],"right":["1","2"],"pairs":{{"0":1,"1":0}} }},
  {{ "type":"memory","show":["🍎","🚗"],"choices":["🍎","🚗","⭐","🎈"] }},
  {{ "type":"gesture","gesture":"Thumbs Up 👍"}}
 ]
}}
"""
