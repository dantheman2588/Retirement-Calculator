import matplotlib.pyplot as plt
import numpy as np
from world_class import World
from world_class import Person
from world_class import Account
#import person_class
#import account_class
#print(dir(world_class))
#print(dir(person_class))
#print(dir(account_class))


#from world_class import World
#from person_class import *
#from account_class import * 

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

def standard_plot_set(person):
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))

    # Top plot contains drivers on networth: income, expense, ect.
    time = world.timeline
    axs[0].plot(time,dan.income_list, 'y', label='Income')
    axs[0].plot(time,dan.take_home_list, 'b', label='Take Home')
    axs[0].plot(time,dan.expenses_list, 'r', label='Expenses')
    axs[0].plot(time,dan.passive_income_list, 'g', label='Passive Income')
    
    axs[0].set_xlabel('Time (Years)')
    axs[0].set_ylabel('Cash flow ($/year)')
    axs[0].set_title('Drivers')
    axs[0].legend(['Income','Take Home','Expenses','Passive Income'])
    axs[0].grid()

    # Botton plot contains net worth and accounts/assets that make that up
    axs[1].plot(time,dan.net_worth_list, 'y', label='Net Worth')
    axs[1].plot(time,dan.account_history('Roth 401k'), 'b', label='Roth 401k')
    axs[1].plot(time,dan.account_history('Roth IRA'), 'r', label='Roth IRA')
    axs[1].plot(time,dan.account_history('Investments'), 'g', label='Investments')
    
    axs[1].set_xlabel('Time (Years)')
    axs[1].set_ylabel('Money ($)')
    axs[1].set_title('Net Worth and Accounts')
    axs[1].legend(['Net Worth','Roth 401k','Roth IRA','Investments'])
    axs[1].grid()

    plt.tight_layout()
    plt.show()

def find_person(world,person):
    for a in world.people:
        if a.name == person:
            return a
        
def list_accounts(world,person,list):
    a = find_person(world,person)
    print(a.name + "'s Accounts:")
    for b in getattr(a,list):
        print(b.name)

#roth = Account("Roth","Roth")
#roth.transfer(1000)
#roth.display_balance()
#'''
world = World(1,"Normal NJ")
dan = Person("Dan",world,strategy="Aggro",benefits="401k match .5 of .08",age=26,income=101000,raise_rate=0.035,expenses=26000,expenses_increase=0.03,retire=40)
#'''

dan.account_transfer('Roth IRA',100000)
#dan.roth_ira.transfer(-83000)
dan.account_transfer('Investments',180000)
dan.account_transfer('Checking',6800)
dan.account_transfer('Roth 401k',130000)
world.add(dan)


for month in range(world.months):
    world.tick()
    world.save_data()

#for account in dan.accounts: 
#    print(account.name)

#list_accounts(world,'Dan','accounts')
#print(find_person(world,'Dan').income_list)

#find_person(world,'Dan').account_full('Roth IRA').print_full_history()
standard_plot_set(find_person(world,'Dan'))


#print(find_person(world,'Dan').roth_ira.history)
#print(find_person(world,'Dan').accounts)

'''
#fig, axs = plt.subplot(2,2,figsize=(8,8))
plt.plot(dan.income_list,'y',dan.t  ake_home_list,'b',dan.expenses_list,'r',dan.passive_income_list,'g')
plt.ylabel('Balance ($)')
plt.xlabel('Time (Years)')
plt.legend(['Income','Take Home','Expenses','Passive Income'])
plt.show()
print(dan.find_tax_rate())
print(pay_tax(100000,dan.world.state_income_tax))
'''

    
