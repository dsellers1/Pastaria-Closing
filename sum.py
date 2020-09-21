import hassapi as hass

class Sum(hass.Hass):
  global drawers
  global vars
  global sensors
  drawers = ["pastaria", "seconda", "sarefinos"]
  vars = ["100", "50", "20", "10", "5", "1", "q", "cc", "gc", "po", "begin", "2pm_x", "5pm_x", "cust_count", "sales"]
  sensors = "drawer_total", "drawer_sales", "begin_total", "drop_total"

  def initialize(self):
    for x in drawers:
      # Following loop used to ensure sensors are valid in HA. These sensors are used to store the results of calculations.
      for y in sensors:
        sensorToCheck = "sensor." + x + "_" + y
        if not self.entity_exists("sensor." + x + "_" + y):
          self.set_state(sensorToCheck, state = 0)     
      # Following loop used to monitor changes in input text boxes.
        entityToMonitor = "input_text." + x + "_" + a
      for a in vars:
        self.listen_state(self.CB, entityToMonitor)

#  def CB(self, entity, attribute, old, new, kwargs):
#    new_state = float(new) * 5 #for example for a 5 dollar shine"
#    self.set_state("sensor.sum", state = new_state)
#    for x in drawers:
#      for y in vars:
#        self.set_state("sensor.sum", state = new_state)

  def CB(self, entity, attribute, old, new, kwargs):
    # Determine what has changed by way of the entity name -- Not really needed. Just calculate everything...
    # Plus, turns out that AD has a function that slice the entity and type already...
    #monitoredEntityDrawer = entity.replace('input_text.', '') # Removes input_text
    #monitoredEntityDrawer = monitoredEntityDrawer.split('_') # Creates list: 0 = drawer, 1 = vars
    
    # Perform math on the each drawer
    math_vars = [("100", 100, "+"), ("50", 50, "+"), ("20", 50, "+"), ("10", 10, "+"), ("5", 5, "+"), ("1", 1, "+"), ("q", 0.25, "+"), ("cc", 1, "+"), ("gc", 1, "+"), ("po", 1, "-")]
    for x in drawers:
        total = 0
        for a, b, c in math_vars:
          entityToEvaluate = "input_text." + x + "_" + a
          total += float(self.get_state(entityToEvaluate)) * b
         
        self.log(x + " " + str(total))
    
    #state = self.get_state("input_text.pastaria_1")
    #self.log(state)
