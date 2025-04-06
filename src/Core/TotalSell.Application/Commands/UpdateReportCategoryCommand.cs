namespace TotalSell.Application.Commands;

public class UpdateReportCategoryCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public Guid? ParentId { get; set; }
    public bool IsActive { get; set; }
} 