# Synchronization schedules

Conf2Git synchronizes **Confluence to GitHub**. Each mapping can have one automatic schedule.
**Sync now** is independent of that schedule. Both require a ready mapping, current Marketplace
entitlement, verified GitHub access, and no other active run for the mapping.

## Choose and save a schedule

In **Connections**, find the mapping and select **Edit schedule**:

1. Choose **Disabled**, **Daily**, **Weekly**, or **Monthly**. New mappings start **Disabled**.
2. For an enabled schedule, choose a timezone and local opportunity time. Summaries use 24-hour time.
3. For **Weekly**, select at least one weekday. For **Monthly**, select a day from 1–31 or
   **Last day**. If a numbered day is missing, that month's final day is used.
4. Review the summary and next three opportunities, including their timezone offsets.
5. Select **Save schedule**. Saving does not start synchronization. A changed schedule applies
   to future opportunities; it does not run an opportunity from before the save.

You can edit the schedule while a mapping is paused. Resuming does not start a run immediately;
the normal eligibility and timing rules still apply. Wait for an active run to finish before
editing. If another administrator changes the schedule or a run starts while you are saving,
refresh the mapping, review the current settings, and try again.

## What the times mean

These are **synchronization opportunities**, not guaranteed execution or completion times.
Configured schedules are checked hourly. Enqueueing normally occurs within the hour after the
selected time; platform delays, an active run, access problems, licensing, and background work
can make execution later. The preview describes the calendar and does not mean work is queued.
Use the overview and run history to see what actually happened.

- Times follow the selected timezone, independently of your computer's timezone.
- Scheduling follows the app's current timezone rules. Your browser's preview may differ after
  a timezone rule change; previews are advisory. If your browser does not recognize a saved
  timezone, upcoming times are labelled in UTC. You can still disable the schedule.
- During a spring clock-change gap, a missing time moves forward by the gap. For example,
  02:30 becomes 03:30 when clocks jump forward one hour.
- During an autumn overlap, a repeated time has one opportunity at its earlier occurrence.
- An entirely skipped calendar date has no opportunity.
- A monthly schedule on day 31 uses February's final day and returns to day 31 in March.
- Only the latest missed opportunity from the preceding 24 hours can catch up. Older
  opportunities are skipped; Conf2Git does not build a backlog of missed runs. Pausing or losing
  access or entitlement does not stop this clock.
- Once a run has been accepted, its normal background retries and recovery continue for that
  same run. A failed run does not create another run for its opportunity. Follow the diagnostic,
  repair access if needed, and use **Sync now** for an independent attempt.

## Existing daily schedules

An existing schedule labelled **Daily · Forge-managed timing (legacy)** retains its daily
cadence until an administrator saves a replacement. Its timing is selected by Atlassian, so no
exact timestamp preview is available. App upgrades can reset that platform-selected timing.
Existing disabled mappings stay disabled. Selecting and saving a preset explicitly replaces the
legacy timing; it does not add a second schedule.

One time per local day is the most frequent supported schedule. Arbitrary cron expressions,
multiple schedules on one mapping, sub-daily schedules, and exact-time guarantees are unavailable.
