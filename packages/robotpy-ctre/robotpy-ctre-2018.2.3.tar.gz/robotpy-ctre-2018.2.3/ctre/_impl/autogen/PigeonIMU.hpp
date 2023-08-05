

class PigeonIMU {

  void * m_handle;

public:
  void _create2(int talonDeviceID) {
    m_handle = c_PigeonIMU_Create2(talonDeviceID);
  }

  void _create1(int deviceNumber) {
    m_handle = c_PigeonIMU_Create1(deviceNumber);
  }

  ctre::phoenix::ErrorCode setYaw(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetYaw(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode addYaw(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_AddYaw(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setYawToCompass(int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetYawToCompass(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setFusedHeading(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetFusedHeading(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode addFusedHeading(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_AddFusedHeading(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setFusedHeadingToCompass(int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetFusedHeadingToCompass(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setAccumZAngle(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetAccumZAngle(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode configTemperatureCompensationEnable(int bTempCompEnable, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_ConfigTemperatureCompensationEnable(m_handle, bTempCompEnable, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setCompassDeclination(double angleDegOffset, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetCompassDeclination(m_handle, angleDegOffset, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setCompassAngle(double angleDeg, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetCompassAngle(m_handle, angleDeg, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode enterCalibrationMode(int calMode, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_EnterCalibrationMode(m_handle, calMode, timeoutMs );
    return __ret;
  }


  std::tuple<int, int, int, int, double, int, int, int, int> getGeneralStatus() {
    int state;int currentMode;int calibrationError;int bCalIsBooting;double tempC;int upTimeSec;int noMotionBiasCount;int tempCompensationCount;int lastError;
     c_PigeonIMU_GetGeneralStatus(m_handle, &state, &currentMode, &calibrationError, &bCalIsBooting, &tempC, &upTimeSec, &noMotionBiasCount, &tempCompensationCount, &lastError );
    return std::make_tuple(state,currentMode,calibrationError,bCalIsBooting,tempC,upTimeSec,noMotionBiasCount,tempCompensationCount,lastError);
  }


  ctre::phoenix::ErrorCode getLastError() {
    
    auto __ret = c_PigeonIMU_GetLastError(m_handle );
    return __ret;
  }


  std::array<double, 4> get6dQuaternion() {
    std::array<double, 4> wxyz;
     c_PigeonIMU_Get6dQuaternion(m_handle, wxyz.data() );
    return wxyz;
  }


  std::array<double, 3> getYawPitchRoll() {
    std::array<double, 3> ypr;
     c_PigeonIMU_GetYawPitchRoll(m_handle, ypr.data() );
    return ypr;
  }


  std::array<double, 3> getAccumGyro() {
    std::array<double, 3> xyz_deg;
     c_PigeonIMU_GetAccumGyro(m_handle, xyz_deg.data() );
    return xyz_deg;
  }


  double getAbsoluteCompassHeading() {
    double value;
     c_PigeonIMU_GetAbsoluteCompassHeading(m_handle, &value );
    return value;
  }


  double getCompassHeading() {
    double value;
     c_PigeonIMU_GetCompassHeading(m_handle, &value );
    return value;
  }


  double getCompassFieldStrength() {
    double value;
     c_PigeonIMU_GetCompassFieldStrength(m_handle, &value );
    return value;
  }


  double getTemp() {
    double value;
     c_PigeonIMU_GetTemp(m_handle, &value );
    return value;
  }


  int getState() {
    int state;
     c_PigeonIMU_GetState(m_handle, &state );
    return state;
  }


  int getUpTime() {
    int value;
     c_PigeonIMU_GetUpTime(m_handle, &value );
    return value;
  }


  std::array<short, 3> getRawMagnetometer() {
    std::array<short, 3> rm_xyz;
     c_PigeonIMU_GetRawMagnetometer(m_handle, rm_xyz.data() );
    return rm_xyz;
  }


  std::array<short, 3> getBiasedMagnetometer() {
    std::array<short, 3> bm_xyz;
     c_PigeonIMU_GetBiasedMagnetometer(m_handle, bm_xyz.data() );
    return bm_xyz;
  }


  std::array<short, 3> getBiasedAccelerometer() {
    std::array<short, 3> ba_xyz;
     c_PigeonIMU_GetBiasedAccelerometer(m_handle, ba_xyz.data() );
    return ba_xyz;
  }


  std::array<double, 3> getRawGyro() {
    std::array<double, 3> xyz_dps;
     c_PigeonIMU_GetRawGyro(m_handle, xyz_dps.data() );
    return xyz_dps;
  }


  std::array<double, 3> getAccelerometerAngles() {
    std::array<double, 3> tiltAngles;
     c_PigeonIMU_GetAccelerometerAngles(m_handle, tiltAngles.data() );
    return tiltAngles;
  }


  std::tuple<int, int, double, int> _getFusedHeading2() {
    int bIsFusing;int bIsValid;double value;int lastError;
     c_PigeonIMU_GetFusedHeading2(m_handle, &bIsFusing, &bIsValid, &value, &lastError );
    return std::make_tuple(bIsFusing,bIsValid,value,lastError);
  }


  double _getFusedHeading1() {
    double value;
     c_PigeonIMU_GetFusedHeading1(m_handle, &value );
    return value;
  }


  int getResetCount() {
    int value;
     c_PigeonIMU_GetResetCount(m_handle, &value );
    return value;
  }


  int getResetFlags() {
    int value;
     c_PigeonIMU_GetResetFlags(m_handle, &value );
    return value;
  }


  int getFirmwareVersion() {
    int firmwareVers;
     c_PigeonIMU_GetFirmwareVersion(m_handle, &firmwareVers );
    return firmwareVers;
  }


  bool hasResetOccurred() {
    bool hasReset;
     c_PigeonIMU_HasResetOccurred(m_handle, &hasReset );
    return hasReset;
  }


  ctre::phoenix::ErrorCode setLastError(int value) {
    
    auto __ret = c_PigeonIMU_SetLastError(m_handle, value );
    return __ret;
  }


  int getFaults() {
    int param;
     c_PigeonIMU_GetFaults(m_handle, &param );
    return param;
  }


  int getStickyFaults() {
    int param;
     c_PigeonIMU_GetStickyFaults(m_handle, &param );
    return param;
  }


  ctre::phoenix::ErrorCode clearStickyFaults(int timeoutMs) {
    
    auto __ret = c_PigeonIMU_ClearStickyFaults(m_handle, timeoutMs );
    return __ret;
  }


  ctre::phoenix::ErrorCode setStatusFramePeriod(int frame, int periodMs, int timeoutMs) {
    
    auto __ret = c_PigeonIMU_SetStatusFramePeriod(m_handle, frame, periodMs, timeoutMs );
    return __ret;
  }


  int getStatusFramePeriod(int frame, int timeoutMs) {
    int periodMs;
     c_PigeonIMU_GetStatusFramePeriod(m_handle, frame, &periodMs, timeoutMs );
    return periodMs;
  }


  ctre::phoenix::ErrorCode setControlFramePeriod(int frame, int periodMs) {
    
    auto __ret = c_PigeonIMU_SetControlFramePeriod(m_handle, frame, periodMs );
    return __ret;
  }


};