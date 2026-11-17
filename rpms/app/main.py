"""
RPMS - Recruitment & Placement Management System
Main Console Application
"""
import sys
from datetime import date, datetime

from rpms.model.candidate import Candidate
from rpms.model.company import Company
from rpms.model.job import Job
from rpms.model.interview import Interview, InterviewFeedback
from rpms.model.offer import Offer
from rpms.model.placement import Placement

from rpms.service.candidate_service import CandidateService
from rpms.service.company_service import CompanyService
from rpms.service.job_service import JobService
from rpms.service.application_service import ApplicationService
from rpms.service.eligibility_service import EligibilityService
from rpms.service.interview_service import InterviewService
from rpms.service.offer_service import OfferService
from rpms.service.placement_service import PlacementService
from rpms.service.report_service import ReportService
from rpms.service.activity_log_service import ActivityLogService
from rpms.exception.exceptions import RPMSBaseException


class RPMSConsoleApp:

    def __init__(self):
        self.candidate_service = CandidateService()
        self.company_service = CompanyService()
        self.job_service = JobService()
        self.eligibility_service = EligibilityService()
        self.application_service = ApplicationService(
            eligibility_service=self.eligibility_service
        )
        self.interview_service = InterviewService()
        self.offer_service = OfferService()
        self.placement_service = PlacementService()
        self.report_service = ReportService()
        self.log_service = ActivityLogService()

    def run(self):
        print("\n==========================================")
        print("  RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM")
        print("==========================================")
        print("  Connected to database 'recruitment_portal'")

        while True:
            self._print_main_menu()
            choice = input("\nEnter Choice (1-9): ").strip()

            if choice == "1":
                self._menu_candidates()
            elif choice == "2":
                self._menu_companies()
            elif choice == "3":
                self._menu_jobs()
            elif choice == "4":
                self._menu_applications()
            elif choice == "5":
                self._menu_interviews()
            elif choice == "6":
                self._menu_offers()
            elif choice == "7":
                self._menu_placements()
            elif choice == "8":
                self._menu_reports()
            elif choice == "9":
                print("\nThank you for using RPMS. Goodbye!\n")
                self.log_service.log("Session ended by user.")
                break
            else:
                print("[!] Invalid option. Please enter a number between 1 and 9.")

    def _print_main_menu(self):
        print("\n" + "=" * 42)
        print("      RECRUITMENT & PLACEMENT SYSTEM")
        print("=" * 42)
        print(" 1. Candidates")
        print(" 2. Companies")
        print(" 3. Jobs")
        print(" 4. Applications")
        print(" 5. Interviews")
        print(" 6. Offers")
        print(" 7. Placements")
        print(" 8. Reports")
        print(" 9. Exit")
        print("=" * 42)

    # -------------------------------------------------------------
    # 1. CANDIDATES
    # -------------------------------------------------------------
    def _menu_candidates(self):
        while True:
            print("\n--- [CANDIDATE MANAGEMENT] ---")
            print(" 1. View All Candidates")
            print(" 2. Add New Candidate")
            print(" 3. Search Candidate by Name")
            print(" 4. Search Candidate by Technology")
            print(" 5. Deactivate Candidate Profile")
            print(" 6. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                candidates = self.candidate_service.get_all_candidates()
                print(f"\n--- Total Candidates: {len(candidates)} ---")
                for cand in candidates:
                    print(cand)
            elif c == "2":
                try:
                    name = input("Full Name: ").strip()
                    email = input("Email: ").strip()
                    mobile = input("Mobile (10 digits): ").strip()
                    tech = input("Primary Technology (Java/Python/Testing/etc.): ").strip()
                    skills = input("Skills (comma-separated): ").strip()
                    pct = float(input("Degree Percentage (0-100): ").strip())
                    yr = int(input("Passing Year (e.g., 2025): ").strip())
                    backlogs = int(input("Active Backlogs count: ").strip())

                    cand = Candidate(
                        full_name=name,
                        email=email,
                        mobile=mobile,
                        primary_technology=tech,
                        skills=skills,
                        percentage=pct,
                        passing_year=yr,
                        backlog_count=backlogs,
                    )
                    cand_id = self.candidate_service.add_candidate(cand)
                    print(f"[✓] Candidate registered successfully! ID = {cand_id}")
                    self.log_service.log(f"Candidate Created: {name} (ID: {cand_id})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "3":
                name = input("Enter candidate name to search: ").strip()
                res = self.candidate_service.search_by_name(name)
                print(f"Found {len(res)} matching candidates:")
                for cand in res:
                    print(cand)
            elif c == "4":
                tech = input("Enter technology to search: ").strip()
                res = self.candidate_service.search_by_technology(tech)
                print(f"Found {len(res)} matching candidates:")
                for cand in res:
                    print(cand)
            elif c == "5":
                try:
                    cid = int(input("Enter Candidate ID to deactivate: ").strip())
                    if self.candidate_service.deactivate_candidate(cid):
                        print(f"[✓] Candidate #{cid} deactivated successfully.")
                        self.log_service.log(f"Candidate Deactivated: ID {cid}")
                    else:
                        print("[!] Update failed.")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "6":
                break

    # -------------------------------------------------------------
    # 2. COMPANIES
    # -------------------------------------------------------------
    def _menu_companies(self):
        while True:
            print("\n--- [COMPANY MANAGEMENT] ---")
            print(" 1. View All Companies")
            print(" 2. Add New Company")
            print(" 3. Search Company by Name")
            print(" 4. Update Company Status")
            print(" 5. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                companies = self.company_service.get_all_companies()
                print(f"\n--- Total Companies: {len(companies)} ---")
                for comp in companies:
                    print(comp)
            elif c == "2":
                try:
                    name = input("Company Name: ").strip()
                    industry = input("Industry (IT Services/Software/FinTech/etc.): ").strip()
                    loc = input("Location (City): ").strip()
                    contact = input("HR Contact Person: ").strip()
                    email = input("HR Contact Email: ").strip()
                    phone = input("HR Contact Phone: ").strip()

                    comp = Company(
                        company_name=name,
                        industry=industry,
                        location=loc,
                        contact_person=contact,
                        contact_email=email,
                        contact_phone=phone,
                    )
                    comp_id = self.company_service.add_company(comp)
                    print(f"[✓] Company added successfully! ID = {comp_id}")
                    self.log_service.log(f"Company Created: {name} (ID: {comp_id})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "3":
                name = input("Enter company name to search: ").strip()
                res = self.company_service.search_by_name(name)
                print(f"Found {len(res)} companies:")
                for comp in res:
                    print(comp)
            elif c == "4":
                try:
                    cid = int(input("Enter Company ID: ").strip())
                    st = input("Enter new status (ACTIVE/INACTIVE): ").strip().upper()
                    if self.company_service.update_status(cid, st):
                        print(f"[✓] Status updated to {st}.")
                        self.log_service.log(f"Company Status Updated: ID {cid} -> {st}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "5":
                break

    # -------------------------------------------------------------
    # 3. JOBS
    # -------------------------------------------------------------
    def _menu_jobs(self):
        while True:
            print("\n--- [JOB OPENING MANAGEMENT] ---")
            print(" 1. View Open Jobs")
            print(" 2. View All Jobs")
            print(" 3. Create New Job Opening")
            print(" 4. Search Job by Title")
            print(" 5. Close a Job Opening")
            print(" 6. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                jobs = self.job_service.get_open_jobs()
                print(f"\n--- Open Jobs ({len(jobs)}) ---")
                for j in jobs:
                    print(j)
            elif c == "2":
                jobs = self.job_service.get_all_jobs()
                print(f"\n--- All Jobs ({len(jobs)}) ---")
                for j in jobs:
                    print(j)
            elif c == "3":
                try:
                    comp_id = int(input("Company ID: ").strip())
                    title = input("Job Title: ").strip()
                    emp_type = input("Employment Type (FULL_TIME/INTERNSHIP/CONTRACT): ").strip() or "FULL_TIME"
                    loc = input("Location: ").strip()
                    openings = int(input("Number of Openings: ").strip())
                    min_pkg = float(input("Min Package (LPA): ").strip())
                    max_pkg = float(input("Max Package (LPA): ").strip())
                    min_pct = float(input("Eligibility Min Percentage (0-100): ").strip())
                    min_yr = int(input("Min Passing Year (e.g. 2024): ").strip())
                    max_yr = int(input("Max Passing Year (e.g. 2026): ").strip())
                    max_bk = int(input("Max Backlogs Allowed: ").strip())
                    deadline_str = input("Application Deadline (YYYY-MM-DD): ").strip()
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None

                    job = Job(
                        company_id=comp_id,
                        job_title=title,
                        employment_type=emp_type,
                        location=loc,
                        openings=openings,
                        min_package_lpa=min_pkg,
                        max_package_lpa=max_pkg,
                        min_percentage=min_pct,
                        min_passing_year=min_yr,
                        max_passing_year=max_yr,
                        max_backlogs=max_bk,
                        posted_date=date.today(),
                        application_deadline=deadline,
                        status="OPEN",
                    )
                    job_id = self.job_service.create_job(job)
                    print(f"[✓] Job created successfully! ID = {job_id}")
                    self.log_service.log(f"Job Created: {title} (ID: {job_id})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "4":
                t = input("Enter job title to search: ").strip()
                res = self.job_service.search_by_title(t)
                for j in res:
                    print(j)
            elif c == "5":
                try:
                    jid = int(input("Enter Job ID to close: ").strip())
                    if self.job_service.close_job(jid):
                        print(f"[✓] Job #{jid} closed.")
                        self.log_service.log(f"Job Closed: ID {jid}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "6":
                break

    # -------------------------------------------------------------
    # 4. APPLICATIONS
    # -------------------------------------------------------------
    def _menu_applications(self):
        while True:
            print("\n--- [APPLICATION & WORKFLOW MANAGEMENT] ---")
            print(" 1. View All Applications")
            print(" 2. Apply for Job (Candidate + Job)")
            print(" 3. View Applications by Candidate")
            print(" 4. View Applications by Job")
            print(" 5. Advance Application Status (Workflow)")
            print(" 6. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                apps = self.application_service.get_all_applications()
                print(f"\n--- Applications ({len(apps)}) ---")
                for app in apps:
                    print(app)
            elif c == "2":
                try:
                    cid = int(input("Candidate ID: ").strip())
                    jid = int(input("Job ID: ").strip())
                    app_id = self.application_service.apply_for_job(cid, jid)
                    print(f"[✓] Application submitted successfully! Application ID = {app_id}")
                    print("    Eligibility verified: Candidate meets criteria.")
                    self.log_service.log(f"Application Created: Candidate#{cid} -> Job#{jid} (App#{app_id})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Application Error: {e}")
            elif c == "3":
                try:
                    cid = int(input("Enter Candidate ID: ").strip())
                    apps = self.application_service.get_by_candidate(cid)
                    print(f"Found {len(apps)} applications:")
                    for a in apps:
                        print(a)
                except ValueError as e:
                    print(f"[!] Error: {e}")
            elif c == "4":
                try:
                    jid = int(input("Enter Job ID: ").strip())
                    apps = self.application_service.get_by_job(jid)
                    print(f"Found {len(apps)} applications:")
                    for a in apps:
                        print(a)
                except ValueError as e:
                    print(f"[!] Error: {e}")
            elif c == "5":
                try:
                    aid = int(input("Enter Application ID: ").strip())
                    app = self.application_service.get_application(aid)
                    print(f"Current Status: {app.application_status}")
                    target = input("Target Status (SHORTLISTED/INTERVIEW_SCHEDULED/INTERVIEWED/SELECTED/OFFERED/JOINED/REJECTED): ").strip().upper()
                    if self.application_service.update_status(aid, target):
                        print(f"[✓] Application #{aid} status updated to {target}.")
                        self.log_service.log(f"Application Status: App#{aid} -> {target}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Transition Error: {e}")
            elif c == "6":
                break

    # -------------------------------------------------------------
    # 5. INTERVIEWS
    # -------------------------------------------------------------
    def _menu_interviews(self):
        while True:
            print("\n--- [INTERVIEW MANAGEMENT] ---")
            print(" 1. Schedule Interview Round")
            print(" 2. View Interviews by Application")
            print(" 3. Record Interview Feedback & Result")
            print(" 4. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                try:
                    aid = int(input("Application ID: ").strip())
                    rnd = int(input("Round Number (1, 2, 3...): ").strip())
                    rtype = input("Round Type (APTITUDE/TECHNICAL/MANAGERIAL/HR): ").strip().upper()
                    d_str = input("Scheduled Date (YYYY-MM-DD): ").strip()
                    d_val = datetime.strptime(d_str, "%Y-%m-%d").date() if d_str else date.today()
                    mode = input("Mode (ONLINE/OFFLINE/TELEPHONIC): ").strip().upper() or "ONLINE"
                    interviewer = input("Interviewer Name: ").strip()

                    interview = Interview(
                        application_id=aid,
                        round_number=rnd,
                        round_type=rtype,
                        interview_date=d_val,
                        mode=mode,
                        interviewer=interviewer,
                    )
                    int_id = self.interview_service.schedule_interview(interview)
                    print(f"[✓] Interview round scheduled! Interview ID = {int_id}")
                    self.log_service.log(f"Interview Scheduled: App#{aid} Round {rnd} ({rtype})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "2":
                try:
                    aid = int(input("Enter Application ID: ").strip())
                    rounds = self.interview_service.get_by_application(aid)
                    print(f"Found {len(rounds)} interview rounds:")
                    for r in rounds:
                        print(r)
                        fb = self.interview_service.get_feedback(r.interview_id)
                        if fb:
                            print(f"   └── {fb}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "3":
                try:
                    iid = int(input("Enter Interview ID: ").strip())
                    tech = float(input("Technical Rating (0-5): ").strip())
                    comm = float(input("Communication Rating (0-5): ").strip())
                    ps = float(input("Problem Solving Rating (0-5): ").strip())
                    overall = float(input("Overall Rating (0-5): ").strip())
                    rec = input("Recommendation (NEXT_ROUND/SELECTED/REJECTED/ON_HOLD): ").strip().upper()
                    remarks = input("Interviewer Remarks: ").strip()

                    fb = InterviewFeedback(
                        interview_id=iid,
                        technical_rating=tech,
                        communication_rating=comm,
                        problem_solving_rating=ps,
                        overall_rating=overall,
                        recommendation=rec,
                        remarks=remarks,
                    )
                    fbid = self.interview_service.add_feedback(fb)
                    print(f"[✓] Feedback saved! (Feedback ID: {fbid})")
                    print(f"    Application status updated based on recommendation: {rec}")
                    self.log_service.log(f"Interview Feedback: Int#{iid} -> Recommendation: {rec}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "4":
                break

    # -------------------------------------------------------------
    # 6. OFFERS
    # -------------------------------------------------------------
    def _menu_offers(self):
        while True:
            print("\n--- [OFFER MANAGEMENT] ---")
            print(" 1. Create Job Offer")
            print(" 2. View All Offers")
            print(" 3. Update Offer Status")
            print(" 4. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                try:
                    aid = int(input("Application ID: ").strip())
                    desig = input("Designation (e.g. Associate Software Engineer): ").strip()
                    pkg = float(input("Offered Package (LPA): ").strip())
                    od_str = input("Offer Date (YYYY-MM-DD): ").strip()
                    od = datetime.strptime(od_str, "%Y-%m-%d").date() if od_str else date.today()
                    jd_str = input("Expected Joining Date (YYYY-MM-DD): ").strip()
                    jd = datetime.strptime(jd_str, "%Y-%m-%d").date() if jd_str else None

                    offer = Offer(
                        application_id=aid,
                        designation=desig,
                        offered_package_lpa=pkg,
                        offer_date=od,
                        expected_joining_date=jd,
                        offer_status="OFFERED",
                    )
                    oid = self.offer_service.create_offer(offer)
                    print(f"[✓] Offer generated! Offer ID = {oid}")
                    self.log_service.log(f"Offer Created: App#{aid} - {desig} @ {pkg} LPA")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "2":
                offers = self.offer_service.get_all_offers()
                print(f"\n--- Total Offers: {len(offers)} ---")
                for o in offers:
                    print(o)
            elif c == "3":
                try:
                    oid = int(input("Enter Offer ID: ").strip())
                    st = input("New Status (OFFERED/ACCEPTED/REJECTED/EXPIRED/WITHDRAWN): ").strip().upper()
                    if self.offer_service.update_offer_status(oid, st):
                        print(f"[✓] Offer status updated to {st}.")
                        self.log_service.log(f"Offer Status: Offer#{oid} -> {st}")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "4":
                break

    # -------------------------------------------------------------
    # 7. PLACEMENTS
    # -------------------------------------------------------------
    def _menu_placements(self):
        while True:
            print("\n--- [PLACEMENT & JOINING CONFIRMATION] ---")
            print(" 1. Confirm Joining / Placement")
            print(" 2. View All Placements")
            print(" 3. View Placed Candidates List")
            print(" 4. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                try:
                    oid = int(input("Offer ID: ").strip())
                    cid = int(input("Candidate ID: ").strip())
                    jd_str = input("Actual Joining Date (YYYY-MM-DD): ").strip()
                    jd = datetime.strptime(jd_str, "%Y-%m-%d").date() if jd_str else date.today()
                    status = input("Joining Status (JOINED/NOT_JOINED/DEFERRED): ").strip().upper() or "JOINED"

                    placement = Placement(
                        offer_id=oid,
                        candidate_id=cid,
                        actual_joining_date=jd,
                        joining_status=status,
                    )
                    pid = self.placement_service.confirm_placement(placement)
                    print(f"[✓] Placement confirmed! Placement ID = {pid}")
                    if status == "JOINED":
                        print("    [✓] Candidate placement_status set to 'PLACED'.")
                        print("    [✓] Offer status set to 'ACCEPTED'.")
                        print("    [✓] Application status set to 'JOINED'.")
                    self.log_service.log(f"Placement Confirmed: Candidate#{cid} Offer#{oid} (Status: {status})")
                except (ValueError, RPMSBaseException) as e:
                    print(f"[!] Error: {e}")
            elif c == "2":
                placements = self.placement_service.get_all_placements()
                print(f"\n--- Total Placements: {len(placements)} ---")
                for p in placements:
                    print(p)
            elif c == "3":
                placed = self.report_service.placed_candidates()
                print(f"\n--- Confirmed Placed Candidates ({len(placed)}) ---")
                for row in placed:
                    print(f"[{row['candidate_id']}] {row['full_name']} | Company: {row['company_name']} | Role: {row['designation']} | Package: {row['offered_package_lpa']} LPA | Joined: {row['actual_joining_date']}")
            elif c == "4":
                break

    # -------------------------------------------------------------
    # 8. REPORTS
    # -------------------------------------------------------------
    def _menu_reports(self):
        while True:
            print("\n--- [REPORTS & ANALYTICS] ---")
            print(" 1. Candidates by Technology")
            print(" 2. Open Jobs Report")
            print(" 3. Applications by Status")
            print(" 4. Company-wise Placements")
            print(" 5. Placed Candidates List")
            print(" 6. Unplaced Candidates List")
            print(" 7. Pending / Scheduled Interviews")
            print(" 8. Recruitment Funnel")
            print(" 9. Back to Main Menu")
            c = input("Choice: ").strip()

            if c == "1":
                data = self.report_service.candidate_count_by_technology()
                print("\n--- Candidates by Technology ---")
                for r in data:
                    print(f"  {r['primary_technology']:<20}: {r['count']} candidates")
            elif c == "2":
                jobs = self.report_service.open_jobs_report()
                print(f"\n--- Open Jobs ({len(jobs)}) ---")
                for j in jobs:
                    print(f"  [{j['job_id']}] {j['job_title']} @ {j['company_name']} | {j['location']} | Openings: {j['openings']} | {j['min_package_lpa']}-{j['max_package_lpa']} LPA | Deadline: {j['application_deadline']}")
            elif c == "3":
                apps = self.report_service.applications_by_status()
                print("\n--- Applications by Status ---")
                for a in apps:
                    print(f"  {a['application_status']:<25}: {a['count']}")
            elif c == "4":
                res = self.report_service.company_wise_placements()
                print("\n--- Company-wise Placements ---")
                for row in res:
                    print(f"  {row['company_name']:<25}: {row['placed_count']} placed")
            elif c == "5":
                placed = self.report_service.placed_candidates()
                print(f"\n--- Placed Candidates ({len(placed)}) ---")
                for p in placed:
                    print(f"  {p['full_name']} -> {p['company_name']} ({p['designation']}) @ {p['offered_package_lpa']} LPA")
            elif c == "6":
                unplaced = self.report_service.unplaced_candidates()
                print(f"\n--- Unplaced Candidates ({len(unplaced)}) ---")
                for u in unplaced:
                    print(f"  [{u['candidate_id']}] {u['full_name']} | Tech: {u['primary_technology']} | {u['percentage']}% | Batch {u['passing_year']}")
            elif c == "7":
                pend = self.report_service.pending_interviews()
                print(f"\n--- Pending Interviews ({len(pend)}) ---")
                for pi in pend:
                    print(f"  Int#{pi['interview_id']} | {pi['candidate_name']} @ {pi['company_name']} | Round {pi['round_number']} ({pi['round_type']}) | Date: {pi['interview_date']} | Mode: {pi['mode']}")
            elif c == "8":
                funnel = self.report_service.recruitment_funnel()
                print("\n--- Recruitment Funnel ---")
                for stage, cnt in funnel.items():
                    bar = "█" * (cnt // 2) if cnt > 0 else ""
                    print(f"  {stage:<22}: {cnt:<4} {bar}")
            elif c == "9":
                break


def main():
    app = RPMSConsoleApp()
    app.run()


if __name__ == "__main__":
    main()
