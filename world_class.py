import matplotlib.pyplot as plt
import numpy as np
from person_class import Person
from account_class import Account

# World class defines the variables global to the people in the world. Also controls time dependant elements.
class World:
    def __init__(self, name, type, years=100, date=[11,2023]):
        self.name = name
        self.months = years*12
        self.fed_income_tax = [[0,9950,40525,86375,164925,209425,523600,float('inf')],[.1,.12,.22,.24,.32,.35,.37,1]]
        self.capital_gains_tax = [[0,40401,445851,float('inf')],[0,.15,.2,1]]
        self.date = date
        self.start = 0
        self.end = float(years) + 0.0833
        self.timeline = np.arange(0,self.end,1/12).tolist()

        self.people = []

        # Type is used to define the world **
        if "Normal" in type:
            self.inflation = 0.0311
            self.index_return = 0.095 

        if "Weak returns" in type:
            self.inflation = 0.0311
            self.index_return = 0.07 
        
        if "NJ" in type:
            self.state_income_tax = [[0,20000,35000,40000,75000,500000,5000000,float('inf')],[.014,.0175,.035,.0553,.0637,.0897,.1075,1]]

    # Adds people to the people list
    def add(self,person):
        self.people.append(person)
        if len(self.people)==1:
            self.start = person.age
        else:
            if self.start > person.age:
                self.start = person.age
        
        self.timeline = np.arange(self.start,self.end,1/12).tolist()
        self.months = len(self.timeline)

    # Progresses time for all people and accounts in world **
    def tick(self):
        for person in self.people:
            if "Aggro" in person.strategy:
                after_tax_income = person.find_after_tax_income()
                if after_tax_income > person.expenses:
                    #income_temp = person.income
                    person.make_contributions() #includes taxes
                    person.pay_expenses()
                    person.pay_debts()
                    person.invest()
                    person.accounts_appreciate()
                    person.incease_expenses()

                else:
                    person.take_withdraws() #includes taxes
                    person.pay_expenses()
                    person.pay_debts()
                    person.accounts_appreciate()
                    person.incease_expenses()
            
            if self.date[0] == 12:
                person.get_raise()
                person.age += 1
                if person.age == person.retirement_age:
                    person.income = 0
        if self.date[0] == 12:   
            self.date[0] = 0

        self.date[0] += 1
    
    def save_data(self):
        for person in self.people:
            person.log_graph_data() 