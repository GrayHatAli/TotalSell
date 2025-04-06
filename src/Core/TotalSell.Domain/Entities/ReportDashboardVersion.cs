using System;
using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class ReportDashboardVersion : BaseEntity
{
    public Guid DashboardId { get; set; }
    public string Version { get; set; } = null!;
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public string? Status { get; set; }
    public string? ApprovedBy { get; set; }
    public DateTime? ApprovedDate { get; set; }
    public string? RejectedBy { get; set; }
    public DateTime? RejectedDate { get; set; }
    public string? RejectionReason { get; set; }
    public bool IsActive { get; set; }

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