#pragma once

#include <string>

#include "ora/types.hh"

namespace ora {

//------------------------------------------------------------------------------
// Exceptions
//------------------------------------------------------------------------------

class DateError
  : public Error
{
public:

  DateError(std::string const& message) : Error(message) {}
  virtual ~DateError() = default;

};


class DateFormatError
: public DateError
{
public:

  DateFormatError(std::string const& message): DateError(message) {}
  virtual ~DateFormatError() = default;

};


class DateRangeError
  : public DateError
{
public:

  DateRangeError() : DateError("date not in range") {}
  virtual ~DateRangeError() = default;

};


class InvalidDateError
  : public DateError
{
public:

  InvalidDateError() : DateError("invalid date") {}
  virtual ~InvalidDateError() = default;

};


class DaytimeError
  : public Error
{
public:

  DaytimeError(std::string const& message) : Error(message) {}
  virtual ~DaytimeError() = default;

};


class DaytimeRangeError
  : public DaytimeError
{
public:

  DaytimeRangeError() : DaytimeError("daytime not in range") {}
  virtual ~DaytimeRangeError() = default;

};


class DaytimeFormatError
  : public DaytimeError
{
public:

  DaytimeFormatError(std::string const& message): DaytimeError(message) {}
  virtual ~DaytimeFormatError() = default;

};


class TimeError
  : public Error
{
public:

  TimeError(std::string const& message) : Error(message) {}
  virtual ~TimeError() = default;

};


class InvalidTimeError
  : public TimeError
{
public:

  InvalidTimeError() : TimeError("invalid time") {}
  virtual ~InvalidTimeError() = default;

};


class TimeRangeError
  : public TimeError
{
public:

  TimeRangeError() : TimeError("time out of range") {}
  virtual ~TimeRangeError() noexcept = default;

};


class InvalidDaytimeError
  : public DaytimeError
{
public:

  InvalidDaytimeError() : DaytimeError("invalid daytime") {}
  virtual ~InvalidDaytimeError() = default;

};


class NonexistentDateDaytime
  : public Error
{
public:

  NonexistentDateDaytime() : Error("local time does not exist") {}
  virtual ~NonexistentDateDaytime() = default;

};


class TimeFormatError
  : public FormatError
{
public:

  TimeFormatError(std::string const& name) : FormatError(std::string("in time pattern: ") + name) {}
  virtual ~TimeFormatError() = default;

};


//------------------------------------------------------------------------------

}  // namespace ora

