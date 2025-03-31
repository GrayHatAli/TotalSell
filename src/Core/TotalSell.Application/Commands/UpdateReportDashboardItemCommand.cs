using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateReportDashboardItemDetailsCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public Guid ReportId { get; set; }
    public string Title { get; set; } = null!;
    public string Type { get; set; } = null!;
    public string? Parameters { get; set; }
    public string? Filters { get; set; }
    public string? Layout { get; set; }
    public int Order { get; set; }
    public bool IsActive { get; set; }
} 