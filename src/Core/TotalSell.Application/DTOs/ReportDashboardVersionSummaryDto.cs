namespace TotalSell.Application.DTOs;

public class ReportDashboardVersionSummaryDto
{
    public Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public string? Version { get; set; }
    public string? Description { get; set; }
    public string? Status { get; set; }
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
    public string? CreatedBy { get; set; }
} 