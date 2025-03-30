namespace TotalSell.Domain.Entities;

public class ReportDashboardComment : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? Comment { get; private set; }
    public Guid? ParentId { get; private set; }
    public ReportDashboardComment? Parent { get; private set; }
    public ICollection<ReportDashboardComment> Replies { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardComment()
    {
        Replies = new List<ReportDashboardComment>();
    }

    public ReportDashboardComment(
        Guid dashboardId,
        string userId,
        string userName,
        string userEmail,
        string comment,
        Guid? parentId = null)
    {
        DashboardId = dashboardId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        Comment = comment;
        ParentId = parentId;
        Replies = new List<ReportDashboardComment>();
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