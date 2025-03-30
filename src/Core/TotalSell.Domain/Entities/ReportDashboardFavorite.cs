namespace TotalSell.Domain.Entities;

public class ReportDashboardFavorite : BaseEntity
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
    public bool IsActive { get; private set; }

    private ReportDashboardFavorite() { }

    public ReportDashboardFavorite(
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
        IsActive = true;
    }

    public void UpdateFavoriteDetails(
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