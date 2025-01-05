# 🛠 Overview  
This repository demonstrates a microservices architecture composed of the following components:  

- **Client**: Front-end or external system interacting with the backend services.  
- **Auth Service**: Manages user authentication and authorization, utilizing PostgreSQL for data storage.  
- **Tracking Service**: Handles event tracking and monitoring, storing data in MongoDB.  
- **Message Broker**: Facilitates asynchronous communication between services, ensuring reliable message delivery.  

## ⚙️ Architecture Overview  
![image](https://github.com/user-attachments/assets/a2a29004-00ea-408d-a2e1-640251740225)


### Components:  
#### **Client**:  
- Interacts with the Auth Service for authentication and data requests.  
- Receives data and updates in response to user actions.  

#### **Auth Service**:  
- **Handles**:  
  - User registration and login.  
  - Token generation (e.g., JWT for secure communication).  
- **Storage**:  
  - Stores user data securely in PostgreSQL.  

#### **Tracking Service**:  
- Consumes events sent by the Auth Service via the Message Broker.  
- Persists tracking data in MongoDB for analytics and monitoring.  

#### **Message Broker**:  
- Acts as a communication layer between services (e.g., RabbitMQ or Kafka).  
- Ensures reliable message delivery and decouples service dependencies.  

## 🖥 Tech Stack  
- **Programming Language**: Python 3.12  
- **Framework**: FastAPI for building REST APIs.  
- **Databases**:  
  - **PostgreSQL**: User data storage for the Auth Service.  
  - **MongoDB**: Event and tracking data storage for the Tracking Service.  
- **Message Broker**: Kafka for asynchronous communication, integrated with FastStream for high-level streaming abstractions.  
- **Containerization**: Docker for packaging and deployment.  
- **Orchestration**: Docker Compose (optionally Kubernetes for scaling).  
