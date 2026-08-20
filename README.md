# 1. Project vision

                    ┌──────────────────────────────┐
                    │       PERSONAL WEBSITE       │
                    │                              │
                    │       Aman Kumar Jha         │
                    │                              │
                    │ Portfolio • Knowledge • Blog │
                    └──────────────┬───────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
        PROFESSIONAL            CONTENT               AI
             │                     │                     │
       ┌─────┼─────┐         ┌─────┼─────┐          ┌────┴────┐
       │     │     │         │     │     │          │         │
     About Projects Work   Articles Notes Practice  RAG      LLM
       │     │     │         │     │     │          │         │
     Skills Experience     Explore Interests        └────┬────┘
       │     │     │                                     │
       └─────┼─────┘                                     ▼
             │                                      Ask Aman AI
             ▼
          CONTACT


## 2. High-level Architecture

                         INTERNET
                            │
                            ▼
                     ┌─────────────┐
                     │ Cloudflare  │
                     │ DNS / CDN   │
                     └──────┬──────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │     Next.js     │
                   │    Frontend     │
                   └────────┬────────┘
                            │
                     HTTPS / REST
                            │
                            ▼
                   ┌─────────────────┐
                   │     FastAPI     │
                   │     Backend     │
                   └────────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       PostgreSQL      Object Storage    AI Service
             │              │              │
             │              │              ▼
             │              │           OpenAI
             │              │              │
             ▼              │              │
          pgvector           │              │
             │              │              │
             └──────────────┴──────────────┘
                            │
                            ▼
                         RAG



## Contributor
         │
         ▼
    Sign in with GitHub
         │
         ▼
    Submit Article / Resource
         │
         ▼
    Draft
         │
         ▼
    Your Admin Dashboard
         │
         ├── Approve ───────► Published
         │
         ├── Request Changes
         │
         └── Reject
    
    
           ┌──────────────────┐
      │   Your Website   │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │    Contribute    │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Login with GitHub│
      └────────┬─────────┘
               │
               ▼
    ┌─────────────────────┐
    │ Contribution Form   │
    └─────────┬───────────┘
              │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
    GitHub Repo   Markdown      Project URL
    │             │             │
    └─────────────┼─────────────┘
              ▼
      ┌──────────────────┐
      │ Preview / Parser │
      └────────┬─────────┘
               ▼
      ┌──────────────────┐
      │ Pending Review   │
      └────────┬─────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
    APPROVE            REJECT
      │
      ▼
    /projects/xyz
