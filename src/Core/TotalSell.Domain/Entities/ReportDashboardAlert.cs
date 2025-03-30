namespace TotalSell.Domain.Entities;

public class ReportDashboardAlert : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? AlertType { get; private set; }
    public string? Metric { get; private set; }
    public string? Condition { get; private set; }
    public string? Threshold { get; private set; }
    public string? Frequency { get; private set; }
    public string? Recipients { get; private set; }
    public string? Message { get; private set; }
    public string? Status { get; private set; }
    public DateTime? LastTriggeredDate { get; private set; }
    public string? LastTriggeredBy { get; private set; }
    public string? LastTriggeredValue { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardAlert() { }

    public ReportDashboardAlert(
        Guid dashboardId,
        string alertType,
        string metric,
        string condition,
        string threshold,
        string frequency,
        string recipients,
        string message)
    {
        DashboardId = dashboardId;
        AlertType = alertType;
        Metric = metric;
        Condition = condition;
        Threshold = threshold;
        Frequency = frequency;
        Recipients = recipients;
        Message = message;
        Status = "Active";
        IsActive = true;
    }

    public void UpdateDetails(
        string alertType,
        string metric,
        string condition,
        string threshold,
        string frequency,
        string recipients,
        string message)
    {
        AlertType = alertType;
        Metric = metric;
        Condition = condition;
        Threshold = threshold;
        Frequency = frequency;
        Recipients = recipients;
        Message = message;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Trigger(string triggeredBy, string triggeredValue)
    {
        LastTriggeredDate = DateTime.UtcNow;
        LastTriggeredBy = triggeredBy;
        LastTriggeredValue = triggeredValue;
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