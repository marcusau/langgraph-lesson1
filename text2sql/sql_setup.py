from sqlalchemy import create_engine,Table, MetaData, Column, String, Date, Integer, Float,insert,text
from datetime import datetime
from random import randint


metadata = MetaData()
db_engine = create_engine("sqlite:///employees.db")


# employees_table = Table(
#     "employees", metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("first_name", String(50), nullable=False),
#     Column("last_name", String(50), nullable=False),
#     Column("email", String(100), unique=True, nullable=False),
#     Column("phone_number", String(15)),
#     Column("hire_date", Date, nullable=False),
#     Column("job_title", String(50), nullable=False),
#     Column("salary", Float, nullable=False),
#     Column("department_id", Integer)
# )

#######################################################################################################


# # Drop the table if it exists
# employees_table.drop(db_engine, checkfirst=True)
# metadata.create_all(db_engine)
###########################################################################################################
if __name__ == "__main__":
    with db_engine.begin() as connection:
        result = connection.execute(text("select * from employees")).fetchall()
    print(result)

##################################################################################################

# Dummy data
# employees = [
#     ['John', 'Doe', 'john.doe@example.com', '123-456-7890', datetime(2021, 5, 1), 'Software Engineer', 70000, 2],
#     ['Jane', 'Smith', 'jane.smith@example.com', '234-567-8901', datetime(2020, 8, 15), 'HR Manager', 80000, 1],
#     ['Jim', 'Beam', 'jim.beam@example.com', '345-678-9012', datetime(2019, 11, 3), 'Sales Representative', 50000, 3],
#     ['Jessica', 'Jones', 'jessica.jones@example.com', '456-789-0123', datetime(2018, 4, 23), 'Marketing Specialist', 60000, 4],
#     ['Michael', 'Brown', 'michael.brown@example.com', '567-890-1234', datetime(2022, 1, 9), 'DevOps Engineer', 75000, 2],
#     ['Emily', 'Davis', 'emily.davis@example.com', '678-901-2345', datetime(2021, 3, 11), 'Product Manager', 85000, 4],
#     ['Daniel', 'Wilson', 'daniel.wilson@example.com', '789-012-3456', datetime(2020, 10, 30), 'Data Scientist', 95000, 2],
#     ['Sophia', 'Taylor', 'sophia.taylor@example.com', '890-123-4567', datetime(2021, 6, 7), 'Recruiter', 55000, 1],
#     ['Lucas', 'Martinez', 'lucas.martinez@example.com', '901-234-5678', datetime(2019, 2, 18), 'Sales Manager', 70000, 3],
#     ['Olivia', 'Garcia', 'olivia.garcia@example.com', '012-345-6789', datetime(2023, 7, 20), 'Junior Developer', 50000, 2]
# ]

# with db_engine.begin() as connection:
#     for emp in employees:
#         query = insert(employees_table).values(
#             id=randint(10000, 99999),
#             first_name=emp[0],
#             last_name=emp[1],
#             email=emp[2],
#             phone_number=emp[3],
#             hire_date=emp[4],
#             job_title=emp[5],
#             salary=emp[6],
#             department_id=emp[7]
#         )
#         connection.execute(query)
# print("Data inserted Successfully")