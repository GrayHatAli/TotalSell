using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateReportDashboardVersionCommand : BaseCommand
{
    public Guid DashboardId { get; set; }
    public string Version { get; set; } = null!;
    public string? Description { get; set; }
    public string? Layout { get; set; }
    public string? Theme { get; set; }
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public int? RefreshInterval { get; set; }
    public bool IsActive { get; set; } = true;
} 