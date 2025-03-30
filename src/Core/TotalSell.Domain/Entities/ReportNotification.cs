namespace TotalSell.Domain.Entities;

public class ReportNotification : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? NotificationType { get; private set; }
    public string? Title { get; private set; }
    public string? Message { get; private set; }
    public string? Link { get; private set; }
    public bool IsRead { get; private set; }
    public DateTime? ReadDate { get; private set; }
    public string? ReadBy { get; private set; }
    public bool IsActive { get; private set; }

    private ReportNotification() { }

    public ReportNotification(
        Guid reportId,
        string userId,
        string userName,
        string userEmail,
        string notificationType,
        string title,
        string message,
        string? link = null)
    {
        ReportId = reportId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        NotificationType = notificationType;
        Title = title;
        Message = message;
        Link = link;
        IsRead = false;
        IsActive = true;
    }

    public void MarkAsRead(string readBy)
    {
        IsRead = true;
        ReadDate = DateTime.UtcNow;
        ReadBy = readBy;
        UpdatedAt = DateTime.UtcNow;
    }

    public void MarkAsUnread()
    {
        IsRead = false;
        ReadDate = null;
        ReadBy = null;
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