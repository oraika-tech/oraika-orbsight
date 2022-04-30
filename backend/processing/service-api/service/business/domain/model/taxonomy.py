from typing import Optional, List, Any, Dict

from pydantic import BaseModel


class TaxonomyInfo(BaseModel):
    term: str
    term_description: Optional[str]
    issue_categories: Optional[List[str]]
    issue_mapping: Optional[Dict[str, Any]]

    def as_dict(self):
        issue_mapping_str = "" if self.issue_mapping is None else str(self.issue_mapping)
        issue_mapping_str = issue_mapping_str.replace("{", "(")
        issue_mapping_str = issue_mapping_str.replace("}", ")")
        issue_mapping_str = issue_mapping_str.replace("\"", "")
        issue_mapping_str = issue_mapping_str.replace(":", " --> ")
        issue_mapping_str = issue_mapping_str.replace(",", "), (")

        return {
            "Term": self.term,
            "Description": self.term_description,
            "Issue Categories": "" if self.issue_categories is None else ", ".join(self.issue_categories),
            "Issue Mapping": issue_mapping_str
        }
