namespace TotalSell.Domain.Interfaces;

public interface IExternalService
{
    Task<bool> IsAvailableAsync();
    Task<string> GetServiceNameAsync();
    Task<DateTime> GetLastCheckTimeAsync();
} 