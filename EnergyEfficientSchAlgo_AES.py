import operator
import copy
import sys

#Global variables
_TYPE2NODENAME = {}   #Dictionary that maps type of node to the list of nodes:   Key: type ; Value: List of nodes of this type
_NODENAME2NODENAMEOBJECT = {}   #Dictionary that maps node name to node object:   Key: node name ; Value: Node Object
_NODENAME2BOTTOM = {} #Dictionary that maps node name to bottom
_PN_HIGHEST = float(sys.argv[2]) #100
_FREQUENCY_HIGHEST_ = 10
_VOLTAGE_HIGHEST_ = 10
TASK_GROUPINGS = [] #List that stores the task groups => This is the result of grouping
_PROCESSORS_ = [] #List of processors

#Class to get and set node details
class Node:

   def __init__(self, name):     #Class variables:
      self.name = name
      self.node_type = ""
      self.parent = ""
      self.child = []
      self.exec_time = ""
      self.bottom = ""
      self.parents = []
      self.ect = 0.0
      self.est = 0.0
      self.fp = ""
      self.power = 0.0
      self.frequency = 0.0
      self.energy = 0.0
      self.lact = 0.0
      self.last = 0.0
      self.st = 0.0
      self.maet = 0.0
      self.voltage = 0.0
   
   def getName(self):
      return self.name

   def getType(self):
      return self.node_type

   def setType(self, node_type):
      self.node_type = node_type
   
   def getParent(self):
      return self.parent

   def setParent(self, parent):
      self.parent = parent

   def getChild(self):
      return self.child
 
   def setChild(self, child):
      self.child = child
 
   def getExecTime(self):
      return self.exec_time

   def setExecTime(self, exec_time):
      self.exec_time = exec_time

   def getBottom(self):
      return self.bottom

   def setBottom(self, bottom):
      self.bottom = bottom

   def getParents(self):
      return self.parents

   def getEST(self):
      return self.est

   def setEST(self, est):
      self.est = est

   def getECT(self):
      return self.ect

   def setECT(self, ect):
      self.ect = ect

   def getFP(self):
      return self.fp

   def setFP(self, fp):
      self.fp = fp

   def getPower(self):
      return self.power

   def setPower(self, power):
      self.power = power

   def getEnergy(self):
      return self.energy

   def setEnergy(self, energy):
      self.energy = energy

   def getLACT(self):
      return self.lact

   def setLACT(self, lact):
      self.lact = lact

   def getLAST(self):
      return self.last

   def setLAST(self, last):
      self.last = last

   def getST(self):
      return self.st

   def setST(self, st):
      self.st = st

   def getMAET(self):
      return self.maet

   def setMAET(self, maet):
      self.maet = maet

   def getFrequency(self):
      return self.frequency

   def setFrequency(self, frequency):
      self.frequency = frequency

   def getVoltage(self):
      return self.voltage

   def setVoltage(self, voltage):
      self.voltage = voltage


class Processor:

   def __init__(self, name):     #Class variables:
      self.processor_name = name
      self.frequency = 0.0
      self.tasks = []

   def getProcessorName(self):
      return self.processor_name

   def getFrequency(self):
      return self.frequency

   def setFrequency(self, frequency):
      self.frequency = frequency

   def getTasks(self):
      return self.tasks

   def setTasks(self, tasks):
      self.tasks = tasks



#Update execution time based on each node
def updateNodeExecTime(node_type, exec_time):
   if node_type in _TYPE2NODENAME:
     nodes = _TYPE2NODENAME[node_type]
     for node in nodes:
         nodeobject = _NODENAME2NODENAMEOBJECT[node]
         nodeobject.setExecTime(exec_time)

#Update frequency based on each node
def updateNodeFrequency(node_type, frequency):
   if node_type in _TYPE2NODENAME:
     nodes = _TYPE2NODENAME[node_type]
     for node in nodes:
         nodeobject = _NODENAME2NODENAMEOBJECT[node]
         nodeobject.setFrequency(frequency)

#Update voltage based on each node
def updateNodeVoltage(node_type, voltage):
   if node_type in _TYPE2NODENAME:
     nodes = _TYPE2NODENAME[node_type]
     for node in nodes:
         nodeobject = _NODENAME2NODENAMEOBJECT[node]
         nodeobject.setVoltage(voltage)


#Parse file and return the file content
def readFile():
   content = ""
   with open(sys.argv[1], "r") as f:  #/home/krishnav/Downloads/tgff-3.6/examples/final.tgff
      content = f.readlines()
   content = [x.strip() for x in content] 
   return content


#Parse file content and update the node details
def parseFileContent(content):
   global _FREQUENCY_HIGHEST_
   global _VOLTAGE_HIGHEST_
   update_exec_time = 0
   update_frequency = 0
   update_voltage = 0
   for x in content:
      if x.startswith("TASK"):
          fields = x.split()
          node_name = fields[1]
          node_type = fields[3]
	       #Update _NODENAME2NODENAMEOBJECT-to store each node as an object to get the values
          if node_name in _NODENAME2NODENAMEOBJECT:
               print(node_name+" present in _NODENAME2NODENAMEOBJECT")
          else:
               node = Node(node_name)#object creation
               node.setType(node_type)
               _NODENAME2NODENAMEOBJECT[node_name] = node
        #Update _TYPE2NODENAME
          if node_type in _TYPE2NODENAME:
              nodes = _TYPE2NODENAME[node_type]
              nodes.append(node_name)
          else:
               nodes = []
               nodes.append(node_name)
               _TYPE2NODENAME[node_type] = nodes
      #Update parent and child for each node
      if x.startswith("ARC"):
          fields = x.split()
          parent = fields[3]
          child = fields[5]
          parent_node = _NODENAME2NODENAMEOBJECT[parent]
          parent_node.getChild().append(child)
          child_node = _NODENAME2NODENAMEOBJECT[child]
          child_node.setParent(parent)
      #Update execution time
      if x.find("exec_time") != -1:
          update_exec_time = 1
      
      if(update_exec_time and not x.startswith("}") and x !="" and "{" not in x):
          fields = x.split()
          node_type = fields[0]
          exec_time = fields[1]
          updateNodeExecTime(node_type, exec_time)
      if(update_exec_time and "{" in x):
          update_exec_time = 0
      
      if x.find("frequency") != -1:
          update_frequency = 1

      if(update_frequency and not x.startswith("}") and x !="" and "{" not in x):  
          fields = x.split()
          node_type = fields[0]
          frequency = fields[1] 
          try:         
              if float(frequency) > _FREQUENCY_HIGHEST_:
                  _FREQUENCY_HIGHEST_ = float(frequency)
              updateNodeFrequency(node_type, float(frequency))
          except:
            print("Frequency is string:"+frequency+":")
	  
      if(update_frequency and "{" in x):
          update_frequency = 0

      if x.find("voltage") != -1:
          update_voltage = 1

      if(update_voltage and not x.startswith("}") and x !="" and "{" not in x):	  
          fields = x.split()
          node_type = fields[0]
          voltage = fields[1]     
          try:     
              if float(voltage) > _VOLTAGE_HIGHEST_:
                  _VOLTAGE_HIGHEST_ = float(voltage)
                  print("Nodetype voltage: "+str(node_type)+" : "+voltage)
              updateNodeVoltage(node_type, float(voltage))
          except:
            print("Voltage is string:  Heading:"+voltage+":")
	  
      if(update_voltage and "{" in x):
          update_voltage = 0


#Display node details
def displayResults():
   for nodename in _NODENAME2NODENAMEOBJECT:
       nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
       print("Node Name: "+nodename)
       print("		Type: "+nodeobject.getType())
       print("		Parent: "+nodeobject.getParent())
       print("		Child count: "+str(len(nodeobject.getChild())))
       print("		Exec. Time: "+nodeobject.getExecTime())
       print("		Bottom Value: "+str(nodeobject.getBottom()))
       print("                Parents count: "+str(len(nodeobject.getParents())))
       print("		ECT:   "+str(nodeobject.getECT()))
       print("		EST:   "+str(nodeobject.getEST()))
       print("		FP:    "+nodeobject.getFP())
       print("		Power: "+str(nodeobject.getPower()))
       print("		Frequency: "+str(nodeobject.getFrequency()))
       print("		Voltage: "+str(nodeobject.getVoltage()))
       print(" 	        LACT: "+str(nodeobject.getLACT()))
       print(" 	        LAST: "+str(nodeobject.getLAST()))
       print("		ST: "+str(nodeobject.getST()))
       print("		MAET: "+str(nodeobject.getMAET()))
       print("                Energy: " +str(nodeobject.getEnergy()))
       print("*********************************************")
       total_energy = getTotalEnergy()
   print("")
   print("")
   print("")
   print("    TOTAL ENERGY :   "+str(total_energy))
   print("")
   print("")
   print("")
   print("****************************************************************")



def updateParents(node):
   children = node.getChild()
   for child in children:
      (_NODENAME2NODENAMEOBJECT[child]).getParents().append(node)
      (_NODENAME2NODENAMEOBJECT[child]).getParents().extend(node.getParents())
      parents = updateParents(_NODENAME2NODENAMEOBJECT[child])
      #print("Parents count of "+(_NODENAME2NODENAMEOBJECT[child]).getName()+" : "+str(len((_NODENAME2NODENAMEOBJECT[child]).getParents())))

def getMaximum(bottoms):
    maxvalue = bottoms[0]
    for bottom in bottoms:
        if bottom > maxvalue:
            maxvalue = bottom
    return maxvalue

def getBottomValues(node):
    if (node is None):
      return 0;
    children = node.getChild()
    nodeexectime = node.getExecTime()
    if len(children) == 2:
        bottom1 = getBottomValues(_NODENAME2NODENAMEOBJECT[children[0]])
        bottom2 = getBottomValues(_NODENAME2NODENAMEOBJECT[children[1]])
        if  bottom1 > bottom2:
            maxtime = bottom1
        else:
             maxtime = bottom2
        node.setBottom((float(maxtime) + float(nodeexectime)))
        _NODENAME2BOTTOM[node] = float(maxtime) + float(nodeexectime)
        return float(maxtime) + float(nodeexectime)
    elif len(children) == 1:
        mintime = getBottomValues(_NODENAME2NODENAMEOBJECT[children[0]])
        node.setBottom((float(mintime) + float(nodeexectime)))
        _NODENAME2BOTTOM[node] = float(mintime) + float(nodeexectime)
        return float(mintime) + float(nodeexectime)
    elif len(children) >= 3:
        bottoms = [] #Children 
        for child in children:
            bottoms.append(getBottomValues(_NODENAME2NODENAMEOBJECT[child]))
        if len(bottoms) > 0:
            maxtime = getMaximum(bottoms)
            node.setBottom((float(maxtime) + float(nodeexectime)))
            _NODENAME2BOTTOM[node] = float(maxtime) + float(nodeexectime)
            return float(maxtime) + float(nodeexectime)
        else:
            return 0
            
    else:
        node.setBottom(nodeexectime)
        _NODENAME2BOTTOM[node] = float(nodeexectime)
        return nodeexectime
    

    return 0   


def getHeadNode():
   for nodename in _NODENAME2NODENAMEOBJECT:
       nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
       if (nodeobject.getParent() == ""):
           return nodeobject



def computeQueue():
   headnode = getHeadNode()
   bottomvalue = getBottomValues(headnode)
   sorted_queue = sorted(_NODENAME2BOTTOM, key=_NODENAME2BOTTOM.get)
   return sorted_queue


def computeECT():
   for nodename in _NODENAME2NODENAMEOBJECT:
      nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
      if(len(nodeobject.getParents()) == 0):
          nodeobject.setEST(0)
          nodeobject.setECT(float(nodeobject.getExecTime()))
      else:
        est = 0
	#for parent in nodeobject.getParents():
	#  est = est + float(parent.getExecTime())
        max_ect = 0
        for parent in nodeobject.getParents():
            if float(parent.getECT()) > max_ect:
                max_ect = float(parent.getECT())
        nodeobject.setEST(max_ect)
        nodeobject.setECT(max_ect + float(nodeobject.getExecTime()))

def computeFP():
    for nodename in _NODENAME2NODENAMEOBJECT:
        nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
        if(len(nodeobject.getParents()) == 0):
            nodeobject.setFP("")
        else:
             maxECT_value = 0.0
             maxECT_node = ""
             for parent in nodeobject.getParents():
                 if parent.getECT() > maxECT_value:
                     maxECT_value = parent.getECT()
                     maxECT_node = parent.getName()
             nodeobject.setFP(maxECT_node)


#Compute max frequency : TODO
def getMaxFrequency():
   return _FREQUENCY_HIGHEST_


#Compute max voltage : TODO
def getMaxVoltage():
   return _VOLTAGE_HIGHEST_


def computePower_Energy():
    global _PN_HIGHEST
    for nodename in _NODENAME2NODENAMEOBJECT:
        nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
        frequency = nodeobject.getFrequency()  
        voltage = nodeobject.getVoltage()  
        max_frequency = getMaxFrequency()
        max_voltage = getMaxVoltage()
        power = _PN_HIGHEST * (frequency * voltage * voltage)/(max_frequency * max_voltage * max_voltage)
        energy = power * float(nodeobject.getExecTime())
        nodeobject.setPower(power)
        nodeobject.setEnergy(energy)
        
def getTotalEnergy():
    total_energy = 0.0
    for nodename in _NODENAME2NODENAMEOBJECT:
        nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
        total_energy = total_energy + nodeobject.getEnergy()
    return total_energy


def computeLAST_LACT():
     for nodename in _NODENAME2NODENAMEOBJECT:
         nodeobject =  _NODENAME2NODENAMEOBJECT[nodename]
         if(len(nodeobject.getParents()) == 0):
             nodeobject.setLACT(nodeobject.getECT())
             nodeobject.setLAST(nodeobject.getLACT() - float(nodeobject.getExecTime()))
         else:
            minECT_value = 1000000
            minECT_node = ""
            for parent in nodeobject.getParents():
                if parent.getECT() < minECT_value:
                    minECT_value = parent.getECT()
                    minECT_node = parent.getName()
            nodeobject.setLACT(minECT_value)
            nodeobject.setLAST(nodeobject.getLACT() - float(nodeobject.getExecTime()))


def computeOptimalThreshold(sorted_queue):
    min_threshold = 65536
    max_threshold = 0
    #min_schedule_len = 0
    c_uv = 0
    for v_node in sorted_queue:
      u = v_node.getFP()
      if u == '':
          continue
      u_node = _NODENAME2NODENAMEOBJECT[u]
      last_v = v_node.getLAST()
      last_u = u_node.getLAST()
      if last_v - last_u < c_uv:
          energy_v = v_node.getEnergy()
          energy_u = u_node.getEnergy()
          moreenergy = abs(energy_u - energy_v)
          lesstime = u_node.getLACT() - c_uv - last_v
          ratio = moreenergy/lesstime
          if ratio < min_threshold:
              if ratio < 0:
                  min_threshold = 0
              else:
                  min_threshold = ratio
          if ratio > max_threshold:
              max_threshold = ratio
      if max_threshold == 0:
          optimal_threshold = 0 
      else:
          min_schedule_len = grouping(max_threshold, sorted_queue)
          max_schedule_len = grouping(min_threshold, sorted_queue)
          #print("max_schedule_len is: "+str(max_schedule_len))
          optimal_threshold = min_threshold - 1
    assigned_makespan = float(sys.argv[3]) #8.0
    if assigned_makespan < min_schedule_len:
       optimal_threshold = max_threshold
    else:
       while optimal_threshold <= max_threshold:
           tmp_sched_len = grouping(optimal_threshold, sorted_queue)
           if tmp_sched_len > assigned_makespan:
               optimal_threshold = optimal_threshold + 1
           else:
               break
    print("Result optimal threshold is: "+str(optimal_threshold))
    return optimal_threshold


def computeST(nodeobject):
   #for nodename in _NODENAME2NODENAMEOBJECT:
     if(len(nodeobject.getParents()) == 0):
         nodeobject.setST(0)
     else:
        max_st = 0.0
        parents = nodeobject.getParents()
        for parent in parents:
            if parent.getST() > max_st:
                max_st = parent.getST()
        nodeobject.setST(max_st + float(nodeobject.getExecTime()))

     children = nodeobject.getChild()
     if len(children) == 0:
         return
     for child in children:
         computeST(_NODENAME2NODENAMEOBJECT[child])


def computeMAET(nodeobject, sorted_queue, i):
   min_st = sorted_queue[i].getST()
   task_count = 0
   for task in sorted_queue:
       if task_count > 0:
           current_st = sorted_queue[task_count].getST()
           if current_st > min_st:  
               min_st = current_st
   nodeobject.setMAET(min_st)
   


def voltageScaling(sorted_queue):
   processors = []
   nodeobject = getHeadNode()
   computeST(nodeobject)
   i = 0
   for v in sorted_queue:
     computeMAET(v, sorted_queue, i)
     i = i  + 1
   for p in _PROCESSORS_:
     #print("Processor name is: "+p.getProcessorName())
     for task in p.getTasks():
         #print task.getName()
         #if p.isIdle():
         #   p.setFrequency(0)
         if task.getMAET() == task.getExecTime():
             p.setFrequency(_FREQUENCY_HIGHEST_)
	#else:
	#   print("Else case")
	   
   #	if task.getStatus == 0:
   #	  p.setFrequency(lowest_freq)
   #	if t.getMAET() == t.getExecTime():
   #	  print("Executing "+t.getName()+" at highest frequency"
   #	else:
	  
	   
	

def grouping(threshold, sorted_queue):
   cc_uv = 0
   c_uv = 0
   cc_zv = 0
   el_uv = 0
   groups = []
   #Initializing groups with an dummy task object
   x = Node("")
   groups.append([x]) 
   groups.append([x])
   groups.append([x])
   groups.append([x])
   q = 0
   v = sorted_queue[q]
   i = 0
   schedule_list = []
   schedule_length = 0
   current_group = groups[0] #[i]
   current_group.append(v)
   sorted_queue1 = copy.copy(sorted_queue)
   #while len(sorted_queue1) > 0:
   for v in sorted_queue:
       if len(sorted_queue1) == 0:
           break
       u = v.getFP()
       if u == '':
           continue
       u_node = _NODENAME2NODENAMEOBJECT[u]
       if u_node in current_group:
           if v.getLAST() - u_node.getLACT() < c_uv:
               moreenergy = u_node.getEnergy() - el_uv
               lesstime = u_node.getLACT() + c_uv - v.getLAST()
               ratio = moreenergy/lesstime
               if ratio <= threshold:
                   current_group.append(u_node)
               else:
                   for z in v.getParents():
                       if u_node.getECT() + cc_uv == z.getECT() + cc_zv and z not in current_group:
                           u_node = z
                           current_group.append(u_node)
                           sorted_queue1.remove(u_node)
                       else:
                            i = i + 1
                            u = sorted_queue[q+1]
                            if i+1 < 5:
                                current_group = groups[i+1]
		    
           else:
                if ratio <= threshold:
                    current_group.append(u_node)
                else:
                     for z in v.getParents():
                         if u_node.getECT() + cc_uv == z.getECT() + cc_zv and z not in current_group:
                             u_node = z
                             current_group.append(u_node)
                             sorted_queue1.remove(u_node)
                             print("Assigned "+u_node.getName())
                         else:
                             i = i + 1
       else:
           current_group.append(u_node)
           if u_node in sorted_queue1:
               sorted_queue1.remove(u_node)
           v = u_node
       if len(v.getParents()) == 0:
           i = i + 1
           v = sorted_queue[q + 1]
           current_group = groups[i] #[i]
           current_group.append(v)
           if v in sorted_queue1:
               sorted_queue1.remove(v)
               print("Assigned to processor with minimum frequency u")
   group_count = 0
   TASK_GROUPINGS = groups #Assigning to the grouping global variable, so that it can be accessed for voltage scaling
   for group in TASK_GROUPINGS:
       group_count = group_count + 1
       for subgroup in group:
           if subgroup != None and subgroup.getName() != "":
               processor = Processor("P"+str(group_count)) #processor names like p0, p1, p2 ...
               print( subgroup.getName()+" is assigned to group: "+str(group_count)+" to processor "+processor.getProcessorName())
               (processor.getTasks()).append(subgroup)
               _PROCESSORS_.append(processor)
   return lesstime


#Start program
def main():
   if len(sys.argv) < 4:
       print("Invalid number of arguments to program")
       print("Expected format is:")
       print("python run.py <absolute path of the tgff file> <_PN_HIGHEST value> <assigned_makespan>")
       print("Example: python Energy.py final.tgff 100 8")
       sys.exit()
   content = readFile()
   parseFileContent(content)
   sorted_queue = computeQueue()
   #print queue results  
   for x in sorted_queue:
      print (x.getName()+" : "+str(x.getBottom()))
   headnode = getHeadNode()
   updateParents(headnode)
   computeECT()
   computeFP()
   computePower_Energy()
   computeLAST_LACT()
   computeOptimalThreshold(sorted_queue)
   voltageScaling(sorted_queue)
   displayResults()
#Starting point of the program
main()



