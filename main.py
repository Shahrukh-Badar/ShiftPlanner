import pandas as pd
import random
import datetime as dt
import numpy as np

pd.options.display.max_columns = None
pd.options.display.max_rows = None

# Configurable data
numberOfEmployee = 10
numberOfShift = 40
shiftStartDateTime = dt.datetime(2020, 8, 1)
shiftEndDateTime = dt.datetime(2020, 8, 5)


# Generate randamshift of given duration
def generateShiftDuration():
    # randomYear = random.randrange(int(shiftStartDateTime.strftime("%Y")), int(shiftEndDateTime.strftime("%Y")))
    # randomMonth = random.randrange(int(shiftStartDateTime.strftime("%m")), int(shiftEndDateTime.strftime("%m")))
    randomDay = random.randrange(int(shiftStartDateTime.strftime("%d")), int(shiftEndDateTime.strftime("%d")))
    randomHour = random.randrange(1, 20)
    randomshiftStartDateTime = dt.datetime(2020, 8, randomDay, randomHour)
    randomshiftEndDateTime = randomshiftStartDateTime + dt.timedelta(hours=2)
    return list([randomshiftStartDateTime, randomshiftEndDateTime])


# Check overlapping of date ranges
def isDateOverlapped(startShiftDate1, endShiftDate1, startShiftDate2, endShiftDate2):
    from collections import namedtuple
    Range = namedtuple('Range', ['start', 'end'])

    r1 = Range(start=startShiftDate1, end=endShiftDate1)
    r2 = Range(start=startShiftDate2, end=endShiftDate2)
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    delta = (earliest_end - latest_start).days + 1
    overlap = max(0, delta)
    if (overlap > 0):
        return True
    else:
        return False


dfEmployee = pd.DataFrame(columns=["empID", "name", "desiredEarnings"])
dfShift = pd.DataFrame(columns=["shiftID", "start", "end", "hourlyEarnings", "assignedEmployee", "isAssigned"])

# Generate Random Employee
for x in range(numberOfEmployee):
    employeeName = "Employee" + str(x)
    employeeDesiredSalary = random.randrange(30, 91)
    dfEmployee = dfEmployee.append({"empID": str(x), "name": employeeName, "desiredEarnings": employeeDesiredSalary},
                                   ignore_index=True)

# Generate Random Shift Data
for x in range(numberOfShift):
    shiftTempDuration = generateShiftDuration()
    start = shiftTempDuration[0]
    end = shiftTempDuration[1]
    hourlyEarnings = random.randrange(1, 11)
    employee = np.NaN
    isAssigned = False
    dfShift = dfShift.append(
        {"shiftID": str(x), "start": start, "end": end, "hourlyEarnings": hourlyEarnings, "assignedEmployee": employee,
         "isAssigned": isAssigned},
        ignore_index=True)

# Iterate over shifts
iteratorEmployee = 0

for index, row in dfShift.iterrows():
    currentEmployee = dfEmployee.iloc[iteratorEmployee]
    currentEmployeeDesiredEarning = currentEmployee["desiredEarnings"]
    currentEmployeeName = currentEmployee["name"]
    # Get all employess shift
    dfEmployeeShifts = dfShift.loc[dfShift["assignedEmployee"] == currentEmployeeName]

    if (dfEmployeeShifts.shape[0] == 0):
        dfShift.at[index, "assignedEmployee"] = currentEmployeeName
        row["isAssigned"] = True
        print(currentEmployeeName + ", First Shift Assigned: " + str(row["start"]) + " " + str(row["end"]))
    else:
        totalEarnings = dfEmployeeShifts['hourlyEarnings'].sum()
        isOverlapExisting = False
        for empInd, empRow in dfEmployeeShifts.iterrows():
            if (isDateOverlapped(empRow["start"], empRow["end"], row["start"], row["end"])):
                print(currentEmployeeName + ", shift " + str(row["start"]) + " " + str(
                    row["end"]) + " is overlapping existing shift" + str(empRow["start"]) + " " + str(empRow["end"]))
                isOverlapExisting = True

        if (isOverlapExisting != True):
            if (totalEarnings + row["hourlyEarnings"] <= currentEmployeeDesiredEarning):
                dfShift.at[index, "assignedEmployee"] = currentEmployeeName
                row["isAssigned"] = True
                print(currentEmployeeName + ", Shift Assigned: " + str(row["start"]) + " " + str(row["end"]))

    iteratorEmployee += 1
    if (iteratorEmployee == numberOfEmployee):
        iteratorEmployee = 0

for index, row in dfShift.iterrows():
    print("Shift " + str(row["shiftID"]) + " [" + str(row["start"]) + " " + str(
        row["end"]) + " has been assigned to employee: " + str(
        row["assignedEmployee"]))

for index, row in dfEmployee.iterrows():
    totalEarnings = dfShift.loc[dfShift['assignedEmployee'] == row["name"], 'hourlyEarnings'].sum()
    print(row["name"] + ", desired earning: " + str(row["desiredEarnings"]) + " and actual earning: " + str(
        totalEarnings))
