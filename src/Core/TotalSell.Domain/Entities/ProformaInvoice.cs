namespace TotalSell.Domain.Entities;

public class ProformaInvoice : Invoice
{
    public Guid CustomerId { get; private set; }
    public Customer? Customer { get; private set; }
    public string ReferenceNumber { get; private set; } = string.Empty;
    public DateTime? ReferenceDate { get; private set; }
    public string PaymentMethod { get; private set; } = string.Empty;
    public string BankName { get; private set; } = string.Empty;
    public string BankAccountNumber { get; private set; } = string.Empty;
    public string BankCardNumber { get; private set; } = string.Empty;
    public string TrackingCode { get; private set; } = string.Empty;
    public DateTime? ValidUntil { get; private set; }
    public string TermsAndConditions { get; private set; } = string.Empty;

    private ProformaInvoice() { }

    public ProformaInvoice(
        string number,
        DateTime date,
        Guid customerId,
        string? referenceNumber = null,
        DateTime? referenceDate = null,
        string? description = null,
        string? paymentTerms = null,
        DateTime? dueDate = null,
        string? paymentMethod = null,
        string? bankName = null,
        string? bankAccountNumber = null,
        string? bankCardNumber = null,
        DateTime? validUntil = null,
        string? termsAndConditions = null)
    {
        Number = number;
        Date = date;
        CustomerId = customerId;
        ReferenceNumber = referenceNumber ?? string.Empty;
        ReferenceDate = referenceDate;
        Description = description ?? string.Empty;
        PaymentTerms = paymentTerms ?? string.Empty;
        DueDate = dueDate;
        PaymentMethod = paymentMethod ?? string.Empty;
        BankName = bankName ?? string.Empty;
        BankAccountNumber = bankAccountNumber ?? string.Empty;
        BankCardNumber = bankCardNumber ?? string.Empty;
        ValidUntil = validUntil;
        TermsAndConditions = termsAndConditions ?? string.Empty;
        Status = "Draft";
    }

    public void AddItem(
        Guid productId,
        decimal quantity,
        decimal unitPrice,
        decimal discountAmount = 0,
        decimal taxAmount = 0,
        string? description = null)
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

    public void SetTermsAndConditions(string termsAndConditions)
    {
        TermsAndConditions = termsAndConditions;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetValidUntil(DateTime validUntil)
    {
        ValidUntil = validUntil;
        UpdatedAt = DateTime.UtcNow;
    }
} 