from typing import List

from schemas import ArticleListItem


class DataExtractor:

    def __init__(self):
        pass

    def get_results(self, query: str) -> List[ArticleListItem]:
        raise NotImplementedError("Subclasses must implement get_resuts method")

    def extract_data(self, query: str):
        raise NotImplementedError(
            "Subclasses must implement extract_data_from_link method"
        )

    @staticmethod
    def get_extractor_class(platform):
        # Logic to determine website and return corresponding subclass
        if platform == "arxiv":
            from data_sources.arxiv import ArxivExtractor
            return ArxivExtractor()
        else:
            # Handle unsupported websites
            return None
        pass
