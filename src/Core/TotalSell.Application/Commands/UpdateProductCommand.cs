using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateProductCommand : BaseCommand
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public decimal UnitPrice { get; set; }
    public string Unit { get; set; } = null!;
    public Guid CategoryId { get; set; }
    public Guid BrandId { get; set; }
    public decimal Cost { get; set; }
    public string? Barcode { get; set; }
    public decimal MinimumStock { get; set; }
    public decimal MaximumStock { get; set; }
    public decimal ReorderPoint { get; set; }
    public IEnumerable<string> Tags { get; set; } = new List<string>();
    public bool IsActive { get; set; }
} 