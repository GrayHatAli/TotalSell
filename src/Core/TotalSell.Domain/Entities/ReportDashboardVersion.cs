using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class ReportDashboardVersion : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public string Version { get; private set; } = null!;
    public string? Description { get; private set; }
    public string? Layout { get; private set; }
    public string? Theme { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public int? RefreshInterval { get; private set; }
    public string? Status { get; private set; }
    public string? ApprovedBy { get; private set; }
    public DateTime? ApprovedDate { get; private set; }
    public string? RejectedBy { get; private set; }
    public DateTime? RejectedDate { get; private set; }
    public string? RejectionReason { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardVersion() { }

    public static ReportDashboardVersion Create(
        Guid dashboardId,
        string version,
        string? description = null,
        string? layout = null,
        string? theme = null,
        string? parameters = null,
        string? filters = null,
        int? refreshInterval = null)
    {
        return new ReportDashboardVersion
        {
            DashboardId = dashboardId,
            Version = version,
            Description = description,
            Layout = layout,
            Theme = theme,
            Parameters = parameters,
            Filters = filters,
            RefreshInterval = refreshInterval,
            Status = "Draft",
            IsActive = false
        };
    }

    public void UpdateDetails(
        string? description,
        string? layout,
        string? theme,
        string? parameters,
        string? filters,
        string? refreshInterval)
    {
        Description = description;
        Layout = layout;
        Theme = theme;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval != null ? int.Parse(refreshInterval) : null;
    }

    public void Approve(string approvedBy)
    {
        Status = "Approved";
        ApprovedBy = approvedBy;
        ApprovedDate = DateTime.UtcNow;
    }

    public void Reject(string rejectedBy, string rejectionReason)
    {
        Status = "Rejected";
        RejectedBy = rejectedBy;
        RejectedDate = DateTime.UtcNow;
        RejectionReason = rejectionReason;
    }

    public void Activate()
    {
        IsActive = true;
    }

    public void Deactivate()
    {
        IsActive = false;
    }
} 