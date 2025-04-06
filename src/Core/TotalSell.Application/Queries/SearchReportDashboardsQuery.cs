using TotalSell.Application.Common;

namespace TotalSell.Application.Queries;

public class SearchReportDashboardsQuery : BaseQuery
{
    public string? SearchTerm { get; set; }
    public Guid? ReportId { get; set; }
    public bool? IsActive { get; set; }
    public int PageNumber { get; set; } = 1;
    public int PageSize { get; set; } = 10;
    public string? SortBy { get; set; }
    public bool SortDescending { get; set; }
} 