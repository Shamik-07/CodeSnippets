"""This class creates new employee records."""
"""This code has been gleaned from [here](https://github.com/CoreyMSchafer/code_snippets/blob/master/Object-Oriented/3-Class-Static-Methods/oop.py)."""

class Employee(object):
    
    num_of_employees = 10
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@email.com'
        self.pay = pay

        Employee.num_of_emps += 1

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

if __name__ == "__main__":
    import datetime
    emp_11 = Employee('Bambino', 'Jones', 50000)
    emp_12 = Employee('Test', 'Employee', 60000)

    Employee.set_raise_amt(1.05)

    print(Employee.raise_amount)
    print(emp_11.raise_amount)
    print(emp_12.raise_amount)

    emp_str_21 = 'John-Doe-70000'
    emp_str_22 = 'Steve-Smith-30000'
    emp_str_23 = 'Jane-Doe-90000'

    first, last, pay = emp_str_21.split('-')

    new_emp_21 = Employee.from_string(emp_str_21)

    print(new_emp_21.email)
    print(new_emp_21.pay)

    
    my_date = datetime.datetime.today()

    print(Employee.is_workday(my_date))
