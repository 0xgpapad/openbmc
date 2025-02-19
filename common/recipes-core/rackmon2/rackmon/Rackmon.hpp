// Copyright 2021-present Facebook. All Rights Reserved.
#pragma once
#include <atomic>
#include <shared_mutex>
#include <thread>
#include "Modbus.hpp"
#include "ModbusDevice.hpp"
#include "PollThread.hpp"

namespace rackmon {

class Rackmon {
  static constexpr time_t kDormantMinInactiveTime = 300;
  static constexpr ModbusTime kProbeTimeout = std::chrono::milliseconds(50);
  std::vector<std::unique_ptr<PollThread<Rackmon>>> threads_{};
  // Has to be before defining active or dormant devices
  // to ensure users get destroyed before the interface.
  std::vector<std::unique_ptr<Modbus>> interfaces_{};
  RegisterMapDatabase registerMapDB_{};

  mutable std::shared_mutex devicesMutex_{};

  std::stringstream profileStore_{};

  // These devices discovered on actively monitored busses
  std::map<uint8_t, std::unique_ptr<ModbusDevice>> devices_{};

  // contains all the possible address allowed by currently
  // loaded register maps. A majority of these are not expected
  // to exist, but are candidates for a scan.
  std::vector<uint8_t> allPossibleDevAddrs_{};
  std::vector<uint8_t>::iterator nextDeviceToProbe_{};

  // As an optimization, devices are normally scanned one by one
  // This allows someone to initiate a forced full scan.
  // This mimicks a restart of rackmond.
  std::atomic<bool> reqForceScan_ = true;

  // Timestamps of last scan
  time_t lastScanTime_;
  time_t lastMonitorTime_;

  // Probe an interface for the presence of the address.
  bool probe(Modbus& interface, uint8_t addr);
  // Probe all interfaces for the presence of the address.
  bool probe(uint8_t addr);

  // --------- Private Methods --------

  // probe dormant devices and return recovered devices.
  std::vector<uint8_t> inspectDormant();
  // Try and recover dormant devices.
  void recoverDormant();

  bool isDeviceKnown(uint8_t);

  // Monitor loop. Blocks forever as long as req_stop is true.
  void monitor();

  // Scan all possible devices. Skips active/dormant devices.
  void fullScan();

  // Scan loop. Blocks forever as long as req_stop is true.
  void scan();

 protected:
  virtual std::unique_ptr<Modbus> makeInterface() {
    return std::make_unique<Modbus>(profileStore_);
  }
  const RegisterMapDatabase& getRegisterMapDatabase() const {
    return registerMapDB_;
  }

 public:
  virtual ~Rackmon() {
    stop();
  }

  // Load Interface configuration.
  void loadInterface(const nlohmann::json& config);

  // Load a register map into the internal database.
  void loadRegisterMap(const nlohmann::json& config);

  // Load configuration, preferable before starting, but can be
  // done at any time, but this is a one time only.
  void load(const std::string& confPath, const std::string& regmapDir);

  // Start the monitoring/scanning loops
  void start(PollThreadTime interval = std::chrono::minutes(3));
  // Stop the monitoring/scanning loops
  void stop();

  // Force rackmond to do a full scan on the next scan loop.
  void forceScan() {
    reqForceScan_ = true;
  }

  // Executes the Raw command. Throws an exception on error.
  void rawCmd(Msg& req, Msg& resp, ModbusTime timeout);

  // Read registers
  void readHoldingRegisters(
      uint8_t deviceAddress,
      uint16_t registerOffset,
      std::vector<uint16_t>& registerContents,
      ModbusTime timeout = ModbusTime::zero());

  // Write Single Register
  void writeSingleRegister(
      uint8_t deviceAddress,
      uint16_t registerOffset,
      uint16_t value,
      ModbusTime timeout = ModbusTime::zero());

  // Write multiple registers
  void writeMultipleRegisters(
      uint8_t deviceAddress,
      uint16_t registerOffset,
      std::vector<uint16_t>& values,
      ModbusTime timeout = ModbusTime::zero());

  // Read File Record
  void readFileRecord(
      uint8_t deviceAddress,
      std::vector<FileRecord>& records,
      ModbusTime timeout = ModbusTime::zero());

  // Get status of devices
  std::vector<ModbusDeviceInfo> listDevices() const;

  // Get monitored data
  void getRawData(std::vector<ModbusDeviceRawData>& data) const;

  // Get formatted monitor data
  void getFmtData(std::vector<ModbusDeviceFmtData>& data) const;

  // Get value data
  void getValueData(std::vector<ModbusDeviceValueData>& data) const;

  // Get profile data
  std::string getProfileData();
};

} // namespace rackmon
