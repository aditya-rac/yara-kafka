import os
import smtplib
from email.mime.text import MIMEText
from kafka import KafkaConsumer
import yara
import time

# Email configuration (credentials are loaded from environment variables)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT_SSL = 465  # Use SSL for encryption

# Ensure that the environment variables are correctly loaded
if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAIL:
    print("Error: One or more environment variables (SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL) are missing.")
    exit(1)

# Initialize Kafka Consumer
topic_name = 'real-network-traffic'

# YARA rule initialization
def initialize_rules():
    try:
        rules = yara.compile(filepath='malware_detection_rules.yar')
        print("Yara rules successfully compiled.")
        return rules
    except yara.YaraError as e:
        print(f"Failed to compile Yara rules: {e}")
        exit(1)

# Send an email notification
def send_email_alert(detected_malware):
    try:
        print(f"Attempting to send email from {SENDER_EMAIL} to {RECIPIENT_EMAIL}...")
        
        # Create the email content
        msg = MIMEText(f"Malware detected: {detected_malware}")
        msg["Subject"] = "Malware Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL

        # Connect to the SMTP server over SSL
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT_SSL) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Consume messages from Kafka and apply YARA rules to detect malware
def consume_and_scan_network_traffic(rules):
    consumer = KafkaConsumer(topic_name, bootstrap_servers='localhost:9092', auto_offset_reset='earliest', group_id='yara-scanner')

    for message in consumer:
        data_segment = message.value.decode('utf-8')
        print(f"Consuming from Kafka: {data_segment}")

        # Apply YARA rule to detect malware
        matches = rules.match(data=data_segment)
        if matches:
            print(f"Malware detected in the network data!")
            for match in matches:
                print(f"Matched rule: {match.rule}, at offsets: {match.strings}")
            print("Pausing the stream for 2 minutes due to detected malware...")
            send_email_alert(matches[0].rule)  # Send notification about the detected malware
            time.sleep(120)  # Pause for 2 minutes
        else:
            print("No malware detected in this packet.")

# Main function
def main():
    rules = initialize_rules()

    # Consume from Kafka and apply YARA rules
    consume_and_scan_network_traffic(rules)

if __name__ == "__main__":
    main()
