## INTERVIEW PREP ASSISTANT BE

#### OVERVIEW
This repository contains the backend code for an Interview Preparation Assistant. The assistant is designed to help users prepare for job interviews by providing various functionalities such as generating questions, giving feedback, and more.

#### ARCHITECTURE
The backend is built using FastAPI and consists of several agents, each responsible for a specific task. The agents communicate with each other to provide a seamless experience for the user.

![Architecture](./docs/architecture.svg)


##### MULTI-AGENT SYSTEM
The system is composed of the following agents:
- **Generate Questions Agents**: These agents generates questions/sample answers based on CV + JD + Role of the candidate.

  ![Generate Questions Agents](./docs/generate-questions-agents.svg)

- **Interview Feedback Agents**: These agents provides feedback based on the interview recording.

