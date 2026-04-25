def run_identity_audit(text_data):
    """
    Appends specific identity fraud detection to the forensics module.
    """
    audit_results = {
        "standing_issue": False,
        "credential_leak": False,
        "flags": []
    }

    # Detect Houston Methodist / Arielle Phillips Credential
    if "24068478" in text_data or "Aphillips" in text_data:
        audit_results["credential_leak"] = True
        audit_results["flags"].append("DETECTED: Houston Methodist In-House Counsel Bar ID (24068478) in local filing metadata.")

    # Detect legacy Bar ID mismatch (19466300 vs 1978 legacy)
    if "19466300" in text_data:
        audit_results["standing_issue"] = True
        audit_results["flags"].append("DETECTED: Bar ID 19466300 associated with legacy W. Frank Suhr practice records (1978).")

    return audit_results
