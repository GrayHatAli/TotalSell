namespace TotalSell.Domain.Entities;

public class ReportDashboardAudit : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? Action { get; private set; }
    public string? ActionType { get; private set; }
    public string? ActionDetails { get; private set; }
    public string? IpAddress { get; private set; }
    public string? UserAgent { get; private set; }
    public string? Status { get; private set; }
    public string? ErrorMessage { get; private set; }

    private ReportDashboardAudit() { }

    public ReportDashboardAudit(
        Guid dashboardId,
        string userId,
        string userName,
        string userEmail,
        string action,
        string actionType,
        string actionDetails,
        string? ipAddress = null,
        string? userAgent = null)
    {
        DashboardId = dashboardId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        Action = action;
        ActionType = actionType;
        ActionDetails = actionDetails;
        IpAddress = ipAddress;
        UserAgent = userAgent;
        Status = "Success";
    }

    public void SetError(string errorMessage)
    {
        Status = "Error";
        ErrorMessage = errorMessage;
        UpdatedAt = DateTime.UtcNow;
    }
} 