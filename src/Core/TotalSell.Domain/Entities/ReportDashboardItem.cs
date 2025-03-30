namespace TotalSell.Domain.Entities;

public class ReportDashboardItem : BaseEntity
{
    public Guid DashboardId { get; private set; }
    public ReportDashboard? Dashboard { get; private set; }
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? Title { get; private set; }
    public string? Description { get; private set; }
    public string? Type { get; private set; }
    public string? Size { get; private set; }
    public string? Position { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? RefreshInterval { get; private set; }
    public int Order { get; private set; }
    public bool IsActive { get; private set; }

    private ReportDashboardItem() { }

    public ReportDashboardItem(
        Guid dashboardId,
        Guid reportId,
        string title,
        string description,
        string type,
        string size,
        string position,
        string parameters,
        string filters,
        string refreshInterval,
        int order)
    {
        DashboardId = dashboardId;
        ReportId = reportId;
        Title = title;
        Description = description;
        Type = type;
        Size = size;
        Position = position;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        Order = order;
        IsActive = true;
    }

    public void UpdateDetails(
        string title,
        string description,
        string type,
        string size,
        string position,
        string parameters,
        string filters,
        string refreshInterval,
        int order)
    {
        Title = title;
        Description = description;
        Type = type;
        Size = size;
        Position = position;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        Order = order;
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