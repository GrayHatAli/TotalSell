namespace TotalSell.Application.Commands;

public class UpdateReportDashboardCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public Guid ReportId { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public bool IsActive { get; set; }
} 