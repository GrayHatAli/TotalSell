using TotalSell.Domain.Common;
using TotalSell.Domain.Enums;

namespace TotalSell.Domain.Entities;

public class SalesInvoice : Invoice
{
    public required Guid CustomerId { get; set; }
    public Customer? Customer { get; private set; }
    public string ReferenceNumber { get; private set; } = string.Empty;
    public DateTime? ReferenceDate { get; private set; }
    public string PaymentMethod { get; private set; } = string.Empty;
    public string BankName { get; private set; } = string.Empty;
    public string BankAccountNumber { get; private set; } = string.Empty;
    public string BankCardNumber { get; private set; } = string.Empty;
    public string TrackingCode { get; private set; } = string.Empty;

    private SalesInvoice() { } // For EF Core

    public static SalesInvoice Create(
        string number,
        DateTime date,
        Guid customerId,
        string? description,
        string? paymentTerms,
        DateTime dueDate)
    {
        var invoice = new SalesInvoice
        {
            Number = number,
            Date = date,
            CustomerId = customerId,
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
        Guid customerId,
        string? description,
        string? paymentTerms,
        DateTime dueDate,
        InvoiceStatus status)
    {
        base.Update(number, date, description, paymentTerms, dueDate, status);
        CustomerId = customerId;
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

    public void SetPaymentDetails(
        string paymentMethod,
        string bankName,
        string bankAccountNumber,
        string bankCardNumber)
    {
        PaymentMethod = paymentMethod;
        BankName = bankName;
        BankAccountNumber = bankAccountNumber;
        BankCardNumber = bankCardNumber;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetTrackingCode(string trackingCode)
    {
        TrackingCode = trackingCode;
        UpdatedAt = DateTime.UtcNow;
    }
} 