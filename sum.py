import hassapi as hass

class Sum(hass.Hass):
  global drawers
  global inputs
  global sensors
  drawers = ["pastaria", "seconda", "sarefinos"]
  inputs = ["100", "50", "20", "10", "5", "1", "q", "cc", "gc", "po", "begin", "2pm_x", "5pm_x", "cust_count", "sales"]
  totals = ["drawer_total", "drawer_sales", "begin_total", "drop_total"]
  sensors = inputs + totals

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
    type, name = self.split_entity(entity)
    parts = name.split("_", 1)
    drawer = parts[0]
    denomination = parts[1]
    
    math_vars = [("100", 100, "+"), ("50", 50, "+"), ("20", 50, "+"), ("10", 10, "+"), ("5", 5, "+"), ("1", 1, "+"), ("q", 0.25, "+"), ("cc", 1, "+"), ("gc", 1, "+"), ("po", 1, "-")]
    for constants, multiplier, operation, in math_vars:
        if denomination == constants:
            state = int(new) * int(multiplier)
            self.set_state(sensorToUpdate, state = state)
            break
        else:
            state = int(new) * int(1)
            self.set_state(sensorToUpdate, state = state)




# Perform math on the each drawer
#math_vars = [("100", 100, "+"), ("50", 50, "+"), ("20", 50, "+"), ("10", 10, "+"), ("5", 5, "+"), ("1", 1, "+"), ("q", 0.25, "+"), ("cc", 1, "+"), ("gc", 1, "+"), ("po", 1, "-")]
#for x in drawers:
#    total = 0
#    for a, b, c in math_vars:
#      entityToEvaluate = "input_text." + x + "_" + a
#      total += float(self.get_state(entityToEvaluate)) * b
#    
#    self.log(x + " " + str(total))
#
#state = self.get_state("input_text.pastaria_1")
#self.log(state)
