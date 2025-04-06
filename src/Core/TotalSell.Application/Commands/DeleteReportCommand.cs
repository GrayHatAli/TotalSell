using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteReportCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 