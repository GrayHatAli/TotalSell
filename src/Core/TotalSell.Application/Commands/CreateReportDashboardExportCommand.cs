namespace TotalSell.Application.Commands;

public class CreateReportDashboardExportCommand : BaseCommand
{
    public Guid DashboardId { get; set; }
    public string ExportType { get; set; } = null!;
    public string Format { get; set; } = null!;
    public string? Parameters { get; set; }
} 