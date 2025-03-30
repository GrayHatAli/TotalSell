namespace TotalSell.Domain.Entities;

public class ReportComment : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? Comment { get; private set; }
    public Guid? ParentId { get; private set; }
    public ReportComment? Parent { get; private set; }
    public ICollection<ReportComment> Replies { get; private set; }
    public bool IsActive { get; private set; }

    private ReportComment()
    {
        Replies = new List<ReportComment>();
    }

    public ReportComment(
        Guid reportId,
        string userId,
        string userName,
        string userEmail,
        string comment,
        Guid? parentId = null)
    {
        ReportId = reportId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        Comment = comment;
        ParentId = parentId;
        Replies = new List<ReportComment>();
        IsActive = true;
    }

    public void UpdateComment(string comment)
    {
        Comment = comment;
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