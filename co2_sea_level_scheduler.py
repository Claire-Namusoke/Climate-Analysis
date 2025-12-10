import schedule
import time
import subprocess

def job():
    print("Running weekly CO2 emissions and sea level data update...")
    subprocess.run(["python", "fetch_world.py"])
    subprocess.run(["python", "fetch_oecd.py"])
    # Add any additional scripts for sea level data if available

# Schedule the job every week (Monday at 03:00 AM)
schedule.every().monday.at("03:00").do(job)

print("CO2 emissions and sea level auto-update scheduler started. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(60)
