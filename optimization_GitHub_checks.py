import pandas as pd
import pulp

# Load data
combinations = pd.read_csv('combinations.csv')
doctor_revenue_target = pd.read_csv('doctor_revenue_target.csv')
doctors_hours = pd.read_csv('doctors_hours.csv')

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("Event", combinations.ID, lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([x[i] * combinations.loc[i-1, 'Procedure Revenue'] for i in combinations.ID]), "Total_Revenue"

# Constraints for doctors' hours
doctor_hours = doctors_hours.set_index('Doctor')['Doctor Hours avail'].to_dict()
for doctor in doctor_hours:
    problem += pulp.lpSum([x[i] * combinations.loc[i-1, 'Duration'] for i in combinations.ID if combinations.loc[i-1, 'Doctor'] == doctor]) <= doctor_hours[doctor], f"{doctor}_hours_constraint"

# Constraints for theatres' hours
for theatre in ['Theatre 1', 'Theatre 2']:
    problem += pulp.lpSum([x[i] * combinations.loc[i-1, 'Duration'] for i in combinations.ID if combinations.loc[i-1, 'Theatre'] == theatre]) <= 55, f"{theatre}_hours_constraint"

# Constraints for doctors' revenue targets
doctor_revenue_targets = doctor_revenue_target.set_index('Doctor')['Doctor weekly revenue Target'].to_dict()
for doctor in doctor_revenue_targets:
    problem += pulp.lpSum([x[i] * combinations.loc[i-1, 'Procedure Revenue'] for i in combinations.ID if combinations.loc[i-1, 'Doctor'] == doctor]) >= doctor_revenue_targets[doctor], f"{doctor}_revenue_constraint"

# Solve the problem
problem.solve()

# Print the results
print("Status:", pulp.LpStatus[problem.status])
#print("Total Revenue:", pulp.value(problem.objective))
num1 = pulp.value(problem.objective)
#print('Total Revenue: £{:0,.0f}'.format(num1))

# Summarize the results in a dataframe
results = pd.DataFrame({
    'ID': combinations.ID,
    'Doctor': combinations.Doctor,
    'Procedure': combinations.Procedure,
    'Theatre': combinations.Theatre,
    'Duration': combinations.Duration,
    'Procedure Revenue': combinations['Procedure Revenue'],
    'Scheduled Times': [x[i].varValue for i in combinations.ID]
})

print(results[results['Scheduled Times'] > 0])

# Verify all constraints are satisfied
for doctor in doctor_hours:
    total_hours = sum([x[i].varValue * combinations.loc[i-1, 'Duration'] for i in combinations.ID if combinations.loc[i-1, 'Doctor'] == doctor])
    print(f"Total hours for {doctor}: {total_hours} (Max: {doctor_hours[doctor]})")

for doctor in doctor_revenue_targets:
    total_revenue = sum([x[i].varValue * combinations.loc[i-1, 'Procedure Revenue'] for i in combinations.ID if combinations.loc[i-1, 'Doctor'] == doctor])
    total_revenue = '£{:0,.0f}'.format(total_revenue)
    doctor_revenue_targets[doctor]= '£{:0,.0f}'.format(doctor_revenue_targets[doctor])
    print(f"Total revenue for {doctor}: {total_revenue} (Target: {doctor_revenue_targets[doctor]})")

for theatre in ['Theatre 1', 'Theatre 2']:
    total_hours = sum([x[i].varValue * combinations.loc[i-1, 'Duration'] for i in combinations.ID if combinations.loc[i-1, 'Theatre'] == theatre])
    print(f"Total hours in {theatre}: {total_hours} (Max: 55)")
    
print('Total Revenue: £{:0,.0f}'.format(num1))