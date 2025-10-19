# README – CIE205 Projects (Data Structures & Algorithms)
## Simulation-Based Project Collection (Fall 2025)

### 1. Introduction
This repository contains four comprehensive **simulation-based programming projects** designed for the CIE205 *Data Structures and Algorithms* course.  
Each project focuses on applying core data structure concepts — queues, priority queues, graphs, and file I/O — within realistic operational systems.  

Students are expected to implement these systems using object-oriented programming principles, modular design, and event-driven logic.  
All projects share a consistent format, enabling parallel study and comparative understanding of different scheduling and resource allocation models.

---

### 2. Project List

| # | Project Title | Domain | Core Concepts | Link |
|---|----------------|---------|----------------|------|
| 1 | **Ambulance Management System** | Healthcare / Emergency Dispatch | Priority Queues, Event Simulation, File I/O | [CIE205_Ambulance_Management_System.md](./CIE205_Ambulance_Management_System.md) |
| 2 | **Restaurant Management System** | Food Service / Scheduling | Priority Queues, Queues, Inheritance, Simulation | [CIE205_Restaurant_Management_System.md](./CIE205_Restaurant_Management_System.md) |
| 3 | **Warehouse & Delivery System** | Logistics / Supply Chain | Hash Maps, Priority Queues, Scheduling | [CIE205_Warehouse_Delivery_System.md](./CIE205_Warehouse_Delivery_System.md) |
| 4 | **University Course Enrollment System** | Education / Scheduling | Graphs, Queues, Sets, Event Simulation | [CIE205_University_Course_Enrollment_System.md](./CIE205_University_Course_Enrollment_System.md) |

---

### 3. Project Comparison

| Concept | Ambulance | Restaurant | Warehouse | Enrollment |
|----------|------------|-------------|-------------|-------------|
| **Primary DS** | PQ + Queues | PQ + Queues | HashMap + PQ | Graph + PQ |
| **Scheduling Basis** | Patient severity | Order priority | Route & capacity | Time & prerequisites |
| **Entities** | Hospitals, Cars, Patients | Chefs, Orders | Warehouses, Vehicles, Items | Students, Courses, Sections |
| **Simulation Mode** | Timesteps (Discrete) | Timesteps (Discrete) | Timesteps (Discrete) | Timesteps (Discrete) |
| **Events** | Request, Cancel | Arrival, Cancel, Promote | Order, Restock, Cancel | Enroll, Drop, Swap |
| **I/O** | Structured Text Files | Structured Text Files | Structured Text Files | Structured Text Files |
| **Performance Metrics** | Waiting time, utilization | Wait/Service time | On-time delivery, utilization | Seat utilization, fairness |
| **Learning Focus** | Priority-driven resource allocation | Scheduling and queuing | Inventory and logistics management | Constraint-based scheduling |

---

### 4. General Implementation Notes
- Use **object-oriented design** with encapsulated classes.  
- Maintain clear **data ownership and pointers** (avoid duplication).  
- Prefer **standard template containers** (e.g., STL in C++ or Python built-ins).  
- Simulations must run deterministically based on input files.  
- Provide **interactive** and **silent** modes for visualization and batch testing.  
- Implement consistent **logging and reporting** formats for outputs.  
- Ensure modular separation between simulation logic, data models, and I/O handling.

---

### 5. Recommended Tools & Technologies
- **Language:** C++ / Python (prefer OOP approach).  
- **Environment:** Visual Studio Code, CLion, or Jupyter Notebook.  
- **Version Control:** Git & GitHub for submissions and revisions.  
- **Documentation:** Markdown and docstrings for readability.  
- **Visualization (optional):** Matplotlib, Graphviz, or simple text logs.

---

### 6. Learning Outcomes
By completing all four projects, students will:
1. Master **event-driven simulation** as an algorithmic modeling technique.  
2. Learn to select appropriate **data structures** for real-world constraints.  
3. Apply **priority scheduling** and **resource allocation** strategies.  
4. Gain proficiency in **file-based system design** and output analysis.  
5. Strengthen understanding of **graphs, queues, and sets** through practical use.  
6. Build transferable **software engineering skills** — modularity, testing, and code reuse.  

---

### 7. Acknowledgments
Prepared under the **CIE205 – Data Structures & Algorithms** course,  
Faculty of Computers & Information Sciences, Mansoura University.  
These projects aim to bridge theoretical learning with applied problem-solving and simulation modeling.

---

**Prepared by:**  
*Dr. Haitham – Associate Professor of Information Systems*  
*Faculty of Computers & Information Sciences, Mansoura University*  
