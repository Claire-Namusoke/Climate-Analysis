import schedule
import time
import subprocess

def job():
    print("Running weekly climate data update...")
    subprocess.run(["python", "climate.py"])

# Schedule the job every week (Monday at 03:00 AM)
schedule.every().monday.at("03:00").do(job)

print("Climate data auto-update scheduler started. Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(60)
