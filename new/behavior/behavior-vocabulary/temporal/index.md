Status: NORMATIVE
Lock State: UNLOCKED
Version: 0.1
Editor: Charles F. Munat

# Behavior Vocabulary — Temporal

This specification defines the **Temporal operator family** for the Behavior Vocabulary.

This document is **Normative**.

---

## 1. Purpose

This specification defines comprehensive temporal operations for Behavior Programs, including:

- Construction and decomposition of temporal values
- Temporal arithmetic
- Comparison and ordering
- Formatting and parsing
- Time zone operations
- Calendar operations

Temporal values are first-class semantic types, not Text with guards.

---

## 2. Temporal Types

As defined by Behavior Dialect Semantics:

- `PlainDate` — calendar date without time
- `PlainTime` — time of day without date
- `PlainDateTime` — local date and time without timezone
- `PlainYearMonth` — year and month
- `PlainMonthDay` — month and day
- `YearWeek` — ISO week date
- `Instant` — absolute point in time (UTC)
- `ZonedDateTime` — date-time with timezone
- `Duration` — ISO 8601 duration
- `TimeZone` — IANA timezone identifier
- `Calendar` — enumerated calendar system (default: `iso8601`)

---

## 3. Construction (Normative)

### 3.1 PlainDate

```
MakePlainDate(year, month, day) -> PlainDate
```

Error behavior:
- If invalid date: `Invalid(...)` with code `Temporal::INVALID_DATE`.

### 3.2 PlainTime

```
MakePlainTime(hour, minute) -> PlainTime
MakePlainTime(hour, minute, second) -> PlainTime
MakePlainTime(hour, minute, second, millisecond) -> PlainTime
MakePlainTime(hour, minute, second, millisecond, microsecond) -> PlainTime
MakePlainTime(hour, minute, second, millisecond, microsecond, nanosecond) -> PlainTime
```

### 3.3 PlainDateTime

```
MakePlainDateTime(year, month, day, hour, minute) -> PlainDateTime
MakePlainDateTime(year, month, day, hour, minute, second) -> PlainDateTime
MakePlainDateTime(year, month, day, hour, minute, second, millisecond) -> PlainDateTime
```

### 3.4 PlainYearMonth

```
MakePlainYearMonth(year, month) -> PlainYearMonth
```

### 3.5 PlainMonthDay

```
MakePlainMonthDay(month, day) -> PlainMonthDay
```

### 3.6 YearWeek

```
MakeYearWeek(year, week) -> YearWeek
```

Error behavior:
- If week < 1 or > max weeks in year: `Invalid(...)`.

### 3.7 Instant

```
MakeInstant(epochMilliseconds) -> Instant
MakeInstantFromNanoseconds(epochNanoseconds) -> Instant
```

### 3.8 ZonedDateTime

```
MakeZonedDateTime(instant, timeZone) -> ZonedDateTime
MakeZonedDateTime(year, month, day, hour, minute, second, timeZone) -> ZonedDateTime
```

### 3.9 Duration

```
MakeDuration(years, months, weeks, days, hours, minutes, seconds) -> Duration
MakeDurationFromMilliseconds(milliseconds) -> Duration
```

All parameters default to 0.

### 3.10 From Components

```
PlainDateFromComponents(record) -> PlainDate
PlainTimeFromComponents(record) -> PlainTime
PlainDateTimeFromComponents(record) -> PlainDateTime
```

Accepts Record with fields: `year`, `month`, `day`, `hour`, `minute`, `second`, etc.

---

## 4. Decomposition (Normative)

### 4.1 Date Components

```
Year(temporal) -> Integer
Month(temporal) -> Integer
Day(temporal) -> Integer
DayOfWeek(temporal) -> Integer
DayOfYear(temporal) -> Integer
WeekOfYear(temporal) -> Integer
```

`DayOfWeek` returns 1 (Monday) to 7 (Sunday) per ISO 8601.

### 4.2 Time Components

```
Hour(temporal) -> Integer
Minute(temporal) -> Integer
Second(temporal) -> Integer
Millisecond(temporal) -> Integer
Microsecond(temporal) -> Integer
Nanosecond(temporal) -> Integer
```

### 4.3 Combined Components

```
DateComponents(temporal) -> Record { year, month, day }
TimeComponents(temporal) -> Record { hour, minute, second, millisecond, microsecond, nanosecond }
DateTimeComponents(temporal) -> Record { year, month, day, hour, minute, second, ... }
```

### 4.4 Duration Components

```
DurationYears(duration) -> Integer
DurationMonths(duration) -> Integer
DurationWeeks(duration) -> Integer
DurationDays(duration) -> Integer
DurationHours(duration) -> Integer
DurationMinutes(duration) -> Integer
DurationSeconds(duration) -> Integer
DurationMilliseconds(duration) -> Integer
DurationTotalMilliseconds(duration) -> Integer
DurationTotalSeconds(duration) -> RealNumber
```

### 4.5 ZonedDateTime Components

```
TimeZoneOf(zonedDateTime) -> TimeZone
InstantOf(zonedDateTime) -> Instant
OffsetOf(zonedDateTime) -> Text
```

`OffsetOf` returns offset string like "+05:30" or "Z".

---

## 5. Conversion (Normative)

### 5.1 Between Temporal Types

```
ToPlainDate(temporal) -> PlainDate
ToPlainTime(temporal) -> PlainTime
ToPlainDateTime(temporal) -> PlainDateTime
ToPlainYearMonth(temporal) -> PlainYearMonth
ToPlainMonthDay(temporal) -> PlainMonthDay
```

### 5.2 To Instant

```
ToInstant(zonedDateTime) -> Instant
ToInstantInTimeZone(plainDateTime, timeZone) -> Instant
```

Note: `ToInstantInTimeZone` may be ambiguous during DST transitions.

Error behavior:
- If ambiguous and no disambiguation rule: `Invalid(...)` with code `Temporal::AMBIGUOUS_TIME`.

```
ToInstantInTimeZoneWithDisambiguation(plainDateTime, timeZone, disambiguation) -> Instant
```

Disambiguation options:
- `earlier` — use earlier of two possible times
- `later` — use later of two possible times
- `compatible` — use behavior compatible with legacy Date
- `reject` — return Invalid

### 5.3 To ZonedDateTime

```
ToZonedDateTime(instant, timeZone) -> ZonedDateTime
PlainDateTimeToZonedDateTime(plainDateTime, timeZone) -> ZonedDateTime
```

### 5.4 To Epoch Values

```
ToEpochMilliseconds(instant) -> Integer
ToEpochSeconds(instant) -> Integer
ToEpochNanoseconds(instant) -> Integer
```

---

## 6. Arithmetic (Normative)

### 6.1 Adding Duration

```
AddDuration(temporal, duration) -> Temporal
AddYears(temporal, years) -> Temporal
AddMonths(temporal, months) -> Temporal
AddWeeks(temporal, weeks) -> Temporal
AddDays(temporal, days) -> Temporal
AddHours(temporal, hours) -> Temporal
AddMinutes(temporal, minutes) -> Temporal
AddSeconds(temporal, seconds) -> Temporal
AddMilliseconds(temporal, milliseconds) -> Temporal
```

### 6.2 Subtracting Duration

```
SubtractDuration(temporal, duration) -> Temporal
SubtractYears(temporal, years) -> Temporal
SubtractMonths(temporal, months) -> Temporal
SubtractWeeks(temporal, weeks) -> Temporal
SubtractDays(temporal, days) -> Temporal
SubtractHours(temporal, hours) -> Temporal
SubtractMinutes(temporal, minutes) -> Temporal
SubtractSeconds(temporal, seconds) -> Temporal
SubtractMilliseconds(temporal, milliseconds) -> Temporal
```

### 6.3 Difference

```
DifferenceBetween(temporal1, temporal2, largestUnit) -> Duration
```

Parameters:
- `largestUnit`: "years", "months", "weeks", "days", "hours", "minutes", "seconds"

```
DaysBetween(date1, date2) -> Integer
MonthsBetween(date1, date2) -> Integer
YearsBetween(date1, date2) -> Integer
HoursBetween(temporal1, temporal2) -> Integer
MinutesBetween(temporal1, temporal2) -> Integer
SecondsBetween(temporal1, temporal2) -> Integer
MillisecondsBetween(temporal1, temporal2) -> Integer
```

### 6.4 Duration Arithmetic

```
AddDurations(duration1, duration2) -> Duration
SubtractDurations(duration1, duration2) -> Duration
MultiplyDuration(duration, factor) -> Duration
DivideDuration(duration, divisor) -> Duration
NegateDuration(duration) -> Duration
AbsoluteDuration(duration) -> Duration
```

---

## 7. Comparison (Normative)

### 7.1 Ordering Relations

```
IsAfter(temporal1, temporal2) -> Boolean
IsBefore(temporal1, temporal2) -> Boolean
IsAfterOrEqual(temporal1, temporal2) -> Boolean
IsBeforeOrEqual(temporal1, temporal2) -> Boolean
IsSameInstant(temporal1, temporal2) -> Boolean
```

### 7.2 Date Relations

```
IsAfterDate(date1, date2) -> Boolean
IsBeforeDate(date1, date2) -> Boolean
IsSameDate(date1, date2) -> Boolean
```

### 7.3 Time Relations

```
IsAfterTime(time1, time2) -> Boolean
IsBeforeTime(time1, time2) -> Boolean
IsSameTime(time1, time2) -> Boolean
```

### 7.4 DateTime Relations

```
IsAfterDateTime(dt1, dt2) -> Boolean
IsBeforeDateTime(dt1, dt2) -> Boolean
IsSameDateTime(dt1, dt2) -> Boolean
```

### 7.5 Range Checks

```
IsBetween(temporal, start, end) -> Boolean
IsBetweenInclusive(temporal, start, end) -> Boolean
```

### 7.6 Duration Comparison

```
IsLongerDuration(duration1, duration2) -> Boolean
IsShorterDuration(duration1, duration2) -> Boolean
IsSameDuration(duration1, duration2) -> Boolean
IsZeroDuration(duration) -> Boolean
IsNegativeDuration(duration) -> Boolean
```

---

## 8. Rounding and Truncation (Normative)

### 8.1 Rounding Temporal Values

```
RoundToNearest(temporal, unit) -> Temporal
RoundUp(temporal, unit) -> Temporal
RoundDown(temporal, unit) -> Temporal
```

Units: "day", "hour", "minute", "second", "millisecond"

### 8.2 Start/End of Period

```
StartOfDay(temporal) -> PlainDateTime
EndOfDay(temporal) -> PlainDateTime
StartOfMonth(temporal) -> PlainDate
EndOfMonth(temporal) -> PlainDate
StartOfYear(temporal) -> PlainDate
EndOfYear(temporal) -> PlainDate
StartOfWeek(temporal) -> PlainDate
EndOfWeek(temporal) -> PlainDate
StartOfHour(temporal) -> PlainDateTime
EndOfHour(temporal) -> PlainDateTime
```

### 8.3 Duration Rounding

```
RoundDuration(duration, largestUnit, smallestUnit) -> Duration
```

---

## 9. Calendar Operations (Normative)

### 9.1 Day Properties

```
IsWeekday(date) -> Boolean
IsWeekend(date) -> Boolean
IsLeapYear(year) -> Boolean
IsLeapYear(date) -> Boolean
DaysInMonth(year, month) -> Integer
DaysInMonth(date) -> Integer
DaysInYear(year) -> Integer
WeeksInYear(year) -> Integer
```

### 9.2 Day Names

```
DayOfWeekName(date) -> Text
DayOfWeekShortName(date) -> Text
MonthName(date) -> Text
MonthShortName(date) -> Text
```

Note: Returns English names. Localization is a presentation concern.

### 9.3 Quarter Operations

```
Quarter(date) -> Integer
StartOfQuarter(date) -> PlainDate
EndOfQuarter(date) -> PlainDate
```

### 9.4 ISO Week Operations

```
IsoWeekYear(date) -> Integer
IsoWeek(date) -> Integer
DateFromIsoWeek(year, week, dayOfWeek) -> PlainDate
```

---

## 10. Time Zone Operations (Normative)

### 10.1 Time Zone Construction

```
MakeTimeZone(identifier) -> TimeZone
```

Error behavior:
- If invalid identifier: `Invalid(...)` with code `Temporal::INVALID_TIMEZONE`.

### 10.2 Time Zone Conversion

```
ConvertToTimeZone(zonedDateTime, timeZone) -> ZonedDateTime
```

### 10.3 Time Zone Information

```
TimeZoneOffset(zonedDateTime) -> Text
TimeZoneOffsetMinutes(zonedDateTime) -> Integer
TimeZoneName(zonedDateTime) -> Text
IsDaylightSavingTime(zonedDateTime) -> Boolean
```

### 10.4 UTC Operations

```
ToUtc(zonedDateTime) -> ZonedDateTime
FromUtc(instant, timeZone) -> ZonedDateTime
```

---

## 11. Parsing and Formatting (Normative)

### 11.1 ISO 8601 Parsing

```
ParsePlainDate(text) -> PlainDate
ParsePlainTime(text) -> PlainTime
ParsePlainDateTime(text) -> PlainDateTime
ParseInstant(text) -> Instant
ParseZonedDateTime(text) -> ZonedDateTime
ParseDuration(text) -> Duration
```

All parse functions accept ISO 8601 format.

Error behavior:
- If invalid format: `Invalid(...)` with code `Temporal::INVALID_FORMAT`.

### 11.2 ISO 8601 Formatting

```
FormatIso(temporal) -> Text
FormatIsoDate(temporal) -> Text
FormatIsoTime(temporal) -> Text
FormatIsoDuration(duration) -> Text
```

### 11.3 Custom Formatting

```
FormatTemporal(temporal, pattern) -> Text
```

Pattern tokens (subset):
- `YYYY` — 4-digit year
- `YY` — 2-digit year
- `MM` — 2-digit month
- `DD` — 2-digit day
- `HH` — 2-digit hour (24h)
- `hh` — 2-digit hour (12h)
- `mm` — 2-digit minute
- `ss` — 2-digit second
- `SSS` — 3-digit millisecond
- `A` / `a` — AM/PM

Note: Pattern formatting returns English. Localization is a presentation concern.

---

## 12. Type Guards (Normative)

```
IsPlainDate(value) -> Boolean
IsPlainTime(value) -> Boolean
IsPlainDateTime(value) -> Boolean
IsPlainYearMonth(value) -> Boolean
IsPlainMonthDay(value) -> Boolean
IsYearWeek(value) -> Boolean
IsInstant(value) -> Boolean
IsZonedDateTime(value) -> Boolean
IsDuration(value) -> Boolean
IsTimeZone(value) -> Boolean
IsCalendar(value) -> Boolean
IsTemporal(value) -> Boolean
```

`IsTemporal` returns true for any temporal type.

---

## 13. Special Values (Normative)

### 13.1 Now (Input-Supplied)

These operators require the current time to be supplied as an explicit input.

```
NowInstant(currentInstant) -> Instant
NowZonedDateTime(currentInstant, timeZone) -> ZonedDateTime
TodayDate(currentInstant, timeZone) -> PlainDate
CurrentTime(currentInstant, timeZone) -> PlainTime
```

Rationale: Behavior evaluation must be deterministic. The current time is an ambient dependency that must be supplied explicitly.

### 13.2 Epoch

```
EpochInstant() -> Instant
```

Returns: 1970-01-01T00:00:00Z

---

## 14. Validation (Normative)

```
IsValidDate(year, month, day) -> Boolean
IsValidTime(hour, minute, second) -> Boolean
IsValidTimeZone(identifier) -> Boolean
```

---

**End of Behavior Vocabulary — Temporal v0.1**
