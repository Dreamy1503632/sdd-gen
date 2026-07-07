"""
data/question_database.py
Server-side question database for HLA questionnaire generation.
Structure: QUESTION_DATABASE[module][industry_key] = list of question dicts.
Industry keys: "base" | "manufacturing" | "healthcare" | "financialServices" | "retail"
"""
from __future__ import annotations

QUESTION_DATABASE: dict[str, dict[str, list[dict]]] = {

    # ──────────────────────────────────────────────────────────────────────────
    "Core HR": {
        "base": [
            {"category": "Strategic Objectives", "question": "What are your primary business drivers for implementing Oracle Fusion Core HR?", "priority": "Critical", "guidance": "Understanding strategic drivers helps align the implementation with business goals."},
            {"category": "Strategic Objectives", "question": "What workforce management challenges are you trying to solve?", "priority": "Critical", "guidance": "Identify specific pain points to prioritise solution features."},
            {"category": "Strategic Objectives", "question": "What are your expected ROI and success metrics for this implementation?", "priority": "High", "guidance": "Define measurable outcomes to track implementation success."},
            {"category": "Current State Assessment", "question": "What HRIS/HCM systems are currently in use? Please list all systems, vendors, and versions.", "priority": "Critical", "guidance": "Complete inventory of existing systems is essential for integration planning."},
            {"category": "Current State Assessment", "question": "How many legal entities, business units, and departments do you operate?", "priority": "Critical", "guidance": "Enterprise structure determines configuration complexity."},
            {"category": "Current State Assessment", "question": "What is your total employee count and breakdown by employment type (FT, PT, Contractors, Temporary)?", "priority": "High", "guidance": "Employee population affects licensing and system design."},
            {"category": "Current State Assessment", "question": "How many countries/regions do you operate in? List all with approximate employee counts.", "priority": "Critical", "guidance": "Geographic footprint impacts localisation and compliance requirements."},
            {"category": "Current State Assessment", "question": "What are the primary languages required in the system?", "priority": "High", "guidance": "Language requirements affect configuration and user experience."},
            {"category": "Business Process - Hiring", "question": "Describe your end-to-end hiring process from requisition creation to employee onboarding.", "priority": "Critical", "guidance": "Detailed process understanding enables accurate configuration."},
            {"category": "Business Process - Hiring", "question": "What approval workflows exist for new hire requisitions?", "priority": "High", "guidance": "Workflow complexity affects configuration effort."},
            {"category": "Business Process - Hiring", "question": "What is your average time-to-hire and what is your target?", "priority": "Medium", "guidance": "Metrics help measure process improvement."},
            {"category": "Business Process - Employee Lifecycle", "question": "How do you currently manage employee transfers (lateral, promotion, location change)?", "priority": "High", "guidance": "Transfer processes affect organisational management design."},
            {"category": "Business Process - Employee Lifecycle", "question": "What is your process for managing terminations (voluntary and involuntary)?", "priority": "High", "guidance": "Termination workflows must comply with legal requirements."},
            {"category": "Business Process - Employee Lifecycle", "question": "How do you manage employee data changes (personal info, emergency contacts, banking)?", "priority": "Medium", "guidance": "Self-service capabilities can reduce HR administrative burden."},
            {"category": "Business Process - Organisational Management", "question": "How frequently does your organisational structure change?", "priority": "High", "guidance": "Change frequency affects how organisational structures are maintained."},
            {"category": "Business Process - Organisational Management", "question": "Who has authority to make organisational changes and what approval is required?", "priority": "High", "guidance": "Governance model affects security and workflow design."},
            {"category": "Data & Integration", "question": "What systems need to integrate with Oracle Fusion HCM Core HR? (Payroll, Finance, Time tracking, Benefits, etc.)", "priority": "Critical", "guidance": "Integration landscape determines technical architecture."},
            {"category": "Data & Integration", "question": "What is your data integration strategy (Real-time, Batch, Event-driven)?", "priority": "High", "guidance": "Integration patterns affect technical solution design."},
            {"category": "Data & Integration", "question": "What data migration scope is required? How many years of historical data must be migrated?", "priority": "Critical", "guidance": "Migration scope affects timeline and effort."},
            {"category": "Data & Integration", "question": "What is your master data management strategy for employee data?", "priority": "High", "guidance": "MDM approach affects integration design."},
            {"category": "Compliance & Governance", "question": "What regulatory compliance requirements apply to your organisation (GDPR, CCPA, local labour laws)?", "priority": "Critical", "guidance": "Compliance requirements are non-negotiable system constraints."},
            {"category": "Compliance & Governance", "question": "What data privacy and security requirements exist for employee information?", "priority": "Critical", "guidance": "Security requirements affect access control design."},
            {"category": "Compliance & Governance", "question": "What audit and reporting requirements must be met?", "priority": "High", "guidance": "Audit requirements affect reporting and data retention design."},
            {"category": "Compliance & Governance", "question": "Do you have specific data residency requirements (where employee data must be stored)?", "priority": "High", "guidance": "Data residency affects cloud deployment options."},
            {"category": "User Experience", "question": "How many HR administrators/specialists will use the system? What are their roles?", "priority": "High", "guidance": "User population affects training and role design."},
            {"category": "User Experience", "question": "What employee self-service capabilities are required (personal data update, document access, etc.)?", "priority": "Critical", "guidance": "ESS requirements drive configuration priorities."},
            {"category": "User Experience", "question": "What manager self-service capabilities are required (team view, approvals, reporting)?", "priority": "Critical", "guidance": "MSS capabilities affect manager adoption and efficiency."},
            {"category": "User Experience", "question": "What are your mobile requirements for HR processes?", "priority": "Medium", "guidance": "Mobile strategy affects user experience design."},
            {"category": "Technical Infrastructure", "question": "What is your preferred deployment model (Public Cloud, Dedicated Cloud, Hybrid)?", "priority": "Critical", "guidance": "Deployment model affects architecture and costs."},
            {"category": "Technical Infrastructure", "question": "Do you have a Single Sign-On (SSO) solution? If yes, which provider?", "priority": "High", "guidance": "SSO integration improves user experience and security."},
            {"category": "Technical Infrastructure", "question": "What are your disaster recovery and business continuity requirements?", "priority": "High", "guidance": "DR/BC requirements affect SLA and architecture."},
            {"category": "Change Management", "question": "What is your organisation's change readiness level and experience with large-scale transformations?", "priority": "High", "guidance": "Change readiness affects implementation approach and timeline."},
            {"category": "Change Management", "question": "What training approach do you envision (train-the-trainer, end-user training, e-learning)?", "priority": "High", "guidance": "Training strategy affects adoption and costs."},
            {"category": "Change Management", "question": "What is your implementation timeline preference and any critical business deadlines?", "priority": "Critical", "guidance": "Timeline constraints affect implementation approach."},
            {"category": "Success Metrics", "question": "What KPIs will you use to measure implementation success?", "priority": "Critical", "guidance": "Success metrics guide implementation priorities."},
            {"category": "Success Metrics", "question": "What baseline metrics do you currently track for HR processes?", "priority": "Medium", "guidance": "Baseline metrics enable before/after comparison."},
        ],
        "manufacturing": [
            {"category": "Industry-Specific - Manufacturing", "question": "How do you manage shift-based workers (day, evening, night, rotating shifts)?", "priority": "Critical", "guidance": "Shift management is core to manufacturing workforce."},
            {"category": "Industry-Specific - Manufacturing", "question": "How do you calculate and pay shift differentials/premiums?", "priority": "Critical", "guidance": "Shift premium calculation affects payroll integration."},
            {"category": "Industry-Specific - Manufacturing", "question": "Do you have a union workforce? If yes, how many unions and what percentage of total workforce?", "priority": "Critical", "guidance": "Union presence significantly affects HR processes."},
            {"category": "Industry-Specific - Manufacturing", "question": "What are the key provisions in your union contracts (seniority, bidding, grievances)?", "priority": "High", "guidance": "Union contract terms drive specific requirements."},
            {"category": "Industry-Specific - Manufacturing", "question": "How do you manage seniority tracking and seniority-based processes (layoffs, recalls, job bidding)?", "priority": "High", "guidance": "Seniority tracking is critical in union environments."},
            {"category": "Industry-Specific - Manufacturing", "question": "What safety certifications and licences must be tracked for production workers (forklift, crane, welding, etc.)?", "priority": "Critical", "guidance": "Safety certification tracking is mandatory for compliance."},
            {"category": "Industry-Specific - Manufacturing", "question": "How do you manage employee transfers between facilities, lines, or departments?", "priority": "High", "guidance": "Inter-facility transfers common in manufacturing."},
            {"category": "Industry-Specific - Manufacturing", "question": "How do you handle temporary plant shutdowns or furloughs?", "priority": "High", "guidance": "Shutdown processes need special handling."},
            {"category": "Industry-Specific - Manufacturing", "question": "Do you use MES (Manufacturing Execution System)? If yes, what integration is needed with HCM?", "priority": "High", "guidance": "MES integration may be required for labour tracking."},
        ],
        "healthcare": [
            {"category": "Industry-Specific - Healthcare", "question": "What is your credentialing and privileging process for clinical staff (physicians, nurses, allied health)?", "priority": "Critical", "guidance": "Credentialing is mandatory and highly regulated in healthcare."},
            {"category": "Industry-Specific - Healthcare", "question": "What professional licences must be tracked (medical licences, DEA, nursing licences)?", "priority": "Critical", "guidance": "Licence tracking is critical for patient safety and compliance."},
            {"category": "Industry-Specific - Healthcare", "question": "How do you manage clinical vs. non-clinical workforce differently?", "priority": "High", "guidance": "Clinical and non-clinical staff have different requirements."},
            {"category": "Industry-Specific - Healthcare", "question": "What certifications must be tracked (BLS, ACLS, specialty certifications)?", "priority": "Critical", "guidance": "Certification tracking affects clinical operations."},
            {"category": "Industry-Specific - Healthcare", "question": "How do you manage on-call schedules and on-call compensation?", "priority": "High", "guidance": "On-call management is complex in healthcare settings."},
            {"category": "Industry-Specific - Healthcare", "question": "Do you need integration with EMR/EHR systems (Epic, Cerner, etc.)? For what purposes?", "priority": "High", "guidance": "EMR integration common for clinician information."},
            {"category": "Industry-Specific - Healthcare", "question": "How do you manage mandatory training and annual competency assessments?", "priority": "High", "guidance": "Mandatory training tracking is a regulatory requirement."},
        ],
        "financialServices": [
            {"category": "Industry-Specific - Financial Services", "question": "What financial industry licences and certifications must be tracked (Series 7, 63, 65, CFA, CFP, etc.)?", "priority": "Critical", "guidance": "Licence tracking is a regulatory requirement."},
            {"category": "Industry-Specific - Financial Services", "question": "How do you manage compliance with FINRA, SEC, or other regulatory requirements related to employees?", "priority": "Critical", "guidance": "Regulatory compliance is paramount in financial services."},
            {"category": "Industry-Specific - Financial Services", "question": "What background check and ongoing monitoring requirements exist for employees?", "priority": "High", "guidance": "Enhanced screening common in financial services."},
            {"category": "Industry-Specific - Financial Services", "question": "How do you track and report employee trading activities and conflicts of interest?", "priority": "High", "guidance": "Trading compliance affects HR data requirements."},
            {"category": "Industry-Specific - Financial Services", "question": "Do you need to track registered representatives and their registrations by state?", "priority": "High", "guidance": "State-by-state registration tracking may be required."},
        ],
        "retail": [
            {"category": "Industry-Specific - Retail", "question": "How many retail locations/stores do you operate and what is the employee turnover rate?", "priority": "Critical", "guidance": "Store count and turnover drive volume requirements."},
            {"category": "Industry-Specific - Retail", "question": "How do you manage seasonal hiring and workforce fluctuations?", "priority": "Critical", "guidance": "Seasonal patterns common in retail."},
            {"category": "Industry-Specific - Retail", "question": "What is your process for managing part-time, variable hour employees?", "priority": "High", "guidance": "Part-time workforce dominant in retail."},
            {"category": "Industry-Specific - Retail", "question": "How do you handle employee scheduling and schedule changes?", "priority": "High", "guidance": "Schedule management critical for retail operations."},
            {"category": "Industry-Specific - Retail", "question": "Do you need POS system integration for employee data? For what purposes?", "priority": "Medium", "guidance": "POS integration common for access control."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Talent Management": {
        "base": [
            {"category": "Strategic Objectives - Talent", "question": "What are your primary talent acquisition challenges and goals?", "priority": "Critical", "guidance": "Understanding talent challenges drives module priorities."},
            {"category": "Recruitment", "question": "Describe your end-to-end recruitment process from requisition to offer acceptance.", "priority": "Critical", "guidance": "Process mapping essential for recruitment configuration."},
            {"category": "Recruitment", "question": "What recruitment channels do you use (job boards, social media, agencies, campus)?", "priority": "High", "guidance": "Channel strategy affects integration needs."},
            {"category": "Recruitment", "question": "What is your applicant tracking workflow and who is involved in hiring decisions?", "priority": "High", "guidance": "Workflow complexity affects configuration."},
            {"category": "Recruitment", "question": "What are your current time-to-fill metrics by role type and what are targets?", "priority": "Medium", "guidance": "Metrics establish improvement baseline."},
            {"category": "Performance Management", "question": "Describe your current performance review process, frequency, and methodology.", "priority": "Critical", "guidance": "Performance process drives configuration approach."},
            {"category": "Performance Management", "question": "What goal-setting framework do you use (OKRs, MBOs, SMART goals, etc.)?", "priority": "High", "guidance": "Goal framework affects system setup."},
            {"category": "Performance Management", "question": "How do you handle continuous feedback and check-ins between formal reviews?", "priority": "Medium", "guidance": "Continuous feedback capabilities enhance performance culture."},
            {"category": "Performance Management", "question": "What is your calibration process for performance ratings?", "priority": "High", "guidance": "Calibration requirements affect workflow design."},
            {"category": "Learning & Development", "question": "What types of training programmes do you offer (mandatory, professional development, leadership)?", "priority": "High", "guidance": "Training types drive learning module requirements."},
            {"category": "Learning & Development", "question": "Do you have a Learning Management System (LMS)? If yes, what integration is needed?", "priority": "High", "guidance": "LMS integration common requirement."},
            {"category": "Learning & Development", "question": "How do you track mandatory training completion and compliance?", "priority": "High", "guidance": "Compliance tracking requirements affect learning setup."},
            {"category": "Career Development", "question": "How do you manage career paths and internal mobility?", "priority": "High", "guidance": "Career development supports retention."},
            {"category": "Career Development", "question": "What is your succession planning process and coverage targets?", "priority": "High", "guidance": "Succession planning capabilities important for leadership pipeline."},
            {"category": "Talent Review", "question": "Do you conduct talent reviews or 9-box assessments? Describe the process.", "priority": "Medium", "guidance": "Talent review process affects configuration."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Workforce Management": {
        "base": [
            {"category": "Time & Attendance", "question": "How do employees currently track time (biometric, swipe cards, mobile app, manual)?", "priority": "Critical", "guidance": "Time capture method affects integration architecture."},
            {"category": "Time & Attendance", "question": "What types of work schedules do you manage (fixed, rotating shifts, flexible, compressed workweeks)?", "priority": "Critical", "guidance": "Schedule complexity drives configuration requirements."},
            {"category": "Time & Attendance", "question": "How do you handle overtime calculation and approval workflows?", "priority": "High", "guidance": "Overtime rules vary by jurisdiction and job type."},
            {"category": "Time & Attendance", "question": "What time entry exceptions need to be managed (late, absent, overtime, missed punch)?", "priority": "High", "guidance": "Exception handling affects manager workload."},
            {"category": "Absence Management", "question": "What types of leave do you manage (vacation, sick, FMLA, parental, sabbatical, etc.)?", "priority": "Critical", "guidance": "Leave types determine absence plan configuration."},
            {"category": "Absence Management", "question": "How are leave balances calculated (accrual, anniversary year, calendar year, unlimited)?", "priority": "High", "guidance": "Accrual rules affect configuration complexity."},
            {"category": "Absence Management", "question": "What approval workflows exist for absence requests?", "priority": "High", "guidance": "Approval routing affects workflow configuration."},
            {"category": "Absence Management", "question": "Do you need to integrate with disability/leave management vendors?", "priority": "Medium", "guidance": "Third-party leave administrators common for complex cases."},
            {"category": "Scheduling", "question": "Do you use shift-based scheduling? If yes, describe your shift patterns.", "priority": "High", "guidance": "Shift complexity determines scheduling requirements."},
            {"category": "Scheduling", "question": "How do you manage schedule changes, shift swaps, and open shift requests?", "priority": "Medium", "guidance": "Schedule flexibility requirements affect configuration."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Payroll": {
        "base": [
            {"category": "Payroll Strategy", "question": "Are you implementing Oracle Global Payroll or integrating with a third-party payroll provider?", "priority": "Critical", "guidance": "Payroll approach fundamentally affects architecture."},
            {"category": "Payroll Processing", "question": "What is your payroll frequency by employee type (weekly, bi-weekly, semi-monthly, monthly)?", "priority": "Critical", "guidance": "Payroll calendar affects processing requirements."},
            {"category": "Payroll Processing", "question": "How many payroll cycles do you process per year including off-cycle payments?", "priority": "High", "guidance": "Processing volume affects capacity planning."},
            {"category": "Payroll Elements", "question": "What earnings types do you process (regular, overtime, bonuses, commissions)?", "priority": "High", "guidance": "Element types determine payroll configuration."},
            {"category": "Payroll Deductions", "question": "What deductions do you process (taxes, benefits, garnishments, loans, pension)?", "priority": "High", "guidance": "Deduction types affect calculation complexity."},
            {"category": "Payroll Compliance", "question": "What payroll compliance requirements must you meet (federal, state, local)?", "priority": "Critical", "guidance": "Compliance requirements are non-negotiable."},
            {"category": "Payroll Integration", "question": "What payroll data needs to flow from HCM to Payroll (new hires, terminations, changes)?", "priority": "Critical", "guidance": "Integration requirements drive technical design."},
            {"category": "Payroll Integration", "question": "What downstream integrations exist from payroll (GL, benefits, 401k, garnishments)?", "priority": "High", "guidance": "Downstream integrations part of overall architecture."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Compensation & Benefits": {
        "base": [
            {"category": "Compensation Strategy", "question": "What is your overall compensation philosophy and strategy?", "priority": "Critical", "guidance": "Compensation philosophy drives design decisions."},
            {"category": "Compensation Strategy", "question": "What types of compensation plans do you offer (base pay, variable pay, bonuses, commissions, equity)?", "priority": "Critical", "guidance": "Plan types determine configuration requirements."},
            {"category": "Compensation Administration", "question": "Describe your annual compensation review process and timeline.", "priority": "High", "guidance": "Annual cycle drives compensation module workflows."},
            {"category": "Compensation Administration", "question": "What compensation approval workflows and budget controls exist?", "priority": "High", "guidance": "Approval hierarchy affects workflow configuration."},
            {"category": "Benefits", "question": "What benefit plans do you offer (health, dental, vision, life, disability, retirement)?", "priority": "Critical", "guidance": "Plan offerings determine configuration scope."},
            {"category": "Benefits", "question": "When are your open enrolment periods and what is the process?", "priority": "High", "guidance": "Enrolment timing affects implementation schedule."},
            {"category": "Benefits", "question": "Do you use a benefits administration vendor? If yes, what integration is needed?", "priority": "High", "guidance": "Benefits vendor integration common requirement."},
            {"category": "Benefits", "question": "How do you handle life events (marriage, birth, divorce) and benefits changes?", "priority": "High", "guidance": "Life event processing requirements affect configuration."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Workforce Analytics": {
        "base": [
            {"category": "Reporting Requirements", "question": "What are your key HR metrics and KPIs that need to be tracked?", "priority": "High", "guidance": "KPIs drive analytics configuration."},
            {"category": "Reporting Requirements", "question": "What standard reports are required for compliance and operations?", "priority": "High", "guidance": "Standard reports affect configuration effort."},
            {"category": "Analytics Strategy", "question": "What workforce analytics capabilities do you need (dashboards, predictive analytics, ad-hoc)?", "priority": "Medium", "guidance": "Analytics maturity affects tool selection."},
            {"category": "Data Visualisation", "question": "What BI tools are currently used and what integration is needed?", "priority": "Medium", "guidance": "Existing BI tools may require integration."},
            {"category": "Data Visualisation", "question": "Do you require integration with external data warehouses or data lakes?", "priority": "Medium", "guidance": "Data warehouse integration affects extract design."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Health & Safety": {
        "base": [
            {"category": "Safety Management", "question": "What safety incidents need to be tracked and reported?", "priority": "High", "guidance": "Incident types drive configuration requirements."},
            {"category": "Safety Management", "question": "What safety training and certifications must be tracked?", "priority": "High", "guidance": "Training requirements affect compliance tracking."},
            {"category": "Compliance", "question": "What safety regulations must you comply with (OSHA, local requirements)?", "priority": "Critical", "guidance": "Regulatory requirements drive feature needs."},
            {"category": "Incident Management", "question": "What is your current process for managing workplace incidents and investigations?", "priority": "High", "guidance": "Incident workflow design depends on current process."},
        ],
    },

    # ──────────────────────────────────────────────────────────────────────────
    "Help Desk & Case Management": {
        "base": [
            {"category": "Service Delivery", "question": "What HR services need case management support?", "priority": "High", "guidance": "Service types determine case categories."},
            {"category": "Service Delivery", "question": "What is your current process for handling HR enquiries?", "priority": "Medium", "guidance": "Current process helps design future state."},
            {"category": "Knowledge Management", "question": "Do you have an HR knowledge base? What content needs to be migrated?", "priority": "Medium", "guidance": "Knowledge base content affects setup effort."},
            {"category": "SLA", "question": "What are your target response and resolution times for HR service requests?", "priority": "Medium", "guidance": "SLA requirements affect case routing configuration."},
        ],
    },
}
