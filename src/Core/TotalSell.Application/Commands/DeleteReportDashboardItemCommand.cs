using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteReportDashboardItemCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 