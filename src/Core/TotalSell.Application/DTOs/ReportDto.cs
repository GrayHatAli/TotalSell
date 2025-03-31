namespace TotalSell.Application.DTOs;

public class ReportDto
{
    public Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Description { get; set; }
    public string? Query { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public int? RefreshInterval { get; set; }
    public string Status { get; set; } = null!;
    public bool IsActive { get; set; }
    public DateTime CreatedAt { get; set; }
    public string CreatedBy { get; set; } = null!;
    public string CreatedByName { get; set; } = null!;
    public DateTime? UpdatedAt { get; set; }
    public string? UpdatedBy { get; set; }
    public DateTime? ApprovedAt { get; set; }
    public string? ApprovedBy { get; set; }
    public string? ApprovedByName { get; set; }
    public DateTime? RejectedAt { get; set; }
    public string? RejectedBy { get; set; }
    public string? RejectionReason { get; set; }
} 