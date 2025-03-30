namespace TotalSell.Domain.Entities;

public class ReportExport : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? ExportType { get; private set; }
    public string? Format { get; private set; }
    public string? Parameters { get; private set; }
    public string? FilePath { get; private set; }
    public string? FileName { get; private set; }
    public long? FileSize { get; private set; }
    public string? FileType { get; private set; }
    public string? Status { get; private set; }
    public DateTime? StartDate { get; private set; }
    public DateTime? EndDate { get; private set; }
    public string? ErrorMessage { get; private set; }

    private ReportExport() { }

    public ReportExport(
        Guid reportId,
        string exportType,
        string format,
        string parameters,
        string createdBy)
    {
        ReportId = reportId;
        ExportType = exportType;
        Format = format;
        Parameters = parameters;
        CreatedBy = createdBy;
        Status = "Pending";
        StartDate = DateTime.UtcNow;
    }

    public void Start()
    {
        Status = "Running";
        UpdatedAt = DateTime.UtcNow;
    }

    public void Complete(
        string filePath,
        string fileName,
        long fileSize,
        string fileType)
    {
        Status = "Completed";
        EndDate = DateTime.UtcNow;
        FilePath = filePath;
        FileName = fileName;
        FileSize = fileSize;
        FileType = fileType;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Fail(string errorMessage)
    {
        Status = "Failed";
        EndDate = DateTime.UtcNow;
        ErrorMessage = errorMessage;
        UpdatedAt = DateTime.UtcNow;
    }
} 