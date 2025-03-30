namespace TotalSell.Domain.Entities;

public class ReportDashboardVersion : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? Version { get; private set; }
    public string? Description { get; private set; }
    public string? Layout { get; private set; }
    public string? Theme { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? RefreshInterval { get; private set; }
    public string? Status { get; private set; }
    public string? ApprovedBy { get; private set; }
    public DateTime? ApprovedDate { get; private set; }
    public string? RejectedBy { get; private set; }
    public DateTime? RejectedDate { get; private set; }
    public string? RejectionReason { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardVersion() { }

    public ReportDashboardVersion(
        Guid dashboardId,
        string version,
        string description,
        string layout,
        string theme,
        string parameters,
        string filters,
        string refreshInterval)
    {
        DashboardId = dashboardId;
        Version = version;
        Description = description;
        Layout = layout;
        Theme = theme;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        Status = "Draft";
        IsActive = true;
    }

    public void UpdateDetails(
        string description,
        string layout,
        string theme,
        string parameters,
        string filters,
        string refreshInterval)
    {
        Description = description;
        Layout = layout;
        Theme = theme;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Approve(string approvedBy)
    {
        Status = "Approved";
        ApprovedBy = approvedBy;
        ApprovedDate = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Reject(string rejectedBy, string rejectionReason)
    {
        Status = "Rejected";
        RejectedBy = rejectedBy;
        RejectedDate = DateTime.UtcNow;
        RejectionReason = rejectionReason;
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