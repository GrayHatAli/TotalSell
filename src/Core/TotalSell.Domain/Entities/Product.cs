using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class Product : BaseEntity
{
    public string Name { get; private set; } = null!;
    public string Code { get; private set; } = null!;
    public string? Description { get; private set; }
    public decimal Price { get; private set; }
    public decimal? DiscountedPrice { get; private set; }
    public string? Barcode { get; private set; }
    public string? SKU { get; private set; }
    public string? Brand { get; private set; }
    public string? Category { get; private set; }
    public string? Unit { get; private set; }
    public decimal StockQuantity { get; private set; }
    public decimal MinimumStockQuantity { get; private set; }
    public bool IsActive { get; private set; }
    public List<string> Tags { get; private set; } = new();

    private Product() { } // For EF Core

    public static Product Create(
        string name,
        string code,
        string? description = null,
        decimal price = 0,
        decimal? discountedPrice = null,
        string? barcode = null,
        string? sku = null,
        string? brand = null,
        string? category = null,
        string? unit = null,
        decimal stockQuantity = 0,
        decimal minimumStockQuantity = 0,
        bool isActive = true,
        List<string>? tags = null)
    {
        return new Product
        {
            Name = name,
            Code = code,
            Description = description,
            Price = price,
            DiscountedPrice = discountedPrice,
            Barcode = barcode,
            SKU = sku,
            Brand = brand,
            Category = category,
            Unit = unit,
            StockQuantity = stockQuantity,
            MinimumStockQuantity = minimumStockQuantity,
            IsActive = isActive,
            Tags = tags ?? new List<string>()
        };
    }

    public void Update(
        string name,
        string code,
        string? description = null,
        decimal? price = null,
        decimal? discountedPrice = null,
        string? barcode = null,
        string? sku = null,
        string? brand = null,
        string? category = null,
        string? unit = null,
        decimal? stockQuantity = null,
        decimal? minimumStockQuantity = null,
        bool? isActive = null,
        List<string>? tags = null)
    {
        Name = name;
        Code = code;
        Description = description;
        if (price.HasValue)
            Price = price.Value;
        DiscountedPrice = discountedPrice;
        Barcode = barcode;
        SKU = sku;
        Brand = brand;
        Category = category;
        Unit = unit;
        if (stockQuantity.HasValue)
            StockQuantity = stockQuantity.Value;
        if (minimumStockQuantity.HasValue)
            MinimumStockQuantity = minimumStockQuantity.Value;
        if (isActive.HasValue)
            IsActive = isActive.Value;
        if (tags != null)
            Tags = tags;
    }
} 