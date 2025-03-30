namespace TotalSell.Application.DTOs;

public class ReportDto : BaseDto
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public string Type { get; set; } = null!;
    public string Status { get; set; } = null!;
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public int? RefreshInterval { get; set; }
    public string? ApprovedBy { get; set; }
    public DateTime? ApprovedDate { get; set; }
    public string? RejectedBy { get; set; }
    public DateTime? RejectedDate { get; set; }
    public string? RejectionReason { get; set; }
    public bool IsActive { get; set; }
} 