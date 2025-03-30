namespace TotalSell.Domain.Entities;

public class ReportDashboard : BaseEntity
{
    public string? Name { get; private set; }
    public string? Description { get; private set; }
    public string? Layout { get; private set; }
    public string? Theme { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? RefreshInterval { get; private set; }
    public bool IsPublic { get; private set; }
    public bool IsActive { get; private set; }
    public ICollection<ReportDashboardItem> Items { get; private set; }

    private ReportDashboard()
    {
        Items = new List<ReportDashboardItem>();
    }

    public ReportDashboard(
        string name,
        string description,
        string layout,
        string theme,
        string parameters,
        string filters,
        string refreshInterval,
        bool isPublic = false)
    {
        Name = name;
        Description = description;
        Layout = layout;
        Theme = theme;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        IsPublic = isPublic;
        IsActive = true;
        Items = new List<ReportDashboardItem>();
    }

    public void UpdateDetails(
        string name,
        string description,
        string layout,
        string theme,
        string parameters,
        string filters,
        string refreshInterval,
        bool isPublic)
    {
        Name = name;
        Description = description;
        Layout = layout;
        Theme = theme;
        Parameters = parameters;
        Filters = filters;
        RefreshInterval = refreshInterval;
        IsPublic = isPublic;
        UpdatedAt = DateTime.UtcNow;
    }

    public void AddItem(ReportDashboardItem item)
    {
        Items.Add(item);
        UpdatedAt = DateTime.UtcNow;
    }

    public void RemoveItem(ReportDashboardItem item)
    {
        Items.Remove(item);
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