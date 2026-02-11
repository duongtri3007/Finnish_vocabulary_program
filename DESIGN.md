# [Project Title] - Group Design Document

**Team Members:** [SON NGHIEM], [TRI DUONG], [KHOI PHAM], [HOANG TRUNG QUAN PHAN]  
**Date:** [6/2/2026]  
**Version:** 1.0

---

## 1. Project Overview
We are building a Finnish learning application for people who wants to learn Finnish vocabulary. 
We think the problem is creating a application that can attract people want to use it every day.

## 2. Goals & Objectives
*What are the specific things our program must accomplish to be considered "finished"?*
It can save words, load words, give user multiple options to learn, track user's learning and run without erorrs. 

* **Core Goal:** [To create a functional Finnish vocabulary learning application that allows users to learn.]
* **Secondary Goal:** [We will include a high-score system that saves to a file.]

## 3. The User Journey
*How will a person interact with our code?*
* **The Experience:** [First, we will greet the user. Then, we will present them with a menu of options. Based on their choice, we will create a learning enviromentt for user such as topic-based vocabulary learning or users can create their own vocabulary list and add examples. Additionally we provide testing mode and review saved words mode so that they can review and practice with those words. Users also have their own learning progress track, the program will notify them based on their daily learning frequency.]
* **Inputs:** [We will accept keyboard strings for navigation and integers for menu selection.]

## 4. Program Logic (Step-by-Step)
*Describe the path our code takes from start to finish. Use a numbered list to show the sequence of events.*

1. **Initialization:** [We load saved vocabulary data, import our modules, and set up global variables.]
2. **Input Phase:** [The user selects a menu option using integers, and we can accept keyboard strings for navigation.]
3. **Processing Phase:** [Based on the user's choice, we run the appropriate module.]
4. **Output Phase:** [The program show result such as correct or incorrect answers, updated scores, new words and progress statistics.]
5. **Loop/Cleanup:** [After completeing an activity, we ask the user if they want to learn again or go out.]

## 5. Team Responsibility Breakdown
*How are we dividing the work? Each member should have a primary area of focus.*
* **HOANG TRUNG QUAN PHAN:** [Lead on Data Storage and File I/O.]
* **KHOI PHAM:** [User Interface and Input Validation.]
* **SON NGHIEM:** [Core Calculation Logic.]
* **TRI DUONG:** [Lead on Testing and Bug Fixing.]

## 6. Module & Function Breakdown
*List the main parts of our code and which team member is responsible for them.*
* **`main.py`**: The entry point that ties all our work together. (Handled by: [SON NGHIEM, TRI DUONG])
* **`logic_module.py`**: Functions for the "math" or "rules" of the project. (Handled by: [TRI DUONG, HOANG TRUNG QUAN PHAN])
* **`storage_module.py`**: Functions for reading/writing files. (Handled by: [KHOI PHAM])

## 7. Data Storage & Structures
*How are we keeping track of information?*
* **Variables/Collections:** [We will use a List to store the inventory and a Dictionary for learning words and a file to track learning progress.]
* **Persistence:** [We will save the team's progress in a file called `save_data.txt`.]

## 8. Development Timeline (Milestones)
*What is our plan for finishing on time?*
1. **Milestone 1:** [28/2] - We will have the basic project structure and main menu working.
2. **Milestone 2:** [25/3] - We will have our individual modules connected and talking to each other.
3. **Milestone 3:** [15/4] - We will finish testing for bugs and submit the final version.

---

### Team Checklist:
* **Consistency:** Are we all using the same variable naming style (user_choice, new_word, score_total)?
* **Communication:** How will we communicate? (Discord, Messenger, WhatsApp, Outlook)
* **Integration:** Have we tested if Member A's function actually works with Member B's function? (They can compete with each other.)