namespace TotalSell.Domain.Entities;

public class ReportExecution : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report Report { get; private set; }
    public Guid? ScheduleId { get; private set; }
    public ReportSchedule Schedule { get; private set; }
    public string Parameters { get; private set; }
    public string Format { get; private set; }
    public string Status { get; private set; }
    public DateTime StartDate { get; private set; }
    public DateTime? EndDate { get; private set; }
    public string Result { get; private set; }
    public string ErrorMessage { get; private set; }
    public string FilePath { get; private set; }
    public string FileName { get; private set; }
    public long? FileSize { get; private set; }
    public string FileType { get; private set; }

    private ReportExecution() { }

    public ReportExecution(
        Guid reportId,
        Guid? scheduleId,
        string parameters,
        string format)
    {
        ReportId = reportId;
        ScheduleId = scheduleId;
        Parameters = parameters;
        Format = format;
        Status = "Pending";
        StartDate = DateTime.UtcNow;
    }

    public void Start()
    {
        Status = "Running";
        UpdatedAt = DateTime.UtcNow;
    }

    public void Complete(string result, string filePath, string fileName, long fileSize, string fileType)
    {
        Status = "Completed";
        EndDate = DateTime.UtcNow;
        Result = result;
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