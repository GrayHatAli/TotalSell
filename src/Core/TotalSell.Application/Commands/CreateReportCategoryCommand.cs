using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateReportCategoryCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public Guid? ParentId { get; set; }
} 