using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class InvoiceItem : BaseEntity
{
    public required Guid InvoiceId { get; set; }
    public required Guid ProductId { get; set; }
    public required decimal Quantity { get; set; }
    public required decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal TotalAmount { get; set; }
    public Invoice? Invoice { get; private set; }
    public Product? Product { get; private set; }

    private InvoiceItem() { } // For EF Core

    public static InvoiceItem Create(
        Guid invoiceId,
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0)
    {
        var item = new InvoiceItem
        {
            InvoiceId = invoiceId,
            ProductId = productId,
            Quantity = quantity,
            UnitPrice = unitPrice,
            DiscountAmount = discountAmount,
            TaxAmount = taxAmount
        };

        item.CalculateTotal();
        return item;
    }

    public void Update(
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0)
    {
        Quantity = quantity;
        UnitPrice = unitPrice;
        DiscountAmount = discountAmount;
        TaxAmount = taxAmount;
        CalculateTotal();
    }

    private void CalculateTotal()
    {
        TotalAmount = (Quantity * UnitPrice) - DiscountAmount + TaxAmount;
    }
} 