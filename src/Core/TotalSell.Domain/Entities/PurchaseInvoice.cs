namespace TotalSell.Domain.Entities;

public class PurchaseInvoice : Invoice
{
    public Guid SupplierId { get; private set; }
    public Supplier Supplier { get; private set; }
    public string SupplierInvoiceNumber { get; private set; }
    public DateTime? SupplierInvoiceDate { get; private set; }

    private PurchaseInvoice() { }

    public PurchaseInvoice(
        string number,
        DateTime date,
        Guid supplierId,
        string supplierInvoiceNumber,
        DateTime? supplierInvoiceDate,
        string description = null,
        string paymentTerms = null,
        DateTime? dueDate = null)
    {
        Number = number;
        Date = date;
        SupplierId = supplierId;
        SupplierInvoiceNumber = supplierInvoiceNumber;
        SupplierInvoiceDate = supplierInvoiceDate;
        Description = description;
        PaymentTerms = paymentTerms;
        DueDate = dueDate;
        Status = "Draft";
    }

    public void AddItem(
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0,
        string description = null)
    {
        var item = new InvoiceItem(
            Id,
            productId,
            quantity,
            unitPrice,
            discountAmount,
            taxAmount,
            description);

        Items.Add(item);
        CalculateTotals();
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 