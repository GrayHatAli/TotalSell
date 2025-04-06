namespace TotalSell.Application.Commands;

public class CreateProductCategoryCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public Guid? ParentId { get; set; }
} 