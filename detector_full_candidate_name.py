import csv
import json
import re

def mask_value(value, pii_type):
    """Mask PII values based on type"""
    if not value or value.strip() == "":
        return value

    if pii_type == "phone":
        return re.sub(r'\d(?=\d{2})', 'X', value)
    elif pii_type == "email":
        if "@" in value:
            parts = value.split("@")
            if len(parts[0]) > 2:
                return parts[0][:2] + "XXX@" + parts[1]
            return "XXX@" + parts[1]
        return "XXX@unknown.com"  # fallback if no @ found
    elif pii_type == "aadhar":
        return value[:4] + " XXXX XXXX " + value[-4:]
    elif pii_type == "upi_id":
        if "@" in value:
            return "usXXX@" + value.split("@")[-1]
        return "usXXX@upi"
    elif pii_type == "name":
        return "".join([c if i == 0 else "X" for i, c in enumerate(value)])
    elif pii_type in ["address", "ip_address", "passport"]:
        return "[REDACTED_PII]"
    else:
        return value

def detect_pii(key):
    """Return PII type if detected from key name"""
    key_lower = key.lower()
    if "phone" in key_lower or "mobile" in key_lower or "contact" in key_lower:
        return "phone"
    elif "email" in key_lower:
        return "email"
    elif "aadhar" in key_lower:
        return "aadhar"
    elif "upi" in key_lower:
        return "upi_id"
    elif "name" in key_lower:
        return "name"
    elif "address" in key_lower:
        return "address"
    elif "ip" in key_lower:
        return "ip_address"
    elif "passport" in key_lower:
        return "passport"
    return None

def process_csv(input_file, output_file):
    with open(input_file, "r", newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["record_id", "redacted_data_json", "is_pii"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            raw_json = row.get("data_json", "").strip()
            try:
                data = json.loads(raw_json)
            except Exception as e:
                print(f"[!] Skipping record {row.get('record_id')} due to JSON error: {e}")
                continue  # skip bad JSON row safely

            redacted_data = {}
            is_pii = False

            for key, value in data.items():
                pii_type = detect_pii(key)
                if pii_type:
                    is_pii = True
                    redacted_data[key] = mask_value(str(value), pii_type)
                else:
                    redacted_data[key] = value

            writer.writerow({
                "record_id": row["record_id"],
                "redacted_data_json": json.dumps(redacted_data, ensure_ascii=False),
                "is_pii": is_pii
            })

    print(f"[+] Redacted output saved to: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detector_full_candidate_name.py <input_csv>")
    else:
        input_file = sys.argv[1]
        output_file = "redacted_output_candidate_full_name.csv"
        process_csv(input_file, output_file)
