import subprocess
from kafka import KafkaProducer
import time

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'real-network-traffic'

# Capture live network traffic using tcpdump and stream to Kafka
def capture_network_traffic():
    command = ['sudo', 'tcpdump', '-i', 'any', '-l']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Stream each captured network packet into Kafka
    for line in iter(process.stdout.readline, b''):
        try:
            packet_data = line.decode('utf-8')
            print(f"Captured packet: {packet_data}")

            # Stream packet data to Kafka
            producer.send(topic_name, value=line)
            print(f"Sent to Kafka: {packet_data.strip()}")

            # Sleep to simulate real-time streaming
            time.sleep(1)

        except Exception as e:
            print(f"Error sending data to Kafka: {str(e)}")

# Main function
def main():
    # Start capturing network traffic and sending to Kafka
    capture_network_traffic()

    # Close Kafka producer
    producer.flush()
    producer.close()

if __name__ == "__main__":
    main()
