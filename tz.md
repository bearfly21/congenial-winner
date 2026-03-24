# OMUZ PLATFORM — HACKATHON

## 1. Project Overview
**Project Name:** Omuz  
**Type:** Online Learning Platform (Mobile-first)  
**Goal:** Build a modern education platform that teaches:  
* IT Foundations  
* AI Foundations  
* Marketing  
* Design  
* Modern digital skills  
* School Subjects  

**Reference Platforms:** 
* Ustoz AI (Uzbekistan) - https://www.ustoz.ai/en  
* Ibrat Farzandlari - https://ibratfarzandlari.uz/  

**Hackathon Constraints:** 
* Duration: 1 week  
* Team size: max 2 people  
* Focus: AI capability + product thinking + execution speed  

---

## 2. Core Concept
The platform should behave like a startup-level product, not a simple LMS.  
**Key principles:** 
* Mobile-first UX  
* Fast onboarding (OTP only)  
* Gamified learning  
* Clear learning paths → job-ready skills  
* Simple but scalable architecture  

---

## 3. User Roles

### 3.1 Student (Main User)
* Register/login via OTP  
* Browse courses  
* Watch lessons  
* Pass tests  
* Earn points/badges  
* Build certificate

### 3.2 Admin (optional for hackathon)
* Manage courses  
* Manage discounts  
* View analytics  

---

## 4. Authentication
**OTP Login Only** 
* Phone number input  
* Name and Surname  
* OTP verification  
* No password system  

**Flow:** 
1. Enter phone  
2. Receive OTP  
3. Verify → login  

---

## 5. Main Features

### 5.1 Home Page
* Course recommendations  
* Popular courses  
* Continue learning  
* Promotions / discounts  

### 5.2 Courses
**Categories:** 
1. **Occupations** 
* SMM  
* Frontend  
* Backend  
* Designer  
* AI specialist  
2. **School Subjects** 
* Math  
* English  
* Physics  

**Course Structure:** Course → Modules → Lessons  
**Each lesson:** 
* Video (YouTube or external)  
* Description  
* Attachments (optional)  

### 5.3 Video Integration
* Use: 
- YouTube embed 
- external video links  
* No need to store videos on server  

### 5.4 Tests / Quizzes
* Multiple choice questions  
* Instant result  
* Score calculation  
* **Optional:** 
- Unlock next lesson only after passing test  

### 5.5 Gamification
**Core mechanic:** 
* Points (XP)  
* Levels  
* Badges  

**Actions:** 
* Complete lesson → +10 XP  
* Pass test → +20 XP  
* Daily streak → bonus  

**Leaderboard:** 
* Top students  

### 5.6 certificate Builder
User can generate a simple certificate.  
**Fields:** 
* Name  
* Skills  
* Completed courses  
* Achievements  
**Output:** 
* Download PDF  

### 5.7 Notifications
**Types:** 
* Course updates  
* Discounts  
* Reminders  
* Push or in-app notifications  

### 5.8 Discounts System
**Example: Ramadan Discount** 
* 20% OFF  
* Date: 1–28 March  
**Logic:** * Applied automatically during period  

---

## 6. Reference Analysis

**Ustoz AI (Insights)** * Course-based learning  
* Video lessons  
* Phone login  
* Tests  
* Certificates  
* Simple UI  
* **Key takeaway:** Focus on speed + accessibility  

**Ibrat Farzandlari (Insights)** 
* Gamification  
* Quizzes  
* Interactive learning  
* Engagement focus  
* **Key takeaway:** Strong engagement mechanics  

---

## 7. AI Usage (IMPORTANT)
Teams must use AI for:  
* Code generation  
* UI creation  
* Architecture decisions  
* Debugging  

**Evaluation includes:** 
* How well they use AI  
* Prompt quality  
* Validation of AI outputs  

---

## 8. Suggested Architecture
* **Frontend:** React Native / Flutter  
* **Backend:** .NET / Node.js / Python  
* **Database:** PostgreSQL / Firebase  
* **Auth:** OTP service (mock allowed)  

---

## 10. User Flow
1. Login (OTP)  
2. Select course  
3. Watch lesson  
4. Pass test  
5. Earn XP  
6. Build certificate  

---

## 11. Evaluation Criteria
1. **Product Thinking:** UX quality, Feature completeness  
2. **Code Quality:** Clean architecture, Maintainability  
3. **AI Usage:** Prompt quality, Efficiency  
4. **Speed:** Delivered features in 1 week  
5. **Teamwork:** Collaboration (2 people)  

---

## 13. Deliverables
Each team must provide:  
* Working app (mobile or web)  
* Demo  
* Code repository  
* Short explanation  

---

## 14. Bonus Features (Optional)
* AI mentor/chatbot  
* Course recommendations  
* Progress analytics