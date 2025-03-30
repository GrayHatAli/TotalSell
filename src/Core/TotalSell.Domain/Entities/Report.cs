namespace TotalSell.Domain.Entities;

public class Report : BaseEntity
{
    public string Name { get; private set; }
    public string Code { get; private set; }
    public string Description { get; private set; }
    public string ReportType { get; private set; }
    public string Parameters { get; private set; }
    public string Query { get; private set; }
    public string Format { get; private set; }
    public string Status { get; private set; }
    public DateTime? LastRunDate { get; private set; }
    public string LastRunBy { get; private set; }
    public string LastRunResult { get; private set; }

    private Report() { }

    public Report(
        string name,
        string code,
        string description,
        string reportType,
        string parameters,
        string query,
        string format)
    {
        Name = name;
        Code = code;
        Description = description;
        ReportType = reportType;
        Parameters = parameters;
        Query = query;
        Format = format;
        Status = "Active";
    }

    public void UpdateDetails(
        string name,
        string description,
        string parameters,
        string query,
        string format)
    {
        Name = name;
        Description = description;
        Parameters = parameters;
        Query = query;
        Format = format;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }

    public void SetLastRun(string runBy, string result)
    {
        LastRunDate = DateTime.UtcNow;
        LastRunBy = runBy;
        LastRunResult = result;
        UpdatedAt = DateTime.UtcNow;
    }
} 