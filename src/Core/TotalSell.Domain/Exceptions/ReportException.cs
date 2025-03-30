namespace TotalSell.Domain.Exceptions;

public class ReportException : DomainException
{
    public Guid ReportId { get; }
    public string? ReportType { get; }

    public ReportException(Guid reportId, string? reportType, string message)
        : base(message)
    {
        ReportId = reportId;
        ReportType = reportType;
    }

    public ReportException(Guid reportId, string? reportType, string message, Exception innerException)
        : base(message, innerException)
    {
        ReportId = reportId;
        ReportType = reportType;
    }
} 