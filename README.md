# ai_job_bot

Job bot that scrapes indeed for a job role then creates an NLP embedding (ie a vector) of the description of each job.

The bot then compares each embedding to the embedding made from my CV, ie. my experience and skills.

It then runs a semantic similarity between them with whatever model I have loaded up (currently using MiniLM from huggingface).

If the semantic similarity is more than a certain threshold it will trigger a telegram bot to notify me with the job link and the match rate.


![job_bot](https://github.com/0xFpf/ai_job_bot/assets/74162889/acf830e8-3ed0-4dc8-8762-dcd13639dd8e)
