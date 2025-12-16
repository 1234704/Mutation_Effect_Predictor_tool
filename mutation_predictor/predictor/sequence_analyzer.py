from Bio.Align import substitution_matrices

class SequenceAnalyzer:
    def __init__(self):
        self.matrix = substitution_matrices.load("BLOSUM62")

        # Amino acid groups
        self.hydrophobic = set("AILMVFWY")
        self.polar = set("STNQ")
        self.positive = set("KRH")
        self.negative = set("DE")
        self.special = set("CGP")

    def aa_group(self, aa):
        if aa in self.hydrophobic:
            return "hydrophobic"
        if aa in self.polar:
            return "polar"
        if aa in self.positive:
            return "positive"
        if aa in self.negative:
            return "negative"
        return "special"

    def analyze(self, ref_seq, query_seq):
        ref_seq = ref_seq.upper().strip()
        query_seq = query_seq.upper().strip()

        # ---------- NO MUTATION ----------
        if ref_seq == query_seq:
            return {
                "Position": "-",
                "Ref": "-",
                "Mut": "-",
                "Type": "No mutation",
                "Score": 0.01,
                "Pathogenicity": "Benign",
                "Disease": "None",
                "Clinical": "Normal sequence",
                "CNV": "None"
            }

        # ---------- LENGTH-BASED EVENTS ----------
        if len(query_seq) > len(ref_seq):
            return {
                "Position": "-",
                "Ref": "-",
                "Mut": "-",
                "Type": "Insertion / Duplication",
                "Score": 0.9,
                "Pathogenicity": "Pathogenic",
                "Disease": "Possible gain-of-function",
                "Clinical": "Likely pathogenic",
                "CNV": "Duplication"
            }

        if len(query_seq) < len(ref_seq):
            return {
                "Position": "-",
                "Ref": "-",
                "Mut": "-",
                "Type": "Deletion",
                "Score": 0.95,
                "Pathogenicity": "Pathogenic",
                "Disease": "Loss-of-function related",
                "Clinical": "Likely pathogenic",
                "CNV": "Deletion"
            }

        # ---------- SUBSTITUTION ----------
        for i in range(len(ref_seq)):
            r = ref_seq[i]
            q = query_seq[i]

            if r != q:
                # Check for stop codon
                if q == "*":
                    score = 0.9
                    pathogenicity = "Pathogenic"
                    clinical = "Likely pathogenic"
                    mut_type = "Nonsense mutation"
                else:
                    # Calculate simple SIFT-like score
                    same_group = self.aa_group(r) == self.aa_group(q)
                    blosum_score = self.matrix[r, q]

                    # Simplified score between 0.01 and 0.9
                    if same_group:
                        score = 0.1
                    else:
                        score = 0.3  # non-conservative

                    # Apply your 0.01–0.25 benign rule
                    if score <= 0.25:
                        pathogenicity = "Benign"
                        clinical = "Likely benign"
                    else:
                        pathogenicity = "Pathogenic"
                        clinical = "Likely pathogenic"

                    mut_type = "Missense substitution"

                return {
                    "Position": i + 1,
                    "Ref": r,
                    "Mut": q,
                    "Type": mut_type,
                    "Score": round(score, 2),
                    "Pathogenicity": pathogenicity,
                    "Disease": "Unknown",
                    "Clinical": clinical,
                    "CNV": "None"
                }

        # Fallback
        return {
            "Position": "-",
            "Ref": "-",
            "Mut": "-",
            "Type": "Undetermined",
            "Score": 0.5,
            "Pathogenicity": "Pathogenic",
            "Disease": "Unknown",
            "Clinical": "Review required",
            "CNV": "None"
        }