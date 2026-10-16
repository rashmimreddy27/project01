print("AI-Based Civic Issue Prioritisation")
print("-----------------------------------")

print("1. Potholes")
print("2. Garbage")
print("3. Water Leakage")
print("4. Broken Streetlights")

issue = input("Enter the issue number: ")

location = input("Enter the location: ")

print("\nSelect severity:")
print("1. High")
print("2. Medium")
print("3. Low")

severity = input("Enter severity number: ")

print("\n----- Complaint Details -----")

if issue == "1":
    print("Issue: Potholes")
elif issue == "2":
    print("Issue: Garbage")
elif issue == "3":
    print("Issue: Water Leakage")
elif issue == "4":
    print("Issue: Broken Streetlights")
else:
    print("Issue: Other")

print("Location:", location)

if severity == "1":
    print("Severity: High")
elif severity == "2":
    print("Severity: Medium")
elif severity == "3":
    print("Severity: Low")
else:
    print("Severity: Not specified")















