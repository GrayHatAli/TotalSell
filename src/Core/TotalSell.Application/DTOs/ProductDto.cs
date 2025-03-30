namespace TotalSell.Application.DTOs;

public class ProductDto : BaseDto
{
    public string Name { get; set; } = null!;
    public string Code { get; set; } = null!;
    public string? Description { get; set; }
    public decimal UnitPrice { get; set; }
    public string Unit { get; set; } = null!;
    public Guid CategoryId { get; set; }
    public string CategoryName { get; set; } = null!;
    public Guid BrandId { get; set; }
    public string BrandName { get; set; } = null!;
    public List<string> Tags { get; set; } = new();
    public bool IsActive { get; set; }
} 