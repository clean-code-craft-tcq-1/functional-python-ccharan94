"""
----------------------------------------
Threshold Limits for BMS:
----------------------------------------    
Temperature      : Celsius
State of Charge  : Percentage
Charge Rate      : Ratio (0 to 1)
----------------------------------------
"""

batteryThresholdParams = { 'Lithium' : 
                            {
                            'Temperature'  : { 'lower':  0   , 'upper': 45 },
                            'StateOfCharge': { 'lower': 20   , 'upper': 80 },
                            'ChargeRate'   : { 'upper': 0.8                },
                            }, 
                                    
                         'NiMh' :   
                            {
                            'Temperature'  : { 'lower': -20  , 'upper': 40 },
                            'StateOfCharge': { 'lower':  20  , 'upper': 80 },
                            'ChargeRate'   : { 'upper': 0.8                },
                            },   
                         }

def getBatteryThresholdLimit(batteryType):
    return batteryThresholdParams[batteryType]

#Check if Battery is working fine
def battery_is_ok(**kwargs):
  
  batteryLimits             = getBatteryThresholdLimit(CURRENT_BATTERYPACK)
  isWithinLimits            = True
  
  global BATTERY_CONDITION_ALL_OK
  BATTERY_CONDITION_ALL_OK  = True
  
  for criteria, criteriavalue in kwargs.items():
      isWithinLimits = checkBoundaryCondition(batteryLimits,criteria, criteriavalue)
       
      if isWithinLimits is False:
          BATTERY_CONDITION_ALL_OK = False        
            
  return BATTERY_CONDITION_ALL_OK

def checkBoundaryCondition(batteryLimits,criteria, criteriavalue):
      if 'upper' in batteryLimits[criteria] and 'lower' in batteryLimits[criteria]:         
          upper = batteryLimits[criteria]['upper']
          lower = batteryLimits[criteria]['lower']
          isWithinLimits = checkRangeLimit(criteria,criteriavalue,upper,lower)
      elif 'upper' in batteryLimits[criteria] and 'lower' not in batteryLimits[criteria]:
          upper = batteryLimits[criteria]['upper']
          isWithinLimits = checkUpperLimit(criteria,criteriavalue,upper)
      elif 'upper' not in batteryLimits[criteria] and 'lower' in batteryLimits[criteria]:
          lower = batteryLimits[criteria]['lower']
          isWithinLimits = checkLowerLimit(criteria,criteriavalue,lower)
          
      return isWithinLimits  
    
def checkUpperLimit(criteria,criteriavalue,upper):
    if  criteriavalue > upper :
        print ('Alert: {} Threshold Value breached. Current value is {}'.format(criteria,criteriavalue))
        return False
    

def checkLowerLimit(criteria,criteriavalue,lower):
    if criteriavalue < lower :
        print ('Alert: {} Threshold Value breached. Current value is {}'.format(criteria,criteriavalue))
        return False

def checkRangeLimit(criteria,criteriavalue,upper,lower):
    if criteriavalue < lower  or criteriavalue > upper:
        print ('Alert: {} Threshold Value breached. Current value is {}'.format(criteria,criteriavalue))
        return False


if __name__ == '__main__':
    
  #declare the battery type to test
  CURRENT_BATTERYPACK       =   'Lithium'
  
  #Create boundary values for test - middle range, upper limit, lower limit
  temperature_limits = batteryThresholdParams[CURRENT_BATTERYPACK]['Temperature']
  soc_limits         = batteryThresholdParams[CURRENT_BATTERYPACK]['StateOfCharge']
  chargerate_limits  = batteryThresholdParams[CURRENT_BATTERYPACK]['ChargeRate']
  
  #middle range
  temp_middle_range        = ( temperature_limits['upper'] - temperature_limits['lower'] ) / 2
  soc_middle_range         = ( soc_limits['upper'] - soc_limits['lower'] ) / 2
  chargerate_middle_range  = chargerate_limits['upper']  / 2
  
  #------------------------------------------------------
  #Generate dynamic testcases independent of battery type
  #------------------------------------------------------
  
  """Temperature Tests"""
  #Testcase for normal temperature working range 
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is True), 'Temperature Range Test'
  #Testcase to check Upper limit breach for temperature
  assert(battery_is_ok(Temperature = temperature_limits['upper']+5, StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is False), 'Temperature Upper Limit Test'
  #Testcase to check Lower limit breach for temperature 
  assert(battery_is_ok(Temperature = temperature_limits['lower']-5, StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is False), 'Temperature Lower Limit Test'
  #Lower limit edge testcase for temperature
  assert(battery_is_ok(Temperature = temperature_limits['lower'], StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is True), 'Temperature Lower Limit Edge Test'
  #Upper limit edge testcase for temperature
  assert(battery_is_ok(Temperature = temperature_limits['upper'], StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is True), 'Temperature Upper Limit Edge Test'

  """State Of Charge Tests"""
  #Testcase for normal State of charge working range 
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range) is True), 'SOC Range Test'
  #Testcase to check Upper limit breach for State of charge
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_limits['upper']+5, ChargeRate = chargerate_middle_range) is False), 'SOC Limit Test'
  #Testcase to check Lower limit breach for State of charge 
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_limits['lower']-5, ChargeRate = chargerate_middle_range) is False), 'SOC Lower Limit Test'
  #Upper limit edge testcase for State of charge 
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_limits['upper'], ChargeRate = chargerate_middle_range) is True), 'SOC Upper Limit Edge Test'
  #Lower limit edge testcase for State of charge
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_limits['lower'], ChargeRate = chargerate_middle_range) is True), 'SOC Lower Limit Edge Test'

  """Charge Rate Tests"""
  #Testcase for normal Charge Rate working range 
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_middle_range, ChargeRate = chargerate_middle_range ) is True), 'Charge Rate Range Test'
  #Testcase to check Upper limit breach for Charge Rate
  assert(battery_is_ok(Temperature = temp_middle_range, StateOfCharge = soc_middle_range, ChargeRate = chargerate_limits['upper']+0.1) is False), 'Charge Upper Limit Test'
