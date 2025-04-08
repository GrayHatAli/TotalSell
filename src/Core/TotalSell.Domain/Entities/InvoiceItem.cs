using TotalSell.Domain.Common;

namespace TotalSell.Domain.Entities;

public class InvoiceItem : BaseEntity
{
    public required Guid InvoiceId { get; set; }
    public required Invoice Invoice { get; set; }
    public required Guid ProductId { get; set; }
    public required Product Product { get; set; }
    public required decimal Quantity { get; set; }
    public required decimal UnitPrice { get; set; }
    public decimal DiscountAmount { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal TotalAmount { get; set; }

    protected InvoiceItem() { } // For EF Core

    public static InvoiceItem Create(
        Guid invoiceId,
        Invoice invoice,
        Guid productId,
        Product product,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount,
        decimal taxAmount)
    {
        var item = new InvoiceItem
        {
            InvoiceId = invoiceId,
            Invoice = invoice,
            ProductId = productId,
            Product = product,
            Quantity = quantity,
            UnitPrice = unitPrice,
            DiscountAmount = discountAmount,
            TaxAmount = taxAmount
        };

        item.CalculateTotal();
        return item;
    }

    public void Update(
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount,
        decimal taxAmount)
    {
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
        DiscountAmount = discountAmount;
        TaxAmount = taxAmount;

        CalculateTotal();
    }

    private void CalculateTotal()
    {
        TotalAmount = (Quantity * UnitPrice) + TaxAmount - DiscountAmount;
    }
} 