namespace TotalSell.Domain.Entities;

public class Product : BaseEntity
{
    public string Name { get; private set; }
    public string Code { get; private set; }
    public string Description { get; private set; }
    public decimal UnitPrice { get; private set; }
    public string Unit { get; private set; }
    public Guid CategoryId { get; private set; }
    public Category Category { get; private set; }
    public Guid BrandId { get; private set; }
    public Brand Brand { get; private set; }
    public ICollection<ProductTag> ProductTags { get; private set; }
    public bool IsActive { get; private set; }

    private Product()
    {
        ProductTags = new List<ProductTag>();
    }

    public Product(
        string name,
        string code,
        string description,
        decimal unitPrice,
        string unit,
        Guid categoryId,
        Guid brandId)
    {
        Name = name;
        Code = code;
        Description = description;
        UnitPrice = unitPrice;
        Unit = unit;
        CategoryId = categoryId;
        BrandId = brandId;
        ProductTags = new List<ProductTag>();
        IsActive = true;
    }

    public void Update(
        string name,
        string code,
        string description,
        decimal unitPrice,
        string unit)
    {
        Name = name;
        Code = code;
        Description = description;
        UnitPrice = unitPrice;
        Unit = unit;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 