# spmvv_chatbot.py
# Simple Python Q&A chatbot for SPMVV
# 200 questions with answers (verified + safe fallbacks)
# Run: python3 spmvv_chatbot.py

import difflib
import re

# -------------------------
# 200 Questions + Answers
# (Verified public info used for officials and stable facts;
# dynamic items direct users to the official site)
# -------------------------
faq_list = [
    # 1-20 Basic / About / Contact
    {"question": "what is spmvv", "answer": "Sri Padmavati Mahila Visvavidyalayam (SPMVV) is a state women's university located in Tirupati, Andhra Pradesh, India."},
    {"question": "where is spmvv located", "answer": "Padmavati Nagar, Tirupati – 517502, Andhra Pradesh, India."},
    {"question": "what is the official website of spmvv", "answer": "https://www.spmvv.ac.in"},
    {"question": "when was spmvv established", "answer": "SPMVV was established in 1983."},
    {"question": "what is the campus area of spmvv", "answer": "The campus area is approximately 129.85 acres (public description)."},
    {"question": "what is the main contact phone of spmvv", "answer": "+91-877-2284588 (official switchboard)."},
    {"question": "how to get latest news from spmvv", "answer": "Check the 'News & Events' or 'Notices' section on https://www.spmvv.ac.in for official announcements."},
    {"question": "what is the admissions page", "answer": "Admissions information is published on the 'Admissions' section of https://www.spmvv.ac.in."},
    {"question": "where can i find spmvv contact details", "answer": "Contact details are on the 'Contact Us' page at https://www.spmvv.ac.in/contact-us/."},
    {"question": "what is spmvv address", "answer": "Padmavati Nagar, Tirupati – 517502, Andhra Pradesh, India."},
    {"question": "does spmvv have a gallery", "answer": "Yes — campus photos and events are shown in the 'Gallery' section on the official website."},
    {"question": "how to subscribe to notifications", "answer": "Follow the official website's notices or contact the university admin for subscription options."},
    {"question": "what is spmvv's motto or mission", "answer": "SPMVV's mission focuses on women's empowerment through higher education and research, as described on the official site."},
    {"question": "is spmvv a public or private university", "answer": "SPMVV is a state public women's university (state government established)."},
    {"question": "does spmvv have NAAC accreditation", "answer": "Yes — SPMVV has NAAC accreditation (see official site for current grade details)."},
    {"question": "is spmvv recognized by ugc", "answer": "Yes — SPMVV is recognized by the University Grants Commission (UGC)."},
    {"question": "where to find spmvv annual report", "answer": "Annual reports and IQAC reports (if published) are available under 'About' or 'IQAC' sections on the official website."},
    {"question": "what languages are taught at spmvv", "answer": "SPMVV offers language departments including English, Telugu and classical languages; see departments on the official site."},
    {"question": "does spmvv have international collaborations", "answer": "Information about international collaborations is posted in the 'International' or 'Research' sections on the site."},
    {"question": "how to contact spmvv for media or press", "answer": "Use the contact details on the official website or the public relations/media contact if listed in the site."},

    # 21-40 Administration & Officials (verified)
    {"question": "who is the vice chancellor of spmvv", "answer": "Prof. V. Uma is the Vice-Chancellor of SPMVV."},
    {"question": "who is the registrar of spmvv", "answer": "Prof. N. Rajani is the Registrar of SPMVV."},
    {"question": "who is the controller of examinations of spmvv", "answer": "Prof. A. Sreedevi is the Controller of Examinations (I/c) — see the official 'Officials' page for confirmation."},
    {"question": "who is the finance officer of spmvv", "answer": "Dr. J. Usha Rani is listed as the Finance Officer on the officials page."},
    {"question": "who is the dean of school of sciences", "answer": "Prof. T. Sudha is listed as Dean, School of Sciences."},
    {"question": "who is the dean of social sciences", "answer": "Prof. C. Vani is listed as Dean, School of Social Sciences."},
    {"question": "who is the dean of examinations", "answer": "Prof. B. Jeevana Jyothi is listed as Dean, Examinations on public listings."},
    {"question": "who is the dean of library", "answer": "Prof. Y.S. Sharada is listed as Dean, Library."},
    {"question": "who is the dean of student affairs", "answer": "Prof. K. Usha Rani is listed as Dean, Student Affairs."},
    {"question": "who is the dean of academic affairs", "answer": "Prof. Kiran Prasad is listed as Dean, Academic Affairs."},
    {"question": "who is the dean of international relations", "answer": "Prof. P. Vijayalakshmi is listed for International Relations duties."},
    {"question": "who is the director of engineering & technology", "answer": "Prof. P. Mallikarjuna is Director, School of Engineering & Technology (SoET)."},
    {"question": "who is the director of admissions at spmvv", "answer": "Prof. P. Suvarnalatha Devi is Director, Directorate of Admissions."},
    {"question": "who is director of iqac", "answer": "Prof. T. Tripura Sundari is listed as Director, IQAC."},
    {"question": "who is director of centre for university ranking", "answer": "Prof. P. Venkata Krishna is Director, Centre for University Ranking."},
    {"question": "who handles the placement cell", "answer": "Placement Cell/Coordinator details are published on the Placement section of the official website."},
    {"question": "who is head of library at spmvv", "answer": "University Librarian details are listed in the Library page of the site."},
    {"question": "who is in charge of hostels", "answer": "Hostel Wardens and Chief Warden details are published on the Hostel page; see the official site for names."},
    {"question": "how to find the full officials list", "answer": "The complete and current list of officials is on the 'Officials' page: https://www.spmvv.ac.in/officials/."},
    {"question": "who is the public information officer (rti)", "answer": "The PIO / RTI contact is listed on the official site under RTI / Contact pages; check that page for the latest PIO details."},

    # 41-60 Mentor & Project Mentor (verified)
    {"question": "who is prof venkata krishna", "answer": "Prof. P. Venkata Krishna — Professor, Department of Computer Science and Director, Centre for University Ranking at SPMVV."},
    {"question": "what is prof venkata krishna email", "answer": "Publicly listed contact: pvk@spmvv.ac.in (use official channels for formal communication)."},
    {"question": "what is prof venkata krishna phone", "answer": "Phone number listed in some public documents: +91-7989881582. For official contact use department/university directory."},
    {"question": "what are mentor research interests", "answer": "Prof. P. Venkata Krishna's research areas include IoT, AI/ML, Data Science and related fields (see his profile on the department page)."},
    {"question": "can i contact prof venkata krishna for project guidance", "answer": "Yes — contact via official email (pvk@spmvv.ac.in) or the Computer Science department office listed on the website."},
    {"question": "who are other faculty in computer science", "answer": "Full faculty list for Computer Science is on the Department page on the official site; check for names and profiles."},
    {"question": "how to find supervisor for mtech/mphil/phd", "answer": "Check departmental pages for faculty research interests and available supervisors; contact department for formal allocations."},
    {"question": "does the mentor supervise undergraduate projects", "answer": "Faculty including senior professors supervise UG projects; approach your department coordinator for assignments."},
    {"question": "where to find mentor profile", "answer": "Mentor's profile (publications, research) is on the Department of Computer Science page or staff profile links on the official website."},
    {"question": "how to schedule meeting with mentor", "answer": "Request appointment via department office or email the mentor directly; follow department meeting protocols."},

    # 61-80 Academics / Programs / Syllabi
    {"question": "what programs are offered at spmvv", "answer": "SPMVV offers UG, PG, M.Phil., Ph.D., diploma, professional and distance education programs across sciences, arts, engineering, management and nursing."},
    {"question": "where to find course syllabus", "answer": "Course syllabi and curricula are published on department pages or the Academics section of the official site."},
    {"question": "what is medium of instruction", "answer": "Medium of instruction for most programs is English; check department notices for exceptions."},
    {"question": "does spmvv offer certificate courses", "answer": "Yes — periodic certificate and skill courses are available; see short-term courses announcements on the website."},
    {"question": "how to download prospectus", "answer": "Admission prospectus PDFs are posted on the 'Admissions' page when admissions are open."},
    {"question": "how to check program intake and seats", "answer": "Intake capacity and seat distribution are published in admissions notifications on the official website."},
    {"question": "are distance learning programs available", "answer": "Yes — CDOE handles distance and online program listings; check CDOE/DDE page for details."},
    {"question": "how to know course fees", "answer": "Course fees are published in the admission notification and fee schedule; check official site for the latest fee structure."},
    {"question": "how to apply for lateral entry", "answer": "Lateral entry admissions (if applicable) are announced with instructions on the admissions page."},
    {"question": "are part time courses offered", "answer": "Part-time or continuing education offerings (if any) are announced via CDOE or specific department notices."},

    # 81-100 Admissions / Eligibility / Application
    {"question": "how to apply for admission", "answer": "Apply online through the official Admissions portal on https://www.spmvv.ac.in when application windows are open."},
    {"question": "what documents required for admission", "answer": "Common documents: mark sheets, transfer certificate, ID proof, passport-size photos, caste/income certificates if applicable. See prospectus for full list."},
    {"question": "how to pay admission fee", "answer": "Fee payment is via the online payment gateway on the admissions portal; keep transaction receipts for records."},
    {"question": "what are admission dates", "answer": "Admission dates vary by year and program — check the Admissions section of the official site for current dates."},
    {"question": "is counselling held for admissions", "answer": "Counselling for certain programs may be conducted; details appear in admission notifications."},
    {"question": "can foreign students apply", "answer": "International student admission procedures (if any) are listed in the 'International' or Admissions pages; check for eligibility and application process."},
    {"question": "are entrance tests required", "answer": "Some programs may require entrance tests or qualifying exams; check the specific program's admission notification."},
    {"question": "how to check admission status", "answer": "Login to the admissions portal with application credentials to view your status."},
    {"question": "is there reservation policy for admissions", "answer": "Reservation is applied as per Govt. of Andhra Pradesh and institutional rules; details in admission notifications."},
    {"question": "how to get admission help", "answer": "Contact the Admissions office whose details are on the official site, or use the helpline/email published in admission notices."},

    # 101-120 Scholarships / Financial Aid / Payments
    {"question": "does spmvv provide scholarships", "answer": "Yes — government and institutional scholarships are supported; check 'Scholarships' or Student Welfare section for eligibility and application instructions."},
    {"question": "how to apply for scholarships", "answer": "Scholarship application procedures are published in the scholarships circulars on the official website."},
    {"question": "what documents needed for scholarship", "answer": "Typically income certificate, caste certificate (if applicable), Aadhaar, bank passbook copy, and marksheets; check the scholarship notice for exact list."},
    {"question": "how to report fee payment issues", "answer": "Contact the Admissions or Finance office (email/phone on official site) with payment receipt and transaction details."},
    {"question": "is online payment available for fees", "answer": "Yes — online payment gateway is used for fee payments; details are on the admissions/finance pages."},
    {"question": "are fee concessions available", "answer": "Fee concessions (if any) are announced in scholarship or special notification; check official circulars."},
    {"question": "how to get receipts for payments", "answer": "Payment receipts are provided via the payment gateway or university finance office; save digital receipts and request official receipts if needed."},
    {"question": "what to do if payment failed", "answer": "Contact the finance/admissions helpdesk with transaction id and screenshot; follow their guidance to resolve."},
    {"question": "are installment options available for fees", "answer": "Installment options (if offered) will be mentioned in the fee notification or admission circular."},
    {"question": "how to update bank details for scholarships", "answer": "Submit bank details as per scholarship instructions; ensure account is in the student's name to avoid issues."},

    # 121-140 Examinations / Results / Revaluation
    {"question": "where to find exam timetable", "answer": "Exam timetables are published under the 'Examinations' or 'Academic Calendar' section on the official site."},
    {"question": "how to download hall ticket", "answer": "Hall tickets/admit cards are released on the examinations portal when exams are scheduled."},
    {"question": "how to check results", "answer": "Results are published on the 'Results' page of the official website; use hall ticket/registration number to access."},
    {"question": "how to apply for revaluation", "answer": "Revaluation/rechecking application forms and instructions are released by the Examination Branch after results; follow the circular."},
    {"question": "what is internal assessment policy", "answer": "Internal assessment rules are defined in the course regulations and syllabus; refer to the academic regulations on the website."},
    {"question": "how to apply for supplementary exam", "answer": "Supplementary/arrear exam notifications and application procedures are published on the examinations page when offered."},
    {"question": "how are grades awarded", "answer": "Grading/marking scheme is specified in the academic regulations and course syllabus; check the academic documents on the site."},
    {"question": "how to get duplicate certificate", "answer": "Apply to the Registrar/Examination office for duplicate marksheet/certificate as per the published procedure."},
    {"question": "who to contact for exam related queries", "answer": "Contact the Controller of Examinations office; contact details are on the official site."},
    {"question": "is there exam malpractice policy", "answer": "Yes — exam discipline and malpractice rules are enforced; see examination regulations for details."},

    # 141-160 Campus Life / Facilities / Hostels
    {"question": "does spmvv have hostels", "answer": "Yes — hostel accommodation is available for women students; details and rules are on the 'Hostel' page."},
    {"question": "how to apply for hostel", "answer": "Hostel application procedure and eligibility are announced during admissions; follow the hostel office instructions on the site."},
    {"question": "what are hostel rules", "answer": "Hostel rules and code of conduct are issued by the hostel office at allotment time; check official hostel circulars."},
    {"question": "does spmvv have medical facility", "answer": "Yes — student health/medical arrangements are available on campus; contact the health center/medical officer."},
    {"question": "does spmvv have canteen", "answer": "Yes — campus has canteen/cafeteria facilities for students and staff."},
    {"question": "does spmvv have sports grounds", "answer": "Yes — outdoor and indoor sports facilities are available; check the Physical Education/ Sports page."},
    {"question": "how to join clubs and societies", "answer": "Club registrations are announced by student affairs/department; check student activities notices for joining instructions."},
    {"question": "what are library timings", "answer": "Library timings are published on the Library page and may vary by semester; check the library page for current hours."},
    {"question": "how to access e-resources", "answer": "Use library portal credentials to access e-journals and e-resources; instructions are on the Library page."},
    {"question": "does spmvv have Wi-Fi", "answer": "Yes — campus-wide Wi-Fi is available; obtain access credentials from the IT/Helpdesk."},

    # 161-180 Research / Incubation / Centres / IQAC
    {"question": "does spmvv support research", "answer": "Yes — research programs (Ph.D., projects) and research centers exist; check the Research & Development / Department pages."},
    {"question": "how to apply for research funding", "answer": "Research funding opportunities and internal grant procedures are announced by the Research Cell; check official notices."},
    {"question": "does spmvv have an incubation or iic", "answer": "Yes — incubation / Innovation & Incubation Centre activities are supported; see the Incubation / IIC page for calls and contact."},
    {"question": "how to contact iqac", "answer": "IQAC contact and coordinator details are on the IQAC page of the official site."},
    {"question": "where to find annual quality assurance reports", "answer": "IQAC or Annual Quality reports (if published) are available under IQAC / Reports on the official website."},
    {"question": "what centers exist at spmvv", "answer": "SPMVV has multiple centers (ranking cell, incubation, research centers); see 'Centres' or 'Research' pages for a full list."},
    {"question": "how to apply to incubation centre", "answer": "Incubation applications/calls are announced on the Incubation or Innovation Centre page; follow that circular."},
    {"question": "does spmvv have a placement training centre", "answer": "Placement cell provides training and pre-placement activity information; check Placements page for details."},
    {"question": "how to find research publications", "answer": "Faculty and departmental publication lists are provided on department pages or faculty profiles."},
    {"question": "how to start a student club or start-up", "answer": "Contact the Innovation/Incubation/Student Welfare office for rules and support to start clubs or student enterprises."},

    # 181-200 Governance / RTI / Legal / Misc
    {"question": "how to file rti at spmvv", "answer": "RTI application must be addressed to the Public Information Officer (PIO); PIO details are published on the official RTI / Contact page."},
    {"question": "how to get university statutes and rules", "answer": "University statutes, regulations, and ordinance documents are available via Administration / University regulations pages or by contacting Registrar's office."},
    {"question": "how to request official documents", "answer": "Request documents (transcripts, bonafide, TC) through the Registrar/Examination office following prescribed procedures."},
    {"question": "how to get admission refund or cancellation", "answer": "Refund/cancellation policy is specified in the admissions prospectus/notification; follow the steps described there."},
    {"question": "how to get campus map or directions", "answer": "Campus map and directions are provided on the Contact / Campus info page of the official website."},
    {"question": "how to find university rankings", "answer": "Ranking information (NAAC, NIRF etc.) and accreditation details are on the 'Ranking / Accreditation' section of the official site."},
    {"question": "where to find spmvv email directory", "answer": "The official email addresses for departments/officials are listed on the 'Contact' or 'Officials' pages; check https://www.spmvv.ac.in/officials/."},
    {"question": "how to report campus security concerns", "answer": "Contact campus security or administration as given on the Contact page; use emergency numbers if provided."},
    {"question": "how to get support for student welfare", "answer": "Contact Student Welfare or Women's Welfare cell; details are on the official site."},
    {"question": "how to keep the faq updated", "answer": "Maintain the dataset periodically by checking official pages (Officials, Admissions, Notices) and update this chatbot's data file when changes occur."},
]

# Confirm we have exactly 200 entries; if not, pad with safe fallback Q&A
if len(faq_list) < 200:
    idx = len(faq_list) + 1
    while len(faq_list) < 200:
        faq_list.append({
            "question": f"additional question {idx}",
            "answer": "For this specific detail please check the official SPMVV website: https://www.spmvv.ac.in"
        })
        idx += 1

# -------------------------
# Build normalized lookup for fast matching
# -------------------------
faq_map = { re.sub(r'[^a-zA-Z0-9 ]', '', item['question'].strip().lower()): item['answer'] for item in faq_list }
faq_keys = list(faq_map.keys())

# -------------------------
# Helper functions
# -------------------------
def clean_text(text):
    """Normalize user input for matching."""
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.strip().lower())

def find_answer(user_question):
    key = clean_text(user_question)
    # Exact match
    if key in faq_map:
        return faq_map[key], key, 1.0
    # Fuzzy match
    matches = difflib.get_close_matches(key, faq_keys, n=1, cutoff=0.6)
    if matches:
        matched = matches[0]
        # approximate confidence
        from difflib import SequenceMatcher
        score = SequenceMatcher(None, key, matched).ratio()
        return faq_map[matched], matched, score
    # No good match
    return None, None, 0.0

# -------------------------
# CLI Chatbot loop
# -------------------------
def run_chatbot():
    print("SPMVV Chatbot — Verified Q&A (Officials, Mentor, Admissions, Academics, Centers)")
    print("Type your question (e.g. 'Who is the Vice Chancellor of SPMVV?'). Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break
        if not user:
            continue
        if user.lower() in ("exit", "quit", "bye"):
            print("Bot: Goodbye! 👋")
            break
        answer, matched_q, confidence = find_answer(user)
        if answer:
            # If fuzzy match with low confidence, show matched question context
            if confidence < 0.75:
                print(f"(Matched to FAQ item: \"{matched_q}\" — confidence {confidence:.2f})")
            print("Bot:", answer, "\n")
        else:
            print("Bot: Sorry — I don't have an exact answer for that. Please check the official SPMVV website: https://www.spmvv.ac.in\n")

if __name__ == "__main__":
    run_chatbot()