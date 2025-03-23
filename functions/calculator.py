from datetime import datetime

def calculate_erythrozyten_indices(hb, rbc, hct):
    """
    Calculate Erythrozyten indices (MCV, MCH, MCHC) and classify the condition.

    Args:
        hb (float): Hämoglobin in g/dL.
        rbc (float): Erythrozytenzahl in 10^12/L.
        hct (float): Hämatokrit in %.

    Returns:
        dict: A dictionary containing the inputs, calculated indices, classification, and timestamp.
    """
    if hb <= 0 or rbc <= 0 or hct <= 0:
        raise ValueError("Hämoglobin, Erythrozytenzahl und Hämatokrit müssen positive Werte sein.")

    # Berechnung der Indizes
    mcv = (hct / rbc) * 10
    mch = (hb / rbc) * 10
    mchc = (hb / hct) * 100

    # Klassifikation basierend auf den Indizes
    if 80 <= mcv <= 100 and 27 <= mch <= 33 and 32 <= mchc <= 36:
        classification = "Normochrom, Normozytär"
    elif mcv < 80:
        classification = "Mikrozytär"
    elif mcv > 100:
        classification = "Makrozytär"
    elif mch < 27:
        classification = "Hypochrom"
    else:
        classification = "Andere Anomalie"

    # Ergebnis-Dictionary erstellen
    result_dict = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hb": hb,
        "rbc": rbc,
        "hct": hct,
        "mcv": round(mcv, 2),
        "mch": round(mch, 2),
        "mchc": round(mchc, 2),
        "classification": classification,
    }

    return result_dict