namespace TotalSell.Domain.Entities;

public class ReportDashboardView : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? ViewType { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? Layout { get; private set; }
    public string? Status { get; private set; }
    public DateTime? LastViewDate { get; private set; }
    public string? LastViewBy { get; private set; }

    private ReportDashboardView() { }

    public ReportDashboardView(
        Guid dashboardId,
        string userId,
        string userName,
        string userEmail,
        string viewType,
        string parameters,
        string filters,
        string layout)
    {
        DashboardId = dashboardId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        ViewType = viewType;
        Parameters = parameters;
        Filters = filters;
        Layout = layout;
        Status = "Active";
    }

    public void UpdateViewDetails(
        string viewType,
        string parameters,
        string filters,
        string layout)
    {
        ViewType = viewType;
        Parameters = parameters;
        Filters = filters;
        Layout = layout;
        UpdatedAt = DateTime.UtcNow;
    }

    public void RecordView(string viewBy)
    {
        LastViewDate = DateTime.UtcNow;
        LastViewBy = viewBy;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 