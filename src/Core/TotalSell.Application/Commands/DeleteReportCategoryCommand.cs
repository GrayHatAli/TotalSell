using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class DeleteReportCategoryCommand : BaseCommand
{
    public new Guid Id { get; set; }
} 