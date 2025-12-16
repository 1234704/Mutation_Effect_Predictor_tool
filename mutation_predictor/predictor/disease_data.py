# Mock disease & clinical significance database

DISEASE_DB = {
    ("R", "H"): {
        "disease": "Li-Fraumeni syndrome",
        "clinical": "Pathogenic"
    },
    ("V", "E"): {
        "disease": "Melanoma",
        "clinical": "Likely pathogenic"
    },
    ("G", "D"): {
        "disease": "Colorectal cancer",
        "clinical": "Pathogenic"
    }
}

def lookup_disease(ref, mut):
    return DISEASE_DB.get(
        (ref, mut),
        {
            "disease": "Unknown",
            "clinical": "Uncertain significance"
        }
    )
