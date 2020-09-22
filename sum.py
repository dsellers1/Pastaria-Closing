import hassapi as hass

global drawers
global inputs
global sensors
global math_vars
drawers = ["pastaria", "seconda", "sarefinos"]
inputs = ["100", "50", "20", "10", "5", "1", "q", "cc", "gc", "po", "begin", "2pm_x", "5pm_x", "cust_count", "sales"]
totals = ["drawer_total", "drawer_sales", "begin_total", "drop_total"]
sensors = inputs + totals
math_vars = [("100", 100, "+"), ("50", 50, "+"), ("20", 20, "+"), ("10", 10, "+"), ("5", 5, "+"), ("1", 1, "+"), ("q", 0.25, "+"), ("cc", 1, "+"), ("gc", 1, "+"), ("po", 1, "-")]

class Sensor_Calculations(hass.Hass):
  def initialize(self):
    for drawer in drawers:
      # Following loop is used to ensure sensors are valid in HA. These sensors are used to store the results of calculations and are defined in the configuration.yaml.
      for sensor in sensors:
        sensorToCheck = "sensor." + drawer + "_" + sensor
        if not self.entity_exists(sensorToCheck):
          self.set_state(sensorToCheck, state = 0)     
      # Following loop used to monitor changes in input text boxes.
      for input in inputs:
        entityToMonitor = "input_text." + drawer + "_" + input
        self.listen_state(self.CB, entityToMonitor)

  def CB(self, entity, attribute, old, new, kwargs):
    sensorToUpdate = entity.replace('input_text.', 'sensor.') # Changes input_text to sensor for the entity
    type, name = self.split_entity(entity) # Breaks apart the entity to determine which drawer and what denomination/data-point
    parts = name.split("_", 1)
    drawer = parts[0]
    denomination = parts[1]
    
    #Takes the input for the changed denomination (number of bills), multiples by its value, and places result in corresponding sensor.
    for constants, multiplier, operation, in math_vars:
        if denomination == constants:
            state = float(new) * float(multiplier)
            self.set_state(sensorToUpdate, state = state)
            break
        else:
            state = float(new) * int(1)
            self.set_state(sensorToUpdate, state = state)
            
    #Calculates how much cash is in each drawer
    for drawer in drawers:
      total = 0
      for input in inputs:
        for constants, multiplier, operation in math_vars:
          if input == constants:
            sensorToEvaulate = "sensor." + drawer + "_" + input
            if operation == "+":
              total += float(self.get_state(sensorToEvaulate))
            if operation == "-":
              total -= float(self.get_state(sensorToEvaulate))
      drawerTotalToUpdate = "sensor." + drawer + "_" + "drawer_total"
      self.set_state(drawerTotalToUpdate, state = total)
      #Calculates how much the drawer says the sales should be (total - beginning cash)
      drawer_begin = float(self.get_state("sensor." + drawer + "_" + "begin")) 
      drawerSalesToUpdate = "sensor." + drawer + "_" + "drawer_sales"
      self.set_state(drawerSalesToUpdate, state = total - drawer_begin)
      #Compares the register sales to the drawer sales to ensure they are balanced (+/- $10)
      
      

    # End calculations

# BELOW IS NOT USED... Currently Disabled. (Couldn't figure out how to make it work but still defined in apps.yaml.)
class Drawer_Calculations(hass.Hass):
  def initialize(self):
    for drawer in drawers:
      for input in inputs:
        entityToMonitor = "input_text." + drawer + "_" + input
  #      self.listen_state(self.CB, entityToMonitor)
    
  def CB(self, entity, attribute, old, new, kwargs): 
    for drawer in drawers:
      total = 0
      for input in inputs:
        for constants, multiplier, operation in math_vars:
          if input == constants:
            sensorToEvaulate = "sensor." + drawer + "_" + input
            if operation == "+":
              total += float(self.get_state(sensorToEvaulate))
            if operation == "-":
              total -= float(self.get_state(sensorToEvaulate))

 #     drawerTotalToUpdate = "sensor." + drawer + "_" + "drawer_total"
 #     self.set_state(drawerTotalToUpdate, state = total)
   
