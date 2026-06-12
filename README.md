###WORKFLOW

Search and Store topic docs:

User Enters topic of study -> Agent uses tool to gather resources on the topic (uses ytsearch to get top k videos) -> check the likes count, view count and filter the videos -> passed videos' descriptions are kept as embeddings for now and run a similarity search -> store top k2 videos' metadata -> retrieve their transcript store it in vectorstore -> similary collect data from arxiv and wikipedia too -> for searching use hybrid query from llm for all usecases -> store all docs in the vectorstore



Retrieval and note generation:

Subtopic order generator -> with respect to each subtopic retrieve docs from vectorstore -> generate notes -> provide in document form -> save it


First Filtering:
- check if description there -> description is there for good videos
- likes, view counts, duration
- tags & categories (if present)
- rank description higher if it has time wise split descritiopn about what is there in the video
- could potentially use NLP techniques for faster filtering or use a seperate function backed by LLM 