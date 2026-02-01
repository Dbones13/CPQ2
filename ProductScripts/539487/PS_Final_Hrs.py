def get_total_final_hours(container):
    """Helper function to get the total final hours from a container."""
    return sum(float(row["Final Hrs"]) for row in container.Rows if row["Final Hrs"])

# Define the container names
container_names = ["PRMS_Engineering_Labor_Container", "PRMS_Engineering_Labor_Container"]

# Initialize total final hours
total_final_hours = 0.0

# Iterate over the container names and accumulate the total final hours
for container_name in container_names:
    container = Product.GetContainerByName(container_name)
    if container:
        total_final_hours += get_total_final_hours(container)
        Trace.Write("total_final_hours: " + str(total_final_hours))

# Round the total final hours
total_final_hours = round(total_final_hours)
Trace.Write("total_final_hours"+str(total_final_hours))

# Assign the final hours to a variable or use it as needed
Final_Hrs = total_final_hours
Trace.Write("Final_Hrs"+str(Final_Hrs))
Product.Attr('Final_Hrs').AssignValue(str(Final_Hrs))