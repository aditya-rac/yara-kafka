from kafka import KafkaProducer

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'real-network-traffic'

# Inject Euler Virus (EICAR string) once in the data stream
def inject_euler_virus():
    eicar_virus_data = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    print("Injecting EICAR test virus into stream...")
    producer.send(topic_name, value=eicar_virus_data.encode('utf-8'))
    producer.flush()

if __name__ == "__main__":
    inject_euler_virus()
