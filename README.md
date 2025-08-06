## COMPANY: CODTECH IT SOLUTIONS

# NAME: THOTI SUMAN

# INTERN ID:CT06DH1347

# DOMAIN: Cyber Security & Ethical Hacking

# DURATION: 6 WEEEKS

# MENTOR:NEELA SANTOSH
# 🛡️ File Integrity Checker

This project implements a **File Integrity Checker** that monitors changes in files by calculating and comparing cryptographic hash values. It helps ensure file integrity by detecting modifications, additions, or deletions in a given directory.

---

## ✅ Task Objective

- **Build a tool to monitor file changes** by:
  - Calculating cryptographic hash values for each file.
  - Storing these hashes as a baseline for comparison.
  - Comparing current hashes with baseline to detect:
    - Modified files
    - New files
    - Deleted files
- **Deliverable:** A Python script using `hashlib` for secure hashing.

---

## 🔑 Key Features

- Uses **SHA-256** (or SHA-512) for secure file hashing.
- Recursively scans all files in a specified directory.
- Compares against a baseline and reports:
  - **Modified** – Files whose content changed.
  - **New** – Files added since last check.
  - **Deleted** – Files removed since last check.
- Stores baseline in a **JSON file** for persistence.

---

## 🛠️ Technologies Used

- **Python 3.7+**
- Libraries:
  - `hashlib` – For cryptographic hashing.
  - `os` – For directory traversal.
  - `json` – For saving and loading baseline hashes.

*(Optional for real-time monitoring: `watchdog`.)*

---

## 🚀 How to Run

1. Clone or download the project.
2. Open a terminal in the project folder.
3. Run the script in one of the following modes:

### Initialize Baseline
```bash
python file_integrity_checker.py init /path/to/monitor
````

### Check for Changes

```bash
python file_integrity_checker.py check /path/to/monitor
```

---

## 📂 Project Structure

```
.
├── file_integrity_checker.py    # Main script
├── baseline_hashes.json         # Stores hashes (created after init)
└── README.md
```

---

## 🧪 Example Output

```
Baseline initialized with 10 files.

Modified files:
 - /home/user/docs/report.txt

New files:
 - /home/user/docs/new_file.pdf

Deleted files:
 - /home/user/docs/old_data.csv
```

---

## ✅ Deliverable Summary

* **Language:** Python
* **Libraries:** hashlib, os, json
* **Purpose:** Detect file changes using hash comparison
* **Output:** Reports modified, new, and deleted files

---

## 📌 Notes

* This tool ensures **data integrity** by leveraging strong cryptographic hashes.
* Real-time monitoring can be added using `watchdog` for instant alerts.

---

## 📜 License

Open for educational use. Add a proper license if used in production.

```

---

Do you want me to **include the full Python script inside this README** as an example for documentation? Or keep it separate and only reference it?
```
