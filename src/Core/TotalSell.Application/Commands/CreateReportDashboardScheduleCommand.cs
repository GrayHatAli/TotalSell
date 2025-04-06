namespace TotalSell.Application.Commands;

public class CreateReportDashboardScheduleCommand : BaseCommand
{
    public Guid DashboardId { get; set; }
    public string ScheduleType { get; set; } = null!;
    public string CronExpression { get; set; } = null!;
    public string? Parameters { get; set; }
    public string Recipients { get; set; } = null!;
    public string Format { get; set; } = null!;
} 