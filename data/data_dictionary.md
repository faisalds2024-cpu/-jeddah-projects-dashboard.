# Data Dictionary

## projects.csv / projects.json

### Project_ID
Unique project identifier.
Type: String
Example: JED-PROJ-001

### Project_Name
Descriptive project title for reporting and dashboard display.
Type: String

### Sector
Project sector classification.
Type: Categorical String
Values: Roads & Transportation, Buildings, Stormwater & Drainage, Parks & Landscaping, Utilities, Street Lighting, Public Facilities, Urban Development

### District
Jeddah district where the project is located.
Type: Categorical String

### Contractor_ID
Unique contractor identifier.
Type: String
Example: CONT-001

### Contractor_Name
Assigned contractor name.
Type: String

### Project_Manager_ID
Unique project manager identifier.
Type: String
Example: PM-001

### Project_Manager_Name
Assigned project manager name.
Type: String

### Contract_Value
Original contract value in SAR.
Type: Integer

### Approved_Budget
Approved working budget in SAR.
Type: Integer

### Amount_Spent
Total spent amount in SAR as of the latest update.
Type: Integer

### Remaining_Budget
Unspent approved budget in SAR.
Type: Integer
Formula: Approved_Budget - Amount_Spent

### Financial_Progress
Spent budget percentage.
Type: Decimal Percentage
Formula: Amount_Spent / Approved_Budget * 100

### Planned_Start_Date
Baseline planned start date.
Type: Date (YYYY-MM-DD)

### Actual_Start_Date
Actual mobilization or construction start date.
Type: Date (YYYY-MM-DD) or Empty

### Planned_End_Date
Baseline planned completion date.
Type: Date (YYYY-MM-DD)

### Expected_End_Date
Current forecast completion date.
Type: Date (YYYY-MM-DD)

### Actual_End_Date
Actual completion date for completed projects only.
Type: Date (YYYY-MM-DD) or Empty

### Project_Duration_Days
Planned baseline duration.
Type: Integer
Formula: Planned_End_Date - Planned_Start_Date

### Elapsed_Days
Elapsed days since actual start until latest update or actual completion.
Type: Integer

### Remaining_Days
Forecast remaining days until expected end for open projects.
Type: Integer

### Planned_Progress
Expected completion percentage by the latest update.
Type: Decimal Percentage

### Actual_Progress
Observed completion percentage by the latest update.
Type: Decimal Percentage

### Schedule_Variance
Difference between actual and planned progress.
Type: Decimal Percentage
Formula: Actual_Progress - Planned_Progress

### Budget_Variance
Difference between financial and physical progress.
Type: Decimal Percentage
Formula: Financial_Progress - Actual_Progress

### Delay_Days
Estimated or realized delay in days for delayed projects.
Type: Integer

### Status
Portfolio execution status.
Type: Categorical String
Values: Not Started, In Progress, Completed, Delayed, On Hold

### Schedule_Status
Schedule performance band.
Type: Categorical String
Values: Ahead of Schedule, On Track, Slightly Delayed, Delayed, Critical Delay, Completed

### Budget_Status
Budget performance band.
Type: Categorical String
Values: Under Budget, On Budget, Watch, Over Budget

### Risk_Level
Overall project risk classification.
Type: Categorical String
Values: Low, Medium, High, Critical

### Project_Health_Score
Composite project health score from 0 to 100.
Type: Decimal
Method: Weighted score using schedule performance, budget performance, progress alignment, and risk level.

### Health_Status
Health category derived from Project_Health_Score.
Type: Categorical String
Values: Healthy, Monitor, At Risk, Critical

### Priority
Management priority classification.
Type: Categorical String
Values: Low, Medium, High, Strategic

### Latitude
Approximate project latitude inside Jeddah.
Type: Decimal

### Longitude
Approximate project longitude inside Jeddah.
Type: Decimal

### Last_Update
Latest reporting date for the record.
Type: Date (YYYY-MM-DD)

### Notes
Short operational note or management remark.
Type: String

## contractors.csv / contractors.json

### Contractor_ID
Unique contractor identifier.
Type: String

### Contractor_Name
Contractor name.
Type: String

### Total_Projects
Number of assigned projects.
Type: Integer

### Completed_Projects
Number of completed projects.
Type: Integer

### Active_Projects
Number of active projects with status In Progress or Delayed.
Type: Integer

### Delayed_Projects
Number of assigned projects with status Delayed.
Type: Integer

### On_Hold_Projects
Number of assigned projects with status On Hold.
Type: Integer

### Total_Contract_Value
Total contract value across assigned projects.
Type: Integer

### Average_Project_Value
Average contract value across assigned projects.
Type: Integer

### Average_Progress
Average actual progress across assigned projects.
Type: Decimal Percentage

### Average_Schedule_Variance
Average schedule variance across assigned projects.
Type: Decimal Percentage

### Average_Delay_Days
Average delay days across assigned projects.
Type: Decimal

### Average_Health_Score
Average project health score across assigned projects.
Type: Decimal

### Contractor_Performance_Score
Composite contractor performance score.
Type: Decimal
Method: Weighted mix of health, progress, schedule, and delayed/on-hold project ratios.

### Performance_Category
Performance band derived from Contractor_Performance_Score.
Type: Categorical String
Values: Excellent, Good, Needs Attention, Poor

## sectors.json

### Sector
Sector name.
Type: String

### Total_Projects
Number of projects in the sector.
Type: Integer

### Total_Contract_Value
Total contract value for the sector.
Type: Integer

### Total_Budget
Total approved budget for the sector.
Type: Integer

### Total_Spent
Total spent amount for the sector.
Type: Integer

### Average_Progress
Average actual progress for sector projects.
Type: Decimal Percentage

### Completed_Projects
Completed projects in the sector.
Type: Integer

### Delayed_Projects
Delayed projects in the sector.
Type: Integer

### Average_Health_Score
Average project health score for the sector.
Type: Decimal

## districts.json

### District
District name in Jeddah.
Type: String

### Total_Projects
Number of projects in the district.
Type: Integer

### Total_Contract_Value
Total contract value in the district.
Type: Integer

### Average_Progress
Average actual progress in the district.
Type: Decimal Percentage

### Completed_Projects
Completed projects in the district.
Type: Integer

### Delayed_Projects
Delayed projects in the district.
Type: Integer

### Critical_Projects
Projects with Health_Status equal to Critical.
Type: Integer

## project_managers.json

### Project_Manager_ID
Unique project manager identifier.
Type: String

### Project_Manager_Name
Project manager name.
Type: String

### Total_Projects
Number of assigned projects.
Type: Integer

### Completed_Projects
Completed assigned projects.
Type: Integer

### Delayed_Projects
Delayed assigned projects.
Type: Integer

### Total_Project_Value
Total assigned contract value.
Type: Integer

### Average_Progress
Average actual progress across assigned projects.
Type: Decimal Percentage

### Average_Health_Score
Average health score across assigned projects.
Type: Decimal

## monthly_progress.csv

### Date
Monthly reporting date.
Type: Date (YYYY-MM-DD)

### Project_ID
Project identifier.
Type: String

### Project_Name
Project name.
Type: String

### Planned_Progress
Planned cumulative progress for the reporting month.
Type: Decimal Percentage

### Actual_Progress
Actual cumulative progress for the reporting month.
Type: Decimal Percentage

### Progress_Variance
Difference between actual and planned cumulative progress.
Type: Decimal Percentage
Formula: Actual_Progress - Planned_Progress

## monthly_financials.csv

### Date
Monthly reporting date.
Type: Date (YYYY-MM-DD)

### Project_ID
Project identifier.
Type: String

### Project_Name
Project name.
Type: String

### Planned_Spend
Planned spend during the month.
Type: Integer

### Actual_Spend
Actual spend during the month.
Type: Integer

### Cumulative_Planned_Spend
Planned cumulative spend by the reporting month.
Type: Integer

### Cumulative_Actual_Spend
Actual cumulative spend by the reporting month.
Type: Integer

### Financial_Variance
Difference between cumulative actual and planned spend.
Type: Integer
Formula: Cumulative_Actual_Spend - Cumulative_Planned_Spend

## dashboard_summary.json

Contains portfolio-level KPIs calculated from projects.csv for direct dashboard initialization.
Type: JSON Object
