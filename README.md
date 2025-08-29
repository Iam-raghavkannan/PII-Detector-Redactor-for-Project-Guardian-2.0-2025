# PII-Detector-Redactor-for-Project-Guardian-2.0-2025
This repository is the submission for Real-time PII Defense (Project Guardian 2.0). It implements a PII Detector &amp; Redactor in Python to safeguard against sensitive data leakage in real-time streams.
Project Guardian 2.0 – Real-time PII Defense

This repository is the submission for Real-time PII Defense (Project Guardian 2.0).
It implements a PII Detector & Redactor in Python to safeguard against sensitive data leakage in real-time streams.

📖 Problem Statement

Flixkart’s recent audit revealed unmonitored API logs leaking PII (Personally Identifiable Information), leading to fraud incidents.
Our mission is to develop a system that can detect, redact, and protect PII in real time while ensuring:

Accuracy (minimize false positives)

Low latency (suitable for streaming data)

Scalability (deployable at network or app layer)

🚀 Features

✅ Detects Standalone PII:

Phone numbers (10 digits)

Aadhaar numbers (12 digits)

Passport numbers (alphanumeric, e.g., P1234567)

UPI IDs (user@upi, number@ybl, etc.)

✅ Detects Combinatorial PII:

Name + Email / Address / Device ID

Email + Address

IP Address + User Context

✅ Avoids False Positives:

Standalone first name/last name

Standalone city, state, or pin code

Order IDs, Transaction IDs, Product IDs

✅ Redaction & Masking:

Example: 9876543210 → 98XXXXXX10

Example: 1234 5678 9012 → 1234 XXXX XXXX 9012

Full sensitive fields replaced with [REDACTED_PII]

✅ Output:

Adds an is_pii column (True/False)

Outputs sanitized redacted_output_candidate_full_name.csv

📂 Repository Structure
📦 project-guardian-2.0  
 ┣ 📜 detector_full_candidate_name.py   # Main Python script  
 ┣ 📜 iscp_pii_dataset.csv              # Input dataset (sample)  
 ┣ 📜 redacted_output_candidate_full_name.csv  # Generated output  
 ┣ 📜 README.md                         # Documentation & Deployment Strategy  

⚡ Usage

Run the script with:

python3 detector_full_candidate_name.py iscp_pii_dataset.csv


Generated output → redacted_output_candidate_full_name.csv

🛡️ Deployment Strategy

To achieve real-time defense, the system can be deployed at different layers:

Sidecar Container (App Layer)

Runs alongside microservices, sanitizing logs before they leave the service.

Scalable, low-latency, language-agnostic.

Ingress / API Gateway Plugin (Network Layer)

Detects & redacts PII at request/response boundaries.

Prevents leaks before data enters internal systems.

DaemonSet (Cluster Level)

Runs on all nodes, intercepting logs centrally.

Good for Kubernetes environments.

Browser Extension / Internal Tool Filter

Ensures internal apps don’t render PII to employees.

Chosen Strategy:
➡ API Gateway Sidecar: Best trade-off between latency, scalability, and cost-effectiveness.
It prevents leaks before they spread into logs, databases, or monitoring systems.

👨‍💻 Author

Candidate: Raghav K
Submission for Real-time PII Defense Challenge
