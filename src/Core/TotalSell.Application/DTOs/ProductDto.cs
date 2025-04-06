namespace TotalSell.Application.DTOs;

public class ProductDto
{
    public Guid Id { get; set; }
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
    public DateTime CreatedAt { get; set; }
    public string CreatedBy { get; set; } = null!;
    public DateTime? LastModifiedAt { get; set; }
    public string? LastModifiedBy { get; set; }
} 