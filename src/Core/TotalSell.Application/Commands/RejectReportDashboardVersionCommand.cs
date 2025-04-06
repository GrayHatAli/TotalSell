namespace TotalSell.Application.Commands;

public class RejectReportDashboardVersionCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string RejectionReason { get; set; } = null!;
} 