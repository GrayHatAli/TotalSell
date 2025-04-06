namespace TotalSell.Application.Commands;

public class UpdateReportDashboardExportCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public Guid DashboardId { get; set; }
    public string ExportType { get; set; } = null!;
    public string Format { get; set; } = null!;
    public string? Parameters { get; set; }
    public string Status { get; set; } = null!;
    public string? ErrorMessage { get; set; }
} 