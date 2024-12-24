import matplotlib.pyplot as plt
import numpy as np
from account_class import Account

# People class defines the variable and accounts local to that individual 
class Person:
    def __init__(self, name, world, strategy, benefits, age=26, income=94003, raise_rate=0.044, expenses=72967, expenses_increase=0.01, retire=65):

        # Initallize variables
        self.name = name
        self.income = income
        self.age = age
        self.raise_rate = raise_rate
        self.expenses = expenses
        self.expenses_increase = expenses_increase
        self.world = world
        self.accounts = []
        self.strategy = strategy
        self.retirement_age = retire

        # Lists for graphs
        #self.income_list = (1+self.world.months) * [0]
        #self.take_home_list = (1+self.world.months) * [0]
        #self.expenses_list = (1+self.world.months) * [0]
        #self.net_worth_list = (1+self.world.months) * [0]
        #self.passive_income_list = (1+self.world.months) * [0]
        self.income_list = []
        self.take_home_list = []
        self.expenses_list = []
        self.net_worth_list = []
        self.passive_income_list = []

        # Basic Accounts
        checking = Account("Checking","checking",self.world)
        investments = Account("Investments","investments",self.world)
        checking.update_rate(0)

        self.add_account(checking)
        self.add_account(investments)
        
        # Strategy is used to define the decisions the person with make
        if "Aggro" in strategy:
            self.checking_goal = 1000
            self.roth_contribution_max = 6500
            self._401k_contribution_max = 22500

            self.contribution_order = []
            self.withdraw_order = ['Roth 401k','Roth IRA','Investments']

            roth_ira = Account("Roth IRA","roth IRA",self.world)
            self.add_account(roth_ira)
            self.roth_ira_remaining = self.roth_contribution_max
        
        if "401k" in benefits and "Aggro" in strategy:
            if " of " in benefits:
                benefits_split = benefits.split()
                self.match_percentage = float(benefits_split[benefits_split.index("of")-1])
                self.match_limit = float(benefits_split[benefits_split.index("of")+1])
                roth_401k = Account("Roth 401k","Roth 401k " + benefits_split[benefits_split.index("of")-1] + " of " + benefits_split[benefits_split.index("of")+1],self.world)
                self.total_employer_match = 0
                self.total_employer_match_max = float(self.income) * roth_401k.employer_match * roth_401k.match_limit
                self.match_remaining = self.total_employer_match_max
                self.add_account(roth_401k)
            else:    
                roth_401k = Account("Roth 401k","Roth 401k",self.world)
                self.add_account(roth_401k)

    # Adds new account to the account list
    def add_account(self,account):
        self.accounts.append(account)

    # Removes account to the account list
    def remove_account(self,account):
        self.accounts.remove(account)

    # Gets account from account list
    def find_account_idx(self,name):
        idx = 0
        for account in self.accounts:
            if account.name == name:
                return idx
            idx += 1
            
    # Transfer money from an account
    def account_transfer(self,account,amount):
        self.accounts[self.find_account_idx(account)].transfer(amount)
    
    # Returns account balance from account list
    def account_balance(self,account):
        return self.accounts[self.find_account_idx(account)].balance
    
    # Returns account history from account list
    def account_history(self,account):
        return self.accounts[self.find_account_idx(account)].history

    # Returns account
    def account_full(self,account):
        return self.accounts[self.find_account_idx(account)]

    # Uses raise rate to increase person's income
    def get_raise(self):
        self.income *= (self.raise_rate + 1)

    # Uses expense increase and inflasion to increase expenses
    def incease_expenses(self,months=1):
        #print((1+self.expenses_increase)**(months/12) * (1+self.world.inflation))
        self.expenses *= ((1+self.expenses_increase) * (1+self.world.inflation))**(months/12)

    # Find the persons affective tax rate
    def find_tax_rate(self,capital_gains=0):
        income_temp = self.income
        if capital_gains == 1:
            income_fed_paid,affective_fed_tax_rate = pay_tax(income_temp,self.world.capital_gains_tax)
            return affective_fed_tax_rate
        else:
            income_fed_paid,affective_fed_tax_rate = pay_tax(income_temp,self.world.fed_income_tax)
        income_state_paid,affective_state_tax_rate = pay_tax(income_temp,self.world.state_income_tax)
        return affective_fed_tax_rate + affective_state_tax_rate
    
    # Returns persons after tax income
    def find_after_tax_income(self):
        income_temp = self.income
        income_fed_paid,affective_fed_tax_rate = pay_tax(income_temp,self.world.fed_income_tax)
        income_state_paid,affective_state_tax_rate = pay_tax(income_temp,self.world.state_income_tax)
        tax_rate = affective_fed_tax_rate + affective_state_tax_rate
        return self.income * (1-tax_rate)
    
    # Determines which accounts to make contributions when employed
    def find_zone(self):
        after_tax_income = self.find_after_tax_income()
        if after_tax_income < self.expenses:
            return 1
        if after_tax_income < self.expenses + self._401k_contribution_max*self.match_percentage*self.match_limit:
            return 2
        if after_tax_income < self.expenses + self._401k_contribution_max:
            return 3
        if after_tax_income < self.expenses + self._401k_contribution_max + self.roth_contribution_max:
            return 4
        else:
            return 5

    # Makes contributions to accounts from income
    def make_contributions(self):
        if "Aggro" in  self.strategy:
            #tax_rate = self.find_tax_rate()
            leftover_month = (self.find_after_tax_income() - self.expenses)/12
            self.account_transfer("Checking",self.expenses/12)
            zone = self.find_zone()
            if zone == 1:
                print('Error: Trying to make contributions with income below expenses')
            if zone == 2:
                self.account_transfer("Roth 401k",leftover_month * (1+self.match_percentage))
            if zone == 3:
                amount_matched = self._401k_contribution_max*(1+self.match_percentage)*self.match_limit/12 # total match (employee plus employer)
                self.account_transfer("Roth 401k",amount_matched)
                leftover_month -= amount_matched
                self.account_transfer("Roth 401k",leftover_month)
            if zone == 4:
                maxed_401k = self._401k_contribution_max * (1+(self.match_percentage*self.match_limit)) / 12
                self.account_transfer("Roth 401k",maxed_401k)
                leftover_month -= maxed_401k
                self.account_transfer("Roth IRA",leftover_month)
            if zone == 5:
                maxed_401k = self._401k_contribution_max * (1+(self.match_percentage*self.match_limit)) / 12
                self.account_transfer("Roth 401k",maxed_401k)
                maxed_ira = self.roth_contribution_max / 12
                self.account_transfer("Roth IRA",maxed_ira)
                leftover_month -= maxed_ira + maxed_401k
                self.account_transfer("Checking",leftover_month)

            #after_tax = self.income * (1 - tax_rate)
            #after_tax_month = after_tax / 12
            #print(after_tax, self.expenses, self._401k_contribution_max/12, sep=', ')
            #if after_tax > (self.expenses + self._401k_contribution_max / 12): # Can max 401k
            #    after_tax_month -= self._401k_contribution_max / 12
            #    self.roth_401k.transfer(self._401k_contribution_max / 12)
            #    match_temp = (self._401k_contribution_max / 12) * self.match_percentage
            #    if self.match_remaining > match_temp:
            #        self.match_remaining -= match_temp
            #        #print(match_temp)
            #        self.roth_401k.transfer(match_temp)
            #    else:
            #        #print(self.match_remaining)
            #        self.roth_401k.transfer(self.match_remaining)
            #        self.match_remaining = 0

            #    self.checking.transfer(after_tax_month)
            #else: # Can't max 401k
            #    pass

    def take_withdraws(self):
        withdraw = self.expenses/12 + self.checking_goal - self.account_balance("Checking")
        if withdraw < 0:
            return
        for account in self.withdraw_order:
            if (self.age < 55) and (('401k' or 'IRA') in account):
                continue
            if (self.age < 59.5) and ('IRA' in account):
                continue
            if self.account_balance(account) > withdraw:
                self.account_transfer(account,-withdraw)
                self.account_transfer('Checking',withdraw)
                withdraw = 0
                break
            else:
                self.account_transfer(account,-self.account_balance(account))
                withdraw -= self.account_balance(account)
                self.account_transfer('Checking',self.account_balance(account))
        
        if withdraw > 0:
            for account in self.withdraw_order:
                if ((self.age < 55) and (('401k' or 'IRA') in account)) or ((self.age < 59.5) and ('IRA' in account)):
                    withdraw *= 1.1
                    penalty = 1.1               
                    if self.account_balance(account) > withdraw:
                        self.account_transfer(account,-withdraw)
                        self.account_transfer('Checking',withdraw/penalty)
                        withdraw = 0
                        break
                    else:
                        self.account_transfer(account,-self.account_balance(account))
                        withdraw -= self.account_balance(account)
                        self.account_transfer('Checking',self.account_balance(account)/penalty)
            
            if withdraw > 0:
                print('Bankrupt at age ' + str(self.age))
        
    
    def pay_expenses(self):
        self.account_transfer("Checking",-self.expenses/12)

    def pay_debts(self):
        overflow = 0
        for account in self.accounts:
            if 'Debt' in account.type:
                payment = get_monthly_payment(account.balance,account.apr,account.months)
                if payment > self.account_balace("Checking"):
                    overflow += payment - self.account_balace("Checking")
                    self.account_transfer("Checking",self.account_balace("Checking"))
                else:
                    self.account_transfer("Checking",-payment)
                account.appreciate(1/12)
        return overflow

    def invest(self):
        if "Aggro" in self.strategy:
            avaliable_to_invest = self.account_balance("Checking") - self.checking_goal
            self.account_transfer("Checking",-avaliable_to_invest)
            #if avaliable_to_invest > self.roth_ira_remaining:
            #    self.roth_ira.transfer(self.roth_ira_remaining)
            #    self.roth_ira_remaining = 0
            #    avaliable_to_invest -= self.roth_ira_remaining
            #else:
            #    self.roth_ira.transfer(avaliable_to_invest)
            #    avaliable_to_invest = 0
            #    self.roth_ira_remaining -= avaliable_to_invest
            
            self.account_transfer('Investments',avaliable_to_invest)
            avaliable_to_invest = 0

    def accounts_appreciate(self):
        for account in self.accounts:
            account.appreciate(years = 1/12)

    def log_graph_data(self):
        self.income_list.append(self.income)
        self.expenses_list.append(self.expenses)
        self.take_home_list.append(self.income * (1-self.find_tax_rate()))
        networth_temp = 0
        passive_income_temp = 0
        
        for account in self.accounts:
            #account.display_balance()
            networth_temp += account.balance
            passive_income_temp += account.balance * account.interest_rate

        self.net_worth_list.append(networth_temp)
        self.passive_income_list.append(passive_income_temp)

        for accounts in self.accounts:
            accounts.record_balance()
        
def pay_tax(taxable,tax_table):
    if taxable <= 0:
        return 0,0

    a = 1
    keep = 0

    while taxable>tax_table[0][a]:
        keep = keep + (tax_table[0][a]-tax_table[0][a-1])*tax_table[1][a-1]
        a+=1
    
    keep = keep + (taxable-tax_table[0][a-1]) * tax_table[1][a-1]
    affective_tax_rate =  keep/taxable
    keep = taxable - keep
    
    return keep,affective_tax_rate

def get_monthly_payment(principal,apr,months_remaining):
    mpr = apr/12
    monthly_payment = principal*(mpr*(1+mpr)**months_remaining)/((1+mpr)**months_remaining-1)
    return monthly_payment

'''
    def log_graph_data(self,time):
        self.income_list[time] = self.income
        self.expenses_list[time] = self.expenses
        self.take_home_list[time] = self.income * (1-self.find_tax_rate())
        networth_temp = 0
        passive_income_temp = 0
        
        for account in self.accounts:
            networth_temp += account.balance
            passive_income_temp += account.balance * account.interest_rate

        self.net_worth_list[time] = networth_temp
        self.passive_income_list[time] = passive_income_temp
'''