using TotalSell.Domain.Common;
using TotalSell.Domain.Enums;

namespace TotalSell.Domain.Entities;

public class PurchaseInvoice : Invoice
{
    public required Guid SupplierId { get; set; }
    public Supplier? Supplier { get; private set; }
    public string SupplierInvoiceNumber { get; private set; } = string.Empty;
    public DateTime? SupplierInvoiceDate { get; private set; }
    public override string? ReferenceNumber { get; set; }
    public override DateTime? ReferenceDate { get; set; }
    public override string? PaymentMethod { get; set; }
    public override required Guid CustomerId { get; set; }
    public override required Customer Customer { get; set; }

    protected PurchaseInvoice() : base()
    {
    }

    public static PurchaseInvoice Create(
        string number,
        DateTime date,
        string? description,
        DateTime dueDate,
        InvoiceStatus status,
        Guid customerId,
        Customer customer,
        Guid supplierId,
        string? referenceNumber,
        DateTime? referenceDate,
        string? paymentMethod)
    {
        var invoice = new PurchaseInvoice
        {
            Number = number,
            Date = date,
            Description = description,
            DueDate = dueDate,
            Status = status,
            CustomerId = customerId,
            Customer = customer,
            SupplierId = supplierId,
            ReferenceNumber = referenceNumber,
            ReferenceDate = referenceDate,
            PaymentMethod = paymentMethod,
            Type = InvoiceType.Purchase
        };

        return invoice;
    }

    public override void Update(
        string number,
        DateTime date,
        string? description,
        DateTime dueDate,
        InvoiceStatus status,
        Guid customerId,
        Customer customer,
        string? referenceNumber,
        DateTime? referenceDate,
        string? paymentMethod)
    {
        base.Update(number, date, description, dueDate, status, customerId, customer, referenceNumber, referenceDate, paymentMethod);
    }

    public override void AddItem(Guid productId, Product product, decimal quantity, decimal unitPrice, decimal discountAmount, decimal taxAmount)
    {
        base.AddItem(productId, product, quantity, unitPrice, discountAmount, taxAmount);
    }

    public void UpdateStatus(InvoiceStatus status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 