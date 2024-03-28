### Problem Statement 💡 :

Build a chatbot API that is able to ingest images or text by a user. The chatbot should be able to fetch accurate YouTube links and respond to the user while answering their query on the chat.

### Tech Stack 💻

Python
Fast API
Crew AI (Simple Orchestration)
Youtube API (Retriving Videos)
Vision GPT API (Analyzing the text in images) -> (if low accuracy is fine, we can use OCR and then ingest text to GPT)

### Example Responses


#### Example 1
```shell
curl --location 'https://math-solver-coteach-production.up.railway.app/search_youtube_chat/' \
--header 'Content-Type: application/json' \
--data '{"question": "If 16 + 4x is 10 more than 14, what is the value of 8x?  A) 2. B) 6. C) 16. D) 80 ","chat_id":"harish"}
'
```
```json
{
    "response": "Sure, here are the most relevant videos to your question:\n\n1. [If 16+4x is 10 more than 14, what is the value of 8x?](https://www.youtube.com/watch?v=aZgEwwKjmfc)\nAuthor: The SAT Tutor\n![Image](https://i.ytimg.com/vi/aZgEwwKjmfc/hqdefault.jpg)\n   \n2. [Solving an equation for y and x](https://www.youtube.com/watch?v=oDosCgJ-L0E)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/oDosCgJ-L0E/hqdefault.jpg)\n\n3. [Solving an equation for y and x using two steps](https://www.youtube.com/watch?v=t3uagRNXLHA)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/t3uagRNXLHA/hqdefault.jpg)\n\n4. [Solving an equation with variables on both side and one solution](https://www.youtube.com/watch?v=JDitz3DY_uU)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/JDitz3DY_uU/hqdefault.jpg)\n\n5. [Learn how to evaluate a function for a given value](https://www.youtube.com/watch?v=6ZVaNa_6LGw)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/6ZVaNa_6LGw/hqdefault.jpg)\n   \nThese will help you understand how to solve this type of problem. Let me know if you need any other resources.",
    "history": [
        {
            "user": "If 16 + 4x is 10 more than 14, what is the value of 8x?  A) 2. B) 6. C) 16. D) 80 "
        },
        {
            "assistant": "Sure, here are the most relevant videos to your question:\n\n1. [If 16+4x is 10 more than 14, what is the value of 8x?](https://www.youtube.com/watch?v=aZgEwwKjmfc)\nAuthor: The SAT Tutor\n![Image](https://i.ytimg.com/vi/aZgEwwKjmfc/hqdefault.jpg)\n   \n2. [Solving an equation for y and x](https://www.youtube.com/watch?v=oDosCgJ-L0E)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/oDosCgJ-L0E/hqdefault.jpg)\n\n3. [Solving an equation for y and x using two steps](https://www.youtube.com/watch?v=t3uagRNXLHA)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/t3uagRNXLHA/hqdefault.jpg)\n\n4. [Solving an equation with variables on both side and one solution](https://www.youtube.com/watch?v=JDitz3DY_uU)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/JDitz3DY_uU/hqdefault.jpg)\n\n5. [Learn how to evaluate a function for a given value](https://www.youtube.com/watch?v=6ZVaNa_6LGw)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/6ZVaNa_6LGw/hqdefault.jpg)\n   \nThese will help you understand how to solve this type of problem. Let me know if you need any other resources."
        }
    ]
}
````

#### Thaanking psot question
```shell
curl --location 'https://math-solver-coteach-production.up.railway.app/search_youtube_chat/' \
--header 'Content-Type: application/json' \
--data '
{"question": "thanks for helping me with this question","chat_id":"harish"}
'
```json
{
    "response": "You're welcome! If you need help with other algebra questions or any other kinds of math problems, feel free to ask. I'm here to provide video resources that could help you understand better.",
    "history": [
        {
            "user": "If 16 + 4x is 10 more than 14, what is the value of 8x?  A) 2. B) 6. C) 16. D) 80 "
        },
        {
            "assistant": "Sure, here are the most relevant videos to your question:\n\n1. [If 16+4x is 10 more than 14, what is the value of 8x?](https://www.youtube.com/watch?v=aZgEwwKjmfc)\nAuthor: The SAT Tutor\n![Image](https://i.ytimg.com/vi/aZgEwwKjmfc/hqdefault.jpg)\n   \n2. [Solving an equation for y and x](https://www.youtube.com/watch?v=oDosCgJ-L0E)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/oDosCgJ-L0E/hqdefault.jpg)\n\n3. [Solving an equation for y and x using two steps](https://www.youtube.com/watch?v=t3uagRNXLHA)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/t3uagRNXLHA/hqdefault.jpg)\n\n4. [Solving an equation with variables on both side and one solution](https://www.youtube.com/watch?v=JDitz3DY_uU)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/JDitz3DY_uU/hqdefault.jpg)\n\n5. [Learn how to evaluate a function for a given value](https://www.youtube.com/watch?v=6ZVaNa_6LGw)\nAuthor: Brian McLogan\n![Image](https://i.ytimg.com/vi/6ZVaNa_6LGw/hqdefault.jpg)\n   \nThese will help you understand how to solve this type of problem. Let me know if you need any other resources."
        },
        {
            "user": "thanks for helping me with this question"
        },
        {
            "assistant": "You're welcome! If you need help with other algebra questions or any other kinds of math problems, feel free to ask. I'm here to provide video resources that could help you understand better."
        }
    ]
}`
````



#### Edge Cases (saying thanks without any question)
```shell
curl --location 'https://math-solver-coteach-production.up.railway.app/search_youtube_chat/' \
--header 'Content-Type: application/json' \
--data '
{"question": "thanks for helping me","chat_id":"harish"}
'
```
```json
{
    "response": "I'm sorry, but could you clarify your needs? Are you asking for specific videos about a particular math topic, algebra, or something else? If you provide more details, I would be able to assist you better.",
    "history": [
        {
            "user": "thanks for helping me"
        },
        {
            "assistant": "I'm sorry, but could you clarify your needs? Are you asking for specific videos about a particular math topic, algebra, or something else? If you provide more details, I would be able to assist you better."
        }
    ]
}
```