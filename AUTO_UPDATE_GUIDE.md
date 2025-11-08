# Automatic Data Updates Setup Guide 🔄

Your Climate Analysis tool now automatically checks for updates from the World Bank API!

## How It Works 🛠️

### Smart Update Detection

The script now:
1. **Checks if data exists locally** - If no local file, fetches new data
2. **Compares data hashes** - Detects if World Bank has updated their dataset
3. **Only downloads when needed** - Saves bandwidth and time
4. **Stores metadata** - Tracks when data was last fetched

### What Changed in `climate.py`

✅ **New Functions:**
- `check_for_updates()` - Compares local vs API data
- `auto_update_data()` - Automatically updates when needed
- `load_local_data()` - Loads previously saved data
- `calculate_data_hash()` - Detects data changes

✅ **Enhanced Functions:**
- `fetch_climate_data()` - Now captures metadata (timestamps, headers)
- `save_data_to_file()` - Stores metadata alongside data
- `main()` - Automatically checks and updates before displaying

## Usage Examples 📝

### Basic Usage (Automatic Updates)

```bash
# Just run the script - it checks for updates automatically!
python climate.py
```

**Output when data is up-to-date:**
```
Checking for updates...
Update check: Local data is up to date
✓ Using existing local data (up to date)
```

**Output when update is needed:**
```
Checking for updates...
Update check: Data content has changed
🔄 Updating data from API...
✓ Data updated successfully!
```

### Force Update (Download Fresh Data)

If you want to force download fresh data:

```python
# Modify the main() function temporarily or create a script:
auto_update_data(api_url, "climate_data.json", force=True)
```

## Automated Scheduling ⏰

### Option 1: Windows Task Scheduler (Recommended for Windows)

**Step 1: Create a batch file** (`update_climate.bat`):
```batch
@echo off
cd /d "C:\Users\clair\OneDrive\OfficeMobile\Desktop\Climate-Analysis"
C:\Users\clair\OneDrive\OfficeMobile\Desktop\Climate-Analysis\.venv\Scripts\python.exe scheduler.py >> update_log.txt 2>&1
```

**Step 2: Set up Task Scheduler:**
1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"**
3. Name: "Climate Data Update"
4. Trigger: Choose frequency (Daily, Weekly, or Monthly)
5. Action: "Start a program"
6. Program/script: Browse to your `update_climate.bat` file
7. Click Finish

**Recommended Schedules:**
- **Daily at midnight** - If you need very fresh data
- **Weekly on Monday** - Good balance for most uses
- **Monthly on 1st** - If data doesn't change often

### Option 2: Python Script with Scheduler

Install the `schedule` library:
```bash
pip install schedule
```

Create `continuous_updater.py`:
```python
import schedule
import time
from scheduler import scheduled_update

# Schedule updates
schedule.every().day.at("00:00").do(scheduled_update)  # Daily at midnight
# schedule.every().monday.at("08:00").do(scheduled_update)  # Weekly on Monday
# schedule.every(6).hours.do(scheduled_update)  # Every 6 hours

print("Climate data update scheduler started...")
print("Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

Run in background:
```bash
python continuous_updater.py
```

### Option 3: Manual Updates (When Needed)

Just run the scheduler script anytime:
```bash
python scheduler.py
```

Or run the main script:
```bash
python climate.py
```

## How to Check Data Freshness 📅

The script shows when data was last updated:

```
==================================================
DATA FRESHNESS
==================================================
Last fetched: 2025-11-09T00:19:29.762955
API last modified: [If available]
```

## Data Storage Structure 💾

The `climate_data.json` file now contains:

```json
{
  "data": {
    "metadata": { /* API metadata */ },
    "data": { /* Climate data for all countries */ }
  },
  "metadata": {
    "last_modified": "Server's last modified date",
    "etag": "Entity tag for caching",
    "fetch_timestamp": "When data was fetched",
    "status_code": 200
  },
  "local_save_timestamp": "When file was saved"
}
```

## Benefits of Auto-Update System ✨

1. **Always Fresh Data** - Automatically gets latest climate data
2. **Efficient** - Only downloads when data actually changes
3. **Fast** - Uses cached data when available
4. **Reliable** - Tracks metadata for verification
5. **Transparent** - Shows you when data was updated

## Troubleshooting 🔧

### If updates aren't working:

1. **Check internet connection**
   ```bash
   ping cckpapi.worldbank.org
   ```

2. **Test manual fetch**
   ```bash
   python climate.py
   ```

3. **Check log file** (if using batch scheduler)
   ```bash
   type update_log.txt
   ```

4. **Force update**
   Edit `climate.py` main() and set `force=True`:
   ```python
   updated = auto_update_data(api_url, data_file, force=True)
   ```

## Performance Notes ⚡

- **First run**: Downloads full dataset (~2-3 seconds)
- **Subsequent runs**: Checks for updates (~1 second if up-to-date)
- **Update frequency**: Check as often as you like (script is efficient)

## Best Practices 📋

1. **Don't over-fetch** - Daily or weekly checks are usually sufficient
2. **Keep backups** - The old data file is replaced on update
3. **Monitor logs** - Check scheduler logs occasionally
4. **Test schedule** - Run scheduler manually first to verify it works

---

**Your data will now stay synchronized with the World Bank API automatically!** 🎉
