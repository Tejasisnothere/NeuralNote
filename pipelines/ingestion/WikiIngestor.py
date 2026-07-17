from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


class WikiIngestor:
    def __init__(self, topic, k=3, max_chars=3000):
        self.topic = topic
        self.k = k
        self.max_chars = max_chars

    
        self.api_wrapper = WikipediaAPIWrapper(
            top_k_results=self.k,
            doc_content_chars_max=self.max_chars
        )

        self.wiki_tool = WikipediaQueryRun(api_wrapper=self.api_wrapper)


    def fetch_docs(self):
        result = self.wiki_tool.invoke(self.topic)

        return result