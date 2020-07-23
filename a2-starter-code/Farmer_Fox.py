'''Farmer_Fox.py
by Kazi Sabrina Sonnet
UWNetID: ksonnet
Student number: 1870554

Assignment 2, in CSE 415, Autumn 2019.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

#<METADATA>
SOLUZION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, fox, chicken, grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Kazi Sabrina Sonnet']
PROBLEM_CREATION_DATE = "10-OCT-2019"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 """Farmer has a fox, a chicken and a sack of grain. Farmer must cross a river with only one of them at a time. 
 If farmer leaves the fox with the chicken he will eat it; if farmer leaves the chicken with the grain he will eat it.
 How can the farmer get all three across safely?"""
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
F = 'Farmer' # farmer/boat location
f= 0 #array index to access fox's location
c= 1 #array index to access chicken's location
g= 2 #array index to access grain's location 
L= 0 #array index for the left shore of the river 
R= 1 #array index for the right shore of the river 
load= ['Fox','Chicken', 'Grain']

class State: 
    def __init__(self, d=None):
        """
        creates an initial state with farmer and fox, chicken, grain on the left side of the river.

        """
        if d==None: 
            d = {'load':[0, 0, 0], F: L}
        self.d = d
    
    def __eq__(self, s2): 
        """
       Returns true when two states are equal

        """
        for prop in ['load','Farmer']:
            if self.d[prop] != s2.d[prop]: 
                return False
        return True
    
    def __str__(self): 
        """
        States the problem

        """
        if self.d[F]== L: 
            RiverSide = 'Left'
        else: 
            RiverSide = 'Right'
        
        output = ['Farmer is on the ' + RiverSide, ', LEFT: ', ', RIGHT: ']

        location =[[], []]
        for index, ld in enumerate(self.d['load']):
            location[ld].append(load[index])
        for n in range(2): 
            if len(location[n])== 0:
                output[n+1] = output[n+1]+ "None"
            else: 
                output[n+1] = output[n+1]+", ".join(location[n])
        return ''.join(output)
    
    def __hash__(self): 
        '''
        Creates a hash code for string version of problem 
        '''
        return (self.__str__()).__hash__()
    
    def copy(self): 
        '''
        Makes a copy of the current state
        '''
        news = State({})
        news.d['load']= self.d['load'][:]
        news.d[F] = self.d[F]
        return news 
    
    def can_move(self, FarmerLoad): 
        '''
        Returns true if a load can legally move to other side of the river with farmer.

        '''
        RiverSide = self.d[F]
        ld = self.d['load']
        if FarmerLoad is not None: 
            #load to move must be on the same shore
            if ld[FarmerLoad]!= RiverSide:
                return False
            # if atleast one load is available in any side of the shore that may be moved along with farmer 
            if ld.count(RiverSide)==1: 
                return True
            #moving chicken is always legal 
            if FarmerLoad is c:
                return True
        if ld[c]==RiverSide:
            if RiverSide ==(ld[g] or ld[f]):
                if FarmerLoad is not (f or g):
                    return False
        if ld.count(RiverSide)==3:
            return False
        return True 
    
    def move(self, FarmerLoad):
        '''
        If a load can be moved computes the next vaid state after moving the load
        '''
        news = self.copy()
        RiverSide = self.d[F]
        new_RiverSide= 1-RiverSide
        news.d[F]= new_RiverSide
        if FarmerLoad is not None: 
            news.d['load'][FarmerLoad] = new_RiverSide
        return news
    
def goal_test(s):
    '''
    if all goods are on the right shore goal state is reached
    '''
    if s.d['load'].__contains__(0):
        return False
    return s.d[F]==1 #returns true if the farmer is on the right shore  
      
def goal_message(s):
       '''
       if goal state is reached a goal message is returned
       '''
       return 'Congratulations! The farmer has sucessfully crossed the river with chicken, fox, grain!'


class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

# </COMMON CODE>
#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'load':[0, 0, 0], F:L })
#</INITIAL_STATE>

#<OPERATORS>
combinations = [None, f, g, c]

OPERATORS = [Operator("Cross the river with farmer", lambda s, m1=m: s.can_move(m1), lambda s, m1=m: s.move(m1) ) for m in combinations]
#</OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>


# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# <GOAL_MESSAGE_FUNCTION>
       


            
            






    







    






