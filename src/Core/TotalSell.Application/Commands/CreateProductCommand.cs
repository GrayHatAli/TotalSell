using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class CreateProductCommand : BaseCommand
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public decimal UnitPrice { get; set; }
    public string Unit { get; set; } = null!;
    public Guid CategoryId { get; set; }
    public Guid BrandId { get; set; }
} 