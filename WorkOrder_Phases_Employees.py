
# Instead of using a database to store the data, write code to store the information in Python data
#    structures. Design classes for this purpose, in a manner that would allow fields to be added
#    easily in the future.


# import garbage collection for object search
import gc
from collections import defaultdict 

class Employee:
    def __init__(self, employee_id, name="", email="", title=""):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.title = title

        # work_order_authored is a dictionary containing the work orders authored by this employee. 
        # in this dictionary: the keys are work order ids, 
        # values are instances of the WorkOrder class
        self.work_order_authored = {}

        # direct_reports is a dictionary containing the employees directly report to this employee. 
        # in this dictionary: the keys are direct report ids (or staff ids), 
        # values are instances of Employee class
        self.direct_reports = {}

        # managers is a dictionary containing the direct managers of this employee. 
        # in this dictionary: the keys are manager ids, 
        # values are instances of Employee class
        self.managers = {}
    
    # this __str__ method below is to print the class instance out as a string 
    # rather than a memory location of the instance
    def __str__(self):
        output_str = f"Id: {self.employee_id}; Name: {self.name}; Email: {self.email}; Title: {self.title}; work order authored: {self.work_order_authored}; Direct_reports: {self.direct_reports}; Managers: {self.managers} "
        return output_str

    def add_manager(self, manager):
        # add manager to this employee
        if manager.employee_id not in self.managers:
            self.managers[manager.employee_id] = manager
            # print(f"Manager {manager.name} assigned successfully to {self.name}!")
        else:
            print(f"Manager {manager.name} was already assigned to {self.name}.")
        # then, add this employee to be the direct report of the manager:
        if self.employee_id not in manager.direct_reports:
            manager.direct_reports[self.employee_id] = self
            # print(f"Direct report {self.name} assigned successfully to manager {manager.name}!")
        else:
            print(f"Direct report {self.name} was already assigned to manager {manager.name}.")

    def author_a_work_order(self, work_order_id, work_order_name):
        if work_order_id not in self.work_order_authored:
            self.work_order_authored[work_order_id] = WorkOrder(work_order_id, name=work_order_name, authored_by=self)

    def add_phase_to_work_order(self, work_order_name, phase_id, phase_name, phase_risk_level):
        # Search for work order to add a phase to
        for work_order in gc.get_objects():
            if isinstance(work_order, WorkOrder) and work_order.name == work_order_name:
                work_order_to_use = work_order
        #check to see if this employee is the author of the work order
        if self == work_order_to_use.authored_by:
            if phase_id not in work_order_to_use.phases:
                work_order_to_use.phases[phase_id] = Phase(phase_id, work_order_to_use, phase_name, phase_risk_level )
        else:
            print("This employee is not the author of this work order and can't add a phase to it.")
# Within the organization, there are multiple levels of management that form a hierarchy. That is, each employee
# has one or more direct managers. The employee at the top of the hierarchy without managers is the CEO.

# Each work order consists of a series of Phases. Each Phase is to be approved by one of the work order author’s
# managers. One manager signs off per Phase, depending on the risk level of that Phase. Here are the risk
# levels and approval requirements:
# ● Low - No manager approval required; the author can approve
# ● Moderate - Requires approval of one of the author’s direct managers
# ● High - Requires approval of any one of the upper-level managers (the direct and indirect managers of
# the author’s direct managers).

class orgStructure: 
   
    def __init__(self, noOfEmployees): 
        # No. of vertices 
        self.V = noOfEmployees+1
          
        # default dictionary to store graph 
        # this is an unordered collection of data values that are used to store data values like a map. 
        # self.graph = defaultdict(<class 'list'>, {})
        self.orgStructure = defaultdict(list)  
        self.directManager = False
        self.indirectManager = False
        self.eligibleApprover = False
        self.shortestPath = ""
        self.shortestPathLen = 0
    # function to add a manager to this employee
    # e is the employee (a node in the graph), and is the key in the dict, to be paired with a list that stores the managers of e
    # m is the destination node, stored in the list of managers of e
    def addManager(self, e, m): 
        self.orgStructure[e].append(m) 
    # graph = <class 'list'>, {7: [9]}
   
    # '''A recursive function to print all paths from 'thisEmployee' e1 to 'thisManager' m1. 
    # visited[]: a list to keep track of managers (nodes) in current path. 
    # path[]: a list to store actual managers 
    def printAllPathsUtil(self, e1, m1, visited, path, thisM=0): 
        # Mark the current node as visited and store in path 
        visited[e1]= True
        path.append(e1) 
  
        # If current vertex is same as destination, then print 
        # current path[] 
        if e1 == m1: 
            if thisM == path[1] and self.directManager == False:
                self.directManager = True
                
                # print("self.directManager: ", self.directManager)
            if thisM in path and self.eligibleApprover == False:
                self.eligibleApprover = True
            if thisM in path and thisM != path[0] and thisM != path[1] and self.indirectManager == False:
                self.indirectManager = True
            # print("len(path): ", len(path), ", self.shortestPathLen: ", self.shortestPathLen, ", self.shortestPath: ", self.shortestPath )
            if self.shortestPathLen == 0:
                self.shortestPathLen = len(path)
                self.shortestPath = ", ".join(str(e) for e in path)
            if len(path) < self.shortestPathLen:
                self.shortestPath = ", ".join(str(e) for e in path)
                self.shortestPathLen = len(path)
            

                # self.indirectManagerList.append(path[i])
            print(path)
        else: 
            # If current vertex is not destination 
            # Recur for all the vertices adjacent to this vertex 
            for i in self.orgStructure[e1]: 
                if visited[i]== False: 
                    self.printAllPathsUtil(i, m1, visited, path, thisM) 
        # Remove current vertex from path[] and mark it as unvisited 
        path.pop() 
        visited[e1]= False
   
   
    # Prints all paths from 's' to 'd' 
    def printAllPaths(self, employee, manager, thisM=0): 
        
        
        # Mark all the vertices as not visited 
        visited =[False]*(self.V) 
  
        # Create an array to store paths 
        path = [] 
  
        # Call the recursive helper function to print all paths 
        self.printAllPathsUtil(employee, manager, visited, path, thisM) 
   




class WorkOrder:
    def __init__(self, tp_id, name="", status="", authored_by=None):
        self.tp_id = tp_id
        self.name = name
        self.status = status
        self.authored_by = authored_by
        self.phases = {}
        self.directManagerList = []
        self.indirectManagerList = []
# need to move this up to Employee level
    # setEligibleApprovers:
        # for m_id, m in self.authored_by.managers.items():
        #     self.directManagerList.append(m)
        # this_work_order = self
        # print(self.name, "self.directManagerList: ", self.directManagerList)
        # def getManagersOfManager(self):
        #         if len(self.managers) == 0:
        #             return
        #         print("self: ", self)
        #         for n_id, n in self.managers.items():
        #             if n not in self.indirectManagerList:
        #                 self.indirectManagerList.append(n)
        #         for manager in self.managers.items():
        #             getManagersOfManager(manager)
        # for i in self.directManagerList:
        #     # print("line 178: ",i.name, "managers: ", i.managers)
        #     getManagersOfManager(i)
    # def __repr__(self):
    #     return pprint.pformat(self.phases) + "\n" + pprint.pformat(self.tp_id)

    # this __str__ method below is to print the class instance out as a string 
    # rather than a memory location of the instance
    # def __str__(self):
    #     output_str = f"Id: {self.tp_id}; Name: {self.name}; Status: {self.status}; Authored by: {self.authored_by}; Phases: {self.phases}"
    #     output_str = f"Id: {self.tp_id}; Name: {self.name}; Phases: {self.phases}"
    #     return output_str

    
class Phase:
    def __init__(self, phase_id, of_work_order, name="", risk_level=1, status=0, actual_approver=None):
        self.phase_id = phase_id
        self.name = name
        self.risk_level = risk_level
        self.eligibleApprovers = []
        self.of_work_order = of_work_order
        self.status = status
        # status = 0: Not approved
        # status = 1: Approved
        # self.eligible_approvers = of_work_order.eligible_approvers
        self.actual_approver = actual_approver

    # setEligibleApprovers:
        if self.risk_level == 1:
            self.eligibleApprovers = [self.of_work_order.authored_by]
        elif self.risk_level == 2:
            self.eligibleApprovers = self.of_work_order.directManagerList
        elif self.risk_level == 3:
            self.eligibleApprovers = self.of_work_order.indirectManagerList


    # this __str__ method below is to print the class instance out as a string 
    # rather than a memory location of the instance
    def __str__(self):
        output_str = f"Id: {self.phase_id}; Name: {self.name}; Risk level: {self.risk_level}; Of work order: {self.of_work_order}; Status: {self.status}; Eligible Approvers: {self.eligibleApprovers}; Actual approver: {self.actual_approver}"
        return output_str


# --------------------------- USERS ---------------------------

def approveAPhase(workOrderName, phaseName, approverEmail):
    # find work order based on work order name:
    for workOrder in gc.get_objects():
        if isinstance(workOrder, WorkOrder) and workOrder.name == workOrderName:
            thisWorkOrder = workOrder
    
    # find id of the work order's author:
    for employee in gc.get_objects():
        if isinstance(employee, Employee) and employee == thisWorkOrder.authored_by:
            authorId = employee.employee_id
    
    # find phase based on phase name:
    for phaseId, phase in thisWorkOrder.phases.items():
        if thisWorkOrder.phases[phaseId].name == phaseName:
            thisPhase = phase
    
    # find employee based on employee's email:
    for employee in gc.get_objects():
        if isinstance(employee, Employee) and employee.email == approverEmail:
            approver = employee
            approverId = employee.employee_id

    
    # Create a org structure as per ort chart
    g = orgStructure(9) 
    g.addManager(7, 9) 
    g.addManager(6, 7) 
    g.addManager(8, 6) 
    g.addManager(8, 9) 
    g.addManager(2, 8) 
    g.addManager(1, 2) 
    g.addManager(1, 8) 
    g.addManager(5, 8) 
    g.addManager(4, 5) 
    g.addManager(3, 4) 
    # graph = defaultdict(<class 'list'>, {7: [9], 6: [7], 8: [6, 9], 2: [8], 1: [2, 8], 5: [8], 4: [5], 3: [4]})
    # e1 = 3 ; e2 = 9
    # print ("Following are all different approval paths of employee #%d to manager #%d:" %(e1, e2)) 
    # the printAllPaths function below also update the check on whether this current approver is an eligible approver
    g.printAllPaths(authorId, 9, approverId)
    print("Shortest sequence of managers to the CEO: ", g.shortestPath)
    # if the current approver is not an eligible approver, print msg and exit function
    if g.eligibleApprover == False:
        print(f"Employee with id# {approverId} is not eligible to approve this phase.")
        return

    # if the current approver is an eligible approver:
    if g.eligibleApprover == True:
        # if this phase is already approved: print msg and exit function:
        if thisPhase.status == 1:
            print("No action taken since this phase was already approved!")
            return

        # if this phase is not approved:
        elif thisPhase.status == 0:
            # if risk level is low, author can approve
            if thisPhase.risk_level == 1 and authorId == approverId:
                thisPhase.status = 1
                thisPhase.actual_approver = approver
                # print("Status of this phase: ", thisPhase.status)
                print(f"{phaseName} of {workOrderName} is now approved!")
            # if risk level is moderate, direct manager can approve    
            elif thisPhase.risk_level == 2 and g.directManager == True:
                thisPhase.status = 1
                thisPhase.actual_approver = approver
                print(f"{phaseName} of {workOrderName} is now approved!")
            # if risk level is high, need higher level to approve:    
            elif thisPhase.risk_level == 3 and g.indirectManager == True:
                thisPhase.status = 1
                thisPhase.actual_approver = approver
                print(f"{phaseName} of {workOrderName} is now approved!")
            else:
                print("No action was taken.")
            approvalCount = 0
            for phase_id, phase in thisWorkOrder.phases.items():
                if phase.status == 1:
                    approvalCount += 1
            if approvalCount == len(thisWorkOrder.phases):
                thisWorkOrder.status = 1
                print(f"All phases of work order {thisWorkOrder.name} are approved.")
    # restore the checks for eligible approvers and managers to False:
    g.eligibleApprover = False
    g.directManager = False
    g.indirectManager = False



# --------------------------- Create employee instances ---------------------------
jAbram = Employee(1, "Johnathan Abram", "jAbram@company.com", "R&D Associate I" )
nAgholor = Employee(2, "Nelson Agholor", "nAgholor@company.com", "R&D Associate II")
dBooker = Employee(3, "Devontae Booker", "dBooker@company.com", "Mechanic Engineer I")
dCarlson = Employee(4, "Daniel Carlson", "dCarlson@company.com", "Mechanic Engineer II")
dCarrier = Employee(5, "Derek Carrier", "dCarrier@company.com", "Senior Mechanic Engineer")
mCollins = Employee(6, "Maliek Collins", "mCollins@company.com", "Production Manager")
bEdwards = Employee(7, "Bryan Edwards", "bEdwards@company.com", "Director of Operation")
iJohnson = Employee(8, "Isaiah Johnson", "iJohnson@company.com", "Lead Engineer")
aRodgerg = Employee(9, "Aaron Rodger", "aRodgerg@company.com", "CEO")
# --------- add managers to employees, and at the same time add direct report to the managers ------------
# the sample organization hierarchy has been visualized in my attached file named "_1.4_Org Chart_v1"
jAbram.add_manager(nAgholor)
jAbram.add_manager(iJohnson)
nAgholor.add_manager(iJohnson)
dBooker.add_manager(dCarlson)
dCarlson.add_manager(dCarrier)
dCarrier.add_manager(iJohnson)
iJohnson.add_manager(mCollins)
iJohnson.add_manager(aRodgerg)
mCollins.add_manager(bEdwards)
bEdwards.add_manager(aRodgerg)


# make a dictionary of all employees
all_employees = {}
# add all employees to all_employees, with keys being employee id, values being the employee instance
for employee in gc.get_objects():
    if isinstance(employee, Employee) and employee.employee_id == 8:
        # print(employee)
        all_employees[employee.employee_id] = employee
# print(len(bEdwards.managers))
# print(all_employees[8])
# for key, val in all_employees.items():
#     print(val)
# for key, val in jAbram.managers.items():
#     print("Manager: ", val);
# print("All employees:", all_employees)

# --------------------------- work orderS ---------------------------
# ----- Create work orders, phases for the work order, and at the same time created a link for creator to the the work orders' author
# risk level = 1: Low
# risk level = 2: Moderate
# risk level = 3: High
jAbram.author_a_work_order(1, "Work order 1")
jAbram.add_phase_to_work_order(work_order_name = "Work order 1", phase_id = 1 , phase_name = "Phase 1", phase_risk_level=1)
jAbram.add_phase_to_work_order(work_order_name = "Work order 1", phase_id = 2 , phase_name = "Phase 2", phase_risk_level=2)
jAbram.add_phase_to_work_order(work_order_name = "Work order 1", phase_id = 3 , phase_name = "Phase 3", phase_risk_level=3)

dBooker.author_a_work_order(2, "Work order 2")
dBooker.add_phase_to_work_order(work_order_name = "Work order 2", phase_id = 4 , phase_name = "Phase 1", phase_risk_level=1)
dBooker.add_phase_to_work_order(work_order_name = "Work order 2", phase_id = 5 , phase_name = "Phase 2", phase_risk_level=2)
dBooker.add_phase_to_work_order(work_order_name = "Work order 2", phase_id = 6 , phase_name = "Phase 3", phase_risk_level=3)

dCarrier.author_a_work_order(3, "Work order 3")
dCarrier.add_phase_to_work_order(work_order_name = "Work order 3", phase_id = 7 , phase_name = "Phase 1", phase_risk_level=1)
dCarrier.add_phase_to_work_order(work_order_name = "Work order 3", phase_id = 8 , phase_name = "Phase 2", phase_risk_level=2)
dCarrier.add_phase_to_work_order(work_order_name = "Work order 3", phase_id = 9 , phase_name = "Phase 3", phase_risk_level=3)

iJohnson.author_a_work_order(4, "Work order 4")
iJohnson.add_phase_to_work_order(work_order_name = "Work order 4", phase_id = 10 , phase_name = "Phase 1", phase_risk_level=1)
iJohnson.add_phase_to_work_order(work_order_name = "Work order 4", phase_id = 11 , phase_name = "Phase 2", phase_risk_level=2)
iJohnson.add_phase_to_work_order(work_order_name = "Work order 4", phase_id = 12 , phase_name = "Phase 3", phase_risk_level=3)

mCollins.author_a_work_order(5, "Work order 5")
mCollins.add_phase_to_work_order(work_order_name = "Work order 5", phase_id = 13 , phase_name = "Phase 1", phase_risk_level=1)

# print work order
# for work_order in gc.get_objects():
#     if isinstance(work_order, WorkOrder) and work_order.tp_id == 1:
#         print(work_order)

approveAPhase("Work order 1", "Phase 1", "jAbram@company.com")
approveAPhase("Work order 1", "Phase 2", "nAgholor@company.com")
approveAPhase("Work order 1", "Phase 3", "bEdwards@company.com")
approveAPhase("Work order 2", "Phase 2", "dCarlson@company.com")
approveAPhase("Work order 1", "Phase 3", "bEdwards@company.com")


# print a phase
# for phase in gc.get_objects():
#     if isinstance(phase, Phase) and phase.phase_id == 1:
#         print(phase)


# for tp in gc.get_objects():
#     if isinstance(tp, WorkOrder) and tp.tp_id == 1:
#         print(tp)

for phase in gc.get_objects():
    if isinstance(phase, Phase) and phase.phase_id == 3:
        print(phase.name, " of work order", phase.of_work_order.name, ":")
        print("work order authored by: ", phase.of_work_order.authored_by.name)
        print("Eligible approver: ")
        for m in phase.eligibleApprovers:
            print(m.name)
        print("Actual approver: ", phase.actual_approver.name)
