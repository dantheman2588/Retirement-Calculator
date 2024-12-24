# Account class for individual account held by people ex. 401k, savings, roth ira ...
class Account:
    def __init__(self, name, type, world, info=['None']):
        self.name = name
        self.balance = 0
        self.world = world
        self.interest_rate = self.world.index_return
        self.type = type
        self.history = []

        # Type is used to define the account **
        if "401k" in type:
            self.employer_match = False
            self.penalty = 0.1
            self.age_penalty = 59.5

            # of signals that there is an employer match
            if " of " in type:
                self.employer_match = True
                benefits_split = type.split()
                self.match_percentage = float(benefits_split[benefits_split.index("of")-1])
                self.match_limit = float(benefits_split[benefits_split.index("of")+1])
                
            

        if "Roth" in type:
            self.penalty = 0.1
            self.age_penalty = 59.5
        if "Debt" in type:
            self.balance = info[0]
            self.apr = info[1]
            self.months = info[2]
    
    # Move money in and out of the account
    def transfer(self,amount):
        self.balance += amount

    # Displays the account balance with name
    def display_balance(self):
        print(self.name + ":\n" + "    Balance: " + "${:,.0f}".format(self.balance))

    # The account appreciates interest based on the time and rate
    def appreciate(self, years):
        #if years==50:
        #print(self.balance)
        if 'Debt' in self.type:
            self.balance *= (1 + self.apr) ** (years)
            self.months -= years/12
        else:
            self.balance *= (1 + self.interest_rate) ** (years)
        #if years==50:
        #print(self.balance)

    # Changes the interest rate of the account
    def update_rate(self, rate):
        self.interest_rate = rate

    def update_penalty(self, penalty):
        self.penalty = penalty

    def record_balance(self):
        self.history.append(self.balance)

    def print_full_history(self):
        print(self.name + ":")
        for balance in self.history:
            print("    Balance: " + "${:,.0f}".format(balance))

