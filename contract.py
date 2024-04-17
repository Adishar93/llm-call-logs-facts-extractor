class GetQuestionAndFactsResponse:
    def __init__(self, question, facts, status):
        self.question = question
        self.facts = facts
        self.status = status

    def to_dict(self):
        return {"question": self.question, "facts": self.facts, "status": self.status}
