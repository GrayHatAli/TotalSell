namespace TotalSell.Domain.Interfaces;

public interface IPaymentService
{
    Task<string> InitiatePaymentAsync(decimal amount, string currency, string description);
    Task<bool> VerifyPaymentAsync(string paymentId);
    Task<decimal> GetPaymentAmountAsync(string paymentId);
    Task<string> GetPaymentStatusAsync(string paymentId);
    Task<bool> RefundPaymentAsync(string paymentId, decimal amount);
    Task<DateTime> GetPaymentDateAsync(string paymentId);
} 