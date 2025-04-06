using System;
using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class ReportSchedule : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string Name { get; private set; } = string.Empty;
    public string Description { get; private set; } = string.Empty;
    public string CronExpression { get; private set; } = string.Empty;
    public string Parameters { get; private set; } = string.Empty;
    public string Format { get; private set; } = string.Empty;
    public string Status { get; private set; } = string.Empty;
    public DateTime? LastRunDate { get; private set; }
    public DateTime? NextRunDate { get; private set; }
    public bool IsActive { get; private set; }

    private ReportSchedule() { }

    public ReportSchedule(
        Guid reportId,
        string name,
        string cronExpression,
        string parameters,
        string format,
        string? description = null)
    {
        ReportId = reportId;
        Name = name;
        Description = description ?? string.Empty;
        CronExpression = cronExpression;
        Parameters = parameters;
        Format = format;
        Status = "Active";
        IsActive = true;
    }

    public void Update(
        string name,
        string cronExpression,
        string parameters,
        string format,
        string? description = null)
    {
        Name = name;
        Description = description ?? string.Empty;
        CronExpression = cronExpression;
        Parameters = parameters;
        Format = format;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        Status = "Inactive";
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        Status = "Active";
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateLastRunDate(DateTime lastRunDate)
    {
        LastRunDate = lastRunDate;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateNextRunDate(DateTime nextRunDate)
    {
        NextRunDate = nextRunDate;
        UpdatedAt = DateTime.UtcNow;
    }
} 