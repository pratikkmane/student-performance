import pandas as pd
import numpy as np

# Create large test file
np.random.seed(42)
num_rows = 1200

data = {
    'age': np.random.randint(15, 23, num_rows),
    'Medu': np.random.randint(1, 5, num_rows),
    'Fedu': np.random.randint(1, 5, num_rows),
    'traveltime': np.random.randint(1, 5, num_rows),
    'studytime': np.random.randint(1, 5, num_rows),
    'failures': np.random.randint(0, 5, num_rows),
    'famrel': np.random.randint(1, 6, num_rows),
    'freetime': np.random.randint(1, 6, num_rows),
    'goout': np.random.randint(1, 6, num_rows),
    'Dalc': np.random.randint(1, 6, num_rows),
    'Walc': np.random.randint(1, 6, num_rows),
    'health': np.random.randint(1, 6, num_rows),
    'absences': np.random.randint(0, 94, num_rows),
    'school_MS': np.random.randint(0, 2, num_rows),
    'sex_M': np.random.randint(0, 2, num_rows),
    'address_U': np.random.randint(0, 2, num_rows),
    'famsize_LE3': np.random.randint(0, 2, num_rows),
    'Pstatus_T': np.random.randint(0, 2, num_rows),
    'Mjob_health': np.random.randint(0, 2, num_rows),
    'Mjob_other': np.random.randint(0, 2, num_rows),
    'Mjob_services': np.random.randint(0, 2, num_rows),
    'Mjob_teacher': np.random.randint(0, 2, num_rows),
    'Fjob_health': np.random.randint(0, 2, num_rows),
    'Fjob_other': np.random.randint(0, 2, num_rows),
    'Fjob_services': np.random.randint(0, 2, num_rows),
    'Fjob_teacher': np.random.randint(0, 2, num_rows),
    'reason_home': np.random.randint(0, 2, num_rows),
    'reason_other': np.random.randint(0, 2, num_rows),
    'reason_reputation': np.random.randint(0, 2, num_rows),
    'guardian_mother': np.random.randint(0, 2, num_rows),
    'guardian_other': np.random.randint(0, 2, num_rows),
    'schoolsup_yes': np.random.randint(0, 2, num_rows),
    'famsup_yes': np.random.randint(0, 2, num_rows),
    'paid_yes': np.random.randint(0, 2, num_rows),
    'activities_yes': np.random.randint(0, 2, num_rows),
    'nursery_yes': np.random.randint(0, 2, num_rows),
    'higher_yes': np.random.randint(0, 2, num_rows),
    'internet_yes': np.random.randint(0, 2, num_rows),
    'romantic_yes': np.random.randint(0, 2, num_rows),
    'subject_portuguese': np.random.randint(0, 2, num_rows),
    'parent_edu_avg': np.random.uniform(1, 4, num_rows),
    'total_alcohol': np.random.randint(1, 11, num_rows),
    'has_support': np.random.randint(0, 2, num_rows),
}

df = pd.DataFrame(data)
df.to_csv('test_large_batch.csv', index=False)
print(f"Created test_large_batch.csv with {len(df)} rows")
