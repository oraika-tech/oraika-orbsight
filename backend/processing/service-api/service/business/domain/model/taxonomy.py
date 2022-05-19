from typing import Optional, List

from pydantic import BaseModel


class TaxonomyInfo(BaseModel):
    term: str
    term_description: Optional[str]
    issue_categories: Optional[List[str]]
    issue_mapping: Optional[List[str]]

    def as_dict(self):
        return {
            "Term": self.term,
            "Description": self.term_description,
            "Issue Categories": "" if self.issue_categories is None else ", ".join(self.issue_categories),
            "Issue Mapping": "" if self.issue_mapping is None else ", ".join(self.issue_mapping)
        }
