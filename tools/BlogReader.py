import trafilatura


class BlogPipeline:
    def __init__(self, url, embedding_model):
        self.url = url
        self.downloaded = trafilatura.fetch_url(url)

        


def fetch_blog(url):
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)

    return text

