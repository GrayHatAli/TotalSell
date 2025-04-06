namespace TotalSell.Domain.Entities;

public class StockTransaction : BaseEntity
{
    public Guid StockId { get; private set; }
    public Stock? Stock { get; private set; }
    public string TransactionType { get; private set; } = string.Empty;
    public decimal Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }
    public string ReferenceType { get; private set; } = string.Empty;
    public Guid? ReferenceId { get; private set; }
    public string ReferenceNumber { get; private set; } = string.Empty;
    public DateTime? ReferenceDate { get; private set; }
    public string Description { get; private set; } = string.Empty;

    private StockTransaction() { }

    public StockTransaction(
        Guid stockId,
        string transactionType,
        decimal quantity,
        decimal unitPrice,
        string referenceType,
        Guid? referenceId = null,
        string? referenceNumber = null,
        DateTime? referenceDate = null,
        string? description = null)
    {
        StockId = stockId;
        TransactionType = transactionType;
        Quantity = quantity;
        UnitPrice = unitPrice;
        ReferenceType = referenceType;
        ReferenceId = referenceId;
        ReferenceNumber = referenceNumber ?? string.Empty;
        ReferenceDate = referenceDate;
        Description = description ?? string.Empty;
    }
} 