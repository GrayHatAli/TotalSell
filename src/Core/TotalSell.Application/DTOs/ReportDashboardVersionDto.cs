namespace TotalSell.Application.DTOs;

public class ReportDashboardVersionDto
{
    public Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public string? Version { get; set; }
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? RefreshInterval { get; set; }
    public string? Status { get; set; }
    public string? ApprovedBy { get; set; }
    public DateTime? ApprovedDate { get; set; }
    public string? RejectedBy { get; set; }
    public DateTime? RejectedDate { get; set; }
    public string? RejectionReason { get; set; }
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
    public string? CreatedBy { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public string? UpdatedBy { get; set; }
} 