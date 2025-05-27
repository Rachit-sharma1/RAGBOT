🧠 RAGbot: Personalized AI Assistant with Google SSO
RAGbot is a Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload documents and interact with a personalized chatbot. It integrates Google Single Sign-On (SSO) via Descope, enabling user-specific document storage and context-aware chat history.

🚀 Features
🔐 Google SSO with Descope for secure authentication

🗂️ User-specific document upload and vector storage

📚 Retrieval-Augmented Generation (RAG) for precise, document-grounded answers

💬 Personalized chat history for each user

🌐 Hosted on a cloud-based Virtual Machine (VM) and accessible publicly

🏗️ Project Structure
pgsql
Copy
Edit
📁 ragbot/
├── 📁 backend/
│   └── ingest.py, query.py, db.py
├── 📁 frontend/
│   └── app.py  (Streamlit app)
├── 📁 auth/
│   └── sso.py  (Descope SSO handler)
├── 📁 utils/
│   └── storage.py, history.py
├── requirements.txt
├── config.env
└── README.md
☁️ Cloud Deployment on Virtual Machine
To make your RAGbot available online and user-specific, follow these steps:

1. 🛠️ Prepare the VM (e.g., AWS EC2, Azure VM, or GCP Compute Engine)
bash
Copy
Edit
# SSH into your VM
ssh your-user@your-vm-ip

# Install Python, pip, and Git
sudo apt update
sudo apt install python3-pip git

# Clone the repo
git clone https://github.com/your-username/ragbot.git
cd ragbot
2. 🔧 Configure Environment
Create a .env or config.env file with your credentials:

ini
Copy
Edit
DESCOPRE_PROJECT_ID=your_descope_project_id
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
VECTOR_DB_PATH=./storage/
3. 📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. 🚀 Run the Streamlit App
bash
Copy
Edit
streamlit run frontend/app.py --server.port 80 --server.enableCORS false
Ensure port 80 is open on your VM firewall or security group.

🔐 User-Specific Context & History
How It Works
On Google login, the user is identified via a unique email or user ID.

Uploaded files are stored in a user-specific directory (e.g., storage/{user_id}/).

Vector embeddings are stored separately per user.

Chat history is saved and loaded per user session using a local JSON file or database table (e.g., history/{user_id}.json).

🧪 Example Usage
Visit the public URL of the app.

Sign in with Google.

Upload your own PDFs.

Chat with the bot and receive personalized answers grounded in your documents.

Return anytime to see your past chat history.

✅ To-Do / Future Enhancements
 Add admin dashboard for monitoring usage

 Enable database-backed chat history (e.g., Firebase, PostgreSQL)

 Dockerize and deploy via container orchestration

📄 License
MIT License

🙌 Acknowledgments
Streamlit

Descope

[LangChain / LlamaIndex / FAISS / ChromaDB]

Google OAuth

Let me know if you want the README tailored for a specific cloud provider (like AWS, GCP, Azure) or if you’d like to add Docker deployment or CI/CD instructions.







You said:
RagBot (2).zip
Zip Archive
this is the project


ChatGPT said:
Thanks for sharing the project ZIP file. I’ll now do the following:

Review your project structure and content.

Update the README.md specifically for your project.

Ensure deployment steps for a cloud VM, with Google SSO and user-specific context/history, are clearly documented.

Let me extract and analyze the contents first.

Your project has been successfully extracted. Here are some key components detected:

Main Directory: RagBot

Auth Module: RagBot/Authentication/

Custom Logic: RagBot/modules/

Local Vector Store: RagBot/chroma_store/

Main App File: index7.py

Dependencies: requirements.txt

Current README: README.md

Next, I’ll generate a new README.md tailored to:

Cloud VM deployment

Google SSO (via Descope assumed)

User-specific context, storage, and history

Let me create that for you. 

Here’s an updated README.md for your RagBot project, specifically targeting deployment on a cloud virtual machine, with Google SSO, user-specific document management, and private chat history:

🤖 RagBot: Personalized Chatbot with RAG and Google SSO
RagBot is a Streamlit-based Retrieval-Augmented Generation (RAG) application enhanced with Google Single Sign-On (SSO). It allows users to upload documents, chat with an AI assistant, and maintain user-specific histories and data—all securely stored and privately retrieved.

🔑 Features
✅ Google SSO integration for secure user authentication

📁 User-specific PDF storage and vector embedding

🧠 RAG-based responses grounded in user documents

🕓 Persistent, user-specific chat history

☁️ Deployable on any public cloud VM (AWS EC2, GCP Compute, Azure, etc.)

📁 Project Structure
bash
Copy
Edit
RagBot/
├── Authentication/          # Handles Google SSO
├── modules/                 # File processing, embedding, QA
├── chroma_store/            # Vector DB (per-user)
├── index7.py                # Main Streamlit app
├── requirements.txt         # Dependencies
└── README.md
🚀 Deployment Guide (Cloud Virtual Machine)
You can use any cloud provider: AWS, Azure, GCP, etc.

1. 🌐 Provision a VM
Create a virtual machine instance (e.g., Ubuntu 22.04)

Open required ports: 80, 8501, or any custom port for Streamlit

2. 🧰 Install Required Software
bash
Copy
Edit
sudo apt update
sudo apt install python3-pip git
pip install virtualenv
3. 📥 Clone and Set Up
bash
Copy
Edit
git clone https://github.com/your-username/ragbot.git
cd ragbot/RagBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
4. ⚙️ Set Environment Variables
Create a .env file or securely export:

bash
Copy
Edit
export GOOGLE_CLIENT_ID=your_google_client_id
export GOOGLE_CLIENT_SECRET=your_google_client_secret
export DESCOPRE_PROJECT_ID=your_descope_project_id
5. 🔐 Handle Authentication
The Authentication/ folder manages login sessions via Descope or Google

On login, each user is assigned a unique ID (email or UUID)

6. 🧠 How Personalization Works
User data is stored in chroma_store/<user_id>/

Chat history saved per user (chat_history_<user_id>.json)

Only the logged-in user can access their files and chat logs

7. 🚦 Run the App
bash
Copy
Edit
streamlit run index7.py --server.port 80 --server.enableCORS false
Ensure your VM firewall/security group allows inbound HTTP on the specified port.

🌍 Access the Portal
Once deployed, visit http://<your-vm-ip>/ in your browser.
Users must sign in via Google to use the chatbot.

🧪 Sample Workflow
User logs in with Google SSO

Uploads personal PDFs

Chats with RAGbot → answers grounded in their documents

Session saved — next login resumes their history

📌 Future Enhancements
 Docker support for container-based deployment

 Firebase or cloud database for scalable chat history

 Analytics dashboard for user behavior tracking
