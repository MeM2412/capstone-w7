import csv
from datetime import datetime
from collections import defaultdict

def process_clinic_data(file_path, target_month, target_year):
    # Dictionaries to store our results
    zip_totals = defaultdict(lambda: {'screenings': 0, 'referrals': 0})
    exception_log = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Parse the date to handle month boundaries
                record_date = datetime.strptime(row['Date'], '%Y-%m-%d')
                
                # Filter: Skip records outside the target month/year
                if record_date.month != target_month or record_date.year != target_year:
                    continue 

                zip_code = row['ZIP_Code'].strip()
                
                # Exception: Identify invalid or missing ZIP codes
                if not zip_code or len(zip_code) != 5:
                    exception_log.append(f"Row {reader.line_num}: Invalid ZIP code '{zip_code}' for Patient {row['Patient_ID']}")
                    continue
                
                # Tally the valid records
                zip_totals[zip_code]['screenings'] += int(row['Screenings'])
                zip_totals[zip_code]['referrals'] += int(row['Referrals'])

            except Exception as e:
                exception_log.append(f"Row {reader.line_num}: Data error - {e}")

    return zip_totals, exception_log

# --- Execution ---
# Person 2 will feed their synthetic data into this file
totals, errors = process_clinic_data('synthetic_data.csv', target_month=10, target_year=2026)

print("=== MONTHLY TOTALS BY ZIP CODE ===")
for zip_code, counts in totals.items():
    print(f"ZIP {zip_code}: {counts['screenings']} Screenings, {counts['referrals']} Referrals")

print("\n=== EXCEPTION LOG ===")
for error in errors:
    print(error)