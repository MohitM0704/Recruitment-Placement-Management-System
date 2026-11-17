-- =========================================================
-- Recruitment & Placement Management System (RPMS)
-- Required Reporting & Analytical Queries
-- =========================================================

USE recruitment_portal;

-- 1. Candidate Count by Primary Technology
SELECT 
    primary_technology, 
    COUNT(*) AS total_candidates,
    ROUND(AVG(percentage), 2) AS avg_percentage
FROM candidates
GROUP BY primary_technology
ORDER BY total_candidates DESC;

-- 2. Open Jobs by Company
SELECT 
    j.job_id,
    j.job_title,
    c.company_name,
    j.location,
    j.openings,
    j.min_package_lpa,
    j.max_package_lpa,
    j.min_percentage,
    j.application_deadline
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
WHERE j.status = 'OPEN'
ORDER BY j.application_deadline ASC;

-- 3. Applications by Workflow Status
SELECT 
    application_status, 
    COUNT(*) AS total_applications,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM applications), 2) AS percentage
FROM applications
GROUP BY application_status
ORDER BY total_applications DESC;

-- 4. Recruitment Funnel Analysis
SELECT
    COUNT(CASE WHEN application_status IN ('APPLIED','SHORTLISTED','INTERVIEW_SCHEDULED','INTERVIEWED','SELECTED','OFFERED','JOINED') THEN 1 END) AS total_applied,
    COUNT(CASE WHEN application_status IN ('SHORTLISTED','INTERVIEW_SCHEDULED','INTERVIEWED','SELECTED','OFFERED','JOINED') THEN 1 END) AS shortlisted,
    COUNT(CASE WHEN application_status IN ('INTERVIEWED','SELECTED','OFFERED','JOINED') THEN 1 END) AS interviewed,
    COUNT(CASE WHEN application_status IN ('SELECTED','OFFERED','JOINED') THEN 1 END) AS selected,
    COUNT(CASE WHEN application_status IN ('OFFERED','JOINED') THEN 1 END) AS offered,
    COUNT(CASE WHEN application_status = 'JOINED' THEN 1 END) AS joined,
    COUNT(CASE WHEN application_status = 'REJECTED' THEN 1 END) AS rejected
FROM applications;

-- 5. Company-Wise Placements (Hiring Leaders)
SELECT 
    c.company_id,
    c.company_name,
    c.industry,
    COUNT(p.placement_id) AS candidates_joined,
    ROUND(AVG(o.offered_package_lpa), 2) AS avg_package_lpa,
    MAX(o.offered_package_lpa) AS highest_package_lpa
FROM placements p
JOIN offers o ON p.offer_id = o.offer_id
JOIN applications a ON o.application_id = a.application_id
JOIN jobs j ON a.job_id = j.job_id
JOIN companies c ON j.company_id = c.company_id
WHERE p.joining_status = 'JOINED'
GROUP BY c.company_id, c.company_name, c.industry
ORDER BY candidates_joined DESC;

-- 6. Technology-Wise Placements
SELECT 
    c.primary_technology,
    COUNT(p.placement_id) AS placed_count,
    ROUND(AVG(o.offered_package_lpa), 2) AS avg_package_lpa
FROM placements p
JOIN candidates c ON p.candidate_id = c.candidate_id
JOIN offers o ON p.offer_id = o.offer_id
WHERE p.joining_status = 'JOINED'
GROUP BY c.primary_technology
ORDER BY placed_count DESC;

-- 7. Placed Candidates Detailed Register
SELECT 
    c.candidate_id,
    c.full_name,
    c.email,
    c.mobile,
    c.primary_technology,
    comp.company_name,
    o.designation,
    o.offered_package_lpa,
    p.actual_joining_date
FROM placements p
JOIN candidates c ON p.candidate_id = c.candidate_id
JOIN offers o ON p.offer_id = o.offer_id
JOIN applications a ON o.application_id = a.application_id
JOIN jobs j ON a.job_id = j.job_id
JOIN companies comp ON j.company_id = comp.company_id
WHERE p.joining_status = 'JOINED'
ORDER BY p.actual_joining_date DESC;

-- 8. Active Unplaced Candidates
SELECT 
    candidate_id,
    full_name,
    email,
    mobile,
    primary_technology,
    percentage,
    passing_year,
    backlog_count
FROM candidates
WHERE placement_status = 'NOT_PLACED' 
  AND profile_status = 'ACTIVE'
ORDER BY passing_year DESC, percentage DESC;

-- 9. Pending / Upcoming Interviews
SELECT 
    i.interview_id,
    c.full_name AS candidate_name,
    comp.company_name,
    j.job_title,
    i.round_number,
    i.round_type,
    i.interview_date,
    i.mode,
    i.interviewer
FROM interview_rounds i
JOIN applications a ON i.application_id = a.application_id
JOIN candidates c ON a.candidate_id = c.candidate_id
JOIN jobs j ON a.job_id = j.job_id
JOIN companies comp ON j.company_id = comp.company_id
WHERE i.status = 'SCHEDULED'
ORDER BY i.interview_date ASC;

-- 10. Offer-to-Joining Conversion Rate
SELECT 
    COUNT(o.offer_id) AS total_offers_extended,
    COUNT(CASE WHEN p.joining_status = 'JOINED' THEN 1 END) AS total_joined,
    ROUND(COUNT(CASE WHEN p.joining_status = 'JOINED' THEN 1 END) * 100.0 / COUNT(o.offer_id), 2) AS conversion_rate_percent
FROM offers o
LEFT JOIN placements p ON o.offer_id = p.offer_id;

-- 11. Job Requirement Aging
SELECT 
    j.job_id,
    j.job_title,
    c.company_name,
    j.posted_date,
    j.application_deadline,
    DATEDIFF(CURRENT_DATE, j.posted_date) AS days_open,
    j.status
FROM jobs j
JOIN companies c ON j.company_id = c.company_id
WHERE j.status = 'OPEN'
ORDER BY days_open DESC;
