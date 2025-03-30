namespace TotalSell.Domain.Interfaces;

public interface IReportService
{
    Task<byte[]> GenerateReportAsync(string reportType, Dictionary<string, object> parameters);
    Task<string> GetReportStatusAsync(Guid reportId);
    Task<DateTime> GetReportGenerationTimeAsync(Guid reportId);
    Task<bool> IsReportReadyAsync(Guid reportId);
    Task CancelReportGenerationAsync(Guid reportId);
} 