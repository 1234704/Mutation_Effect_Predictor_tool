from .sequence_analyzer import SequenceAnalyzer
from .disease_data import lookup_disease

class MutationPredictor:
    def __init__(self):
        self.analyzer = SequenceAnalyzer()

    def analyze(self, ref_seq, query_seq):
        result = self.analyzer.analyze(ref_seq, query_seq)

        if result["Ref"] != "-":
            disease = lookup_disease(result["Ref"], result["Mut"])
            result["Disease"] = disease["disease"]
            result["Clinical"] = disease["clinical"]

        return result
