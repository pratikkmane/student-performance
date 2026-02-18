# Student Performance Dataset - Data Dictionary

**Dataset:** UCI Student Performance Dataset  
**Source:** Two Portuguese secondary schools (Gabriel Pereira and Mousinho da Silveira)  
**Records:** 1,044 student-course enrollments (Math: 395, Portuguese: 649)  
**Total Features:** 33 attributes

---

## Feature Documentation

### 1. school
- **What it measures:** Which secondary school the student attends
- **Data type:** Categorical (Binary)
- **Values:** "GP" (Gabriel Pereira) or "MS" (Mousinho da Silveira)
- **Range:** 2 possible values
- **Why it predicts performance:** Different schools may have varying academic standards, teaching quality, student resources, and educational culture

---

### 2. sex
- **What it measures:** Student's biological sex
- **Data type:** Categorical (Binary)
- **Values:** "F" (Female) or "M" (Male)
- **Range:** 2 possible values
- **Why it predicts performance:** Research shows gender differences in performance across subjects (e.g., STEM vs humanities); different study patterns and social expectations may affect outcomes

---

### 3. age
- **What it measures:** Student's current age in years
- **Data type:** Numeric (Discrete)
- **Values:** Integer values
- **Range:** 15 to 22 years
- **Why it predicts performance:** Older students in the same grade level may indicate grade repetition or late start; maturity level affects learning ability and motivation

---

### 4. address
- **What it measures:** Type of residential area where student lives
- **Data type:** Categorical (Binary)
- **Values:** "U" (Urban) or "R" (Rural)
- **Range:** 2 possible values
- **Why it predicts performance:** Urban students typically have better access to educational resources, libraries, tutoring centers, and study facilities; rural students may face transportation challenges

---

### 5. famsize
- **What it measures:** Size of student's family
- **Data type:** Categorical (Binary)
- **Values:** "LE3" (≤3 members) or "GT3" (>3 members)
- **Range:** 2 possible values
- **Why it predicts performance:** Family size affects resource allocation per child; smaller families may provide more focused attention and financial support for education

---

### 6. Pstatus
- **What it measures:** Parents' cohabitation status
- **Data type:** Categorical (Binary)
- **Values:** "T" (Together - married/partnered) or "A" (Apart - separated/divorced)
- **Range:** 2 possible values
- **Why it predicts performance:** Family stability affects emotional well-being, study environment, and financial resources; separation may cause stress and distraction

---

### 7. Medu
- **What it measures:** Mother's education level
- **Data type:** Numeric (Ordinal)
- **Values:** 0=none, 1=primary (4th grade), 2=5th-9th grade, 3=secondary, 4=higher education
- **Range:** 0 to 4
- **Why it predicts performance:** Maternal education strongly correlates with student achievement; educated mothers can help with homework, emphasize education's value, and create supportive learning environments

---

### 8. Fedu
- **What it measures:** Father's education level
- **Data type:** Numeric (Ordinal)
- **Values:** 0=none, 1=primary (4th grade), 2=5th-9th grade, 3=secondary, 4=higher education
- **Range:** 0 to 4
- **Why it predicts performance:** Similar to Medu; parental education indicates socioeconomic status, educational values, and ability to provide academic support

---

### 9. Mjob
- **What it measures:** Mother's occupation/job
- **Data type:** Categorical (Nominal)
- **Values:** "teacher", "health", "services", "at_home", "other"
- **Range:** 5 possible values
- **Why it predicts performance:** Occupation indicates socioeconomic status, work schedule (availability to help with studies), and educational role modeling

---

### 10. Fjob
- **What it measures:** Father's occupation/job
- **Data type:** Categorical (Nominal)
- **Values:** "teacher", "health", "services", "at_home", "other"
- **Range:** 5 possible values
- **Why it predicts performance:** Similar to Mjob; combined with parental education gives complete picture of family's socioeconomic status and resources

---

### 11. reason
- **What it measures:** Student's reason for choosing this particular school
- **Data type:** Categorical (Nominal)
- **Values:** "home" (proximity), "reputation" (school quality), "course" (program preference), "other"
- **Range:** 4 possible values
- **Why it predicts performance:** Students choosing schools for academic reasons (reputation, course) may be more motivated than those choosing for convenience (proximity)

---

### 12. guardian
- **What it measures:** Student's primary guardian/caretaker
- **Data type:** Categorical (Nominal)
- **Values:** "mother", "father", "other"
- **Range:** 3 possible values
- **Why it predicts performance:** Indicates family structure and who provides educational oversight; "other" guardians may signal less stable home environment

---

### 13. traveltime
- **What it measures:** Daily commute time from home to school
- **Data type:** Numeric (Ordinal)
- **Values:** 1=<15min, 2=15-30min, 3=30min-1hr, 4=>1hr
- **Range:** 1 to 4
- **Why it predicts performance:** Long commutes reduce available study time, increase fatigue, and limit participation in after-school activities and study groups

---

### 14. studytime
- **What it measures:** Weekly study time outside of regular classes
- **Data type:** Numeric (Ordinal)
- **Values:** 1=<2hrs/week, 2=2-5hrs/week, 3=5-10hrs/week, 4=>10hrs/week
- **Range:** 1 to 4
- **Why it predicts performance:** Direct measure of academic effort; more study time typically correlates with better understanding and higher grades

---

### 15. failures
- **What it measures:** Number of past class failures in previous years
- **Data type:** Numeric (Discrete)
- **Values:** 0, 1, 2, 3, or 4 (where 4 = three or more failures)
- **Range:** 0 to 4
- **Why it predicts performance:** Past academic failure is one of the strongest predictors of future struggles; indicates accumulated knowledge gaps and possible learning difficulties

---

### 16. schoolsup
- **What it measures:** Receiving extra educational support from school
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Indicates both struggling students (need support) and available interventions; mixed signal as support can improve outcomes

---

### 17. famsup
- **What it measures:** Family provides educational support at home
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Direct measure of family involvement; students with engaged families typically perform better due to homework help and encouragement

---

### 18. paid
- **What it measures:** Taking extra paid classes/tutoring in the subject
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Shows family financial investment in education and/or student's need for extra help; wealthier families can afford additional tutoring

---

### 19. activities
- **What it measures:** Participation in extracurricular activities
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Extracurriculars develop skills and school engagement, but may reduce study time; research shows mixed effects on grades

---

### 20. nursery
- **What it measures:** Attended nursery school (preschool)
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Early childhood education provides academic foundation; indicates family prioritizes education from young age

---

### 21. higher
- **What it measures:** Desires to pursue higher education (university/college)
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Strong indicator of motivation and future orientation; students planning for university work harder in secondary school

---

### 22. internet
- **What it measures:** Internet access available at home
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Internet enables research, online learning resources, and homework submission; also indicates household's socioeconomic status

---

### 23. romantic
- **What it measures:** Currently in a romantic relationship
- **Data type:** Categorical (Binary)
- **Values:** "yes" or "no"
- **Range:** 2 possible values
- **Why it predicts performance:** Romantic relationships can be distracting and time-consuming during adolescence; may reduce focus on academics

---

### 24. famrel
- **What it measures:** Quality of family relationships
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very bad, 2=bad, 3=neutral, 4=good, 5=excellent
- **Range:** 1 to 5
- **Why it predicts performance:** Positive family relationships provide emotional support and stable environment for studying; family conflict creates stress

---

### 25. freetime
- **What it measures:** Amount of free time after school
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very low, 2=low, 3=medium, 4=high, 5=very high
- **Range:** 1 to 5
- **Why it predicts performance:** Balance needed - too little free time causes burnout; too much may indicate lack of engagement or poor time management

---

### 26. goout
- **What it measures:** Frequency of going out with friends
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very low, 2=low, 3=medium, 4=high, 5=very high
- **Range:** 1 to 5
- **Why it predicts performance:** Excessive socializing reduces study time; complete isolation may indicate social problems; moderate levels are healthiest

---

### 27. Dalc
- **What it measures:** Workday alcohol consumption (Monday-Friday)
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very low, 2=low, 3=medium, 4=high, 5=very high
- **Range:** 1 to 5
- **Why it predicts performance:** Alcohol consumption during school week directly impacts attendance, focus, and cognitive function; indicator of risky behavior

---

### 28. Walc
- **What it measures:** Weekend alcohol consumption (Saturday-Sunday)
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very low, 2=low, 3=medium, 4=high, 5=very high
- **Range:** 1 to 5
- **Why it predicts performance:** While less direct than Dalc, weekend drinking may indicate behavioral issues and affect Monday performance; part of lifestyle pattern

---

### 29. health
- **What it measures:** Current health status
- **Data type:** Numeric (Ordinal scale)
- **Values:** 1=very bad, 2=bad, 3=neutral, 4=good, 5=very good
- **Range:** 1 to 5
- **Why it predicts performance:** Poor health leads to absences and reduced focus; chronic conditions affect energy and ability to concentrate

---

### 30. absences
- **What it measures:** Number of school absences during the academic year
- **Data type:** Numeric (Discrete count)
- **Values:** Integer count of absent days
- **Range:** 0 to 93 days
- **Why it predicts performance:** Missing class means missing instruction; excessive absences create knowledge gaps and reduce learning opportunities

---

### 31. G1
- **What it measures:** First period grade (1st trimester/quarter)
- **Data type:** Numeric (Continuous)
- **Values:** Grade on 0-20 scale
- **Range:** 0 to 20
- **Why it predicts performance:** First-term performance strongly predicts final outcomes; early grades show initial mastery and effort

---

### 32. G2
- **What it measures:** Second period grade (2nd trimester/quarter)
- **Data type:** Numeric (Continuous)
- **Values:** Grade on 0-20 scale
- **Range:** 0 to 20
- **Why it predicts performance:** Mid-year performance; combined with G1 provides strong prediction of final grade

---

### 33. G3
- **What it measures:** Final grade (end of year)
- **Data type:** Numeric (Continuous)
- **Values:** Grade on 0-20 scale
- **Range:** 0 to 20
- **Why it predicts performance:** This IS the target variable we're trying to predict; represents overall academic achievement for the course

---

## Summary Statistics

- **Total Features:** 33
- **Binary Features:** 17
- **Numeric Features:** 16
- **Nominal Categorical:** 4 (Mjob, Fjob, reason, guardian)
- **Grade Features:** 3 (G1, G2, G3)

---

## Feature Categories

### 📊 DEMOGRAPHICS (6 features)
Features describing basic student characteristics

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 1 | school | Binary | GP, MS | School identification |
| 2 | sex | Binary | F, M | Gender |
| 3 | age | Numeric | 15-22 | Student age |
| 4 | address | Binary | U, R | Urban vs Rural residence |
| 5 | famsize | Binary | LE3, GT3 | Family size |
| 6 | Pstatus | Binary | T, A | Parents together or apart |

**Why this category matters:** Demographics provide context about the student's basic situation and may reveal underlying socioeconomic factors.

---

### 👨‍👩‍👧 FAMILY BACKGROUND (6 features)
Features related to family socioeconomic status and support

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 7 | Medu | Numeric (0-4) | Education level | Mother's education |
| 8 | Fedu | Numeric (0-4) | Education level | Father's education |
| 9 | Mjob | Nominal | 5 categories | Mother's occupation |
| 10 | Fjob | Nominal | 5 categories | Father's occupation |
| 12 | guardian | Nominal | mother/father/other | Primary caretaker |
| 17 | famsup | Binary | yes/no | Family educational support |

**Why this category matters:** Family background is a strong predictor of academic success. Parent education and occupation indicate resources, values, and ability to provide academic support.

**Key predictors:** Medu and Fedu are particularly strong predictors of student performance.

---

### 🎓 SCHOOL-RELATED (9 features)
Features related to education, study habits, and school support

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 11 | reason | Nominal | 4 categories | Reason for school choice |
| 13 | traveltime | Numeric (1-4) | Ordinal scale | Commute time |
| 14 | studytime | Numeric (1-4) | Ordinal scale | Weekly study hours |
| 15 | failures | Numeric (0-4) | Count | Past class failures |
| 16 | schoolsup | Binary | yes/no | Extra school support |
| 18 | paid | Binary | yes/no | Paid extra classes |
| 19 | activities | Binary | yes/no | Extracurricular activities |
| 20 | nursery | Binary | yes/no | Attended preschool |
| 21 | higher | Binary | yes/no | Wants higher education |

**Why this category matters:** Direct indicators of academic engagement, effort, and past performance. These are actionable factors that interventions can target.

**Key predictors:** 
- **failures** - Strongest single predictor (past performance → future performance)
- **studytime** - Direct measure of effort
- **higher** - Indicator of motivation

---

### 🎉 SOCIAL & BEHAVIORAL (7 features)
Features related to lifestyle, social activities, and behavior

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 22 | internet | Binary | yes/no | Internet access at home |
| 23 | romantic | Binary | yes/no | In a relationship |
| 24 | famrel | Numeric (1-5) | Quality scale | Family relationship quality |
| 25 | freetime | Numeric (1-5) | Amount scale | Free time after school |
| 26 | goout | Numeric (1-5) | Frequency scale | Going out with friends |
| 27 | Dalc | Numeric (1-5) | Consumption scale | Workday alcohol use |
| 28 | Walc | Numeric (1-5) | Consumption scale | Weekend alcohol use |

**Why this category matters:** Social behaviors and lifestyle choices affect time available for studying and cognitive function. Risky behaviors (alcohol) are red flags.

**Key considerations:** These factors may be sensitive; some indicate risky behavior that needs intervention beyond academics.

---

### 🏥 HEALTH & ATTENDANCE (2 features)
Features related to physical health and school attendance

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 29 | health | Numeric (1-5) | Status scale | Current health status |
| 30 | absences | Numeric (0-93) | Count | Days absent from school |

**Why this category matters:** Health affects ability to attend and focus. Absences create learning gaps.

**Key predictor:** Absences directly impact learning opportunity - you can't learn if you're not there!

---

### 📈 GRADES - TARGET VARIABLES (3 features)
Performance measurements - these are what we're trying to predict

| # | Feature | Type | Values | Purpose |
|---|---------|------|--------|---------|
| 31 | G1 | Numeric (0-20) | Grade | First period grade |
| 32 | G2 | Numeric (0-20) | Grade | Second period grade |
| 33 | G3 | Numeric (0-20) | Grade | **FINAL GRADE (TARGET)** |

**Special note:** These are NOT features for prediction - they are outcomes.
- **G3** is our TARGET variable (what we want to predict)
- **G1 and G2** must be EXCLUDED for early intervention (not available at start of year)

---

## Category Summary

| Category | Count | Key Predictors | Actionable? |
|----------|-------|----------------|-------------|
| Demographics | 6 | age, address | ❌ Not changeable |
| Family Background | 6 | Medu, Fedu, famsup | ⚠️ Hard to change |
| School-Related | 9 | failures, studytime, higher | ✅ Can be targeted |
| Social/Behavioral | 7 | Dalc, Walc, goout | ✅ Can be influenced |
| Health/Attendance | 2 | absences | ✅ Can be reduced |
| Grades | 3 | G3 (target) | 🎯 What we predict |

**For interventions:** Focus on School-Related, Social/Behavioral, and Attendance factors - these can actually be changed through support programs!
