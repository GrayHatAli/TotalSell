namespace TotalSell.Domain.Interfaces;

public interface IAuthenticationService
{
    Task<string> GenerateTokenAsync(string userId, string[] roles);
    Task<bool> ValidateTokenAsync(string token);
    Task<string> GetUserIdFromTokenAsync(string token);
    Task<string[]> GetUserRolesFromTokenAsync(string token);
    Task<DateTime> GetTokenExpirationAsync(string token);
    Task RevokeTokenAsync(string token);
} 