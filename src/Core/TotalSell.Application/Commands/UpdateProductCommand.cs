using MediatR;
using TotalSell.Application.Common;

namespace TotalSell.Application.Commands;

public class UpdateProductCommand : BaseCommand, IRequest<Unit>
{
    public new Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public decimal Price { get; set; }
    public decimal? DiscountedPrice { get; set; }
    public string? Barcode { get; set; }
    public string? SKU { get; set; }
    public string? Brand { get; set; }
    public string? Category { get; set; }
    public string? Unit { get; set; }
    public decimal StockQuantity { get; set; }
    public decimal MinimumStockQuantity { get; set; }
    public bool IsActive { get; set; }
    public List<string> Tags { get; set; } = new();
} 