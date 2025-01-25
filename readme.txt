I've an optimization problem. 

I have a list of doctors, the procedures they can perform, the duration for each procedure, the revenue for each procedure, and the number of hours available for each doctor.
All procedures can be run in theatre 1. Not all procedures can be run in theatre 2.

I have created a file listing all possible combinations of doctors performing procedures (with given durations, and revenues) in either theatre 1 or theatre 2.

Each doctor has a revenue target outlined in "doctor_revenue_target.csv". 
Each doctor has a limited number of hours available: "doctors_hours.csv".
Each event in the combinations file can be run multiple times. i.e. a doctor can perform the same procedure multiple times.

Given that the maximum duration for each theatre is 55 hours each, what combination of events will lead to a maximum total "Procedure revenue" while adhereing to all conditions above?

I used GitHub Copilot to produce the code.

It produced the following output:

Status: Optimal
Total Revenue: 669230.0
Event 4: 10.0 times
Event 5: 2.0 times
Event 7: 67.0 times
Event 11: 1.0 times
Event 15: 3.0 times
Event 18: 1.0 times
Event 19: 41.0 times

I checked the output in Excel and found the following:

1. Theatre Hours
Total hours for Theatre 1 = 55
Total hours for Theatre 2 = 51.5
Total hours less than or equal to 55 hours each? TRUE

2. Revenue Target
Doctor	Doctor weekly revenue Target	Check
Bl	 125,000 	 127,950 
ST	 75,000 	 309,200 
MO	 25,000 	 35,685 
IT	 12,500 	 196,395 

TRUE

3. Doctor's Hours
Doctor	Doctor Hours avail	Check
Bl	36	36
ST	36	36
MO	12	10.5
IT	24	24

TRUE

Conclusion:
Problem is optimized with given constraints.
Total revenue = £669,230