# 🧪 RPMS — Test Cases

**Project:** Recruitment & Placement Management System  
**Version:** 1.0  
**Total Test Cases:** 30  

---

## Legend

| Symbol | Meaning          |
|--------|------------------|
| ✅     | Positive test    |
| ❌     | Negative test    |
| 🔄     | Workflow test    |

---

## Test Cases Table

| Test ID | Module              | Test Case Description                        | Input / Preconditions                                                                 | Expected Result                                                               | Type |
|---------|---------------------|----------------------------------------------|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|------|
| TC-01   | Candidate Mgmt      | Add valid candidate                          | name="Rahul Patil", email="rahul@test.com", mobile="9876543210", %=72.5, backlogs=0  | Candidate added successfully; new `candidate_id` returned                     | ✅   |
| TC-02   | Candidate Mgmt      | Duplicate email rejected                     | Same email as TC-01: "rahul@test.com"                                                 | Raises `DuplicateEntryError` / DB unique constraint; error message shown      | ❌   |
| TC-03   | Candidate Mgmt      | Duplicate mobile rejected                    | Same mobile as TC-01: "9876543210", different email                                   | Error: "Mobile number already registered"                                     | ❌   |
| TC-04   | Candidate Mgmt      | Invalid mobile (< 10 digits)                 | mobile="98765"                                                                        | ValidationError: "Mobile must be exactly 10 digits"                           | ❌   |
| TC-05   | Candidate Mgmt      | Invalid mobile (non-numeric)                 | mobile="ABCDEFGHIJ"                                                                   | ValidationError: "Mobile must be numeric"                                     | ❌   |
| TC-06   | Candidate Mgmt      | Invalid percentage (> 100)                   | percentage=105.0                                                                      | ValidationError: "Percentage must be between 0 and 100"                       | ❌   |
| TC-07   | Candidate Mgmt      | Invalid percentage (negative)                | percentage=-5.0                                                                       | ValidationError: "Percentage must be between 0 and 100"                       | ❌   |
| TC-08   | Candidate Mgmt      | Invalid backlog count (negative)             | backlog_count=-1                                                                      | ValidationError: "Backlog count cannot be negative"                           | ❌   |
| TC-09   | Candidate Mgmt      | Search candidate by name                     | search_term="Rahul"                                                                   | Returns list of candidates whose name contains "Rahul"                        | ✅   |
| TC-10   | Candidate Mgmt      | Deactivate candidate                         | candidate_id=1 (ACTIVE)                                                               | Candidate status changed to INACTIVE; confirmation message shown              | ✅   |
| TC-11   | Job Mgmt            | Create valid job posting                     | company_id=1, title="Java Developer", openings=5, min_%=65, min_year=2022, deadline=future | Job created with status=OPEN; new `job_id` returned                      | ✅   |
| TC-12   | Job Mgmt            | Close an open job                            | job_id=1 (OPEN)                                                                       | Job status changed to CLOSED; no new applications accepted                    | ✅   |
| TC-13   | Job Mgmt            | Search jobs by title keyword                 | keyword="Java"                                                                        | Returns all jobs whose title contains "Java"                                  | ✅   |
| TC-14   | Eligibility Check   | Eligible candidate passes all rules          | candidate %=72 ≥ job min_%=65; year=2022 in [2021,2023]; backlogs=0 ≤ max=2; deadline not passed; not already applied | Application saved with eligibility_status=ELIGIBLE | ✅   |
| TC-15   | Eligibility Check   | Not eligible — percentage too low            | candidate %=58, job min_%=65                                                          | Application saved with eligibility_status=NOT_ELIGIBLE, reason="Percentage below minimum" | ❌ |
| TC-16   | Eligibility Check   | Not eligible — passing year out of range     | candidate passing_year=2019, job min_year=2021                                        | NOT_ELIGIBLE, reason="Passing year does not meet requirement"                 | ❌   |
| TC-17   | Eligibility Check   | Not eligible — backlogs exceed maximum       | candidate backlogs=3, job max_backlogs=2                                              | NOT_ELIGIBLE, reason="Too many backlogs"                                      | ❌   |
| TC-18   | Eligibility Check   | Not eligible — application deadline passed   | Current date > job.application_deadline                                               | NOT_ELIGIBLE, reason="Application deadline has passed"                        | ❌   |
| TC-19   | Eligibility Check   | Not eligible — candidate INACTIVE            | candidate status=INACTIVE                                                             | Raises `CandidateNotFoundError` or eligibility fails: "Candidate not active"  | ❌   |
| TC-20   | Application         | Duplicate application blocked                | Same candidate_id + job_id applied twice                                              | Raises `DuplicateApplicationError`: "Already applied for this job"            | ❌   |
| TC-21   | Application         | Apply for non-existent job                   | job_id=99999 (not in DB)                                                              | Raises `JobNotFoundError`                                                     | ❌   |
| TC-22   | Workflow            | Valid status transition: APPLIED→SHORTLISTED | application_id with status=APPLIED; action=SHORTLIST                                  | Status updated to SHORTLISTED; workflow_history row inserted                  | 🔄   |
| TC-23   | Workflow            | Valid transition: SHORTLISTED→INTERVIEW_SCHEDULED | status=SHORTLISTED; action=SCHEDULE_INTERVIEW                                  | Status updated to INTERVIEW_SCHEDULED                                         | 🔄   |
| TC-24   | Workflow            | Invalid jump: APPLIED→SELECTED               | application status=APPLIED; attempt to set SELECTED directly                          | Raises `InvalidWorkflowTransitionError`: "Invalid status transition"          | 🔄 ❌|
| TC-25   | Interview           | Schedule interview for shortlisted app       | application_id (INTERVIEW_SCHEDULED), round=1, type=TECHNICAL, date=future, mode=ONLINE | Interview record created; confirmation message shown                       | ✅   |
| TC-26   | Interview           | Add feedback with valid ratings              | interview_id=1; technical=4, communication=3, problem_solving=4, overall=4, recommendation=SELECTED | Feedback saved; overall_rating stored                          | ✅   |
| TC-27   | Offer               | Create offer for SELECTED candidate          | application_id (SELECTED), designation="Java Dev", package=5.5, offer_date=today, joining_date=future | Offer created with status=OFFERED                             | ✅   |
| TC-28   | Offer               | Update offer status to ACCEPTED              | offer_id=1 (OFFERED); new_status=ACCEPTED                                             | Offer status updated to ACCEPTED                                              | ✅   |
| TC-29   | Placement           | Confirm joining                              | offer_id=1 (ACCEPTED), actual_joining_date=today, joining_status=JOINED               | Placement record created; candidate.placement_status updated to PLACED        | ✅   |
| TC-30   | Reports             | All 6 reports execute without error          | Invoke each report function in `report_service.py` with active DB connection          | Each report returns a non-empty result set or prints formatted table          | ✅   |

---

## Module Coverage Summary

| Module              | Test IDs              | Positive | Negative |
|---------------------|-----------------------|----------|----------|
| Candidate Mgmt      | TC-01 to TC-10        | 3        | 7        |
| Job Mgmt            | TC-11 to TC-13        | 3        | 0        |
| Eligibility Check   | TC-14 to TC-19        | 1        | 5        |
| Application         | TC-20 to TC-21        | 0        | 2        |
| Workflow            | TC-22 to TC-24        | 2        | 1        |
| Interview           | TC-25 to TC-26        | 2        | 0        |
| Offer               | TC-27 to TC-28        | 2        | 0        |
| Placement           | TC-29                 | 1        | 0        |
| Reports             | TC-30                 | 1        | 0        |
| **Total**           |                       | **15**   | **15**   |

---

## Notes

> [!NOTE]
> All test cases assume `recruitment_portal` database is seeded with `sql/rpms_full_setup.sql` before running.

> [!TIP]
> Run negative tests first to verify validation layers, then positive tests to verify successful CRUD paths.

> [!IMPORTANT]
> Workflow tests (TC-22 to TC-24) must be run in sequence as each transition depends on the previous state.
