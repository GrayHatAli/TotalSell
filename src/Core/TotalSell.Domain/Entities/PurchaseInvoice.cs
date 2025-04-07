using TotalSell.Domain.Common;
using TotalSell.Domain.Enums;

namespace TotalSell.Domain.Entities;

public class PurchaseInvoice : Invoice
{
    public required Guid SupplierId { get; set; }
    public Supplier? Supplier { get; private set; }
    public string SupplierInvoiceNumber { get; private set; } = string.Empty;
    public DateTime? SupplierInvoiceDate { get; private set; }

    private PurchaseInvoice() { } // For EF Core

    public static PurchaseInvoice Create(
        string number,
        DateTime date,
        Guid supplierId,
        string? description,
        string? paymentTerms,
        DateTime dueDate)
    {
        var invoice = new PurchaseInvoice
        {
            Number = number,
            Date = date,
            SupplierId = supplierId,
            Description = description,
            PaymentTerms = paymentTerms,
            DueDate = dueDate,
            Status = InvoiceStatus.Draft,
            SubTotal = 0,
            TaxAmount = 0,
            DiscountAmount = 0,
            TotalAmount = 0
        };

        return invoice;
    }

    public void Update(
        string number,
        DateTime date,
        Guid supplierId,
        string? description,
        string? paymentTerms,
        DateTime dueDate,
        InvoiceStatus status)
    {
        base.Update(number, date, description, paymentTerms, dueDate, status);
        SupplierId = supplierId;
    }

    public void AddItem(
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0)
    {
        var item = InvoiceItem.Create(
            Id,
            productId,
            quantity,
            unitPrice,
            discountAmount,
            taxAmount);

        base.AddItem(item);
    }

    public void UpdateStatus(InvoiceStatus status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 