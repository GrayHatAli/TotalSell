namespace TotalSell.Domain.Entities;

public class SalesInvoice : Invoice
{
    public Guid CustomerId { get; private set; }
    public Customer Customer { get; private set; }
    public string ReferenceNumber { get; private set; }
    public DateTime? ReferenceDate { get; private set; }
    public string PaymentMethod { get; private set; }
    public string BankName { get; private set; }
    public string BankAccountNumber { get; private set; }
    public string BankCardNumber { get; private set; }
    public string TrackingCode { get; private set; }

    private SalesInvoice() { }

    public SalesInvoice(
        string number,
        DateTime date,
        Guid customerId,
        string referenceNumber = null,
        DateTime? referenceDate = null,
        string description = null,
        string paymentTerms = null,
        DateTime? dueDate = null,
        string paymentMethod = null,
        string bankName = null,
        string bankAccountNumber = null,
        string bankCardNumber = null)
    {
        Number = number;
        Date = date;
        CustomerId = customerId;
        ReferenceNumber = referenceNumber;
        ReferenceDate = referenceDate;
        Description = description;
        PaymentTerms = paymentTerms;
        DueDate = dueDate;
        PaymentMethod = paymentMethod;
        BankName = bankName;
        BankAccountNumber = bankAccountNumber;
        BankCardNumber = bankCardNumber;
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