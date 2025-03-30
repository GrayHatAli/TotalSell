namespace TotalSell.Domain.Entities;

public class ReportFavorite : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? UserId { get; private set; }
    public string? UserName { get; private set; }
    public string? UserEmail { get; private set; }
    public string? ViewType { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? SortOrder { get; private set; }
    public string? GroupBy { get; private set; }
    public string? Aggregations { get; private set; }
    public string? Layout { get; private set; }
    public bool IsActive { get; private set; }

    private ReportFavorite() { }

    public ReportFavorite(
        Guid reportId,
        string userId,
        string userName,
        string userEmail,
        string viewType,
        string parameters,
        string? filters = null,
        string? sortOrder = null,
        string? groupBy = null,
        string? aggregations = null,
        string? layout = null)
    {
        ReportId = reportId;
        UserId = userId;
        UserName = userName;
        UserEmail = userEmail;
        ViewType = viewType;
        Parameters = parameters;
        Filters = filters;
        SortOrder = sortOrder;
        GroupBy = groupBy;
        Aggregations = aggregations;
        Layout = layout;
        IsActive = true;
    }

    public void UpdateFavoriteDetails(
        string viewType,
        string parameters,
        string? filters,
        string? sortOrder,
        string? groupBy,
        string? aggregations,
        string? layout)
    {
        ViewType = viewType;
        Parameters = parameters;
        Filters = filters;
        SortOrder = sortOrder;
        GroupBy = groupBy;
        Aggregations = aggregations;
        Layout = layout;
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