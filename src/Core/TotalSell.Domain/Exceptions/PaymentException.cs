namespace TotalSell.Domain.Exceptions;

public class PaymentException : DomainException
{
    public Guid PaymentId { get; }
    public decimal Amount { get; }

    public PaymentException(Guid paymentId, decimal amount, string message)
        : base(message)
    {
        PaymentId = paymentId;
        Amount = amount;
    }

    public PaymentException(Guid paymentId, decimal amount, string message, Exception innerException)
        : base(message, innerException)
    {
        PaymentId = paymentId;
        Amount = amount;
    }
} 