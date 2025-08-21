# 🎨 Atlas: The Joy of Painting API

Atlas: The Joy of Painting API is a backend project that makes episodes of Bob Ross’ *The Joy of Painting* accessible through a structured database and API.  
Users can filter episodes by **broadcast month, subject matter, and color palette**, making it easy to explore Bob Ross’ work programmatically.

---

## 👨‍💻 About the Developer
Hi, I’m Tyler — a full-stack developer and USMC veteran currently studying at **Atlas School**.  
This project allowed me to bring together my skills in **ETL, databases, and API development** while working with a dataset I enjoyed.  

- [LinkedIn](https://www.linkedin.com/in/tylerwhitchurch)
---

## ✨ Features
- RESTful API built with **Flask + PostgreSQL**  
- Filter episodes by:  
  - 🎬 Broadcast month  
  - 🎨 Color palette  
  - 🌲 Subject matter (mountains, lakes, cabins, etc.)  
- Normalized PostgreSQL schema with multiple joined tables  
- Local development setup with Docker  

---

## 🚧 Future Features
- Full-text search across episode descriptions  
- Deploy API publicly with authentication  
- Front-end client for searching + displaying episodes  
- GraphQL support for more flexible queries  

---

## 📖 Project Story
This project started as an **ETL exercise** — I had three messy datasets with inconsistent formats.  
The challenge was to **normalize them into a single relational database** while keeping the relationships clear (episodes ↔ subjects ↔ colors).  

After building the schema, I created an API layer to expose the data in a user-friendly way.  
The goal was to make it easy for fans of Bob Ross (and developers) to query the episodes without digging through raw data.

---

## ⚡ Challenges & Lessons Learned
- **ETL complexity**: Parsing and cleaning three different datasets taught me the importance of consistent data types and schema design.  
- **Database design**: Choosing primary/foreign keys to handle many-to-many relationships was tricky but rewarding.  
- **API filtering**: Designing endpoints flexible enough to allow combined filters (month + subject + color) required careful query building.  

---

## 🛠 Tools & Technologies
- Python 3  
- Flask (API layer)  
- PostgreSQL (database)  
- SQLAlchemy (ORM)  
- Docker & Docker Compose  

---
