namespace TotalSell.Domain.Entities;

public class ReportDashboardSubscription : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? SubscriptionType { get; private set; }
    public string? Schedule { get; private set; }
    public string? Format { get; private set; }
    public string? Parameters { get; private set; }
    public string? Recipients { get; private set; }
    public DateTime? LastSentDate { get; private set; }
    public string? LastSentBy { get; private set; }
    public string? LastSentResult { get; private set; }
    public DateTime? NextSendDate { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardSubscription() { }

    public ReportDashboardSubscription(
        Guid dashboardId,
        string userId,
        string userName,
        string userEmail,
        string subscriptionType,
        string schedule,
        string format,
        string parameters,
        string recipients)
    {
        DashboardId = dashboardId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        SubscriptionType = subscriptionType;
        Schedule = schedule;
        Format = format;
        Parameters = parameters;
        Recipients = recipients;
        IsActive = true;
    }

    public void UpdateSubscriptionDetails(
        string subscriptionType,
        string schedule,
        string format,
        string parameters,
        string recipients)
    {
        SubscriptionType = subscriptionType;
        Schedule = schedule;
        Format = format;
        Parameters = parameters;
        Recipients = recipients;
        UpdatedAt = DateTime.UtcNow;
    }

    public void RecordLastSent(string sentBy, string result)
    {
        LastSentDate = DateTime.UtcNow;
        LastSentBy = sentBy;
        LastSentResult = result;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetNextSend(DateTime nextSendDate)
    {
        NextSendDate = nextSendDate;
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