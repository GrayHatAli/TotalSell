namespace TotalSell.Domain.Entities;

public class ReportView : BaseEntity
{
    public Guid ReportId { get; private set; }
    public Report? Report { get; private set; }
    public string? ViewType { get; private set; }
    public string? Parameters { get; private set; }
    public string? Filters { get; private set; }
    public string? SortOrder { get; private set; }
    public string? GroupBy { get; private set; }
    public string? Aggregations { get; private set; }
    public string? Layout { get; private set; }
    public string? Status { get; private set; }
    public DateTime? LastViewDate { get; private set; }
    public string? LastViewBy { get; private set; }

    private ReportView() { }

    public ReportView(
        Guid reportId,
        string viewType,
        string parameters,
        string? filters = null,
        string? sortOrder = null,
        string? groupBy = null,
        string? aggregations = null,
        string? layout = null)
    {
        ReportId = reportId;
        ViewType = viewType;
        Parameters = parameters;
        Filters = filters;
        SortOrder = sortOrder;
        GroupBy = groupBy;
        Aggregations = aggregations;
        Layout = layout;
        Status = "Active";
    }

    public void UpdateViewDetails(
        string viewType,
        string parameters,
        string filters,
        string sortOrder,
        string groupBy,
        string aggregations,
        string layout)
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

    public void RecordView(string viewBy)
    {
        LastViewDate = DateTime.UtcNow;
        LastViewBy = viewBy;
        UpdatedAt = DateTime.UtcNow;
    }

    public void UpdateStatus(string status)
    {
        Status = status;
        UpdatedAt = DateTime.UtcNow;
    }
} 