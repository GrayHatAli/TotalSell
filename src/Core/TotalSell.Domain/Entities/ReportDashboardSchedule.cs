namespace TotalSell.Domain.Entities;

public class ReportDashboardSchedule : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? ScheduleType { get; private set; }
    public string? CronExpression { get; private set; }
    public string? Parameters { get; private set; }
    public string? Recipients { get; private set; }
    public string? Format { get; private set; }
    public string? Status { get; private set; }
    public DateTime? LastRunDate { get; private set; }
    public string? LastRunBy { get; private set; }
    public string? LastRunResult { get; private set; }
    public DateTime? NextRunDate { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardSchedule() { }

    public ReportDashboardSchedule(
        Guid dashboardId,
        string scheduleType,
        string cronExpression,
        string parameters,
        string recipients,
        string format)
    {
        DashboardId = dashboardId;
        ScheduleType = scheduleType;
        CronExpression = cronExpression;
        Parameters = parameters;
        Recipients = recipients;
        Format = format;
        Status = "Active";
        IsActive = true;
    }

    public void UpdateDetails(
        string scheduleType,
        string cronExpression,
        string parameters,
        string recipients,
        string format)
    {
        ScheduleType = scheduleType;
        CronExpression = cronExpression;
        Parameters = parameters;
        Recipients = recipients;
        Format = format;
        UpdatedAt = DateTime.UtcNow;
    }

    public void RecordLastRun(string runBy, string result)
    {
        LastRunDate = DateTime.UtcNow;
        LastRunBy = runBy;
        LastRunResult = result;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetNextRun(DateTime nextRunDate)
    {
        NextRunDate = nextRunDate;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 