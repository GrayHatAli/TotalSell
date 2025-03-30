namespace TotalSell.Domain.Exceptions;

public class InvoiceException : DomainException
{
    public Guid InvoiceId { get; }

    public InvoiceException(Guid invoiceId, string message) 
        : base(message)
    {
        InvoiceId = invoiceId;
    }

    public InvoiceException(Guid invoiceId, string message, Exception innerException)
        : base(message, innerException)
    {
        InvoiceId = invoiceId;
    }
} 