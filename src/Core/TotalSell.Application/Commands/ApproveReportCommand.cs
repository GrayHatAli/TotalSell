namespace TotalSell.Application.Commands;

public class ApproveReportCommand : BaseCommand
{
    public Guid ReportId { get; set; }
    public string? Comments { get; set; }
} 