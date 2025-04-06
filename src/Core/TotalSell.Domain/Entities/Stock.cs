namespace TotalSell.Domain.Entities;

public class Stock : BaseEntity
{
    public Guid ProductId { get; private set; }
    public Product? Product { get; private set; }
    public decimal Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }
    public string Location { get; private set; } = string.Empty;
    public string? BatchNumber { get; private set; } = string.Empty;
    public DateTime? ExpiryDate { get; private set; }
    public string Status { get; private set; } = string.Empty;

    private Stock() { }

    public Stock(
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        string location,
        string? batchNumber = null,
        DateTime? expiryDate = null)
    {
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
        Location = location;
        BatchNumber = batchNumber;
        ExpiryDate = expiryDate;
        Status = "Active";
    }

    public void UpdateQuantity(decimal quantity)
    {
        Quantity = quantity;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateUnitPrice(decimal unitPrice)
    {
        UnitPrice = unitPrice;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateLocation(string location)
    {
        Location = location;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 