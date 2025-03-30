namespace TotalSell.Domain.Entities;

public class ReportSubscription : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
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

    private ReportSubscription() { }

    public ReportSubscription(
        Guid reportId,
        string userId,
        string userName,
        string userEmail,
        string subscriptionType,
        string schedule,
        string format,
        string parameters,
        string recipients)
    {
        ReportId = reportId;
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