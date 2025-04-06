namespace TotalSell.Application.Commands;

public class UpdateReportDashboardItemCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public string Title { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Description { get; set; }
    public string? Query { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public int RefreshInterval { get; set; }
    public int Order { get; set; }
    public bool IsActive { get; set; }
} 