namespace TotalSell.Domain.Entities;

public class ReportDashboardExport : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
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

    private ReportDashboardExport() { }

    public ReportDashboardExport(
        Guid dashboardId,
        string exportType,
        string format,
        string parameters)
    {
        DashboardId = dashboardId;
        ExportType = exportType;
        Format = format;
        Parameters = parameters;
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