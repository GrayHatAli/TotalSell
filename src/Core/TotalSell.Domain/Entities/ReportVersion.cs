namespace TotalSell.Domain.Entities;

public class ReportVersion : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? Version { get; private set; }
    public string? Description { get; private set; }
    public string? Content { get; private set; }
    public string? Parameters { get; private set; }
    public string? Query { get; private set; }
    public string? Format { get; private set; }
    public string? Status { get; private set; }
    public string? ApprovedBy { get; private set; }
    public DateTime? ApprovedDate { get; private set; }
    public string? RejectedBy { get; private set; }
    public DateTime? RejectedDate { get; private set; }
    public string? RejectionReason { get; private set; }
    public bool IsActive { get; private set; }

    private ReportVersion() { }

    public ReportVersion(
        Guid reportId,
        string version,
        string description,
        string content,
        string parameters,
        string query,
        string format,
        string createdBy)
    {
        ReportId = reportId;
        Version = version;
        Description = description;
        Content = content;
        Parameters = parameters;
        Query = query;
        Format = format;
        CreatedBy = createdBy;
        Status = "Draft";
        IsActive = true;
    }

    public void UpdateDetails(
        string description,
        string content,
        string parameters,
        string query,
        string format)
    {
        Description = description;
        Content = content;
        Parameters = parameters;
        Query = query;
        Format = format;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Approve(string approvedBy)
    {
        Status = "Approved";
        ApprovedBy = approvedBy;
        ApprovedDate = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Reject(string rejectedBy, string rejectionReason)
    {
        Status = "Rejected";
        RejectedBy = rejectedBy;
        RejectedDate = DateTime.UtcNow;
        RejectionReason = rejectionReason;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Deactivate()
    {
        IsActive = false;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Activate()
    {
        IsActive = true;
        UpdatedAt = DateTime.UtcNow;
    }
} 