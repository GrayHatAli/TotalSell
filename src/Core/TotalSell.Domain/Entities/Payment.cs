namespace TotalSell.Domain.Entities;

public class Payment : BaseEntity
{
    public Guid InvoiceId { get; private set; }
    public Invoice Invoice { get; private set; }
    public decimal Amount { get; private set; }
    public DateTime PaymentDate { get; private set; }
    public string PaymentMethod { get; private set; }
    public string BankName { get; private set; }
    public string BankAccountNumber { get; private set; }
    public string BankCardNumber { get; private set; }
    public string ReferenceNumber { get; private set; }
    public DateTime? ReferenceDate { get; private set; }
    public string Description { get; private set; }
    public string Status { get; private set; }

    private Payment() { }

    public Payment(
        Guid invoiceId,
        decimal amount,
        DateTime paymentDate,
        string paymentMethod,
        string bankName,
        string bankAccountNumber,
        string bankCardNumber,
        string referenceNumber = null,
        DateTime? referenceDate = null,
        string description = null)
    {
        InvoiceId = invoiceId;
        Amount = amount;
        PaymentDate = paymentDate;
        PaymentMethod = paymentMethod;
        BankName = bankName;
        BankAccountNumber = bankAccountNumber;
        BankCardNumber = bankCardNumber;
        ReferenceNumber = referenceNumber;
        ReferenceDate = referenceDate;
        Description = description;
        Status = "Pending";
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 