namespace TotalSell.Domain.Entities;

public class InvoiceItem : BaseEntity
{
    public Guid InvoiceId { get; private set; }
    public Invoice Invoice { get; private set; }
    public Guid ProductId { get; private set; }
    public Product Product { get; private set; }
    public decimal Quantity { get; private set; }
    public decimal UnitPrice { get; private set; }
    public decimal DiscountAmount { get; private set; }
    public decimal TaxAmount { get; private set; }
    public decimal TotalAmount { get; private set; }
    public string Description { get; private set; }

    private InvoiceItem() { }

    public InvoiceItem(
        Guid invoiceId,
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0,
        string description = null)
    {
        InvoiceId = invoiceId;
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
        DiscountAmount = discountAmount;
        TaxAmount = taxAmount;
        Description = description;
        CalculateTotalAmount();
    }

    private void CalculateTotalAmount()
    {
        TotalAmount = (Quantity * UnitPrice) + TaxAmount - DiscountAmount;
    }
} 