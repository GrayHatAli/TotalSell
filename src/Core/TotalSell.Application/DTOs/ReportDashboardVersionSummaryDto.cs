namespace TotalSell.Application.DTOs;

public class ReportDashboardVersionSummaryDto : BaseDto
{
    public Guid DashboardId { get; set; }
    public string Version { get; set; } = null!;
    public string? Description { get; set; }
    public string? Status { get; set; }
    public bool IsActive { get; set; }
} 