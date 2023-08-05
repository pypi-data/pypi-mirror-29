

class CANifier {

  void * m_handle;

public:
  void _create1(int deviceNumber) {
    m_handle = c_CANifier_Create1(deviceNumber);
  }

  ctre::phoenix::ErrorCode setLEDOutput(uint32_t dutyCycle, uint32_t ledChannel) {
    
    auto __ret = c_CANifier_SetLEDOutput(m_handle, dutyCycle, ledChannel );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutputs(uint32_t outputsBits, uint32_t isOutputBits) {
    
    auto __ret = c_CANifier_SetGeneralOutputs(m_handle, outputsBits, isOutputBits );
    return __ret;
  }


  ctre::phoenix::ErrorCode setGeneralOutput(uint32_t outputPin, bool outputValue, bool outputEnable) {
    
    auto __ret = c_CANifier_SetGeneralOutput(m_handle, outputPin, outputValue, outputEnable );
    return __ret;
  }


  ctre::phoenix::ErrorCode setPWMOutput(uint32_t pwmChannel, uint32_t dutyCycle) {
    
    auto __ret = c_CANifier_SetPWMOutput(m_handle, pwmChannel, dutyCycle );
    return __ret;
  }


  ctre::phoenix::ErrorCode enablePWMOutput(uint32_t pwmChannel, bool bEnable) {
    
    auto __ret = c_CANifier_EnablePWMOutput(m_handle, pwmChannel, bEnable );
    return __ret;
  }


  bool getGeneralInput(uint32_t inputPin) {
    bool measuredInput;
     c_CANifier_GetGeneralInput(m_handle, inputPin, &measuredInput );
    return measuredInput;
  }


  std::array<double, 2> getPWMInput(uint32_t pwmChannel) {
    std::array<double, 2> dutyCycleAndPeriod;
     c_CANifier_GetPWMInput(m_handle, pwmChannel, dutyCycleAndPeriod.data() );
    return dutyCycleAndPeriod;
  }


  ctre::phoenix::ErrorCode getLastError() {
    
    auto __ret = c_CANifier_GetLastError(m_handle );
    return __ret;
  }


  double getBusVoltage() {
    double batteryVoltage;
     c_CANifier_GetBusVoltage(m_handle, &batteryVoltage );
    return batteryVoltage;
  }


  void setLastError(int error) {
    
     c_CANifier_SetLastError(m_handle, error );
    
  }


  ctre::phoenix::ErrorCode configSetParameter(int param, double value, int subValue, int ordinal, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigSetParameter(m_handle, param, value, subValue, ordinal, timeoutMs );
    return __ret;
  }


  double configGetParameter(int param, int ordinal, int timeoutMs) {
    double value;
     c_CANifier_ConfigGetParameter(m_handle, param, &value, ordinal, timeoutMs );
    return value;
  }


  ctre::phoenix::ErrorCode configSetCustomParam(int newValue, int paramIndex, int timeoutMs) {
    
    auto __ret = c_CANifier_ConfigSetCustomParam(m_handle, newValue, paramIndex, timeoutMs );
    return __ret;
  }


  int configGetCustomParam(int paramIndex, int timoutMs) {
    int readValue;
     c_CANifier_ConfigGetCustomParam(m_handle, &readValue, paramIndex, timoutMs );
    return readValue;
  }


  int getFaults() {
    int param;
     c_CANifier_GetFaults(m_handle, &param );
    return param;
  }


  int getStickyFaults() {
    int param;
     c_CANifier_GetStickyFaults(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode clearStickyFaults(int timeoutMs) {
    
    auto __ret = c_CANifier_ClearStickyFaults(m_handle, timeoutMs );
    return __ret;
  }


  int getFirmwareVersion() {
    int firmwareVers;
     c_CANifier_GetFirmwareVersion(m_handle, &firmwareVers );
    return firmwareVers;
  }


  bool hasResetOccurred() {
    bool hasReset;
     c_CANifier_HasResetOccurred(m_handle, &hasReset );
    return hasReset;
  }


  ctre::phoenix::ErrorCode setStatusFramePeriod(int frame, int periodMs, int timeoutMs) {
    
    auto __ret = c_CANifier_SetStatusFramePeriod(m_handle, frame, periodMs, timeoutMs );
    return __ret;
  }


  int getStatusFramePeriod(int frame, int timeoutMs) {
    int periodMs;
     c_CANifier_GetStatusFramePeriod(m_handle, frame, &periodMs, timeoutMs );
    return periodMs;
  }


  ctre::phoenix::ErrorCode setControlFramePeriod(int frame, int periodMs) {
    
    auto __ret = c_CANifier_SetControlFramePeriod(m_handle, frame, periodMs );
    return __ret;
  }


};