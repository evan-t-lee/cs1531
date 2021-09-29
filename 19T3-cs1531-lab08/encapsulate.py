from datetime import datetime

class Student:
    def __init__(self, firstName, lastName, birth_year):
        # standardise strings (use f strings throughout)
        self.name = f"{firstName} {lastName}"
        self.birth_year = birth_year

    # dont access class attributes directly, use methods
    def get_name(self):
        return self.name

    def get_birth_year(self):
        return self.birth_year

# abstract calculation of age into function
def calculate_age(birth_year):
    # getting current year is now dynamic (wont break when year changes)
    curr_year = datetime.now().year
    age = curr_year - birth_year
    return age

if __name__ == '__main__':
    s = Student("Rob", "Everest", 1961)
    years_old = calculate_age(s.get_birth_year())
    # fix grammar
    print(f"{s.get_name()} is {years_old} year/s old")