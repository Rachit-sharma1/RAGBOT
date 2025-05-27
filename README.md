# 🧠 RagBot — Personalized AI Assistant with Google SSO

**RagBot** is a document-grounded chatbot powered by Retrieval-Augmented Generation (RAG), built with Streamlit and secured using Google Single Sign-On (SSO) via Descope. It allows users to upload documents, ask questions, and receive accurate, context-aware responses—while ensuring all data and history remain user-specific and private.

---

## 🚀 Features

- 🔐 **Secure Authentication** via Google SSO (Descope)
- 📂 **User-Specific File Uploads** and isolated vector embeddings
- 🧠 **RAG-Based QA System** over uploaded PDFs
- 💬 **Personalized Chat History** persisted per user
- 🌍 **Public Deployment** on any cloud-based Virtual Machine

---

## 🗂️ Project Structure

```text
RagBot/
├── Authentication/            # Handles Descope SSO logic
├── chroma_store/              # Per-user vector DB
├── modules/                   # Core logic: ingestion, embedding, QA
├── index7.py                  # Main Streamlit app
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ☁️ Cloud Deployment Guide

You can deploy RagBot on any public cloud VM (e.g., AWS EC2, Azure VM, GCP Compute Engine).

### 1. 🛠️ Provision a VM

- Choose Ubuntu 22.04 (recommended)
- Open the following ports:
  - `80` or `8501` (for Streamlit)
  - `22` (for SSH access)

### 2. 🔧 Install System Dependencies

```bash
sudo apt update
sudo apt install python3-pip git
pip install virtualenv
```

### 3. 📦 Set Up the Project

```bash
git clone https://github.com/your-username/ragbot.git
cd ragbot/RagBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. ⚙️ Configure Environment Variables

Create a `.env` file or export securely:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
DESCOPRE_PROJECT_ID=your_descope_project_id
```

---

## 🔐 How Personalization Works

- Upon Google SSO login, users are identified via email or a UUID.
- Uploaded documents are stored in:
  ```
  chroma_store/<user_id>/
  ```
- Embeddings are indexed per user and queried independently.
- Chat history is stored in:
  ```
  chat_history_<user_id>.json
  ```
- This ensures **only the authenticated user can access their data and chats**.

---

## 🚦 Run the Application

```bash
streamlit run index7.py --server.port 80 --server.enableCORS false
```

> ✅ Ensure port 80 is open on your VM’s firewall or security group.

---

## 🌍 Accessing the Portal

Visit:  
```http
http://<your-vm-public-ip>/
```

Sign in with your Google account and start interacting with your personal AI assistant.

---

## 🧪 Sample Workflow

1. ✅ Log in with Google SSO  
2. 📤 Upload your PDF files  
3. 💬 Ask questions to the bot  
4. 🧠 Get answers grounded in your own documents  
5. 🔁 Resume conversations with retained context

---

## 📌 Roadmap & Enhancements

- [ ] Docker support for containerized deployment  
- [ ] Firebase/PostgreSQL for scalable chat history  
- [ ] Admin dashboard for usage monitoring  
- [ ] CI/CD integration for automated deployments

---

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/)  
- [Descope](https://www.descope.com/)  
- [FAISS / ChromaDB / LangChain / LlamaIndex]  
- [Google OAuth 2.0]

---

> 📫 Need help customizing or scaling this project? Feel free to raise an issue or open a pull request.
