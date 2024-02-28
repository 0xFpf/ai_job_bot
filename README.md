# ai_job_bot

Job bot that scrapes indeed for a job role then creates an NLP embedding (ie a vector) of the description of each job.

The bot then compares each embedding to the embedding made from my CV, ie. my experience and skills.

It then runs a semantic similarity between them with whatever model I have loaded up (currently using MiniLM from huggingface).

If the semantic similarity is more than a certain threshold it will trigger a telegram bot to notify me with the job link and the match rate.

![tg_jobbot](https://github.com/0xFpf/ai_job_bot/assets/74162889/1f8b646d-edfe-4583-b3ee-d909ca8c9e92)
