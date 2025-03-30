namespace TotalSell.Domain.Entities;

public class ReportShare : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? ShareType { get; private set; }
    public DateTime? ExpiryDate { get; private set; }
    public string? AccessToken { get; private set; }
    public bool IsActive { get; private set; }

    private ReportShare() { }

    public ReportShare(
        Guid reportId,
        string userId,
        string userName,
        string userEmail,
        string shareType,
        DateTime? expiryDate = null)
    {
        ReportId = reportId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        ShareType = shareType;
        ExpiryDate = expiryDate;
        AccessToken = Guid.NewGuid().ToString();
        IsActive = true;
    }

    public void UpdateShareDetails(
        string shareType,
        DateTime? expiryDate)
    {
        ShareType = shareType;
        ExpiryDate = expiryDate;
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